#!/usr/bin/env python3
"""
blackxss.py - Main entry point for XSS Tool
Author: Fakhar Saleem
Do not modify this file. Use CLI arguments to control execution.
"""
import argparse
from cli.cli import build_parser
from utils.logger import init_logger
from core.scanner import run_full_scan
from config.settings import PROJECT_NAME, VERSION

def main():
    print(f"{PROJECT_NAME} v{VERSION} - By Fakhar Saleem")
    parser = build_parser()
    args = parser.parse_args()
    init_logger(args.log_file)
    run_full_scan(args)

if __name__ == "__main__":
    main()
