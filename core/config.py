import os

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = "sqlite:////home/sasha/PycharmProjects/Parser_ya_maps/core/db.sqlite3"
    # 'sqlite+aiosqlite://./dbs.sqlite3'
    db_echo: bool = False
    # Celery
    celery_broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    celery_result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")

class Config:
    env_file = ".env"


settings = Settings()
