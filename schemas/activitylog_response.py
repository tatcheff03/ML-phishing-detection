from pydantic import BaseModel
from datetime import datetime

# pydantic model for activity log 
class ActivityLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    endpoint: str
    ip_address: str | None
    url_check_id: int | None
    created_at: datetime
    
    class Config:
        from_attributes = True