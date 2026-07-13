from sqlalchemy.orm import Session

from models.user import User
from models.activity_logs import ActivityLogs
from models.url_checks import URLChecks
from models.anomalies import Anomalies

class StatisticsService:


    def __init__(self, db: Session):

        self.db = db


    
    # stats for admin dashboard
    def get_statistics(self):

        return {

            "total_users":
                self.db.query(User).count(),


            "total_url_checks":
                self.db.query(URLChecks).count(),


            "phishing_detected":
                self.db.query(URLChecks)
                .filter(
                    URLChecks.prediction == "Phishing"
                )
                .count(),


            "total_anomalies":
                self.db.query(Anomalies).count(),


            "failed_logins":
                self.db.query(ActivityLogs)
                .filter(
                    ActivityLogs.action == "FAILED_LOGIN"
                )
                .count()

        }