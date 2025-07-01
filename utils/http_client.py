# utils/http_client.py

import requests
from requests.adapters import HTTPAdapter, Retry
from utils.logger import log
from config.settings import DEFAULT_TIMEOUT, MAX_RETRIES, RETRY_DELAY_SECONDS, USER_AGENT_LIST

class HTTPClient:
    def __init__(self, timeout=DEFAULT_TIMEOUT, headers=None):
        self.session = requests.Session()
        retry_strategy = Retry(
            total=MAX_RETRIES,
            backoff_factor=RETRY_DELAY_SECONDS,
            status_forcelist=[429, 500, 502, 503, 504],
            method_whitelist=["HEAD", "GET", "OPTIONS", "POST"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("https://", adapter)
        self.session.mount("http://", adapter)
        self.session.headers.update(headers or {})
        # set random user-agent
        self.session.headers.update({"User-Agent": __import__('random').choice(USER_AGENT_LIST)})
        self.timeout = timeout

    def get(self, url, **kwargs):
        try:
            log(f"HTTP GET {url}")
            return self.session.get(url, timeout=self.timeout, **kwargs)
        except Exception as e:
            log(f"HTTP GET ERROR {url}: {e}")
            raise

    def post(self, url, data=None, **kwargs):
        try:
            log(f"HTTP POST {url} data={data}")
            return self.session.post(url, data=data, timeout=self.timeout, **kwargs)
        except Exception as e:
            log(f"HTTP POST ERROR {url}: {e}")
            raise
