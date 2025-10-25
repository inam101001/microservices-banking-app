from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    phone: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str

    class Config:
        orm_mode = True
