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
    allow_origins=origins,       # frontend URLs allowed
    allow_credentials=True,
    allow_methods=["*"],         # allow all HTTP methods
    allow_headers=["*"],         # allow all headers
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
    return {"message": "Account Service is running"}

# CRUD Endpoints
@app.post("/accounts", response_model=schemas.AccountResponse)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    # Validate user_id by calling User Service
    user_service_url = f"http://127.0.0.1:8001/users/{account.user_id}"
    try:
        response = requests.get(user_service_url)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="User ID does not exist")
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Cannot connect to User Service")

    db_account = crud.create_account(db, account)
    return db_account

@app.get("/accounts", response_model=list[schemas.AccountResponse])
def read_accounts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_accounts(db, skip=skip, limit=limit)

@app.get("/accounts/{account_id}", response_model=schemas.AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    db_account = crud.get_account(db, account_id)
    if db_account is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return db_account
@app.delete("/accounts/{account_id}")
def delete_account(account_id: int, db: Session = Depends(get_db)):
    account = crud.get_account(db, account_id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    crud.delete_account(db, account_id)
    return {"message": f"Account {account_id} deleted successfully"}
