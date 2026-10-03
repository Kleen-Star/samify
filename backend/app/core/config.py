from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "development"
    database_url: str
    secret_key: str
    access_token_expire_minutes: int = 60
    cors_origins: str = "http://localhost:5173"
    media_storage_path: str = "../storage"
    smtp_host: str = ""
    smtp_port: str = ""
    smtp_username: str = ""
    smtp_password: str = ""

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
