from urllib.parse import urlparse
import ipaddress
from models.url_checks import URLChecks
from datetime import datetime


class URLService:
    def __init__(self, db):
        self.db = db

    # check if it is valid url that contains IP address
    def has_ip(self, url: str):
        host = urlparse(url).hostname

        if not host:
            return False

        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            return False

    # extract features logic from the URL
    def extract_features(self, url: str):
        return {
            "url_length": len(url),
            "dots": url.count('.'),
            "dashes": url.count('-'),
            "has_ip": self.has_ip(url),
            "has_https": url.startswith('https://'),
        }

    # calculate risk based on the hardcoded features
    def calc_risk(self, features):
        score = 0
        if features["url_length"] > 75:
            score += 25

        if features["dashes"] > 3:
            score += 15

        if features["dots"] > 3:
            score += 15

        if not features["has_https"]:
            score += 10
        return score

    # label the risk based on the calculated score
    def classify_risk(self, score):
        if score > 70:
            return "Phishing"
        elif score > 40:
            return "Suspicious"
        else:
            return "safe"

    def save_check(self, url: str, score: float, label: str, user_id: int):
        check = URLChecks(
            user_id=user_id,
            url_address=url,
            risk_score=score,
            prediction=label,
        )

        self.db.add(check)
        self.db.commit()
        self.db.refresh(check)

        return check