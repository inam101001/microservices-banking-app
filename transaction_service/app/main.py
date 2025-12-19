from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator
import requests
from . import models, schemas, crud
from .database import Base, engine, SessionLocal
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from rabbitmq_utils import RabbitMQPublisher

app = FastAPI(title="Transaction Service", version="1.0.0")

# Prometheus metrics instrumentation
Instrumentator().instrument(app).expose(app)

# Create tables
Base.metadata.create_all(bind=engine)

# Initialize RabbitMQ Publisher
rabbitmq_publisher = RabbitMQPublisher()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Transaction Service is running"}

def get_account_from_service(account_id: int):
    """Helper function to get account data from Account Service"""
    try:
        account_service_url = f"http://account-service:8002/accounts/{account_id}"
        response = requests.get(account_service_url, timeout=5)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
        elif response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Account Service error: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Cannot connect to Account Service: {str(e)}")

def update_account_balance_in_service(account_id: int, new_balance: float):
    """Helper function to update account balance in Account Service"""
    try:
        account_service_url = f"http://account-service:8002/accounts/{account_id}"
        update_data = {"balance": new_balance}
        response = requests.put(account_service_url, json=update_data, timeout=5)
        if response.status_code == 404:
            raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
        elif response.status_code != 200:
            raise HTTPException(status_code=500, detail=f"Failed to update account balance: {response.status_code}")
        return response.json()
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Cannot connect to Account Service: {str(e)}")

def publish_notification_event(user_id: int, message: str, transaction_id: int, transaction_type: str):
    """Publish notification event to RabbitMQ"""
    try:
        event_data = {
            'user_id': user_id,
            'message': message,
            'transaction_id': transaction_id,
            'transaction_type': transaction_type
        }
        rabbitmq_publisher.publish_message('transaction.completed', event_data)
    except Exception as e:
        print(f"Failed to publish notification event: {e}")  # Don't fail transaction for notification errors

# --- CRUD Endpoints ---
@app.post("/transactions", response_model=schemas.TransactionResponse)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    try:
        # Validate account exists and get current balance
        account_data = get_account_from_service(transaction.account_id)
        current_balance = account_data['balance']
        user_id = account_data['user_id']

        # Process transaction based on type
        if transaction.type == "deposit":
            new_balance = current_balance + transaction.amount
            message = f"Deposit of ${transaction.amount:.2f} completed. New balance: ${new_balance:.2f}"
            
        elif transaction.type == "withdraw":
            if current_balance < transaction.amount:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient balance. Current balance: ${current_balance:.2f}, Requested: ${transaction.amount:.2f}"
                )
            new_balance = current_balance - transaction.amount
            message = f"Withdrawal of ${transaction.amount:.2f} completed. New balance: ${new_balance:.2f}"
            
        elif transaction.type == "transfer":
            if current_balance < transaction.amount:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Insufficient balance for transfer. Current balance: ${current_balance:.2f}, Requested: ${transaction.amount:.2f}"
                )
            
            # Validate target account exists
            target_account_data = get_account_from_service(transaction.target_account_id)
            target_user_id = target_account_data['user_id']
            target_current_balance = target_account_data['balance']
            
            # Update both accounts
            new_balance = current_balance - transaction.amount
            target_new_balance = target_current_balance + transaction.amount
            
            # Update target account first (in case of failure, source account remains unchanged)
            update_account_balance_in_service(transaction.target_account_id, target_new_balance)
            
            message = f"Transfer of ${transaction.amount:.2f} to account {transaction.target_account_id} completed. New balance: ${new_balance:.2f}"
            
            # Send notification to target account user
            target_message = f"Received transfer of ${transaction.amount:.2f} from account {transaction.account_id}. New balance: ${target_new_balance:.2f}"
            publish_notification_event(target_user_id, target_message, 0, transaction.type)

        # Update source account balance
        update_account_balance_in_service(transaction.account_id, new_balance)

        # Create transaction record in database
        db_transaction = crud.create_transaction(db, transaction)

        # Publish notification event to RabbitMQ
        publish_notification_event(user_id, message, db_transaction.id, transaction.type)

        return db_transaction

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction failed: {str(e)}")

@app.get("/transactions", response_model=list[schemas.TransactionResponse])
def read_transactions(account_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud.get_transactions(db, account_id=account_id, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve transactions: {str(e)}")

@app.get("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    try:
        if transaction_id <= 0:
            raise HTTPException(status_code=400, detail="Transaction ID must be a positive integer")
        
        db_transaction = crud.get_transaction(db, transaction_id)
        if db_transaction is None:
            raise HTTPException(status_code=404, detail="Transaction not found")
        return db_transaction
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve transaction: {str(e)}")

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    try:
        if transaction_id <= 0:
            raise HTTPException(status_code=400, detail="Transaction ID must be a positive integer")
        
        transaction = crud.get_transaction(db, transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transaction not found")
        
        crud.delete_transaction(db, transaction_id)
        return {"message": f"Transaction {transaction_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete transaction: {str(e)}")

# Graceful shutdown
@app.on_event("shutdown")
def shutdown_event():
    rabbitmq_publisher.close()