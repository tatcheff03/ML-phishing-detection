import random
import pandas as pd

def generate(n=5000):
    data = []

    for _ in range(n):
        
        # --- realistic distributions ---
        url_length = int(random.gauss(80, 25))
        url_length = max(15, min(200, url_length))  # clamp

        dots = max(1, int(random.gauss(2.5, 1.2)))
        dashes = max(0, int(random.gauss(1.5, 1)))

        # --- probabilistic features ---
        has_ip = 1 if random.random() < 0.08 else 0
        has_https = 1 if random.random() < 0.7 else 0

        suspicious_tld = 1 if random.random() < 0.15 else 0
        free_hosting = 1 if random.random() < 0.10 else 0

        brand_match = 1 if random.random() < 0.12 else 0

        phishing_keyword = 1 if (
            random.random() < 0.2 and url_length > 70
        ) else 0

        generic_keyword = 1 if random.random() < 0.25 else 0

        # --- rule-based scoring --- #
        score = 0

        if has_ip:
            score += 45

        if url_length > 120:
            score += 35
        elif url_length > 90:
            score += 25

        if dashes > 3:
            score += 15

        if dots > 3:
            score += 10

        if not has_https:
            score += 12

        if suspicious_tld:
            score += 25

        if free_hosting:
            score += 20

        if brand_match and (suspicious_tld or free_hosting):
            score += 35

        if phishing_keyword:
            score += 10

        if generic_keyword:
            score += 5

        # --- noise (imperfection of real-world ) ---
        score += random.randint(-8, 8)

        # --- final label ---
        label = 1 if score >= 70 else 0

        data.append([
            url_length,
            dots,
            dashes,
            has_ip,
            has_https,
            suspicious_tld,
            free_hosting,
            brand_match,
            phishing_keyword,
            generic_keyword,
            label
        ])

    df = pd.DataFrame(data, columns=[
        "url_length",
        "dots",
        "dashes",
        "has_ip",
        "has_https",
        "suspicious_tld",
        "free_hosting",
        "brand_match",
        "phishing_keyword",
        "generic_keyword",
        "label"
    ])

    df.to_csv("dataset.csv", index=False)
    print(f"Dataset generated successfully ({n} samples)")

generate()