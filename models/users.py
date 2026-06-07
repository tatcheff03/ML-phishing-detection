from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role=Column(String, nullable=False, default="USER")
    created_at = Column(DateTime, default=datetime.utcnow)