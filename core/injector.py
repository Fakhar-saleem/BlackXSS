
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse
from utils.http_client import HTTPClient
from engine.payload_engine import load_payloads
from utils.logger import log

def inject_payloads(url):
    """
    Inject payloads into URL query parameters and check for reflected XSS.
    Returns a list of findings: dicts with keys: type, url, payload.
    """
    client = HTTPClient()
    results = []
    parsed = urlparse(url)
    qs = parse_qs(parsed.query)

    if qs:
        for payload in load_payloads():
            new_qs = {k: payload for k in qs}
            encoded = urlencode(new_qs, doseq=True)
            injected_url = urlunparse(parsed._replace(query=encoded))
            try:
                resp = client.get(injected_url)
                if payload in resp.text:
                    finding = {"type": "Reflected", "url": injected_url, "payload": payload}
                    results.append(finding)
                    log(f"[INJECT] XSS found at {injected_url}")
            except Exception as e:
                log(f"[INJECT ERROR] {injected_url}: {e}")

    return results

# Form injection

def inject_forms(forms):
    """
    Inject payloads into parsed HTML forms.
    forms: list of dicts with page_url, action, method, inputs
    Returns list of findings.
    """
    client = HTTPClient()
    findings = []
    for form in forms:
        action = form['action']
        method = form['method']
        base_data = form['inputs']
        for payload in load_payloads():
            data = {k: payload if k in base_data else v for k, v in base_data.items()}
            try:
                if method == 'post':
                    resp = client.post(action, data=data)
                else:
                    # merge into URL
                    parsed = urlparse(action)
                    qs = {k: payload for k in qs} if 'qs' in locals() else {}
                    url = urlunparse(parsed._replace(query=urlencode(qs)))
                    resp = client.get(url)
                if payload in resp.text:
                    finding = {"type": "Stored", "url": action, "payload": payload}
                    findings.append(finding)
                    log(f"[INJECT FORM] XSS found in form at {action}")
            except Exception as e:
                log(f"[INJECT FORM ERROR] {action}: {e}")
    return findings
