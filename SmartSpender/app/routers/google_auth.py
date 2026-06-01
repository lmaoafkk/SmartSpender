import secrets
from urllib.parse import quote, urlencode

import httpx
from fastapi import Request, status
from fastapi.responses import RedirectResponse

from app.config import get_settings
from app.dependencies import SessionDep
from app.repositories.user import UserRepository
from app.services.auth_service import AuthService

from . import router


GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"


@router.get("/auth/google")
async def google_auth_start(request: Request):
    settings = get_settings()
    if not settings.google_client_id or not settings.google_client_secret:
        return _redirect_with_error(request, "Google sign-in is not configured yet.")

    state = secrets.token_urlsafe(32)
    request.session["google_oauth_state"] = state

    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": _google_redirect_uri(request),
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
    }
    return RedirectResponse(f"{GOOGLE_AUTH_URL}?{urlencode(params)}")


@router.get("/auth/google/callback")
async def google_auth_callback(request: Request, db: SessionDep):
    settings = get_settings()
    expected_state = request.session.pop("google_oauth_state", None)
    received_state = request.query_params.get("state")
    code = request.query_params.get("code")
    google_error = request.query_params.get("error")

    if google_error:
        return _redirect_with_error(request, "Google sign-in was cancelled.")
    if not expected_state or not received_state or not secrets.compare_digest(expected_state, received_state):
        return _redirect_with_error(request, "Google sign-in could not be verified.")
    if not code:
        return _redirect_with_error(request, "Google did not return an authorization code.")
    if not settings.google_client_id or not settings.google_client_secret:
        return _redirect_with_error(request, "Google sign-in is not configured yet.")

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": code,
                    "client_id": settings.google_client_id,
                    "client_secret": settings.google_client_secret,
                    "redirect_uri": _google_redirect_uri(request),
                    "grant_type": "authorization_code",
                },
            )
            token_response.raise_for_status()
            token_data = token_response.json()
            id_token = token_data.get("id_token")
            if not id_token:
                return _redirect_with_error(request, "Google did not return an identity token.")

            info_response = await client.get(GOOGLE_TOKEN_INFO_URL, params={"id_token": id_token})
            info_response.raise_for_status()
            profile = info_response.json()
    except httpx.HTTPError:
        return _redirect_with_error(request, "Google sign-in failed. Please try again.")

    if profile.get("aud") != settings.google_client_id:
        return _redirect_with_error(request, "Google sign-in could not be verified.")
    if profile.get("email_verified") != "true":
        return _redirect_with_error(request, "Google account email is not verified.")

    email = profile.get("email")
    if not email:
        return _redirect_with_error(request, "Google did not return an email address.")

    auth_service = AuthService(UserRepository(db))
    access_token = auth_service.authenticate_google_user(email=email, name=profile.get("name", ""))

    response = RedirectResponse(url="/finance/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=request.url.scheme == "https",
    )
    return response


def _google_redirect_uri(request: Request) -> str:
    settings = get_settings()
    return settings.google_redirect_uri or str(request.url_for("google_auth_callback"))


def _redirect_with_error(request: Request, message: str) -> RedirectResponse:
    return RedirectResponse(
        url=f"{request.url_for('landing_view')}?auth_error={quote(message)}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
