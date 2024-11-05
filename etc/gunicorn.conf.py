import multiprocessing
import os
from pathlib import Path

workers = multiprocessing.cpu_count() * 2 + 1
BASE_DIR = Path(__file__).resolve().parent.parent

bind = '0.0.0.0:8000'

loglevel = 'info'

accesslog = os.path.join(BASE_DIR, 'logs/access.log')
errorlog = os.path.join(BASE_DIR, 'logs/gunicorn.log')

timeout = 30

worker_connections = 1000

max_requests = 1000

max_requests_jitter = 50
