from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from jose import jwt
from ninja import Router
from ninja.errors import HttpError
from pydantic import BaseModel

from users.utils import create_otp, verify_otp
from users.email_service import send_otp_email_sync


User = get_user_model()
router = Router()
ALGORITHM = "HS256"


class LoginSchema(BaseModel):
    email: str
    password: str


class RegisterSchema(BaseModel):
    username: str
    email: str
    password: str
    confirm_password: str


class OTPSchema(BaseModel):
    email: str
    otp: str


class ForgotPasswordSchema(BaseModel):
    email: str


class ResetPasswordSchema(BaseModel):
    email: str
    otp: str
    new_password: str
    confirm_password: str


def _issue_tokens(user):
    now = timezone.now()
    access_payload = {
        "user_id": str(user.id),
        "username": user.username,
        "exp": now + timedelta(hours=1),
        "type": "access",
    }
    refresh_payload = {
        "user_id": str(user.id),
        "exp": now + timedelta(hours=12),
        "type": "refresh",
    }
    return {
        "access_token": jwt.encode(access_payload, settings.SECRET_KEY, algorithm=ALGORITHM),
        "refresh_token": jwt.encode(refresh_payload, settings.SECRET_KEY, algorithm=ALGORITHM),
    }


@router.post("/login")
def login(request, payload: LoginSchema):
    user = User.objects.filter(email__iexact=payload.email, is_active=True).first()
    if not user or not user.check_password(payload.password):
        raise HttpError(401, "Invalid credentials")
    return _issue_tokens(user)


@router.post("/register")
def register(request, payload: RegisterSchema):
    if payload.password != payload.confirm_password:
        raise HttpError(400, "Passwords do not match")
    if User.objects.filter(username__iexact=payload.username).exists():
        raise HttpError(400, "Username already exists")
    if User.objects.filter(email__iexact=payload.email).exists():
        raise HttpError(400, "Email already exists")

    user = User.objects.create_user(
        username=payload.username,
        email=payload.email,
        password=payload.password,
        is_active=True,
    )
    otp = create_otp(user.id, "register")

    # Send OTP via FormSubmit.co (free, no credentials needed)
    email_sent = send_otp_email_sync(payload.email, otp, purpose="register")
    if not email_sent:
        # Log but don't fail - user can retry
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to send registration OTP to {payload.email}")
    
    return {"message": "OTP sent to your email"}


@router.post("/otp-verify")
def otp_verify(request, payload: OTPSchema):
    user = User.objects.filter(email__iexact=payload.email).first()
    if not user:
        raise HttpError(400, "Invalid OTP")

    if not verify_otp(payload.otp, "register", user.id):
        raise HttpError(400, "Invalid OTP")

    return _issue_tokens(user)


@router.post("/forgot-password")
def forgot_password(request, payload: ForgotPasswordSchema):
    user = User.objects.filter(email__iexact=payload.email, is_active=True).first()
    if not user:
        # Avoid user enumeration - always return success message
        return {"message": "If the email exists, an OTP was sent"}

    otp = create_otp(user.id, "reset")
    
    # Send OTP via FormSubmit.co (free, no credentials needed)
    email_sent = send_otp_email_sync(payload.email, otp, purpose="reset")
    if not email_sent:
        import logging
        logger = logging.getLogger(__name__)
        logger.warning(f"Failed to send password reset OTP to {payload.email}")
    
    return {"message": "If the email exists, an OTP was sent"}


@router.post("/reset-password")
def reset_password(request, payload: ResetPasswordSchema):
    if payload.new_password != payload.confirm_password:
        raise HttpError(400, "Passwords do not match")

    user = User.objects.filter(email__iexact=payload.email, is_active=True).first()
    if not user or not verify_otp(payload.otp, "reset", user.id):
        raise HttpError(400, "Invalid OTP")

    user.set_password(payload.new_password)
    user.save(update_fields=["password", "email_encrypted"])
    return _issue_tokens(user)
