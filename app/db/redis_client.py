import aioredis
import os

class RedisClient:
    def _init_(self):
        self.redis = None

    async def initialize(self):
        self.redis = aioredis.from_url(
            os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True
        )

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def get(self, key):
        return await self.redis.get(key)

    async def set(self, key, value, expire=None):
        return await self.redis.set(key, value, ex=expire)

redis = RedisClient()