from fastapi import HTTPException
from models.user import User
from services.user_service import UserService
from services.pass_utils import hash_password, verify_password
from utils.activities_actions import LOGIN, FAILED_LOGIN

class AuthService:
    failed_login_counter = {}

    def __init__(self,  user_service, activitylog_service, anomaly_service):
        self.user_service = user_service
        self.activitylog_service = activitylog_service
        self.anomaly_service = anomaly_service
        
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
        key = f"{ip_address}:{username}" 
        
        user = self.authenticate(username, password)

        if not user:
            # Track failed attempts per IP + username
            
            current = self.failed_login_counter.get(key, 0) + 1
            self.failed_login_counter[key] = current
            
            self._log(user_id=None, action=FAILED_LOGIN, endpoint=endpoint, ip_address=ip_address)
            
            # after 5 failed attempts, create an anomaly and raise an exception
            if current >= 5:
                
                self.anomaly_service.create_anomaly(
                user_id=None,
                risk_score=80,
                description=f"Multiple failed login attempts detected for username: {username}"
            )
                raise HTTPException(
                status_code=429,
                detail="Too many failed login attempts."
            )

            return None

        # when login is successful reset counter
        self.failed_login_counter[key] = 0  
        
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