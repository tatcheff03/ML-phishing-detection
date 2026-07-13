from models.anomalies import Anomalies

class AnomalyService:
    def __init__(self, db):
        self.db = db

    # crud method to create anomaly
    def create_anomaly(self, user_id, risk_score, description):
        anomaly = Anomalies(
            user_id=user_id,
            risk_score=risk_score,
            description=description
        )
        self.db.add(anomaly)
        self.db.commit()
        self.db.refresh(anomaly)
        return anomaly
    # list all anomalies
    def get_all_anomalies(self):
        return self.db.query(Anomalies).order_by(Anomalies.created_at.desc()).all()

    # list anomalies for user
    def get_user_anomalies(self, user_id):
        return self.db.query(Anomalies).filter(Anomalies.user_id == user_id).order_by(Anomalies.created_at.desc()).all()

    # latest 10 anomalies
    def get_recent_anomalies_by_user(self, user_id: int, limit: int = 10):
        return (
            self.db.query(Anomalies)
            .filter(Anomalies.user_id == user_id)
            .order_by(Anomalies.created_at.desc())
            .limit(limit)
            .all()
        )
