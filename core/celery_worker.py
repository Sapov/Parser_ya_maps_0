from celery import Celery
from .config import settings

# Создаем экземпляр Celery
celery_app = Celery(
    "worker",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["core.tasks"]  # Список модулей с задачами
)

# Настройка Celery
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 минут
    task_soft_time_limit=25 * 60,  # 25 минут
    worker_prefetch_multiplier=1,  # Для справедливого распределения задач
    result_expires=3600,  # Результаты хранятся 1 час
)