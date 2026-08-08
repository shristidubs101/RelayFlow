from sqlalchemy import text
import redis

from app.core.config import settings
from app.db.session import SessionLocal
from app.core.celery import celery_app


def check_database() -> bool:
    db = SessionLocal()

    try:
        db.execute(text("SELECT 1"))
        return True

    except Exception:
        return False

    finally:
        db.close()
        
        
def check_redis() -> bool:
    client = redis.from_url(settings.REDIS_URL)

    try:
        return client.ping()
    except redis.RedisError:
        return False
    finally:
        client.close()
        

def check_celery() -> bool:
    try:
        inspector = celery_app.control.inspect()
        response = inspector.ping()

        return response is not None

    except Exception:
        return False