from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AutoCare CRM"
    database_url: str = "sqlite:///./data.db"
    jwt_secret_key: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24

    class Config:
        env_prefix = "CRM_"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
