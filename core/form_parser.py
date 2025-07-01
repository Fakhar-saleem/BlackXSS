
from bs4 import BeautifulSoup
from utils.http_client import HTTPClient
from urllib.parse import urljoin
from utils.logger import log

def parse_forms(urls):
    """
    Given a list of URLs, fetch each page and extract form details.
    Returns a list of dicts: {
        'page_url': original page,
        'action': full form action URL,
        'method': HTTP method ('get' or 'post'),
        'inputs': {name: default_value}
    }
    """
    client = HTTPClient()
    forms = []
    log(f"[FORMS] Starting form parsing on {len(urls)} URLs")

    for page_url in urls:
        try:
            resp = client.get(page_url)
            soup = BeautifulSoup(resp.text, "html.parser")
            for form in soup.find_all("form"):
                action = form.get("action") or page_url
                full_action = urljoin(page_url, action)
                method = form.get("method", "get").lower()
                inputs = {}
                for inp in form.find_all(["input", "textarea"]):
                    name = inp.get("name")
                    if not name:
                        continue
                    value = inp.get("value") or ""
                    inputs[name] = value
                forms.append({
                    "page_url": page_url,
                    "action": full_action,
                    "method": method,
                    "inputs": inputs
                })
            log(f"[FORMS] Parsed {len(forms)} forms so far")
        except Exception as e:
            log(f"[FORMS ERROR] {page_url} - {e}")

    log(f"[FORMS] Completed parsing forms: {len(forms)} total")
    return forms
