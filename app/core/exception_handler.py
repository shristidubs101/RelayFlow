from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import (
    DuplicateWebhookEndpointError,
    WebhookEndpointNotFoundError,
)


async def webhook_endpoint_not_found_handler(
    request: Request,
    exc: WebhookEndpointNotFoundError,
):

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "detail": str(exc),
        },
    )


async def duplicate_webhook_endpoint_handler(
    request: Request,
    exc: DuplicateWebhookEndpointError,
):

    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "detail": str(exc),
        },
    )


def register_exception_handlers(
    app: FastAPI,
):

    app.add_exception_handler(
        WebhookEndpointNotFoundError,
        webhook_endpoint_not_found_handler,
    )

    app.add_exception_handler(
        DuplicateWebhookEndpointError,
        duplicate_webhook_endpoint_handler,
    )