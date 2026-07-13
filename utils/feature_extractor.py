from urllib.parse import urlparse
import ipaddress
from typing import Dict, Any

from utils.url_patterns import *


# check if the URL contains an IP address 
def has_ip(parsed):
    host = parsed.hostname

    if not host:
        return False

    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        return False


# check if domain contains an exact trusted brand name
def has_brand_match(domain):

    normalized = domain.replace("-", ".")
    parts = normalized.split(".")

    return any(
        brand in parts
        for brand in ALL_BRANDS
    )

# check if domain belongs to official trusted domain
def is_trusted_domain(domain):

    for trusted in TRUSTED_DOMAINS:

        if domain == trusted or domain.endswith("." + trusted):
            return True

    return False


# check if domain imitates a trusted brand
def is_brand_impersonation(domain):

    if is_trusted_domain(domain):
        return False

    normalized = domain.replace("-", ".")

    parts = normalized.split(".")

    return any(
        brand in parts
        for brand in ALL_BRANDS
    )

# number of subdomains
def get_subdomain_count(domain):

    parts = domain.split(".")

    # remove main domain and TLD
    if len(parts) <= 2:
        return 0

    return len(parts) - 2


# Check for suspicious subdomains
def has_suspicious_subdomain(domain):

    parts = domain.split(".")

    if len(parts) <= 2:
        return False

    subdomains = parts[:-2]

    for subdomain in subdomains:
        for keyword in GENERIC_KEYWORDS:
            if keyword in subdomain:
                return True

    return False


# Extract features from URL
def extract_features(original_url: str) -> Dict[str, Any]:

    original_url = original_url.strip().lower()

    # Original URL 
    has_scheme = original_url.startswith(("http://", "https://"))
    has_https = original_url.startswith("https://")

    # URL for parsing
    url = original_url

    if not has_scheme:
        url = "https://" + url

    parsed = urlparse(url)

    domain = (parsed.hostname or "").lower()
    

    # Remove "www." prefix
    if domain.startswith("www."):
        domain = domain[4:]
    
    trusted_domain = is_trusted_domain(domain)

    subdomain_count = get_subdomain_count(domain)

    suspicious_subdomain = has_suspicious_subdomain(domain)

    # analyze based on normalized domain
    text = domain.replace("-", " ").replace("_", " ")

    return {

        
        "url_length": len(original_url),
        "dots": original_url.count("."),
        "dashes": original_url.count("-"),

        "has_ip": has_ip(parsed),

        "has_https": has_https,
        "has_scheme": has_scheme,


        
        "subdomain_count": subdomain_count,

        "suspicious_tld": any(
            domain.endswith(tld)
            for tld in SUSPICIOUS_TLDS
        ),

        "free_hosting": any(
            domain.endswith(h)
            for h in FREE_HOSTING_SUFFIXES
        ),


       
        "brand_match": has_brand_match(domain),
        "trusted_domain": trusted_domain,

        "brand_impersonation": is_brand_impersonation(domain),


        "text": text,

        "phishing_keyword": any(
            k in text
            for k in PHISHING_KEYWORDS
        ),

        "generic_keyword": any(
            k in text
            for k in GENERIC_KEYWORDS
        ),


        
        "domain": domain,

        "suspicious_subdomain": suspicious_subdomain,
    }