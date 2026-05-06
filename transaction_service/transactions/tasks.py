from celery import shared_task
from django.utils import timezone

from transactions.models import Transaction


@shared_task
def auto_delete_old_transactions():
    """
    PRD requires 30-day cleanup from user history while retaining records for audit.
    We soft-delete by hiding old records from default querysets.
    """
    now = timezone.now()
    updated = Transaction.objects.filter(
        delete_at__lte=now,
        is_soft_deleted=False,
    ).update(is_soft_deleted=True)
    return updated


@shared_task(bind=True)
def confirm_transaction(self, transaction_id: str):
    tx = Transaction.objects.get(id=transaction_id)
    tx.status = "confirmed"
    tx.version = tx.version + 1
    tx.save(update_fields=["status", "version"])
    return str(tx.id)
