from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models.event import Event
from app.schemas.events import EventCreate
from app.services.deliveries import create_deliveries
from app.services.webhook_endpoint import get_webhook_endpoints
from app.tasks.delivery import process_delivery

logger = get_logger(__name__)


def create_event(
    db: Session,
    event: EventCreate,
) -> Event:
    logger.info(
        "Creating event of type '%s'",
        event.event_type,
    )

    event_obj = Event(**event.model_dump())

    try:
        db.add(event_obj)
        db.flush()

        logger.info(
            "Event %s created",
            event_obj.id,
        )

        endpoints = get_webhook_endpoints(db)

        logger.info(
            "Found %s active webhook endpoint(s)",
            len(endpoints),
        )

        deliveries = create_deliveries(
            db,
            event_obj.id,
            endpoints,
        )

        logger.info(
            "Created %s delivery record(s) for event %s",
            len(deliveries),
            event_obj.id,
        )

        db.commit()

        logger.info(
            "Event %s committed successfully",
            event_obj.id,
        )

        for delivery in deliveries:
            logger.info(
                "Queueing delivery %s",
                delivery.id,
            )

            process_delivery.delay(delivery.id)

        db.refresh(event_obj)

        return event_obj

    except Exception:
        db.rollback()

        logger.exception(
            "Failed to create event of type '%s'",
            event.event_type,
        )

        raise


def get_events(
    db: Session,
) -> list[Event]:
    logger.info("Fetching all events")

    events = db.query(Event).all()

    logger.info(
        "Fetched %s event(s)",
        len(events),
    )

    return events