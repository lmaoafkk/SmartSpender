from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi import Request, status, Form
from app.dependencies import SessionDep
from . import router, templates
from app.services.auth_service import AuthService
from app.repositories.user import UserRepository
from app.utilities.flash import flash

@router.get("/login", response_class=HTMLResponse)
async def login_view(request: Request):
    return templates.TemplateResponse(request=request, name="login.html")

@router.post("/login", response_class=HTMLResponse)
async def login_action_ajax(
    db: SessionDep,
    request: Request,
    username: str = Form(),
    password: str = Form(),
):
    user_repo = UserRepository(db)
    auth_service = AuthService(user_repo)
    access_token = auth_service.authenticate_user(username, password)
    if not access_token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"success": False, "message": "Incorrect username or password"},
        )
    
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"success": True, "redirect_url": "/finance/dashboard"},
    )
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=request.url.scheme == "https",
    )
    return response
