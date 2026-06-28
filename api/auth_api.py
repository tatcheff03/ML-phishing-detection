from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from services.user_service import UserService
from services.auth_service import AuthService
from services.activitylog_service import ActivityLogService
from schemas.usercreatemodels import UserCreate, UserOut, UserLogin
from fastapi import HTTPException, Request
from auth.dependencies import get_current_user
from auth.jwt import create_access_token

router = APIRouter()

def get_auth_service(db: Session = Depends(get_db)) -> AuthService:
    return AuthService(
        UserService(db),
        ActivityLogService(db)
    )

# register user endpoint
@router.post("/register", response_model=UserOut)
def register(user: UserCreate, auth_service: AuthService = Depends(get_auth_service)):
    return auth_service.register(user)

# login user endpoint
@router.post("/login")
def login(user: UserLogin, request: Request, auth_service: AuthService = Depends(get_auth_service)):
    result = auth_service.login(
        username=user.username,
        password=user.password,
        ip_address= request.headers.get("X-Forwarded-For", "").split(",")[0].strip() or request.client.host
         )

    if not result:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token(result.id, result.role)

    return {"access_token": token, "token_type": "bearer"}

# get info about logged user
@router.get("/me")
def get_me(user = Depends(get_current_user)):
    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": user.role
    }