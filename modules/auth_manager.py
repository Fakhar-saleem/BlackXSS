
import json
from utils.logger import log
from utils.http_client import HTTPClient

class AuthManager:
    def __init__(self, auth_config_path=None):
        """
        auth_config_path: Path to a JSON file with auth settings.
        Example JSON:
        {
            "method": "form",
            "login_url": "https://example.com/login",
            "fields": {
                "username": "user",
                "password": "pass"
            },
            "success_indicator": "Welcome"
        }
        """
        self.config = {}
        if auth_config_path:
            try:
                with open(auth_config_path) as f:
                    self.config = json.load(f)
                log(f"[AUTH] Loaded config from {auth_config_path}")
            except Exception as e:
                log(f"[AUTH ERROR] Could not load config: {e}")

    def authenticate(self, client: HTTPClient):
        """
        Perform authentication on the provided HTTPClient session.
        Supports 'basic' and 'form' methods.
        """
        method = self.config.get("method")
        if method == "basic":
            creds = (self.config.get("username"), self.config.get("password"))
            client.session.auth = creds
            log("[AUTH] Set HTTP Basic auth credentials")
        elif method == "form":
            url = self.config.get("login_url")
            fields = self.config.get("fields", {})
            success_str = self.config.get("success_indicator", "")
            try:
                resp = client.post(url, data=fields)
                if success_str in resp.text:
                    log("[AUTH] Form-based login successful")
                else:
                    log("[AUTH] Form-based login may have failed")
            except Exception as e:
                log(f"[AUTH ERROR] Form login exception: {e}")
        else:
            log("[AUTH] No valid authentication method specified or no --auth used")
