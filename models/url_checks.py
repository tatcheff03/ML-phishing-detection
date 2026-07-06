from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from sqlalchemy.orm import relationship
from config.database import Base

class URLChecks(Base):
    __tablename__ = "url_checks"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    url_address = Column(String, nullable=False)
    
    rule_score = Column(Float, nullable=True)
    ml_score = Column(Float, nullable=True)
    final_score = Column(Float, nullable=True)
    
    prediction = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="url_checks")