"""Logging utility"""
import datetime

def init_logger(log_file='blackxss.log'):
    with open(log_file, 'w') as f:
        f.write('=== BlackXSS Log ===\n')

def log(message, log_file='blackxss.log'):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, 'a') as f:
        f.write(f'[{timestamp}] {message}\n')
