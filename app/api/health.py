from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder

from app.schemas.health import HealthResponse
from app.services.health import check_celery, check_database, check_redis


router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health_check() -> HealthResponse:
    database_status = check_database()
    redis_status = check_redis()
    worker_status = check_celery()

    is_healthy = (
        database_status
        and redis_status
        and worker_status
    )

    health_response = HealthResponse(
        status="healthy" if is_healthy else "unhealthy",
        timestamp=datetime.now(timezone.utc),
        version="1.0.0",
        database="up" if database_status else "down",
        redis="up" if redis_status else "down",
        worker="up" if worker_status else "down"
    )
    
    if not is_healthy:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=jsonable_encoder(health_response),
        )

    return health_response