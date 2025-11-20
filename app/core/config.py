from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "AutoCare CRM"
    database_url: str = "sqlite:///./data.db"
    jwt_secret_key: str = "change_me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24
    redis_url: str = "redis://localhost:6379/0"
    celery_task_always_eager: bool = True
    sms_provider_url: str = "https://sms-gateway.example/send"
    email_from: str = "noreply@autocare.local"
    telegram_bot_token: str = "test-token"
    websocket_base_url: str = "ws://localhost:8000/ws"

    class Config:
        env_prefix = "CRM_"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
