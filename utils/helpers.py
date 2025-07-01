
from urllib.parse import urlparse, urljoin
from config.settings import USER_AGENT_LIST
import random

def is_valid_url(url):
    """
    Check if the URL has a valid scheme and netloc.
    """
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def normalize_url(base, link):
    """
    Resolve relative links against the base URL and strip fragments.
    """
    return urljoin(base, link).split('#')[0]

def get_random_user_agent():
    """
    Return a random User‑Agent header from the configured list.
    """
    return random.choice(USER_AGENT_LIST)
