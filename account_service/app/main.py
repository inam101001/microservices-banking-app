from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
import requests
from . import models, schemas, crud
from .database import Base, engine, SessionLocal

app = FastAPI()

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
    return {"message": "Account Service is running"}

# CRUD Endpoints
@app.post("/accounts", response_model=schemas.AccountResponse)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    try:
        # Validate user_id by calling User Service
        user_service_url = f"http://127.0.0.1:8001/users/{account.user_id}"
        try:
            response = requests.get(user_service_url, timeout=5)
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail="User ID does not exist")
        except requests.exceptions.RequestException as e:
            raise HTTPException(status_code=500, detail=f"Cannot connect to User Service: {str(e)}")

        # Validate account type
        if account.account_type not in ["checking", "savings", "business"]:
            raise HTTPException(status_code=400, detail="Invalid account type. Must be 'checking', 'savings', or 'business'")

        # Validate balance
        if account.balance < 0:
            raise HTTPException(status_code=400, detail="Initial balance cannot be negative")

        db_account = crud.create_account(db, account)
        return db_account
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/accounts", response_model=list[schemas.AccountResponse])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        return crud.get_accounts(db, skip=skip, limit=limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve accounts: {str(e)}")

@app.get("/accounts/{account_id}", response_model=schemas.AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    try:
        if account_id <= 0:
            raise HTTPException(status_code=400, detail="Account ID must be a positive integer")
        
        db_account = crud.get_account(db, account_id)
        if db_account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        return db_account
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve account: {str(e)}")

@app.put("/accounts/{account_id}", response_model=schemas.AccountResponse)
def update_account_balance(account_id: int, account_update: schemas.AccountUpdate, db: Session = Depends(get_db)):
    try:
        if account_id <= 0:
            raise HTTPException(status_code=400, detail="Account ID must be a positive integer")
        
        if account_update.balance < 0:
            raise HTTPException(status_code=400, detail="Balance cannot be negative")
        
        db_account = crud.update_account_balance(db, account_id, account_update.balance)
        if db_account is None:
            raise HTTPException(status_code=404, detail="Account not found")
        return db_account
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update account balance: {str(e)}")

@app.delete("/accounts/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    try:
        if account_id <= 0:
            raise HTTPException(status_code=400, detail="Account ID must be a positive integer")
        
        account = crud.get_account(db, account_id)
        if not account:
            raise HTTPException(status_code=404, detail="Account not found")
        
        # Check if account has balance before deletion
        if account.balance > 0:
            raise HTTPException(status_code=400, detail="Cannot delete account with remaining balance")
        
        crud.delete_account(db, account_id)
        return {"message": f"Account {account_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete account: {str(e)}")
