from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    database_url: str = Field(
        default="postgresql+psycopg2://app:app@localhost:5432/clans",
        alias="DATABASE_URL",
    )
    app_env: str = Field(default="local", alias="APP_ENV")

settings = Settings()
