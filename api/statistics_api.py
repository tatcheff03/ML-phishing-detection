from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from auth.dependencies import require_admin

from services.statistics_service import StatisticsService

from schemas.statistics_response import StatisticsResponse

router = APIRouter()


def get_statistics_service(db: Session = Depends(get_db)):

    return StatisticsService(db)

# get stats for admin dashboard
@router.get("", response_model=StatisticsResponse)
def get_statistics(
    service: StatisticsService = Depends(get_statistics_service),
    admin=Depends(require_admin),
):

    return service.get_statistics()
