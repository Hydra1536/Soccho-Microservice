from ninja import Schema
from pydantic import validator
from typing import Optional
import re

class LoginIn(Schema):
    email: str
    password: str
    
    @validator('email')
    def validate_email(cls, v):
        if not re.match(r'^[^@]+@[^@]+\.[^@]+$', v):
            raise ValueError('Invalid email')
        return v

class RegisterIn(Schema):
    username: str
    email: str
    password: str
    confirm_password: str
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3 or len(v) > 20:
            raise ValueError('Username 3-20 chars')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password min 8 chars')
        return v

class OTPIn(Schema):
    email: str
    otp: str
    
    @validator('otp')
    def validate_otp(cls, v):
        if not re.match(r'^\d{6}$', v):
            raise ValueError('OTP must be 6 digits')
        return v

class TokenOut(Schema):
    access_token: str
    refresh_token: Optional[str] = None

