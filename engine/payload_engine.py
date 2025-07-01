
import os
from utils.logger import log
from config.settings import PAYLOAD_FILE_PATH

class PayloadEngine:
    def __init__(self, payload_file=None):
        self.payload_file = payload_file or PAYLOAD_FILE_PATH
        self.payloads = []
        self.load_payloads()

    def load_payloads(self):
        """
        Read payloads from the configured payload file, ignoring empty lines and comments.
        """
        if not os.path.isfile(self.payload_file):
            log(f"[PAYLOAD] Payload file not found: {self.payload_file}")
            return
        try:
            with open(self.payload_file, 'r') as f:
                for line in f:
                    pl = line.strip()
                    if not pl or pl.startswith('#'):
                        continue
                    self.payloads.append(pl)
            log(f"[PAYLOAD] Loaded {len(self.payloads)} payloads")
        except Exception as e:
            log(f"[PAYLOAD ERROR] Could not load payloads: {e}")

    def get_all(self):
        """Return the list of all loaded payloads."""
        return self.payloads.copy()

    def count(self):
        """Return the number of loaded payloads."""
        return len(self.payloads)

# Helper function
_payload_engine = None

def load_payloads(path=None):
    global _payload_engine
    if _payload_engine is None:
        _payload_engine = PayloadEngine(path)
    return _payload_engine.get_all()
