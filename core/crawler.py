# core/crawler.py

import time
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
from utils.http_client import HTTPClient
from utils.helpers import is_valid_url, normalize_url
# from modules.scope_filter import ScopeFilter  # COMMENTED OUT
from config.settings import CRAWL_DELAY_SECONDS, DEFAULT_CRAWL_DEPTH
from utils.logger import log

def crawl_site(start_url, depth=None, scope=None):
    """
    Crawl the target site starting from start_url.
    - depth: maximum link depth (overrides DEFAULT_CRAWL_DEPTH if provided)
    - scope: domain to restrict crawling (simplified implementation)
    Returns a list of discovered URLs.
    """
    max_depth = depth if depth is not None else DEFAULT_CRAWL_DEPTH
    
    # Simple scope filtering without ScopeFilter class
    allowed_domain = None
    if scope:
        if scope.startswith(('http://', 'https://')):
            allowed_domain = urlparse(scope).netloc
        else:
            allowed_domain = scope
        log(f"[CRAWL] Limiting crawl to domain: {allowed_domain}")
    
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
                
                # Simple scope check
                should_crawl = is_valid_url(full) and full not in visited
                if allowed_domain:
                    parsed_url = urlparse(full)
                    url_domain = parsed_url.netloc.lower()
                    should_crawl = should_crawl and (url_domain == allowed_domain.lower() or url_domain.endswith('.' + allowed_domain.lower()))
                
                if should_crawl:
                    to_visit.append((full, lvl + 1))

        except Exception as e:
            log(f"[CRAWL ERROR] {url} - {e}")

    log(f"[CRAWL] Completed crawl: {len(discovered)} URLs found")
    return discovered