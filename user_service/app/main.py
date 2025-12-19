from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator
from . import models, schemas, crud
from .database import Base, engine, SessionLocal

app = FastAPI(title="User Service", version="1.0.0")

# Create tables
Base.metadata.create_all(bind=engine)

# Prometheus metrics instrumentation
Instrumentator().instrument(app).expose(app)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "User Service is running"}

# CRUD Endpoints
@app.post("/users", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if email already exists
        existing_user = crud.get_user_by_email(db, user.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        db_user = crud.create_user(db, user)
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create user: {str(e)}")

@app.get("/users", response_model=list[schemas.UserResponse])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        if skip < 0:
            raise HTTPException(status_code=400, detail="Skip parameter must be non-negative")
        if limit <= 0 or limit > 1000:
            raise HTTPException(status_code=400, detail="Limit must be between 1 and 1000")
        
        users = crud.get_users(db, skip=skip, limit=limit)
        return users
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve users: {str(e)}")

@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    try:
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="User ID must be a positive integer")
        
        db_user = crud.get_user(db, user_id)
        if db_user is None:
            raise HTTPException(status_code=404, detail="User not found")
        return db_user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to retrieve user: {str(e)}")

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    try:
        if user_id <= 0:
            raise HTTPException(status_code=400, detail="User ID must be a positive integer")
        
        user = crud.get_user(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Check if user has accounts (optional business rule)
        # This would require calling Account Service, but for now we'll skip this check
        # In a real application, you might want to prevent deletion of users with active accounts
        
        crud.delete_user(db, user_id)
        return {"message": f"User {user_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete user: {str(e)}")