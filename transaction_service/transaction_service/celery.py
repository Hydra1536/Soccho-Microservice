import os
from datetime import timedelta

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'transaction_service.settings')

app = Celery('transaction_service')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete-old-transactions-daily": {
        "task": "transactions.tasks.auto_delete_old_transactions",
        "schedule": timedelta(days=1),
    },
}

