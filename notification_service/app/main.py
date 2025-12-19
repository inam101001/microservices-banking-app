from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator
from . import models, schemas, crud
from .database import Base, engine, SessionLocal
import threading
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rabbitmq_utils import RabbitMQConsumer

app = FastAPI(title="Notification Service", version="1.0.0")

# Prometheus metrics instrumentation
Instrumentator().instrument(app).expose(app)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize RabbitMQ Consumer
rabbitmq_consumer = RabbitMQConsumer()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Notification Service is running"}

def process_notification_message(ch, method, properties, body):
    """Process incoming notification messages from RabbitMQ"""
    try:
        # Parse the message
        data = json.loads(body)
        user_id = data.get('user_id')
        message = data.get('message')
        
        if user_id and message:
            # Create notification in database
            db = SessionLocal()
            try:
                notification_data = schemas.NotificationCreate(
                    user_id=user_id,
                    message=message
                )
                crud.create_notification(db, notification_data)
                print(f"Created notification for user {user_id}: {message}")
            finally:
                db.close()
        
        # Acknowledge the message
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        print(f"Error processing notification message: {e}")
        # Reject the message and don't requeue it
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_rabbitmq_consumer():
    """Start consuming messages from RabbitMQ in a separate thread"""
    try:
        rabbitmq_consumer.setup_queue('notifications', 'transaction.completed')
        rabbitmq_consumer.start_consuming('notifications', process_notification_message)
    except Exception as e:
        print(f"Error in RabbitMQ consumer: {e}")

# Start RabbitMQ consumer in background thread
consumer_thread = threading.Thread(target=start_rabbitmq_consumer, daemon=True)
consumer_thread.start()

# CRUD Endpoints
@app.post("/notifications", response_model=schemas.NotificationResponse)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    try:
        db_notification = crud.create_notification(db, notification)
        return db_notification
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create notification: {str(e)}")

@app.get("/notifications", response_model=list[schemas.NotificationResponse])
def read_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip parameter must be non-negative")
        if limit <= 0 or limit > 1000:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        
        return crud.get_notifications(db, skip=skip, limit=limit)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve notifications: {str(e)}")

@app.get("/notifications/{notification_id}", response_model=schemas.NotificationResponse)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    try:
        if notification_id <= 0:
            raise HTTPException(status_code=400, detail="Notification ID must be a positive integer")
        
        db_notification = crud.get_notification(db, notification_id)
        if db_notification is None:
            raise HTTPException(status_code=404, detail="Notification not found")
        return db_notification
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve notification: {str(e)}")

@app.delete("/notifications/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    try:
        if notification_id <= 0:
            raise HTTPException(status_code=400, detail="Notification ID must be a positive integer")
        
        notification = crud.get_notification(db, notification_id)
        if not notification:
            raise HTTPException(status_code=404, detail="Notification not found")
        
        crud.delete_notification(db, notification_id)
        return {"message": f"Notification {notification_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete notification: {str(e)}")

# Graceful shutdown
@app.on_event("shutdown")
def shutdown_event():
    rabbitmq_consumer.stop_consuming()
    rabbitmq_consumer.close()