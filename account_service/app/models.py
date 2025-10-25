from sqlalchemy import Column, Integer, Float, String
from .database import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    account_type = Column(String)
    balance = Column(Float, default=0.0)
