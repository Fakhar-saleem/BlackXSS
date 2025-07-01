
import os
import datetime
from config.settings import DEFAULT_LOG_FILE, LOG_FORMAT, OUTPUT_VERBOSE

class Logger:
    _log_file = None

    @classmethod
    def init(cls, path=None):
        cls._log_file = path or DEFAULT_LOG_FILE
        # Ensure directory exists
        os.makedirs(os.path.dirname(cls._log_file) or '.', exist_ok=True)
        with open(cls._log_file, 'w') as f:
            header = f"=== XSS Log started by Fakhar Saleem at {datetime.datetime.now()} ===\n"
            f.write(header)
        if OUTPUT_VERBOSE:
            print(header.strip())

    @classmethod
    def log(cls, message):
        if cls._log_file is None:
            cls.init()
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = LOG_FORMAT.format(timestamp=timestamp, message=message)
        with open(cls._log_file, 'a') as f:
            f.write(entry + "\n")
        if OUTPUT_VERBOSE:
            print(entry)

# Shortcut functions
def init_logger(path=None):
    Logger.init(path)

def log(message):
    Logger.log(message)
