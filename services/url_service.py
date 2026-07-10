from utils.feature_extractor import extract_features
from models.url_checks import URLChecks
from utils.activities_actions import URL_CHECK


class URLService:
    PHISHING_THRESHOLD = 70
    SUSPICIOUS_THRESHOLD = 40
    MAX_RULE_SCORE = 120
    
    RULE_WEIGHT=0.6
    ML_WEIGHT=0.4
    
    def __init__(self, db, activitylog_service, anomaly_service, ml_service):
        self.db = db
        self.activitylog_service = activitylog_service
        self.anomaly_service = anomaly_service
        self.ml_service = ml_service
        


    # all methods executed when checking a probale phishing URL
    def check_url(self, url: str, user_id: int, ip_address: str) -> URLChecks:
        endpoint = "/check"
        
        features = extract_features(url)
        
        # exctracted features converted into input vector for the ML model
        features_vector = [
            features["url_length"],
            features["dots"],
            features["dashes"],
            int(features["has_ip"]),
            int(features["has_https"]),
            int(features["has_scheme"]),
            int(features["subdomain_count"]),
            int(features["suspicious_tld"]),
            int(features["free_hosting"]),
            int(features["brand_match"]),
            int(features["brand_impersonation"]),
            int(features["phishing_keyword"]),
            int(features["generic_keyword"]),
            int(features["suspicious_subdomain"]),
            int(features["trusted_domain"])
        ]
    
        
        # rule-based score      
        raw_rule_score = self.calc_risk(features)
        rule_score = min((raw_rule_score / self.MAX_RULE_SCORE) * 100, 100)
        
        # ML model score
        ml_score = self.ml_service.predict(features_vector)
        
        print (features_vector)
        print ("ML:", ml_score)
        
        # hybrid decision 
        final_score = (rule_score * self.RULE_WEIGHT) + (ml_score * self.ML_WEIGHT)  # final score is a weighted average 60/40
        label = self.classify_risk(final_score) 

        # save to DB
        check = self.save_check(url, rule_score, ml_score, final_score, label, user_id)
        
        # create anomaly when URL is phishing
        if final_score >= self.PHISHING_THRESHOLD:
            self.anomaly_service.create_anomaly(
                user_id=user_id,
                risk_score=final_score,  
                description=f"Phishing URL detected: {url}"
            )
        print (features)
        # log the activity
        self._log(
            user_id=user_id,
            action=URL_CHECK,
            endpoint=endpoint,
            ip_address=ip_address
        )

        return check

    # calculate structural risk
    def structural_risk(self, features):
        score = 0
        score += 40 if features["has_ip"] else 0
        score += 15 if features["url_length"] > 120 else 0
        score += 15 if features["dashes"] > 3 else 0
        score += 10 if features["dots"] > 3 and not features["brand_match"] else 0
        score += 10 if features["has_scheme"] and not features["has_https"] else 0
        return score

    # calculate domain risk
    def domain_risk(self, features):
        score = 0
        score += 30 if features["suspicious_tld"] else 0
        score += 20 if features["free_hosting"] else 0
        return score

    # calculate brand impersonation risk
    def brand_risk(self, f):
        
        if f["brand_match"] and f["suspicious_tld"] :
            return 50
        
        if f["brand_match"] and f["free_hosting"]:
            return 40
        

        return 0
        
    # calculate risk by spec.keywords
    def keyword_risk(self, features):
        score = 0
        score += 10 if features["phishing_keyword"] else 0
        score += 5 if features["generic_keyword"] else 0
        return score

    # label the risk based on the calculated score
    def classify_risk(self, final_score:float)-> str:
        if final_score >= self.PHISHING_THRESHOLD:
            return "Phishing"
        if final_score >= self.SUSPICIOUS_THRESHOLD:
            return "Suspicious"
        
        return "Safe"


    #calculate total risk score
    def calc_risk(self, features:dict)-> float:
        score = 0

        score += self.structural_risk(features)
        score += self.domain_risk(features)
        score += self.brand_risk(features)
        score += self.keyword_risk(features)

        return score

    def save_check(self, url: str,rule_score: float, ml_score: float, final_score: float, label: str, user_id: int):
        check = URLChecks(
            user_id=user_id,
            url_address=url,
            rule_score=round(rule_score, 2),
            ml_score=round(ml_score, 2),
            final_score=round(final_score, 2),
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