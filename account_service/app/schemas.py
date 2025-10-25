from pydantic import BaseModel

class AccountCreate(BaseModel):
    user_id: int
    account_type: str
    balance: float = 0.0

class AccountUpdate(BaseModel):
    balance: float

class AccountResponse(BaseModel):
    id: int
    user_id: int
    account_type: str
    balance: float

    class Config:
        orm_mode = True
