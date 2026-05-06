from django.conf import settings
from django.core.cache import cache
from redis import Redis
from redis.exceptions import RedisError

from shared.exceptions import IdempotencyError


TTL_SECONDS = 24 * 60 * 60
REDIS_KEY_PREFIX = "idempotency:"
rdb = Redis.from_url(settings.REDIS_URL) if getattr(settings, "REDIS_URL", None) else None


def check_idempotency(key: str):
    """Enforce one-time use idempotency key (24h TTL)."""
    if not key:
        raise IdempotencyError("Missing idempotency key.")

    redis_key = f"{REDIS_KEY_PREFIX}{key}"

    if rdb:
        try:
            created = rdb.set(redis_key, "1", ex=TTL_SECONDS, nx=True)
            if created:
                return
            raise IdempotencyError(f"Duplicate request: {key}")
        except RedisError:
            # Fall back to Django cache if Redis is temporarily unavailable.
            pass

    if cache.add(redis_key, "1", TTL_SECONDS):
        return
    raise IdempotencyError(f"Duplicate request: {key}")
