
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

# bg government related brands 
BULGARIAN_GOVT_BRANDS = (
    'mvr',      
    'mvrbg',      
    'mvr-bg',     
    'e-uslugi',   
    'euslugi',    
    'mvr-gov',    
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