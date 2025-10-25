from pydantic import BaseModel, validator, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    phone: str

    @validator('name')
    def validate_name(cls, v):
        if not v or len(v.strip()) < 2:
            raise ValueError('Name must be at least 2 characters long')
        return v.strip()

    @validator('phone')
    def validate_phone(cls, v):
        # Basic phone validation - remove spaces and check if it's numeric
        phone_digits = ''.join(filter(str.isdigit, v))
        if len(phone_digits) < 10:
            raise ValueError('Phone number must contain at least 10 digits')
        return v

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        orm_mode = True
