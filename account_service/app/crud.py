from sqlalchemy.orm import Session
from . import models, schemas

def get_account(db: Session, account_id: int):
    return db.query(models.Account).filter(models.Account.id == account_id).first()

def get_accounts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Account).offset(skip).limit(limit).all()

def create_account(db: Session, account: schemas.AccountCreate):
    db_account = models.Account(
        user_id=account.user_id,
        account_type=account.account_type,
        balance=account.balance
    )
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account

def update_account_balance(db: Session, account_id: int, new_balance: float):
    db_account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if db_account:
        db_account.balance = new_balance
        db.commit()
        db.refresh(db_account)
        return db_account
    return None

def delete_account(db: Session, account_id: int):
    account = db.query(models.Account).filter(models.Account.id == account_id).first()
    if account:
        db.delete(account)
        db.commit()
