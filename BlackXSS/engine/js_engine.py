"""DOM XSS detection using Playwright"""
from playwright.sync_api import sync_playwright
from utils.logger import log

def run_dom_detection(url):
    hits = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, timeout=10000)
            content = page.content()
            for payload in load_payloads():
                if payload in content:
                    hits.append({"type":"DOM","url":url,"payload":payload})
                    log(f"[DOM] XSS at {url}")
                    break
        except Exception as e:
            log(f"[DOM ERR] {url} - {e}")
        browser.close()
    return hits
