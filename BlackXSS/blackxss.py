#!/usr/bin/env python3
"""BlackXSS - Advanced XSS Vulnerability Scanner"""
import argparse
from cli.cli import build_parser
from utils.logger import init_logger
from core.scanner import run_full_scan

def main():
    parser = build_parser()
    args = parser.parse_args()
    init_logger(args.log_file)
    run_full_scan(args)

if __name__ == "__main__":
    main()
