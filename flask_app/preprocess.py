import re
import tldextract
from urllib.parse import urlparse, unquote

def preprocess_url(url):
    features = []

    # URL_Length
    features.append(len(url))

    # Special characters
    special_chars = ['@', '?', '-', '=', '.', '#', '%', '+', '$', '!', ',', '//']
    for char in special_chars:
        features.append(url.count(char))

    # Abnormal_URL
    hostname = urlparse(url).hostname
    hostname = str(hostname)
    match = re.search(hostname, url)
    features.append(1 if match else 0)

    # Has_HTTPS
    features.append(1 if "https" in url else 0)

    # Digit_Count and Letter_Count
    digits = sum(c.isdigit() for c in url)
    letters = sum(c.isalpha() for c in url)
    features.append(digits)
    features.append(letters)

    # Has_Shortening_Service
    shortening_pattern = r'bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|' \
                     r'yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|' \
                     r'short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|' \
                     r'doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|' \
                     r'db\.tt|qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|' \
                     r'q\.gs|is\.gd|po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|' \
                     r'x\.co|prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|' \
                     r'tr\.im|link\.zip\.net'
    features.append(1 if re.search(shortening_pattern, url, flags=re.I) else 0)

    # Has_IP_Address
    ip_pattern = (
    r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
    r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'
    r'(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.'
    r'([01]?\d\d?|2[0-4]\d|25[0-5])\/)|'
    r'((0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\.(0x[0-9a-fA-F]{1,2})\/)'
    r'(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}|'
    r'([0-9]+(?:\.[0-9]+){3}:[0-9]+)|'
    r'((?:(?:\d|[01]?\d\d|2[0-4]\d|25[0-5])\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d|\d)(?:\/\d{1,2})?)'
)
    features.append(1 if re.search(ip_pattern, url, flags=re.I) else 0)

    # Has_javascript_Code
    if re.search(r'javascript:', url):
        features.append(1)
    elif re.search(r'<\s*script', url, re.IGNORECASE) or re.search(r'on\w*=', url, re.IGNORECASE):
        features.append(1)
    else:
        features.append(0)

    # Has_Text_Encoding
    parsed_url = urlparse(url)
    text_part = parsed_url.path
    decoded_text = unquote(text_part)
    features.append(1 if decoded_text != text_part else 0)
    
    return features
