import pandas as pd

df = pd.read_csv("ml/data/phishing_dataset.csv")


# for url in [
#     "github.com",
#     "stackoverflow.com",
#     "statista.com"
# ]:
#     print("\n", url)

#     print(
#         df[
#             df["URL"].str.contains(
#                 url,
#                 case=False,
#                 na=False
#             )
#         ]["label"].value_counts()
#     )

tests = [
    "github.com",
    "stackoverflow.com",
    "statista.com",
    "google.com",
    "aws.amazon.com",
    "fake-github-login.com",
    "google-security-alert.com"
]


for t in tests:
    print("\n", t)

    print(
        df[
            df["URL"].str.contains(
                t,
                case=False,
                na=False
            )
        ][["URL","label"]]
    )