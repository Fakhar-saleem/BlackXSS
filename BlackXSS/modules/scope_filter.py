"""Filter URLs based on domain scope"""
from urllib.parse import urlparse

class ScopeFilter:
    def __init__(self, scope):
        self.scope = scope

    def is_allowed(self, url):
        if not self.scope:
            return True
        netloc = urlparse(url).netloc
        return self.scope in netloc
