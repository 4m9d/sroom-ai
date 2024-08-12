from celery import Celery

celery_app = Celery(
    'celery',
    broker='redis://127.0.0.1:6379',
    backend='redis://127.0.0.1:6379',
    include=['app.index'])
