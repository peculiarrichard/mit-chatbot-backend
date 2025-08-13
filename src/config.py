import os
from typing import List, Any
from pydantic_settings import BaseSettings, SettingsConfigDict
from src.constants import Environment

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/university_chatbot")
JWT_SECRET = os.getenv("JWT_SECRET", "your-secret-key")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
SMTP_SERVER = os.getenv("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USERNAME = os.getenv("SMTP_USERNAME")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    # Environment and Logging
    ENVIRONMENT: Environment = Environment.PRODUCTION
    LOG_LEVEL: str = "INFO"
    JWT_SECRET: str = JWT_SECRET

    # External Services
    OPENROUTER_API_KEY: str = OPENROUTER_API_KEY

    # Database
    DATABASE_URL: str = DATABASE_URL

    #Smtp
    SMTP_SERVER: str = SMTP_SERVER
    SMTP_PASSWORD: str = SMTP_PASSWORD
    ADMIN_EMAIL: str = ADMIN_EMAIL
    SMTP_USERNAME: str = SMTP_USERNAME
    SMTP_PORT: str = SMTP_PORT

    # CORS
    CORS_ORIGINS: List[str] = ["*"]
    CORS_HEADERS: List[str] = ["*"]

    # Application Metadata
    APP_VERSION: str = "1.0"


settings = Settings()

app_configs: dict[str, Any] = {"title": "MIT Smart Chatbot API", "version": settings.APP_VERSION}
if settings.ENVIRONMENT.is_deployed:
    app_configs["root_path"] = f"/v{settings.APP_VERSION}"

# if not settings.ENVIRONMENT.is_debug:
#     app_configs["openapi_url"] = None  # hide docs