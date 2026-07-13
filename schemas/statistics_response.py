from pydantic import BaseModel

# stats response for admin dashboard
class StatisticsResponse(BaseModel):

    total_users: int

    total_url_checks: int

    phishing_detected: int

    total_anomalies: int

    failed_logins: int
