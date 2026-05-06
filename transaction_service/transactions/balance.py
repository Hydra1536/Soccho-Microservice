from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from shared.encryption import decrypt_field, encrypt_field
from shared.exceptions import OptimisticLockError
from transactions.models import Balance


User = get_user_model()


def _ordered_pair(user_a: User, user_b: User):
    if str(user_a.id) <= str(user_b.id):
        return user_a, user_b
    return user_b, user_a


def update_balance(giver: User, receiver: User, amount):
    """
    Maintain materialized net balance with row lock + optimistic version.
    Positive value means user_a is owed by user_b.
    """
    amount = Decimal(str(amount))
    ordered_a, ordered_b = _ordered_pair(giver, receiver)
    delta = amount if str(giver.id) == str(ordered_a.id) else -amount

    with transaction.atomic():
        balance, _ = Balance.objects.select_for_update().get_or_create(
            user_a=ordered_a,
            user_b=ordered_b,
            defaults={"net_balance_encrypted": encrypt_field("0")},
        )

        current = Decimal(decrypt_field(balance.net_balance_encrypted))
        old_version = balance.version
        balance.net_balance_encrypted = encrypt_field(current + delta)
        balance.version = old_version + 1
        balance.updated_at = timezone.now()
        balance.save(update_fields=["net_balance_encrypted", "version", "updated_at"])

        refreshed_version = Balance.objects.get(pk=balance.pk).version
        if refreshed_version != old_version + 1:
            raise OptimisticLockError("Balance updated concurrently")

        return balance
