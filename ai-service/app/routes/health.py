from fastapi import APIRouter
from app.schemas.schemas import HealthCheck
from app.utils.cache import redis_cache
from app.core.logging import logger

router = APIRouter(prefix="/health", tags=["health"])


@router.get("", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    redis_status = "connected" if redis_cache.is_connected() else "disconnected"

    return HealthCheck(
        status="healthy",
        version="1.0.0",
        redis=redis_status
    )
