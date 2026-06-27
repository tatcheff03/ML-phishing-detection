from datetime import datetime

from pydantic import BaseModel

# user provides a URL
class URLCheckRequest(BaseModel):
    url: str

# response returned to user
class URLCheckResponse(BaseModel):
    id: int
    url_address: str
    risk_score: float
    prediction: str
    created_at: datetime

    class Config:
        from_attributes = True