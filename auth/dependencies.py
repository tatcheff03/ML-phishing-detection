from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from config.database import get_db
from models.user import User
from auth.jwt import decode_token
from fastapi import HTTPException

# extract the JWT token from Auth header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# get the curr. logged-in user from the token
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    payload = decode_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.id == payload["sub"]).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# require admin access for some of the endpoints
def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user
    