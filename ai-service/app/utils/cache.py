import json
import redis
from typing import Optional, Any, Dict
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


class RedisCache:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return

        try:
            self.client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB,
                decode_responses=True,
                socket_connect_timeout=5
            )
            self._initialized = True
            logger.info("Redis cache initialized")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            self.client = None
            self._initialized = True

    def is_connected(self) -> bool:
        if not self.client:
            return False
        try:
            return self.client.ping()
        except:
            return False

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if not self.is_connected():
            return None
        try:
            value = self.client.get(key)
            if value:
                return json.loads(value)
        except Exception as e:
            logger.error(f"Redis get error: {e}")
        return None

    def set(
        self,
        key: str,
        value: Any,
        expire: int = 3600
    ) -> bool:
        """Set value in cache with expiration (seconds)."""
        if not self.is_connected():
            return False
        try:
            self.client.setex(
                key,
                expire,
                json.dumps(value, default=str)
            )
            return True
        except Exception as e:
            logger.error(f"Redis set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        if not self.is_connected():
            return False
        try:
            return bool(self.client.delete(key))
        except Exception as e:
            logger.error(f"Redis delete error: {e}")
            return False

    def get_question_cache_key(self, question_id: str) -> str:
        return f"question:{question_id}"

    def get_generation_cache_key(self, topic: str, difficulty: str) -> str:
        return f"generation:{topic}:{difficulty}"


redis_cache = RedisCache()
