from fastapi import FastAPI
import app.db.base

from app.api.webhook_endpoints import router
from app.core.exception_handler import register_exception_handlers

app = FastAPI(title="RelayFlow")

register_exception_handlers(app)

app.include_router(
    router,
    prefix="/api/v1",
    tags=["Webhook Endpoints"],
)


@app.get("/")
async def root():
    return {"message": "Up and running!"}