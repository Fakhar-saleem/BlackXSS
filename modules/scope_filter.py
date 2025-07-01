
from urllib.parse import urlparse
from utils.logger import log

class ScopeFilter:
    def __init__(self, scope_domain=None):
        """
        scope_domain: e.g., 'example.com'. If None, all domains are allowed.
        """
        self.scope = scope_domain

    def is_allowed(self, url):
        """
        Return True if the URL’s domain matches the scope (or if no scope is set).
        """
        if not self.scope:
            return True
        try:
            domain = urlparse(url).netloc
            allowed = self.scope.lower() in domain.lower()
            if not allowed:
                log(f"[SCOPE FILTER] Skipping out-of-scope URL: {url}")
            return allowed
        except Exception as e:
            log(f"[SCOPE FILTER ERROR] {url}: {e}")
            return False
