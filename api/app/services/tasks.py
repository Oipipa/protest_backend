from datetime import datetime
from celery import shared_task
from redis import Redis
from app.core.config import settings

@shared_task
def heartbeat():
    r = Redis.from_url(settings.redis_url)
    r.publish("events", f'{{"channel":"system","event":"heartbeat","data":"{datetime.utcnow().isoformat()}Z"}}')
    return "ok"
