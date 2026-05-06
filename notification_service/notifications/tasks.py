from celery import shared_task
from notifications.models import Notification

@shared_task
def send_due_reminder():
    """
    Due reminders are created by the transaction flow; this task can be used by
    beat to report pending reminders and trigger downstream alerting hooks.
    """
    return Notification.objects.filter(type="due_reminder", is_read=False).count()

