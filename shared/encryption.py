import base64
import os
from typing import Any

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


def _resolve_secret(aes_secret: str | None = None) -> str:
    secret = aes_secret or os.getenv("AES_SECRET_KEY")
    if not secret:
        raise ValueError("AES secret key is missing. Set AES_SECRET_KEY.")
    return secret


def derive_key(aes_secret: str | None = None) -> bytes:
    """Derive Fernet-compatible key from configured AES secret."""
    password = _resolve_secret(aes_secret).encode()
    salt = b"soccho_salt_2024"
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )
    return base64.urlsafe_b64encode(kdf.derive(password))


def encrypt_field(value: Any, aes_secret: str | None = None) -> str:
    """Encrypt scalar value and return ciphertext string."""
    if value is None:
        raise ValueError("Cannot encrypt None value.")
    f = Fernet(derive_key(aes_secret))
    return f.encrypt(str(value).encode()).decode()


def decrypt_field(encrypted: str, aes_secret: str | None = None) -> str:
    """Decrypt ciphertext string into plaintext string."""
    f = Fernet(derive_key(aes_secret))
    return f.decrypt(encrypted.encode()).decode()
