from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
import os
from pathlib import Path


APP_DIR = Path(__file__).resolve().parent.parent
PROJECT_DIR = APP_DIR.parent
REPO_DIR = PROJECT_DIR.parent

@lru_cache
def get_settings():
    return Settings()

class Settings(BaseSettings):
    database_uri: str
    secret_key: str
    env: str
    jwt_algorithm: str="HS256"
    jwt_access_token_expires:int=30
    app_host: str="0.0.0.0"
    app_port: int=int(os.getenv("PORT", 8000))
    db_pool_size:int=10
    db_additional_overflow:int=10
    db_pool_timeout:int=10
    db_pool_recycle:int=10
    google_client_id: str = ""
    google_client_secret: str = ""
    google_redirect_uri: str = ""
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = ""
    smtp_from_name: str = "SmartSpender"
    smtp_use_tls: bool = True
    
    model_config = SettingsConfigDict(
        env_file=(
            APP_DIR / ".env",
            PROJECT_DIR / ".env",
            REPO_DIR / ".env",
        )
    )
