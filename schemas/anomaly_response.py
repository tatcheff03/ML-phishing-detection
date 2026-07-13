
from pydantic import BaseModel
from datetime import datetime

# pydantic model for anomaly response
class AnomalyResponse(BaseModel):
    id: int
    user_id: int | None
    risk_score: float
    description: str | None
    created_at: datetime
    
    class Config:
        from_attributes = True