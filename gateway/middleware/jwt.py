import os

from fastapi import HTTPException, Request
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


SECRET_KEY = os.getenv("JWT_SECRET") or os.getenv("GATEWAY_SECRET_KEY") or "dev-secret-key"
ALGORITHM = "HS256"
PUBLIC_PATH_PREFIXES = ("/auth/", "/health", "/docs", "/openapi.json", "/redoc")


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith(PUBLIC_PATH_PREFIXES):
            return await call_next(request)

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing bearer token"})

        token = auth_header.split(" ", 1)[1].strip()
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        request.state.user_id = payload.get("user_id")
        request.state.username = payload.get("username")
        return await call_next(request)


async def get_current_user(request: Request):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return str(user_id)
