from pydantic import BaseModel, validator
from datetime import datetime

class NotificationCreate(BaseModel):
    user_id: int
    message: str

    @validator('user_id')
    def validate_user_id(cls, v):
        if v <= 0:
            raise ValueError('User ID must be a positive integer')
        return v

    @validator('message')
    def validate_message(cls, v):
        if not v or len(v.strip()) < 1:
            raise ValueError('Message cannot be empty')
        return v.strip()

class NotificationResponse(BaseModel):
    id: int
    user_id: int
    message: str
    timestamp: datetime

    class Config:
        orm_mode = True
