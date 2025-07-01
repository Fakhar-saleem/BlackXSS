"""
Global configuration settings for BlackXSS.
Modify these values or override via CLI arguments or environment variables.
"""

import os

# General settings
PROJECT_NAME      = os.getenv('BXXS_PROJECT_NAME', 'BlackXSS')
VERSION           = os.getenv('BXXS_VERSION', '1.0.0')
LOG_FORMAT        = os.getenv('BXXS_LOG_FORMAT', '[{timestamp}] {message}')
DEFAULT_LOG_FILE  = os.getenv('BXXS_LOG_FILE', 'blackxss.log')

# Crawling settings
DEFAULT_CRAWL_DEPTH    = int(os.getenv('BXXS_CRAWL_DEPTH', 3))
CRAWL_DELAY_SECONDS    = float(os.getenv('BXXS_CRAWL_DELAY', 0.5))
MAX_CRAWL_THREADS      = int(os.getenv('BXXS_CRAWL_THREADS', 5))

# HTTP client settings
DEFAULT_TIMEOUT        = float(os.getenv('BXXS_TIMEOUT', 10.0))
MAX_RETRIES            = int(os.getenv('BXXS_MAX_RETRIES', 2))
RETRY_DELAY_SECONDS    = float(os.getenv('BXXS_RETRY_DELAY', 1.0))
USER_AGENT_LIST        = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "BlackXSS/1.0"
]

# Injection settings
PAYLOAD_FILE_PATH       = os.getenv('BXXS_PAYLOAD_FILE', 'payload.txt')
INJECTION_MODE          = os.getenv('BXXS_INJECTION_MODE', 'reflected')  # reflected, stored, dom
MAX_INJECTION_THREADS   = int(os.getenv('BXXS_INJECT_THREADS', 10))

# DOM detection settings
HEADLESS_BROWSER        = os.getenv('BXXS_HEADLESS', 'True').lower() in ['true', '1']
BROWSER_LAUNCH_TIMEOUT  = int(os.getenv('BXXS_BROWSER_TIMEOUT', 15000))
SCREENSHOT_ON_HIT       = os.getenv('BXXS_SCREENSHOT', 'False').lower() in ['true', '1']
SCREENSHOT_DIR          = os.getenv('BXXS_SCREENSHOT_DIR', 'screenshots/')

# Reporting settings
REPORT_TEMPLATE_DIR     = os.getenv('BXXS_TEMPLATE_DIR', 'reporting/templates')
DEFAULT_TEMPLATE        = os.getenv('BXXS_TEMPLATE', 'report.html.j2')
REPORT_OUTPUT_DIR       = os.getenv('BXXS_REPORT_DIR', 'reports/')
EXPORT_JSON             = os.getenv('BXXS_EXPORT_JSON', 'True').lower() in ['true', '1']
EXPORT_CSV              = os.getenv('BXXS_EXPORT_CSV', 'False').lower() in ['true', '1']

# Plugin settings
PLUGIN_DIRECTORY        = os.getenv('BXXS_PLUGIN_DIR', 'plugins/')
ENABLE_PLUGIN_AUTODISC  = os.getenv('BXXS_PLUGIN_AUTO', 'True').lower() in ['true', '1']

# Authentication defaults
AUTH_CONFIG_PATH        = os.getenv('BXXS_AUTH_CONFIG', None)
AUTH_RETRY_COUNT        = int(os.getenv('BXXS_AUTH_RETRIES', 1))
AUTH_TIMEOUT            = float(os.getenv('BXXS_AUTH_TIMEOUT', 5.0))

# Misc settings
OUTPUT_VERBOSE          = os.getenv('BXXS_VERBOSE', 'False').lower() in ['true', '1']
MAX_TOTAL_TIMEOUT       = float(os.getenv('BXXS_MAX_TOTAL_TIMEOUT', 3600.0))  # in seconds
