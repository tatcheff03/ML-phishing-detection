from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from config.database import Base
from sqlalchemy.orm import relationship

class Anomalies(Base):
    __tablename__ = "anomalies"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    risk_score = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="anomalies")