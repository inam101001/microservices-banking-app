from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    account_id: int
    type: str  # deposit, withdraw, transfer
    amount: float
    target_account_id: Optional[int] = None

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float
    target_account_id: Optional[int]
    timestamp: datetime

    class Config:
        orm_mode = True
