import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from shared.encryption import encrypt_field


class CustomUser(AbstractUser):
    email_encrypted = models.TextField(blank=True, default="")
    loyalty_score = models.DecimalField(max_digits=7, decimal_places=4, default=0.0)
    google_id = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def save(self, *args, **kwargs):
        if self.email:
            self.email_encrypted = encrypt_field(self.email)
        super().save(*args, **kwargs)


class OTPToken(models.Model):
    PURPOSE_CHOICES = [
        ("register", "register"),
        ("reset", "reset"),
        ("change_pw", "change_pw"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=64)
    purpose = models.CharField(max_length=20, choices=PURPOSE_CHOICES)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["user", "purpose", "used"])]


class RefreshToken(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    token_hash = models.CharField(max_length=255)
    expires_at = models.DateTimeField()
    revoked = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["token_hash"]), models.Index(fields=["user", "revoked"])]
