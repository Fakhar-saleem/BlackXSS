import argparse

def build_parser():
    parser = argparse.ArgumentParser(
        prog='blackxss',
        description='BlackXSS - All-in-one XSS Scanner'
    )
    parser.add_argument('url', help='Base URL to scan (e.g., https://example.com)')
    parser.add_argument('--depth',        type=int,   default=3,     help='Crawl depth')
    parser.add_argument('--threads',      type=int,   default=10,    help='Number of worker threads')
    parser.add_argument('--scope',        type=str,               help='Domain scope filter (e.g., example.com)')
    parser.add_argument('--auth',         type=str,               help='Path to auth config JSON')
    parser.add_argument('--payload-file', type=str, default='payload.txt', help='Payload list file')
    parser.add_argument('--plugins',      type=str, default='plugins',    help='Custom plugin directory')
    parser.add_argument('--output',       type=str, default='report.html', help='HTML report file')
    parser.add_argument('--template',     type=str, default='report.html.j2', help='Jinja2 template')
    parser.add_argument('--log-file',     type=str, default='blackxss.log',  help='Log file path')
    parser.add_argument('--skip-crawl',   action='store_true', help='Skip crawling step')
    parser.add_argument('--skip-inject',  action='store_true', help='Skip injection step')
    parser.add_argument('--skip-dom',     action='store_true', help='Skip DOM detection step')
    parser.add_argument('--skip-forms',   action='store_true', help='Skip form parsing step')
    parser.add_argument('--skip-plugins', action='store_true', help='Skip plugin scanning step')
    return parser
