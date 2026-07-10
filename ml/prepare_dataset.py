import pandas as pd
import os 
import sys



# Get project root directory 
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)
# add root dir to module search
sys.path.append(PROJECT_ROOT)

from utils.feature_extractor import extract_features

dataset_path = os.path.join(PROJECT_ROOT, "ml", "data", "phishing_dataset.csv") # build path to original phishing dataset

df = pd.read_csv(dataset_path) # load raw dataset



features = [] # store extracted features for each URL

# extract features from each URL in the dataset
for _, row in df.iterrows():

    url = row["URL"]
    
    # Kaggle dataset:
    # label 1 = legitimate
    # label 0 = phishing
    #
    # Convert labels:
    # 0 = legitimate
    # 1 = phishing
    label = 0 if row["label"] == 1 else 1
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    extracted = extract_features(url) # convert raw URL into numerical features

        
    # create feature vector usable for model input
    features.append([
        extracted["url_length"],
        extracted["dots"],
        extracted["dashes"],
        int(extracted["has_ip"]),
        int(extracted["has_https"]),
        int(extracted["has_scheme"]),
        int(extracted["subdomain_count"]),
        int(extracted["suspicious_tld"]),
        int(extracted["free_hosting"]),
        int(extracted["brand_match"]),
        int(extracted["brand_impersonation"]),
        int(extracted["phishing_keyword"]),
        int(extracted["generic_keyword"]),
        int(extracted["suspicious_subdomain"]),
        int(extracted["trusted_domain"]),
        label
    ])


    
new_df = pd.DataFrame(features, columns=[
    "url_length",
    "dots",
    "dashes",
    "has_ip",
    "has_https",
    "has_scheme",
    "subdomain_count",
    "suspicious_tld",
    "free_hosting",
    "brand_match",
    "brand_impersonation",
    "phishing_keyword",
    "generic_keyword",
    "suspicious_subdomain",
    "trusted_domain",
    "label"
])
print(new_df.head())
print(new_df.columns)
print(new_df["subdomain_count"].value_counts())

output_path = os.path.join(PROJECT_ROOT,"ml", "dataset_features.csv")
new_df.to_csv(output_path, index=False) # save processed dataset for model training

print("Original labels:")
print(df["label"].value_counts())
print("Prepared labels:")
print(new_df["label"].value_counts())
print(f"Dataset prepared: {len(new_df)} samples")


