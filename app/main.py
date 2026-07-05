from fastapi import FastAPI
import app.db.base

from app.api.webhook_endpoints import router

app = FastAPI(title="RelayFlow")

app.include_router(
    router,
    prefix="/api/v1",
    tags=["Webhook Endpoints"],
)


@app.get("/")
async def root():
    return {"message": "Up and running!"}