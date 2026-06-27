from fastapi import HTTPException
from models.user import User
from services.user_service import UserService
from services.pass_utils import hash_password, verify_password

class AuthService:
    def __init__(self, user_service):
        self.user_service = user_service

    # register a user
    def register(self, user_data):
        try:
            hashed = hash_password(user_data.password)
        except ValueError as exc:
            raise HTTPException(status_code=422, detail=str(exc))

        user = User(
            username=user_data.username,
            email=user_data.email,
            password_hash=hashed
        )

        return self.user_service.create_user(user)

    # login user
    def authenticate(self, username, password):
        user = self.user_service.get_by_username(username)

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        return user