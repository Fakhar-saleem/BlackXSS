# BlackXSS

**BlackXSS** is a powerful, extensible, and modular XSS vulnerability scanner built in Python. It crawls target websites, parses forms, injects payloads, and performs DOM-based detection using Playwright.

## Author
Fakhar Saleem

## Features
- Multi-layered XSS scanning: reflected, stored, and DOM-based
- Headless browser support for DOM XSS (via Playwright)
- Automatic crawling with depth control
- Form extraction and injection
- User-defined payload support via `payload.txt`
- Modular plugin-ready structure
- HTML, JSON, and optional CSV report generation

## Usage
```bash
python3 blackxss.py https://example.com --payload-file payload.txt --output results/report.html
```

## Arguments (CLI)
| Argument        | Description                             |
|----------------|-----------------------------------------|
| `url`          | Base URL to scan                        |
| `--depth`      | Crawl depth (default: 3)                |
| `--threads`    | Number of concurrent threads            |
| `--auth`       | Path to auth config JSON                |
| `--payload-file` | Path to your XSS payloads file        |
| `--output`     | HTML report output file                 |
| `--log-file`   | Log output path                         |
| `--skip-*`     | Skip any phase: crawl, inject, dom, etc |

## Requirements
- Python 3.8+
- Playwright (`pip install playwright && playwright install`)
- `beautifulsoup4`, `jinja2`, `requests`



