from pydantic import BaseModel, validator
from typing import Optional
from datetime import datetime

class TransactionCreate(BaseModel):
    account_id: int
    type: str  # deposit, withdraw, transfer
    amount: float
    target_account_id: Optional[int] = None

    @validator('type')
    def validate_type(cls, v):
        if v not in ['deposit', 'withdraw', 'transfer']:
            raise ValueError('Transaction type must be deposit, withdraw, or transfer')
        return v

    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

    @validator('target_account_id')
    def validate_target_account(cls, v, values):
        if values.get('type') == 'transfer' and v is None:
            raise ValueError('Target account ID is required for transfer transactions')
        return v

class TransactionResponse(BaseModel):
    id: int
    account_id: int
    type: str
    amount: float
    target_account_id: Optional[int]
    timestamp: datetime

    class Config:
        orm_mode = True
