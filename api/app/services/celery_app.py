from celery import Celery
from app.core.config import settings

celery_app = Celery(
    "app",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=["app.services.tasks"],
)

celery_app.conf.task_routes = {"app.services.tasks.*": {"queue": "default"}}
celery_app.conf.beat_schedule = {
    "heartbeat-30s": {"task": "app.services.tasks.heartbeat", "schedule": 30.0}
}
celery_app.conf.timezone = "UTC"
