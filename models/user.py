from database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship         
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role=Column(String, nullable=False, default="USER")
    created_at = Column(DateTime, default=datetime.utcnow)

    
    url_checks = relationship("URLChecks", back_populates="user", cascade="all, delete-orphan")
    activity_logs = relationship("ActivityLogs", back_populates="user", cascade="all, delete-orphan")
    anomalies = relationship("Anomalies", back_populates="user", cascade="all, delete-orphan")