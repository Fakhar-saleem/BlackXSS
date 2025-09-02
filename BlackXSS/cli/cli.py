"""Command-line parser definitions"""
import argparse

def build_parser():
    parser = argparse.ArgumentParser(description='BlackXSS CLI')
    parser.add_argument('url', help='Target URL to scan')
    parser.add_argument('--depth', type=int, default=None, help='Crawl depth')
    parser.add_argument('--threads', type=int, default=None, help='Number of threads')
    parser.add_argument('--scope', type=str, default=None, help='Domain scope filter (e.g. example.com)')
    parser.add_argument('--auth', type=str, default=None, help='Path to auth config file (JSON)')
    parser.add_argument('--output', type=str, default='report.html', help='Output report file')
    parser.add_argument('--log-file', type=str, default='blackxss.log', help='Log file path')
    parser.add_argument('--headless', action='store_true', help='Enable headless browser mode for DOM XSS')
    return parser
