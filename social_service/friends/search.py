import json
import time

from django.conf import settings
from django.contrib.auth import get_user_model
from redis import Redis


User = get_user_model()
rdb = Redis.from_url(settings.REDIS_URL) if getattr(settings, "REDIS_URL", None) else None


def fuzzy_search_users(query: str, limit: int = 10):
    """
    Fallback fuzzy-like search. If pg_trgm is available, this can be swapped to
    TrigramSimilarity/GIN-backed query without changing call sites.
    """
    if not query:
        return []
    return list(
        User.objects.filter(is_active=True, username__icontains=query)
        .order_by("username")
        .values("id", "username")[:limit]
    )


def save_search_history(user_id: str, query: str):
    if not rdb:
        return
    payload = json.dumps({"query": query, "ts": time.time()})
    pipe = rdb.pipeline()
    pipe.lpush(f"search_history:{user_id}", payload)
    pipe.ltrim(f"search_history:{user_id}", 0, 49)
    pipe.expire(f"search_history:{user_id}", 86400)
    pipe.execute()


def get_search_history(user_id: str, limit: int = 10):
    if not rdb:
        return []
    history = rdb.lrange(f"search_history:{user_id}", 0, limit - 1)
    return [json.loads(h.decode() if isinstance(h, bytes) else h) for h in history]
