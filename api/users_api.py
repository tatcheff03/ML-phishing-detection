from schemas.usercreatemodels import UserOut
from fastapi import Depends, APIRouter
from services.user_service import UserService
from auth.dependencies import require_admin
from sqlalchemy.orm import Session
from config.database import get_db

router = APIRouter()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(db)

# get all users
@router.get("", response_model=list[UserOut])
def get_users(
    service: UserService = Depends(get_user_service),
    admin = Depends(require_admin)
):
    return service.list_users()