from pydantic import BaseModel
from datetime import datetime

from schemas.urlcheckinfo import URLCheckInfo

# pydantic model for activity log 
class ActivityLogResponse(BaseModel):
    id: int
    user_id: int | None
    action: str
    endpoint: str
    ip_address: str | None
    url_check_id: int | None
    created_at: datetime
    
    url_check: URLCheckInfo | None=None 
    
    class Config:
        from_attributes = True