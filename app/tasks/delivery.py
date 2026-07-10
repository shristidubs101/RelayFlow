from app.core.celery import celery_app


@celery_app.task
def process_delivery(delivery_id: int):
    print(f"Processing delivery {delivery_id}")
