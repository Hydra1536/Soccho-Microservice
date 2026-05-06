import os

import httpx
from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel

from gateway.middleware.jwt import get_current_user


router = APIRouter()
TRANSACTION_SERVICE_URL = os.getenv("TRANSACTION_SERVICE_URL", "http://localhost:8003/api/transactions")


class TransactionCreate(BaseModel):
    friend_id: str
    amount: float
    due_date: str | None = None
    idempotency_key: str


def _gateway_headers(request: Request):
    return {
        "X-User-Id": str(request.state.user_id),
        "X-Username": str(getattr(request.state, "username", "")),
    }


@router.post("/create")
async def create_transaction(
    tx: TransactionCreate,
    request: Request,
    user_id: str = Depends(get_current_user),
):
    payload = {
        "friend_id": tx.friend_id,
        "amount": tx.amount,
        "due_date": tx.due_date,
        "idempotency_key": tx.idempotency_key,
    }
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.post(f"{TRANSACTION_SERVICE_URL}/", json=payload, headers=_gateway_headers(request))
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Transaction service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/balance/{friend_id}")
async def get_balance(
    friend_id: str,
    request: Request,
    user_id: str = Depends(get_current_user),
):
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{TRANSACTION_SERVICE_URL}/balance/{friend_id}/",
                headers=_gateway_headers(request),
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Transaction service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()


@router.get("/list/{friend_id}")
async def list_transactions(
    friend_id: str,
    request: Request,
    cursor: str | None = None,
    user_id: str = Depends(get_current_user),
):
    params = {}
    if cursor:
        params["cursor"] = cursor
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            resp = await client.get(
                f"{TRANSACTION_SERVICE_URL}/list/{friend_id}/",
                params=params,
                headers=_gateway_headers(request),
            )
    except httpx.HTTPError as exc:
        raise HTTPException(status_code=503, detail=f"Transaction service unavailable: {exc}") from exc

    if resp.status_code >= 400:
        raise HTTPException(status_code=resp.status_code, detail=resp.text)
    return resp.json()
