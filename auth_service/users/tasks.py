from celery import shared_task
from django.utils import timezone
from users.models import OTPToken

@shared_task
def cleanup_expired_otps():
    now = timezone.now()
    OTPToken.objects.filter(expires_at__lt=now).delete()

