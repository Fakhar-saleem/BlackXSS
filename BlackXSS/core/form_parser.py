"""Discover and parse HTML forms for auto-submission"""
from bs4 import BeautifulSoup
from utils.logger import log

def parse_forms(html_urls):
    forms = []
    from utils.http_client import HTTPClient
    client = HTTPClient()
    for url in html_urls:
        try:
            resp = client.get(url)
            soup = BeautifulSoup(resp.text, "html.parser")
            for f in soup.find_all("form"):
                action = f.get('action') or url
                method = f.get('method', 'get').lower()
                inputs = {i.get('name'): i.get('value', '') for i in f.find_all('input') if i.get('name')}
                forms.append({"url": url, "action": action, "method": method, "inputs": inputs})
            log(f"[FORM] Parsed forms from {url}")
        except Exception as e:
            log(f"[FORM ERR] {url} - {e}")
    return forms
