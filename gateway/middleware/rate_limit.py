import time
from collections import defaultdict

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Simple in-memory 100 requests/hour limiter per client IP."""

    _hits = defaultdict(list)
    _limit = 100
    _window_seconds = 60 * 60

    async def dispatch(self, request: Request, call_next):
        if request.url.path.startswith("/health"):
            return await call_next(request)

        ip = request.client.host if request.client else "unknown"
        now = time.time()

        entries = [ts for ts in self._hits[ip] if now - ts < self._window_seconds]
        if len(entries) >= self._limit:
            return JSONResponse(status_code=429, content={"detail": "Rate limit exceeded"})

        entries.append(now)
        self._hits[ip] = entries
        return await call_next(request)
