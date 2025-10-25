from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from fastapi.middleware.cors import CORSMiddleware
from . import models, schemas, crud
from .database import Base, engine, SessionLocal

app = FastAPI()

# Allow requests from frontend
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables
Base.metadata.create_all(bind=engine)

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

# --- CRUD Endpoints ---
@app.post("/transactions", response_model=schemas.TransactionResponse)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    account_service_url = f"http://127.0.0.1:8002/accounts/{transaction.account_id}"
    try:
        response = requests.get(account_service_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Source account does not exist")
        account_data = response.json()
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Cannot connect to Account Service")

    # Handle deposit
    if transaction.type == "deposit":
        new_balance = account_data['balance'] + transaction.amount
    # Handle withdraw
    elif transaction.type == "withdraw":
        if account_data['balance'] < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        new_balance = account_data['balance'] - transaction.amount
    # Handle transfer
    elif transaction.type == "transfer":
        if transaction.target_account_id is None:
            raise HTTPException(status_code=400, detail="Target account ID required for transfer")
        if account_data['balance'] < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient balance")

        # Update target account balance
        target_url = f"http://127.0.0.1:8002/accounts/{transaction.target_account_id}"
        target_resp = requests.get(target_url)
        if target_resp.status_code != 200:
            raise HTTPException(status_code=400, detail="Target account does not exist")
        target_account = target_resp.json()
        target_new_balance = target_account['balance'] + transaction.amount
        # Update target account
        requests.put(target_url, json={"balance": target_new_balance})

        new_balance = account_data['balance'] - transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    # Update source account balance
    requests.put(f"http://127.0.0.1:8002/accounts/{transaction.account_id}", json={"balance": new_balance})

    # Create transaction in DB
    db_transaction = crud.create_transaction(db, transaction)

    # --- Send Notification ---
    try:
        # Use user_id from source account
        user_id = account_data['user_id']
        message = f"{transaction.type.capitalize()} of {transaction.amount} completed for account {transaction.account_id}"
        notification_payload = {
            "user_id": user_id,
            "message": message
        }
        requests.post("http://127.0.0.1:8004/notifications", json=notification_payload)
    except Exception as e:
        print(f"Failed to send notification: {e}")

    return db_transaction

@app.get("/transactions", response_model=list[schemas.TransactionResponse])
def read_transactions(account_id: int = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_transactions(db, account_id=account_id, skip=skip, limit=limit)

@app.get("/transactions/{transaction_id}", response_model=schemas.TransactionResponse)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    db_transaction = crud.get_transaction(db, transaction_id)
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return db_transaction
@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = crud.get_transaction(db, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    crud.delete_transaction(db, transaction_id)
    return {"message": f"Transaction {transaction_id} deleted successfully"}
