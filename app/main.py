from fastapi import FastAPI
import app.db.base

from app.api.webhook_endpoints import router as webhook_endpoints_router
from app.api.events import router as events_router
from app.core.exception_handler import register_exception_handlers

app = FastAPI(title="RelayFlow")

register_exception_handlers(app)

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

@app.get("/")
async def root():
    return {"message": "Up and running!"}