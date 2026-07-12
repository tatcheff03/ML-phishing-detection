from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config.database import get_db
from services.anomaly_service import AnomalyService
from auth.dependencies import get_current_user, require_admin
from schemas.anomaly_response import AnomalyResponse

router = APIRouter()

# dependency injection
def get_anomaly_service(db: Session = Depends(get_db)) -> AnomalyService:
    return AnomalyService(db)

# get all anomalies (admin only)
@router.get("/all" , response_model=list[AnomalyResponse])
def get_all_anomalies(
    admin_user = Depends(require_admin), 
    anomaly_service: AnomalyService = Depends(get_anomaly_service)):
    return anomaly_service.get_all_anomalies()

# get anomalies for the current user
@router.get("/me", response_model=list[AnomalyResponse])
def my_anomalies(
    current_user = Depends(get_current_user), 
    anomaly_service: AnomalyService = Depends(get_anomaly_service)):
    return anomaly_service.get_user_anomalies(current_user.id)