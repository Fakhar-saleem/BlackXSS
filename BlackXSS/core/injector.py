"""Inject payloads into URL parameters and forms"""
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.http_client import HTTPClient
from engine.payload_engine import load_payloads
from utils.logger import log

def inject_payloads(url):
    client = HTTPClient()
    results = []
    # URL params
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)
    if qs:
        for payload in load_payloads():
            new_qs = {k: payload for k in qs}
            new_url = urlunparse(parsed._replace(query=urlencode(new_qs, doseq=True)))
            resp = client.get(new_url)
            if payload in resp.text:
                log(f"[XSS] {new_url}")
                results.append({"type":"Reflected","url":new_url,"payload":payload})
    return results
