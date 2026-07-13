from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from services.activitylog_service import ActivityLogService
from schemas.activitylog_response import ActivityLogResponse
from auth.dependencies import get_current_user, require_admin

router = APIRouter()

# dependency injection 
def get_activitylog_service(db: Session = Depends(get_db)) -> ActivityLogService:
    return ActivityLogService(db)


# recent 30 logs
@router.get("/recent", response_model=list[ActivityLogResponse])
def get_recent_logs(
    limit: int = 30,
    service: ActivityLogService = Depends(get_activitylog_service),
    user = Depends(require_admin)
):
    return service.get_recent_logs(limit)

# logs by action
@router.get("/action/{action}", response_model=list[ActivityLogResponse])
def get_logs_by_action(
    action: str,
    limit: int = 30,
    service: ActivityLogService = Depends(get_activitylog_service),
    user = Depends(require_admin)
):
    return service.get_logs_by_action(action, limit)

# get my activity logs (with actions)
@router.get("/me", response_model=list[ActivityLogResponse])
def get_my_logs(
    service: ActivityLogService = Depends(get_activitylog_service),
    user = Depends(get_current_user)
):
    return service.get_recent_logs_by_user(user.id, limit=15)