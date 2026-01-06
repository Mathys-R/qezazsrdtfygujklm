import time
import sys
from datetime import datetime

def log_message(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}", flush=True)

if __name__ == '__main__':
    log_message('Application started')
    while True:
        time.sleep(300)
        log_message('5 minutes have passed')
