# core/scanner.py

import time
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from core.crawler import crawl_site
from core.form_parser import parse_forms
from core.injector import inject_payloads, inject_forms
from engine.js_engine import run_dom_detection
from reporting.reporter import Reporter
# from modules.auth_manager import AuthManager  # COMMENTED OUT
from utils.logger import log

def run_full_scan(args):
    """
    Main scanning function with improved threading and error handling
    """
    log("[SCAN] Starting BlackXSS full scan")
    start_time = time.time()
    findings = []
    
    try:
        # Authentication setup - DISABLED
        # auth_mgr = None
        if args.auth:
            log("[AUTH WARNING] Authentication feature disabled - ignoring --auth parameter")
            # try:
            #     auth_mgr = AuthManager(args.auth)
            #     log("[AUTH] Authentication manager initialized")
            # except Exception as e:
            #     log(f"[AUTH ERROR] Failed to initialize auth: {e}")

        # Crawling phase
        urls = [args.url]
        if not args.skip_crawl:
            try:
                log("[CRAWL] Starting crawling phase...")
                urls = crawl_site(args.url, depth=args.depth, scope=args.scope)
                if not urls:
                    log("[CRAWL WARNING] No URLs found during crawling, using base URL only")
                    urls = [args.url]
                log(f"[CRAWL] Found {len(urls)} URLs to test")
            except Exception as e:
                log(f"[CRAWL ERROR] Crawling failed: {e}")
                urls = [args.url]

        # Form parsing phase
        forms = []
        if not args.skip_forms:
            try:
                log("[FORMS] Starting form parsing phase...")
                forms = parse_forms(urls)
                log(f"[FORMS] Found {len(forms)} forms to test")
            except Exception as e:
                log(f"[FORMS ERROR] Form parsing failed: {e}")

        # URL-based injection phase (with threading)
        if not args.skip_inject:
            try:
                log("[INJECT] Starting URL injection phase...")
                url_findings = []
                
                max_workers = min(args.threads, len(urls), 10)  # Limit max workers
                with ThreadPoolExecutor(max_workers=max_workers) as executor:
                    future_to_url = {executor.submit(inject_payloads, url): url for url in urls}
                    
                    for future in as_completed(future_to_url):
                        url = future_to_url[future]
                        try:
                            results = future.result(timeout=30)  # 30 second timeout per URL
                            url_findings.extend(results)
                        except Exception as e:
                            log(f"[INJECT ERROR] Failed to test {url}: {e}")
                
                findings.extend(url_findings)
                log(f"[INJECT] URL injection completed: {len(url_findings)} findings")
                
            except Exception as e:
                log(f"[INJECT ERROR] URL injection phase failed: {e}")

        # Form-based injection phase
        if not args.skip_inject and forms:
            try:
                log("[INJECT] Starting form injection phase...")
                form_findings = inject_forms(forms)
                findings.extend(form_findings)
                log(f"[INJECT] Form injection completed: {len(form_findings)} findings")
            except Exception as e:
                log(f"[INJECT FORMS ERROR] Form injection failed: {e}")

        # DOM-based detection phase
        if not args.skip_dom:
            try:
                log("[DOM] Starting DOM detection phase...")
                dom_findings = []
                
                # Limit DOM testing to prevent browser overload
                test_urls = urls[:10]  # Test only first 10 URLs for DOM XSS
                
                for url in test_urls:
                    try:
                        results = run_dom_detection(url)
                        dom_findings.extend(results)
                    except Exception as e:
                        log(f"[DOM ERROR] DOM detection failed for {url}: {e}")
                
                findings.extend(dom_findings)
                log(f"[DOM] DOM detection completed: {len(dom_findings)} findings")
                
            except Exception as e:
                log(f"[DOM ERROR] DOM detection phase failed: {e}")

        # Reporting phase
        try:
            log("[REPORT] Generating reports...")
            reporter = Reporter(args.template)
            reporter.generate(findings, args.output)
            log(f"[REPORT] Reports generated successfully")
        except Exception as e:
            log(f"[REPORT ERROR] Report generation failed: {e}")
            # Try to save findings as JSON at least
            try:
                import json
                fallback_path = args.output.replace('.html', '_fallback.json')
                with open(fallback_path, 'w') as f:
                    json.dump(findings, f, indent=2)
                log(f"[REPORT] Saved fallback JSON report to {fallback_path}")
            except:
                log("[REPORT ERROR] Could not save fallback report")

    except KeyboardInterrupt:
        log("[SCAN] Scan interrupted by user")
    except Exception as e:
        log(f"[SCAN ERROR] Unexpected error during scan: {e}")
    finally:
        end_time = time.time()
        duration = end_time - start_time
        log(f"[SCAN] Scan completed in {duration:.2f} seconds")
        log(f"[SCAN] Total findings: {len(findings)}")
        
        # Print summary to console
        print(f"\n=== BLACKXSS SCAN SUMMARY ===")
        print(f"Duration: {duration:.2f} seconds")
        print(f"URLs tested: {len(urls)}")
        print(f"Forms tested: {len(forms)}")
        print(f"Total findings: {len(findings)}")
        
        if findings:
            print(f"\n=== FINDINGS BY TYPE ===")
            finding_types = {}
            for finding in findings:
                ftype = finding.get('type', 'Unknown')
                finding_types[ftype] = finding_types.get(ftype, 0) + 1
            
            for ftype, count in finding_types.items():
                print(f"{ftype}: {count}")
        else:
            print("No XSS vulnerabilities found.")
            
        print(f"\nReport saved to: {args.output}")
        if findings:
            print("\n⚠️  WARNING: XSS vulnerabilities found! Review the report immediately.")