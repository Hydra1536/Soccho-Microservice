import os

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request

from gateway.middleware.jwt import get_current_user


router = APIRouter()
NOTIFICATION_SERVICE_URL = os.getenv("NOTIFICATION_SERVICE_URL", "http://localhost:8004/api/notifications")


def _gateway_headers(request: Request):
    return {
        "X-User-Id": str(request.state.user_id),
        "X-Username": str(getattr(request.state, "username", "")),
    }


@router.get("/unread-count")
async def unread_count(
    request: Request,
    user_id: str = Depends(get_current_user),
):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{NOTIFICATION_SERVICE_URL}/unread-count/",
                headers=_gateway_headers(request),
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Notification service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/")
async def list_notifications(
    request: Request,
    user_id: str = Depends(get_current_user),
):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{NOTIFICATION_SERVICE_URL}/", headers=_gateway_headers(request))
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Notification service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
