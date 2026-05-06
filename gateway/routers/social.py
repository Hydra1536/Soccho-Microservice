import os

import httpx
from fastapi import APIRouter, Depends, HTTPException, Query, Request

from gateway.middleware.jwt import get_current_user


router = APIRouter()
SOCIAL_SERVICE_URL = os.getenv("SOCIAL_SERVICE_URL", "http://localhost:8002/api/friendships")


def _gateway_headers(request: Request):
    return {
        "X-User-Id": str(request.state.user_id),
        "X-Username": str(getattr(request.state, "username", "")),
    }


@router.get("/search")
async def search_friends(
    request: Request,
    q: str = Query(..., min_length=2),
    cursor: str | None = None,
    user_id: str = Depends(get_current_user),
):
    params = {"q": q}
    if cursor:
        params["cursor"] = cursor

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{SOCIAL_SERVICE_URL}/search/", params=params, headers=_gateway_headers(request))
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Social service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/friends")
async def list_friends(
    request: Request,
    cursor: str | None = None,
    user_id: str = Depends(get_current_user),
):
    params = {}
    if cursor:
        params["cursor"] = cursor
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{SOCIAL_SERVICE_URL}/accepted/", params=params, headers=_gateway_headers(request))
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Social service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/search-history")
async def search_history(
    request: Request,
    user_id: str = Depends(get_current_user),
):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(f"{SOCIAL_SERVICE_URL}/search-history/", headers=_gateway_headers(request))
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Social service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.post("/friends/{friend_id}/request")
async def send_friend_request(
    friend_id: str,
    request: Request,
    user_id: str = Depends(get_current_user),
):
    payload = {"addressee_id": friend_id}
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{SOCIAL_SERVICE_URL}/", json=payload, headers=_gateway_headers(request))
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Social service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
