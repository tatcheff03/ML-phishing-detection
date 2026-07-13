from sqlalchemy.orm import joinedload

from models.activity_logs import ActivityLogs

class ActivityLogService:
    def __init__(self, db):
        self.db = db
        
    # log a new activity from user
    def log_activity(self, user_id: int, action: str, endpoint: str, ip_address: str | None, url_check_id:int | None = None):
        log = ActivityLogs(user_id=user_id, action=action, endpoint=endpoint, ip_address=ip_address, url_check_id=url_check_id)
        self.db.add(log)
        self.db.commit()
        self.db.refresh(log)
        return log
    
    def get_all_logs(self):
        return self.db.query(ActivityLogs).order_by(ActivityLogs.created_at.desc()).all()
    
    def get_all_logs_by_user(self, user_id: int):
        return self.db.query(ActivityLogs).options(joinedload(ActivityLogs.url_check)).filter(ActivityLogs.user_id == user_id).order_by(ActivityLogs.created_at.desc()).all()
    
    def get_recent_logs_by_user(self, user_id: int, limit: int = 10):
        return (
            self.db.query(ActivityLogs)
            .options(joinedload(ActivityLogs.url_check))
            .filter(ActivityLogs.user_id == user_id)
            .order_by(ActivityLogs.created_at.desc())
            .limit(limit)
            .all()
        )
    
    # get recent 40 logs
    def get_recent_logs(self, limit: int = 40):
        return self.db.query(ActivityLogs).order_by(ActivityLogs.created_at.desc()).limit(limit).all()
    
    # filter logs by action
    def get_logs_by_action(self, action: str):
        return self.db.query(ActivityLogs).filter(ActivityLogs.action == action).order_by(ActivityLogs.created_at.desc()).all()