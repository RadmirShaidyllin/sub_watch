from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, PostgresDsn
from pathlib import Path
import os

env_file = Path(__file__).resolve().parent.parent / ".env"
print("ENV FILE EXISTS:", env_file.exists())
print("CWD:", os.getcwd())


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=env_file,
        env_file_encoding="utf-8",
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="SUB_WATCH", validation_alias="APP_NAME")
    app_env: str = Field(default="dev", validation_alias="APP_ENV")
    app_debug: bool = Field(default=False, validation_alias="APP_DEBUG")
    app_host: str = Field(default="0.0.0.0", validation_alias="APP_HOST")
    app_port: int = Field(default=8000, validation_alias="APP_PORT")
    timezone: str = Field(default="UTC", validation_alias="TIMEZONE")

    secret_key: str = Field(..., validation_alias="SECRET_KEY")
    access_token_expire_minutes: int = Field(default=1440, validation_alias="ACCESS_TOKEN_EXPIRE_MINUTES")
    refresh_token_expire_days: int = Field(default=30, validation_alias="REFRESH_TOKEN_EXPIRE_DAYS")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    token_type: str = Field(default="bearer", validation_alias="TOKEN_TYPE")

    db_host: str = Field(default="localhost", validation_alias="DB_HOST")
    db_port: int = Field(default=5432, validation_alias="DB_PORT")
    db_name: str = Field(default="subwatch_db", validation_alias="DB_NAME")
    db_user: str = Field(default="subwatch_user", validation_alias="DB_USER")
    db_password: str = Field(default="subwatch_password", validation_alias="DB_PASSWORD")
    database_url: PostgresDsn = Field(..., validation_alias="DATABASE_URL")
    async_database_url: PostgresDsn = Field(..., validation_alias="ASYNC_DATABASE_URL")


settings = Settings()

print("APP NAME:", settings.app_name)
print("ENV:", settings.app_env)
print("DEBUG:", settings.app_debug)
print("DATABASE URL:", settings.database_url)
