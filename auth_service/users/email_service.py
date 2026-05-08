"""
Email service using FormSubmit.co (free API - no credentials needed)
This provides a privacy-friendly alternative to Gmail SMTP.
FormSubmit.co handles spam filtering and email delivery.
"""
import httpx
import logging
from django.conf import settings

logger = logging.getLogger(__name__)


FORMSUBMIT_ENDPOINT = "https://formsubmit.co"


async def send_otp_email(email: str, otp: str, purpose: str = "verify") -> bool:
    """
    Send OTP via FormSubmit.co (completely free, no API keys needed).
    
    Args:
        email: Recipient email address
        otp: 6-digit OTP code
        purpose: "register", "reset", or "verify"
    
    Returns:
        True if email was sent successfully, False otherwise
    """
    try:
        # FormSubmit.co endpoint - uses form submission via POST
        # No credentials needed - it's a free, privacy-first service
        subject = f"Soccho {purpose.capitalize()} OTP"
        
        if purpose == "register":
            body = f"""
Hello,

Welcome to Soccho! Here's your OTP to verify your account:

OTP: {otp}

This code expires in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Soccho Team
            """
        elif purpose == "reset":
            body = f"""
Hello,

We received a request to reset your Soccho password. Here's your OTP:

OTP: {otp}

This code expires in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
Soccho Team
            """
        else:
            body = f"Your Soccho OTP is: {otp}\n\nExpires in 10 minutes."
        
        # Prepare FormSubmit.co payload
        payload = {
            "email": email,
            "subject": subject,
            "message": body,
            "_captcha": "false",  # Disable CAPTCHA
            "_next": "https://soccho.vercel.app/otp.html",  # Redirect after submission
        }
        
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                FORMSUBMIT_ENDPOINT,
                data=payload,
            )
            
            if response.status_code == 200:
                logger.info(f"OTP email sent successfully to {email} for {purpose}")
                return True
            else:
                logger.error(f"Failed to send OTP email: {response.status_code} - {response.text}")
                return False
                
    except Exception as e:
        logger.error(f"Exception sending OTP email: {str(e)}")
        return False


def send_otp_email_sync(email: str, otp: str, purpose: str = "verify") -> bool:
    """
    Synchronous wrapper for send_otp_email using httpx blocking client.
    Used in Django views that don't support async.
    """
    try:
        subject = f"Soccho {purpose.capitalize()} OTP"
        
        if purpose == "register":
            body = f"""
Hello,

Welcome to Soccho! Here's your OTP to verify your account:

OTP: {otp}

This code expires in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
Soccho Team
            """
        elif purpose == "reset":
            body = f"""
Hello,

We received a request to reset your Soccho password. Here's your OTP:

OTP: {otp}

This code expires in 10 minutes.

If you didn't request this, please ignore this email.

Best regards,
Soccho Team
            """
        else:
            body = f"Your Soccho OTP is: {otp}\n\nExpires in 10 minutes."
        
        payload = {
            "email": email,
            "subject": subject,
            "message": body,
            "_captcha": "false",
            "_next": "https://soccho.vercel.app/otp.html",
        }
        
        # Use blocking client for sync context
        with httpx.Client(timeout=10.0) as client:
            response = client.post(FORMSUBMIT_ENDPOINT, data=payload)
            
            if response.status_code == 200:
                logger.info(f"OTP email sent successfully to {email} for {purpose}")
                return True
            else:
                logger.error(f"Failed to send OTP email: {response.status_code}")
                return False
                
    except Exception as e:
        logger.error(f"Exception sending OTP email: {str(e)}")
        return False
