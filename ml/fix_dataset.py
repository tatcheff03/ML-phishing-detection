import pandas as pd
from urllib.parse import urlparse


backup = pd.read_csv(
    "ml/data/phishing_dataset_backup.csv"
)


legitimate_domains = [
    # Google
    "google.com",
    "gmail.com",
    "youtube.com",
    "cloud.google.com",

    # Microsoft
    "microsoft.com",
    "outlook.com",
    "office.com",
    "office365.com",
    "live.com",
    "azure.com",
    "azure.microsoft.com",

    # Apple
    "apple.com",
    "icloud.com",
    "appleid.apple.com",
    "developer.apple.com",

    # Amazon
    "amazon.com",
    "amazon.co.uk",
    "aws.amazon.com",

    # Developer platforms
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "stackoverflow.com",
    "stackexchange.com",
    "npmjs.com",
    "pypi.org",
    "docker.com",
    "kubernetes.io",

    # Documentation
    "docs.python.org",
    "developer.mozilla.org",
    "w3.org",

    # Education / Bulgaria
    "nbu.bg",
    "student.nbu.bg",
    "mvr.bg",
    "egov.bg",
    "bnb.bg",

    # Other popular
    "wikipedia.org",
    "linkedin.com",
    "facebook.com",
    "instagram.com",
    "paypal.com",
]


def get_domain(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    return urlparse(url).netloc.lower().removeprefix("www.")


fixed = 0


for index, row in backup.iterrows():

    domain = get_domain(row["URL"])

    if any(
        domain == legit or domain.endswith("." + legit)
        for legit in legitimate_domains
    ):
        if backup.loc[index, "label"] != 1:
            backup.loc[index, "label"] = 1
            fixed += 1

backup.to_csv(
    "ml/data/phishing_dataset.csv",
    index=False
)


print("Dataset fixed")
print("Changed labels:", fixed)


print(
    backup[
        backup["URL"].str.contains(
            "github|google|stackoverflow|statista",
            case=False,
            na=False
        )
    ][["URL","label"]]
)