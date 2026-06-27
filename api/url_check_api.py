from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db
from services.url_service import URLService
from schemas.urlcheckrequest import URLCheckRequest, URLCheckResponse
from auth.dependencies import get_current_user


router = APIRouter()

def get_url_service(db: Session = Depends(get_db)) -> URLService:
    return URLService(db)


@router.post("/check", response_model=URLCheckResponse)
def check_url(
    payload: URLCheckRequest,
    user = Depends(get_current_user),
    url_service: URLService = Depends(get_url_service)
):
    features = url_service.extract_features(payload.url)
    score = url_service.calc_risk(features)
    label = url_service.classify_risk(score)

    check = url_service.save_check(payload.url, score, label, user.id)

    return check