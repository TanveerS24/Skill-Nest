from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.redis_client import get_redis
import time


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Only rate limit submission endpoints
        if "/submissions" in request.url.path and request.method == "POST":
            redis_client = await get_redis()
            
            # Get user from request (if authenticated)
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                user_key = f"rate_limit:submission:{auth_header}"
            else:
                # Rate limit by IP for anonymous users
                user_key = f"rate_limit:submission:{request.client.host}"
            
            # Check rate limit
            current = await redis_client.get(user_key)
            if current and int(current) >= 30:  # 30 submissions per minute
                return JSONResponse(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    content={"detail": "Rate limit exceeded. Maximum 30 submissions per minute."}
                )
            
            # Increment counter
            pipe = redis_client.pipeline()
            pipe.incr(user_key)
            pipe.expire(user_key, 60)  # Reset after 1 minute
            await pipe.execute()
        
        response = await call_next(request)
        return response
