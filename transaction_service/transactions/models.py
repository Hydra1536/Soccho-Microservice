import uuid
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from shared.encryption import decrypt_field, encrypt_field


User = get_user_model()


class Transaction(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("denied", "Denied"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    giver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions_given")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="transactions_received")
    amount_encrypted = models.TextField()
    due_date_encrypted = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    idempotency_key = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    delete_at = models.DateTimeField(null=True, blank=True)
    version = models.PositiveIntegerField(default=0)
    is_soft_deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=["giver"]),
            models.Index(fields=["receiver"]),
            models.Index(fields=["status"]),
            models.Index(fields=["idempotency_key"]),
            models.Index(fields=["delete_at"]),
        ]

    def save(self, *args, **kwargs):
        if not self.delete_at:
            base = self.created_at or timezone.now()
            self.delete_at = base + timedelta(days=30)
        super().save(*args, **kwargs)

    @property
    def amount(self) -> Decimal:
        return Decimal(decrypt_field(self.amount_encrypted))

    @amount.setter
    def amount(self, value):
        self.amount_encrypted = encrypt_field(value)

    @property
    def due_date(self):
        if not self.due_date_encrypted:
            return None
        return decrypt_field(self.due_date_encrypted)

    @due_date.setter
    def due_date(self, value):
        if value in (None, ""):
            self.due_date_encrypted = None
        else:
            self.due_date_encrypted = encrypt_field(value)


class Balance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    user_b = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+")
    net_balance_encrypted = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    version = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ("user_a", "user_b")
        constraints = [
            models.CheckConstraint(
                check=models.Q(user_a__lt=models.F("user_b")),
                name="user_a_lt_user_b",
            )
        ]

    @property
    def net_balance(self) -> Decimal:
        return Decimal(decrypt_field(self.net_balance_encrypted))

    @net_balance.setter
    def net_balance(self, value):
        self.net_balance_encrypted = encrypt_field(value)
