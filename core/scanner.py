
from core.crawler import crawl_site
from core.form_parser import parse_forms
from core.injector import inject_payloads, inject_forms
from engine.js_engine import run_dom_detection
from reporting.reporter import Reporter
from modules.auth_manager import AuthManager
from utils.logger import log

def run_full_scan(args):
    log("[SCAN] Starting BlackXSS full scan")
    findings = []

    # Auth
    if args.auth:
        auth_mgr = AuthManager(args.auth)
        auth_mgr.authenticate(None)  # will bind later if needed

    # Crawl
    urls = [args.url]
    if not args.skip_crawl:
        urls = crawl_site(args.url, depth=args.depth, scope=args.scope)

    # Form Parsing
    forms = []
    if not args.skip_forms:
        forms = parse_forms(urls)

    # URL-based injection
    if not args.skip_inject:
        for url in urls:
            results = inject_payloads(url)
            findings.extend(results)

    # Form-based injection
    if not args.skip_inject:
        results = inject_forms(forms)
        findings.extend(results)

    # DOM-based detection
    if not args.skip_dom:
        for url in urls:
            results = run_dom_detection(url)
            findings.extend(results)

    # Plugins (future module)
    if not args.skip_plugins:
        log("[PLUGINS] Skipped plugin engine (not implemented)")

    # Report
    reporter = Reporter(args.template)
    reporter.generate(findings, args.output)

    log(f"[SCAN] Scan completed. {len(findings)} potential XSS issues found.")
