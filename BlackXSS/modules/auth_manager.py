"""Handle authentication configurations"""
import json

class AuthManager:
    def __init__(self, auth_config_path=None):
        self.config = {}
        if auth_config_path:
            with open(auth_config_path) as f:
                self.config = json.load(f)

    def authenticate(self, client):
        if not self.config:
            return
        method = self.config.get("method")
        if method == "basic":
            client.session.auth = (self.config["username"], self.config["password"])
        # Extend for form-based or token...
