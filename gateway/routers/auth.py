import os

import httpx
from fastapi import APIRouter, HTTPException, Request


router = APIRouter()
AUTH_SERVICE_URL = os.getenv("AUTH_SERVICE_URL", "http://localhost:8001/api")


async def _get_request_payload(request: Request) -> dict:
    content_type = (request.headers.get("content-type") or "").lower()

    if "application/json" in content_type:
        return await request.json()

    form = await request.form()
    # Convert starlette FormData -> plain dict
    return dict(form)


async def _forward_post(path: str, payload: dict):
    url = f"{AUTH_SERVICE_URL.rstrip('/')}/{path.lstrip('/')}"
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(url, json=payload)
    except httpx.HTTPError as exc:
        raise HTTPException(
            status_code=503,
            detail=f"Auth service unavailable (AUTH_SERVICE_URL={AUTH_SERVICE_URL}): {exc}",
        ) from exc

    if resp.status_code >= 400:
        try:
            detail = resp.json()
        except Exception:
            detail = resp.text or "Auth request failed"
        raise HTTPException(status_code=resp.status_code, detail=detail)
    return resp.json()


@router.post("/login")
async def login(request: Request):
    body = await _get_request_payload(request)
    payload = {
        "email": body.get("email"),
        "password": body.get("password"),
    }
    return await _forward_post("login", payload)


@router.post("/register")
async def register(request: Request):
    body = await _get_request_payload(request)
    payload = {
        "username": body.get("username"),
        "email": body.get("email"),
        "password": body.get("password"),
        "confirm_password": body.get("confirm_password") or body.get("confirmPassword"),
    }
    return await _forward_post("register", payload)


@router.post("/otp-verify")
async def otp_verify(request: Request):
    body = await _get_request_payload(request)
    payload = {
        "email": body.get("email"),
        "otp": body.get("otp"),
    }
    return await _forward_post("otp-verify", payload)


@router.post("/forgot-password")
async def forgot_password(request: Request):
    body = await _get_request_payload(request)
    payload = {"email": body.get("email")}
    return await _forward_post("forgot-password", payload)


@router.post("/reset-password")
async def reset_password(request: Request):
    body = await _get_request_payload(request)
    payload = {
        "email": body.get("email"),
        "otp": body.get("otp"),
        "new_password": body.get("new_password") or body.get("newPassword"),
        "confirm_password": body.get("confirm_password") or body.get("confirmPassword"),
    }
    return await _forward_post("reset-password", payload)


@router.get("/google/login")
async def google_login():
    # Placeholder endpoint until OAuth callback service flow is wired.
    return {"detail": "Google OAuth flow is not configured in gateway yet."}



@router.get("/google/callback")
async def google_callback(code: str):
    return {"detail": "Google OAuth callback handling is not configured yet.", "code": code}
