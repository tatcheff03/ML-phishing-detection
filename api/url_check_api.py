from fastapi import Depends, APIRouter, Request
from sqlalchemy.orm import Session

from config.database import get_db
from services.url_service import URLService
from services.activitylog_service import ActivityLogService
from schemas.urlcheckrequest import URLCheckRequest, URLCheckResponse
from auth.dependencies import get_current_user


router = APIRouter()

# services dependency injection
def get_activitylog_service(db: Session = Depends(get_db)):
    return ActivityLogService(db)

def get_url_service(db: Session = Depends(get_db), 
                    activity_log_service: ActivityLogService = Depends(get_activitylog_service)
                    ) -> URLService:
    return URLService(db, activity_log_service)


@router.post("/check", response_model=URLCheckResponse)
def check_url(
    request: Request,
    payload: URLCheckRequest,
    user = Depends(get_current_user),
    url_service: URLService = Depends(get_url_service)
):
    return url_service.check_url(
        url=payload.url,
        user_id=user.id,
        ip_address= (
        request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.client.host
    )
    )