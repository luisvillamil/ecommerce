# import os

# # web config
# host = os.getenv("WEB_HOST", "127.0.0.1")
# port = int(os.getenv("WEB_PORT", 8080))
# project_name = os.getenv("PROJECT_NAME", "Ecommerce App")
# api_version = os.getenv("API_VERSION", "api/v1")

import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    AnyHttpUrl, EmailStr, HttpUrl,
    PostgresDsn, field_validator, ValidationInfo
    )
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Main settings for project, to be defined in deployment yaml"""
    API_VERSION: str = "/api/v1"
    # secrets.token_urlsafe(32)
    SECRET_KEY: str = ''
    ALGORITHM:str = "HS256"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    SERVER_NAME: str = "Ecommmerce"
    SERVER_HOST: AnyHttpUrl = "http://localhost:8080"
    # postgres data
    POSTGRES_SCHEME: str = "postgresql+psycopg2"
    POSTGRES_SERVER: str = "127.0.0.1"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "ecommerce"
    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200", "http://localhost:3000", \
    # "http://localhost:8080", "http://local.dockertoolbox.tiangolo.com"]'
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """takes str list and converst to list of urls"""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str = "Ecommerce APP"
    # SENTRY_DSN: Optional[HttpUrl] = None

    # @validator("SENTRY_DSN", pre=True)
    # def sentry_dsn_can_be_blank(cls, v: str) -> Optional[str]:
    #     if len(v) == 0:
    #         return None
    #     return vPOSTGRES_SERVER: str = "127.0.0.1"
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode='before')
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: ValidationInfo) -> Any:
        """builds sqlalchemy compatible connection"""
        if isinstance(v, str):
            return v
        postgres_url: str = (
            f"{values.data.get('POSTGRES_SCHEME')}://"
            f"{values.data.get('POSTGRES_USER')}:"
            f"{values.data.get('POSTGRES_PASSWORD')}"
            f"@{values.data.get('POSTGRES_SERVER')}/"
            f"{values.data.get('POSTGRES_DB')}"
        )
        return PostgresDsn(postgres_url)
        # had to comment this because pydantic V2 removed the build method >:(
        # return PostgresDsn.build(
        #     scheme="postgresql",
        #     user=values.data.get("POSTGRES_USER"),
        #     password=values.data.get("POSTGRES_PASSWORD"),
        #     host=values.data.get("POSTGRES_SERVER"),
        #     path=f"/{values.data.get('POSTGRES_DB') or ''}",
        # )

    # SMTP_TLS: bool = True
    # SMTP_PORT: Optional[int] = None
    # SMTP_HOST: Optional[str] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    # EMAILS_FROM_NAME: Optional[str] = None

    # @validator("EMAILS_FROM_NAME")
    # def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
    #     if not v:
    #         return values["PROJECT_NAME"]
    #     return v

    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    # EMAIL_TEMPLATES_DIR: str = "/app/app/email-templates/build"
    # EMAILS_ENABLED: bool = False

    # @validator("EMAILS_ENABLED", pre=True)
    # def get_emails_enabled(cls, v: bool, values: Dict[str, Any]) -> bool:
    #     return bool(
    #         values.get("SMTP_HOST")
    #         and values.get("SMTP_PORT")
    #         and values.get("EMAILS_FROM_EMAIL")
    #     )

    # EMAIL_TEST_USER: EmailStr = "test@example.com"  # type: ignore
    FIRST_SUPERUSER: EmailStr = "test@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "test123"
    # USERS_OPEN_REGISTRATION: bool = False
    model_config = SettingsConfigDict(case_sensitive=True)


settings = Settings()
