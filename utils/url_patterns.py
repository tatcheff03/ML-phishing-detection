
# suspictious top-level domain (commonly abused)
SUSPICIOUS_TLDS = (
    '.cfd',
    '.tk',
    '.ml',
    '.ga',
    '.cf',
    '.gq',
    '.top',
    '.xyz',
    '.club',
    '.online',
    '.site',
    '.space',
    '.click',
    '.link',
    '.live',
    '.icu',
    '.sbs',
    '.cam',
    '.shop',
    '.one',
    '.autos',
    '.life',
    '.qpon',
    '.uno',
    '.ink',
    '.cyou',
)

# free hosting platforms
FREE_HOSTING_SUFFIXES = (
    '.vercel.app',
    '.netlify.app',
    '.web.app',
    '.firebaseapp.com',
    '.pages.dev',
    '.onrender.com',
    '.github.io',
    '.replit.app',
    '.replit.dev',
    '.glitch.me',
    '.gitlab.io',
    '.surge.sh',
    '.fly.dev'
)

# bg courier brands (often impersonated)
BG_COURIER_BRANDS = (
    'econt',
    'speedy',
    'bulgariapost',
    'bgpost',
    'bg-post',
    'samedaybg',
    'boxnowbg',
    'expressonebg'
)

# international brands
GLOBAL_BRANDS = (
    "gmail",
    "google",
    "paypal",
    "microsoft",
    "apple",
    "amazon",
    "facebook",
    "instagram",
    "github",
    "gitlab",
    "stackoverflow",
    "youtube",
    "wikipedia",
    "linkedin",
    "statista",
    "aws",
)


# bg government related brands 
BULGARIAN_GOVT_BRANDS = (
    'mvr',      
    'mvrbg',      
    'mvr-bg',     
    'e-uslugi',   
    'euslugi',    
    'mvr-gov',    
)

# verified brands
TRUSTED_DOMAINS = (
    "google.com",
    "gmail.com",
    "youtube.com",

    "paypal.com",

    "microsoft.com",
    "outlook.com",
    "office.com",
    "azure.com",

    "apple.com",
    "icloud.com",

    "amazon.com",
    "aws.amazon.com",

    "facebook.com",
    "instagram.com",

    "github.com",
    "gitlab.com",

    "stackoverflow.com",
    "stackexchange.com",

    "wikipedia.org",
    "linkedin.com",

    "econt.com",
    "speedy.bg",
    "bgpost.bg",

    "mvr.bg",
    "egov.bg",
    "bnb.bg",
    
    "statista.com",
    "docs.python.org",
    "python.org",
    "react.dev",
    "developer.mozilla.org",
    "w3.org",
    "pypi.org",
    "npmjs.com",
    "docker.com",
    "fastapi.tiangolo.com",
    "scikit-learn.org",
    "numpy.org",
    "pandas.pydata.org",
    )

# generic delivery keywords (weak signal) )
GENERIC_KEYWORDS = [
    "login",
    "account",
    "update",
    "payment",
    "delivery",
    "shipment",
    "client"
]

# strong phishing intent keywords (high signal)
PHISHING_KEYWORDS = (
   "verify account",
    "suspended",
    "urgent action",
    "confirm identity",
    "security alert",
    "payment failed",
    "account locked"
)