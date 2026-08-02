from fastapi import FastAPI
import app.db.base

from app.api.webhook_endpoints import router as webhook_endpoints_router
from app.api.events import router as events_router
from app.api.delivery import router as deliveries_router
from app.api.health import router as health_router
from app.core.exception_handler import register_exception_handlers
from app.core.logging import get_logger


app = FastAPI(title="RelayFlow")

logger = get_logger(__name__)

logger.info("RelayFlow application started")

register_exception_handlers(app)

app.include_router(
    health_router,
    tags=["Health Checkup"]
)

app.include_router(  
    webhook_endpoints_router,
    prefix="/api/v1",
    tags=["Webhook Endpoints"],
)

app.include_router(
    events_router,
    prefix="/api/v1",
    tags=["Events"],
)

app.include_router(
    deliveries_router,
    prefix="/api/v1",
    tags=["Deliveries"],
)

@app.get("/")
async def root():
    return {"message": "Up and running!"}