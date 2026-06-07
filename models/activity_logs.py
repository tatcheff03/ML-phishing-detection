from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from database import Base

class ActivityLogs(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    action = Column(String, nullable=False)
    ip_address = Column(String, nullable=True)
    endpoint = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)