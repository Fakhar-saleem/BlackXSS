"""HTTP client wrapper with session management"""
import requests
from utils.logger import log

class HTTPClient:
    def __init__(self, timeout=10, headers=None):
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        self.timeout = timeout

    def get(self, url):
        log(f"HTTP GET {url}")
        return self.session.get(url, timeout=self.timeout)

    def post(self, url, data):
        log(f"HTTP POST {url} data={data}")
        return self.session.post(url, data=data, timeout=self.timeout)
