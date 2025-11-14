# # src/cache.py
# import json
# import hashlib
# from typing import Any, Dict, Optional
# import redis
# import os

# # === Option 1: In-memory LRU Cache (default) ===
# from functools import lru_cache

# # === Option 2: Redis (uncomment to use) ===
# REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
# redis_client = None
# try:
#     if REDIS_URL:
#         redis_client = redis.from_url(REDIS_URL, decode_responses=True)
#         redis_client.ping()  # Test connection
#         print("Connected to Redis for caching")
# except Exception as e:
#     print(f"Redis not available: {e}")
#     redis_client = None

# def get_cache_key(country: str) -> str:
#     """Generate a consistent cache key."""
#     return f"country_data:{country.lower()}"

# def set_redis_cache(key: str, data: Dict[str, Any], ttl: int = 3600):
#     if redis_client:
#         try:
#             redis_client.setex(key, ttl, json.dumps(data))
#         except Exception as e:  
#             print(f"Redis set failed: {e}")

# def get_redis_cache(key: str) -> Optional[Dict[str, Any]]:
#     if redis_client:
#         try:
#             data = redis_client.get(key)
#             return json.loads(data) if data else None
#         except Exception as e:
#             print(f"Redis get failed: {e}")
#     return None