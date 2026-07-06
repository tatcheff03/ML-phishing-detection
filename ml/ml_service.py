import os
import joblib
import pandas as pd

class MLService:
    
    FEATURE_COLUMNS = [
    "url_length",
    "dots",
    "dashes",
    "has_ip",
    "has_https",
    "suspicious_tld",
    "free_hosting",
    "brand_match",
    "phishing_keyword",
    "generic_keyword"
    ]
    
    # load trained model
    def __init__(self,model_path = 'model.pkl'):
       
       # get current directory and append it (recieve model.pkl path)
       base_dir = os.path.dirname(os.path.abspath(__file__))
       full_path = os.path.join(base_dir, model_path)

       self.model = joblib.load(full_path) 
    

    # returns the probability of a URL being phishing (in percentage)
    def predict(self, features_vector):
        features = pd.DataFrame([features_vector], columns=self.FEATURE_COLUMNS) # convert feature vector -> DataFrame with the orig. feature names
        # get phishing probability
        proba = self.model.predict_proba(features)[0][1]
        return float(proba * 100)  
    
