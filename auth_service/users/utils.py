import hashlib
import random
from datetime import timedelta

from django.utils import timezone

from users.models import OTPToken


def hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_otp(user_id, purpose: str) -> str:
    otp = "".join(str(random.randint(0, 9)) for _ in range(6))
    OTPToken.objects.create(
        user_id=user_id,
        token_hash=hash_token(otp),
        purpose=purpose,
        expires_at=timezone.now() + timedelta(minutes=10),
    )
    return otp


def verify_otp(token: str, purpose: str, user_id=None) -> bool:
    queryset = OTPToken.objects.filter(
        token_hash=hash_token(token),
        purpose=purpose,
        used=False,
    )
    if user_id:
        queryset = queryset.filter(user_id=user_id)

    token_obj = queryset.first()
    if token_obj and token_obj.expires_at > timezone.now():
        token_obj.used = True
        token_obj.save(update_fields=["used"])
        return True
    return False
