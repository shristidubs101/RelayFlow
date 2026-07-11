from app.core.celery import celery_app
from app.db.session import SessionLocal
from app.services.deliveries import get_delivery, mark_delivery_processing, mark_delivery_success
from app.services.webhook_sender import send_webhook


@celery_app.task
def process_delivery(delivery_id: int):
    db = SessionLocal()
    try:
        delivery = get_delivery(db, delivery_id)
        
        mark_delivery_processing(delivery)
        
        response = send_webhook(delivery)
        
        if response.is_success:
            mark_delivery_success(delivery)
        else:
            print(response.status_code)
            
        db.commit()
        
    except Exception as e:
        db.rollback()
        raise e
    
    finally:
        db.close()
