
import os
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from utils.logger import log
from config.settings import BROWSER_LAUNCH_TIMEOUT, HEADLESS_BROWSER, SCREENSHOT_ON_HIT, SCREENSHOT_DIR
from engine.payload_engine import load_payloads

# Ensure screenshot directory exists if needed
if SCREENSHOT_ON_HIT:
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

def run_dom_detection(url):
    """
    Launch a headless browser, navigate to the URL,
    inject payloads via DOM APIs, and detect execution.
    Returns list of findings: dicts with type, url, payload, screenshot (optional).
    """
    findings = []
    payloads = load_payloads()
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=HEADLESS_BROWSER, timeout=BROWSER_LAUNCH_TIMEOUT)
        page = browser.new_page()
        try:
            # Navigate to the target page
            page.goto(url, timeout=BROWSER_LAUNCH_TIMEOUT)
            # For each payload, execute it in page context and check for reflection
            for idx, payload in enumerate(payloads):
                try:
                    # Use evaluate to insert payload into location.hash
                    script = f"window.location.hash = '#{payload}';"
                    page.evaluate(script)
                    page.wait_for_timeout(500)  # wait for JS execution
                    content = page.content()
                    if payload in content:
                        finding = {
                            "type": "DOM",
                            "url": url,
                            "payload": payload
                        }
                        # Capture screenshot if enabled
                        if SCREENSHOT_ON_HIT:
                            screenshot_path = os.path.join(SCREENSHOT_DIR, f"screenshot_{idx}.png")
                            page.screenshot(path=screenshot_path)
                            finding["screenshot"] = screenshot_path
                        findings.append(finding)
                        log(f"[DOM] XSS payload reflected on {url}")
                        break  # Stop on first hit per URL
                except PlaywrightTimeoutError:
                    log(f"[DOM TIMEOUT] Waiting on payload {payload} at {url}")
                except Exception as e:
                    log(f"[DOM ERROR] {url} payload injection error: {e}")
        except PlaywrightTimeoutError:
            log(f"[DOM TIMEOUT] Navigation timeout for {url}")
        except Exception as e:
            log(f"[DOM ERROR] Navigation failed {url}: {e}")
        finally:
            browser.close()
    return findings
