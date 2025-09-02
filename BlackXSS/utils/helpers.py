"""Helper functions"""
from urllib.parse import urlparse, urljoin

def is_valid_url(url):
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def normalize_url(base, link):
    return urljoin(base, link).split('#')[0]
