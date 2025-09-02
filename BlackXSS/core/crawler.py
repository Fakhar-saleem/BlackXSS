"""URL and link crawler with scope and depth"""
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from utils.http_client import HTTPClient
from utils.helpers import is_valid_url, normalize_url
from modules.scope_filter import ScopeFilter
from config.settings import DEPTH, USER_AGENT
from utils.logger import log

def crawl_site(start_url, depth=None, scope=None):
    max_depth = depth or DEPTH
    sf = ScopeFilter(scope)
    client = HTTPClient(headers={'User-Agent': USER_AGENT})
    to_visit = [(start_url, 0)]
    visited = set()
    discovered = set()

    while to_visit:
        url, lvl = to_visit.pop(0)
        if url in visited or lvl > max_depth:
            continue
        try:
            resp = client.get(url)
            visited.add(url)
            discovered.add(url)
            log(f"[CRAWL] {url} (lvl {lvl})")
            soup = BeautifulSoup(resp.text, "html.parser")
            for a in soup.find_all("a", href=True):
                full = normalize_url(url, a['href'])
                if is_valid_url(full) and full not in visited and sf.is_allowed(full):
                    to_visit.append((full, lvl+1))
        except Exception as e:
            log(f"[CRAWL ERR] {url} - {e}")
    return list(discovered)
