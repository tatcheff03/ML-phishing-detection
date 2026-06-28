from fastapi import HTTPException
from models.user import User
from services.user_service import UserService
from services.pass_utils import hash_password, verify_password
from utils.activities_actions import LOGIN, FAILED_LOGIN

class AuthService:
    def __init__(self,  user_service, activitylog_service):
        self.user_service = user_service
        self.activitylog_service = activitylog_service

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
    
    # verify credentials and log the activity (failed or logged successfully)
    def login(self, username, password, ip_address):
        endpoint = "/auth/login"
        user = self.authenticate(username, password)

        if not user:
           self._log(user_id=None, action=FAILED_LOGIN, endpoint=endpoint, ip_address=ip_address)
           return None

        self._log(user_id=user.id, action=LOGIN, endpoint=endpoint, ip_address=ip_address)
        print(f"User logged in successfully: {user.username}")
        return user
    
    # helper method for logging
    def _log (self, *, user_id= None, action, endpoint, ip_address):
        self.activitylog_service.log_activity(
            user_id=user_id,
            action=action,
            endpoint=endpoint,
            ip_address=ip_address
        )