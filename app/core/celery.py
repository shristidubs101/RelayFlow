from celery import Celery
import app.db.base

from app.core.config import settings

celery_app = Celery("relayflow")

celery_app.conf.update(
    broker_url=settings.REDIS_URL,
    broker_connection_retry_on_startup=True,
    timezone="UTC",
    enable_utc=True,
)

celery_app.conf.imports = (
    "app.tasks.delivery",
)