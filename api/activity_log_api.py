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

# get all logs
@router.get("", response_model=list[ActivityLogResponse])
def get_all_logs(
    service: ActivityLogService = Depends (get_activitylog_service),
    user = Depends(require_admin)
):
    return service.get_all_logs()
            
# get logs by user 
@router.get("/user/{user_id}", response_model=list[ActivityLogResponse])
def get_logs_by_user(
    user_id: int,
    service: ActivityLogService = Depends(get_activitylog_service),
    user = Depends(require_admin)
):
    return service.get_logs_by_user(user_id)

# recent 40 logs
@router.get("/recent", response_model=list[ActivityLogResponse])
def get_recent_logs(
    limit: int = 40,
    service: ActivityLogService = Depends(get_activitylog_service),
    user = Depends(require_admin)
):
    return service.get_recent_logs(limit)

# logs by action
@router.get("/action/{action}", response_model=list[ActivityLogResponse])
def get_logs_by_action(
    action: str,
    service: ActivityLogService = Depends(get_activitylog_service),
    user = Depends(require_admin)
):
    return service.get_logs_by_action(action)

# get my activity logs (with actions)
@router.get("/me", response_model=list[ActivityLogResponse])
def get_my_logs(
    service: ActivityLogService = Depends(get_activitylog_service),
    user = Depends(get_current_user)
):
    return service.get_logs_by_user(user.id)