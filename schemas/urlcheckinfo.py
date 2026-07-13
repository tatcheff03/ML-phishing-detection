from pydantic import BaseModel
from datetime import datetime


class URLCheckInfo(BaseModel):
    id: int
    url_address: str

    prediction: str

    rule_score: float
    ml_score: float
    final_score: float

    created_at: datetime

    class Config:
        from_attributes = True