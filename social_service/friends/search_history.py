import json
import time

from django.conf import settings
from redis import Redis


rdb = Redis.from_url(settings.REDIS_URL) if getattr(settings, "REDIS_URL", None) else None


class SearchHistory:
    TTL = 86400  # 24h
    MAX_ENTRIES = 50

    @classmethod
    def add(cls, user_id: str, query: str):
        if not rdb:
            return
        data = json.dumps({"query": query, "ts": time.time()})
        pipe = rdb.pipeline()
        pipe.lpush(f"search_history:{user_id}", data)
        pipe.ltrim(f"search_history:{user_id}", 0, cls.MAX_ENTRIES - 1)
        pipe.expire(f"search_history:{user_id}", cls.TTL)
        pipe.execute()

    @classmethod
    def get(cls, user_id: str, limit: int = 10):
        if not rdb:
            return []
        keys = rdb.lrange(f"search_history:{user_id}", 0, limit - 1)
        return [json.loads(k.decode() if isinstance(k, bytes) else k) for k in keys]
