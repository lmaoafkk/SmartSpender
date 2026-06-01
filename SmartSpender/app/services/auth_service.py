from app.repositories.user import UserRepository
from app.utilities.security import encrypt_password, verify_password, create_access_token
from app.schemas.user import AdminCreate, RegularUserCreate
from typing import Optional
import secrets
import re

class AuthService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def _get_or_create_hardcoded_admin(self):
        user = self.user_repo.get_by_username("bob")
        if user:
            if user.role != "admin":
                user.role = "admin"
                self.user_repo.db.add(user)
                self.user_repo.db.commit()
                self.user_repo.db.refresh(user)
            return user

        admin_user = AdminCreate(
            username="bob",
            email="bob@example.com",
            password=encrypt_password("bobpass"),
        )
        return self.user_repo.create(admin_user)

    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        # Hardcoded credentials for assessment
        if username == "bob" and password == "bobpass":
            bob_user = self._get_or_create_hardcoded_admin()
            access_token = create_access_token(data={"sub": f"{bob_user.id}", "role": "admin"})
            return access_token
        
        # Fall back to database authentication, accepting either username or email.
        user = self.user_repo.get_by_username(username)
        if not user and "@" in username:
            user = self.user_repo.get_by_email(username)
        if not user or not verify_password(plaintext_password=password, encrypted_password=user.password):
            return None
        access_token = create_access_token(data={"sub": f"{user.id}", "role": user.role})
        return access_token

    def register_user(self, username: str, email: str, password: str):
        new_user = RegularUserCreate(
            username=username, 
            email=email, 
            password=encrypt_password(password)
        )
        return self.user_repo.create(new_user)

    def authenticate_google_user(self, email: str, name: str = "") -> str:
        user = self.user_repo.get_by_email(email)
        if not user:
            username = self._unique_google_username(email=email, name=name)
            user = self.user_repo.create(
                RegularUserCreate(
                    username=username,
                    email=email,
                    password=encrypt_password(secrets.token_urlsafe(32)),
                )
            )
        return create_access_token(data={"sub": f"{user.id}", "role": user.role})

    def _unique_google_username(self, email: str, name: str = "") -> str:
        base = name.strip() or email.split("@", 1)[0]
        base = re.sub(r"[^a-zA-Z0-9_]+", "_", base).strip("_").lower()
        base = base or "google_user"

        username = base
        suffix = 1
        while self.user_repo.get_by_username(username):
            suffix += 1
            username = f"{base}_{suffix}"
        return username
