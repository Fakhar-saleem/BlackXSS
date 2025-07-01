
import time
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from utils.http_client import HTTPClient
from utils.helpers import is_valid_url, normalize_url
from modules.scope_filter import ScopeFilter
from config.settings import CRAWL_DELAY_SECONDS, DEFAULT_CRAWL_DEPTH
from utils.logger import log

def crawl_site(start_url, depth=None, scope=None):
    """
    Crawl the target site starting from start_url.
    - depth: maximum link depth (overrides DEFAULT_CRAWL_DEPTH if provided)
    - scope: domain to restrict crawling
    Returns a list of discovered URLs.
    """
    max_depth = depth if depth is not None else DEFAULT_CRAWL_DEPTH
    sf = ScopeFilter(scope)
    client = HTTPClient()
    to_visit = [(start_url, 0)]
    visited = set()
    discovered = []

    log(f"[CRAWL] Starting crawl at {start_url} with max_depth={max_depth}")

    while to_visit:
        url, lvl = to_visit.pop(0)
        if url in visited or lvl > max_depth:
            continue

        try:
            resp = client.get(url)
            visited.add(url)
            discovered.append(url)
            log(f"[CRAWL] Visited ({lvl}): {url}")
            time.sleep(CRAWL_DELAY_SECONDS)

            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.find_all("a", href=True):
                full = normalize_url(url, a['href'])
                if is_valid_url(full) and sf.is_allowed(full) and full not in visited:
                    to_visit.append((full, lvl + 1))

        except Exception as e:
            log(f"[CRAWL ERROR] {url} - {e}")

    log(f"[CRAWL] Completed crawl: {len(discovered)} URLs found")
    return discovered
