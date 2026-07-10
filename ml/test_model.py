import os
import sys

# Get project root directory 
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
# add root dir to module search
sys.path.append(PROJECT_ROOT)

from utils.feature_extractor import extract_features
from ml_service import MLService


service = MLService()



test_urls = [

# legitimate
# "https://google.com",
# "https://mail.google.com",
# "https://github.com",
# "https://github.com/login",
# "https://stackoverflow.com",
# "https://stackoverflow.com/questions",
# "https://aws.amazon.com",
# "https://console.aws.amazon.com",
# "https://www.statista.com/statistics/273018/number-of-internet-users-worldwide/",
# "https://www.wikipedia.org",
# "https://www.youtube.com",

# # phishing
# "https://google-security-alert.com",
# "https://paypal-login-security.xyz",
# "https://amazon-security-check.xyz",
# "https://apple-id-verification.com",
# "https://microsoft-login-support.com",
# "https://fake-github-login.com",
# "http://192.168.1.50/login",
# "https://github.com.security-check.xyz",
# "https://amazon.verify-account.xyz"

#bonus
"gmail.com",
"www.gmail.com",
"http://gmail.com"



]

for url in test_urls:

    features = extract_features(url)

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

    risk_score = service.predict(features_vector)

    prediction = "phishing" if risk_score >= 50 else "legitimate"

    print("=" * 80)
    print("URL:", url)
    print("Features:", features)
    print("Prediction:", prediction)
    print("Risk:", round(risk_score, 2), "%")