from urllib.parse import urlparse
import ipaddress
from models.url_checks import URLChecks
from utils.url_patterns import *
from utils.activities_actions import URL_CHECK


class URLService:
    def __init__(self, db, activitylog_service, anomaly_service):
        self.db = db
        self.activitylog_service = activitylog_service
        self.anomaly_service = anomaly_service

    # all methods executed when checking a probale phishing URL
    def check_url(self, url: str, user_id: int, ip_address: str):
        endpoint = "/check"
        
        features = self.extract_features(url)
        score = self.calc_risk(features)
        label = self.classify_risk(score)

        check = self.save_check(url, score, label, user_id)
        
        # create anomaly when URL is phishing
        if label == "Phishing":
            self.anomaly_service.create_anomaly(
                user_id=user_id,
                risk_score=score,  
                description=f"Phishing URL detected: {url}"
            )

        # log the activity
        self._log(
            user_id=user_id,
            action=URL_CHECK,
            endpoint=endpoint,
            ip_address=ip_address
        )

        return check
    
    # check if it is valid url that contains IP address
    def has_ip(self, parsed):
        host = parsed.hostname

        if not host:
            return False

        try:
            ipaddress.ip_address(host)
            return True
        except ValueError:
            return False

    # extract features logic from the URL
    def extract_features(self, url: str):
        url = url.strip().lower() # normalize url
        
        has_https = url.startswith("https://") # check if orig.URl uses https
        url_for_parse = url
        
        # Add default scheme so urlparse extracts the hostname
        if not url_for_parse.startswith(('http://', 'https://')):
            url_for_parse = 'https://' + url_for_parse 
        parsed = urlparse(url_for_parse)

        domain = (parsed.hostname or "").lower() # extract normalized hostname 
        text = url.replace("-", " ").replace("_", " ") # prepare text for keyword search
        return {
            "url_length": len(url),
            "dots": url.count('.'),
            "dashes": url.count('-'),
            "has_ip": self.has_ip(parsed),
            "has_https": has_https,

            "domain": domain,

            "suspicious_tld": any(domain.endswith(tld) for tld in SUSPICIOUS_TLDS),
            "free_hosting": any(domain.endswith(h) for h in FREE_HOSTING_SUFFIXES),

            "brand_match": any(
                b in domain for b in (BG_COURIER_BRANDS + BULGARIAN_GOVT_BRANDS)
            ),
        
            "text":text,
            "phishing_keyword": any(k in text for k in PHISHING_KEYWORDS),
            "generic_keyword": any(k in text for k in GENERIC_KEYWORDS)
            
            
        }
        


    # calculate structural risk
    def structural_risk(self, features):
        score = 0
        score += 40 if features["has_ip"] else 0
        score += 25 if features["url_length"] > 75 else 0
        score += 15 if features["dashes"] > 3 else 0
        score += 10 if features["dots"] > 3 and not features["brand_match"] else 0
        score += 10 if not features["has_https"] else 0 
        return score

    # calculate domain risk
    def domain_risk(self, features):
        score = 0
        score += 30 if features["suspicious_tld"] else 0
        score += 20 if features["free_hosting"] else 0
        return score

    # calculate brand impersonation risk
    def brand_risk(self, f):
        
        is_impersonation = (f["brand_match"] and 
                           (f["suspicious_tld"] or f["free_hosting"]))
        if is_impersonation:
            return 30

        return 0
        
    # calculate risk by spec.keywords
    def keyword_risk(self, features):
        score = 0
        score += 10 if features["phishing_keyword"] else 0
        score += 5 if features["generic_keyword"] else 0
        return score

    # label the risk based on the calculated score
    def classify_risk(self, score):
        if score >= 70:
            return "Phishing"
        elif score >= 40:
            return "Suspicious"
        else:
            return "safe"


    #calculate total risk score
    def calc_risk(self, features):
        score = 0

        score += self.structural_risk(features)
        score += self.domain_risk(features)
        score += self.brand_risk(features)
        score += self.keyword_risk(features)

        return score

    def save_check(self, url: str, score: float, label: str, user_id: int):
        check = URLChecks(
            user_id=user_id,
            url_address=url,
            risk_score=score,
            prediction=label
        )

        self.db.add(check)
        self.db.commit()
        self.db.refresh(check)

        return check
    
    # helper method for logging
    def _log(self, *, user_id= None, action, endpoint, ip_address):
        self.activitylog_service.log_activity(
            user_id=user_id,
            action=action,
            endpoint=endpoint,
            ip_address=ip_address
        )