from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.database import get_db
from app.schemas.admin import (
    TopUserResponse,
    AdminStatsResponse,
    LanguageUsageResponse,
    ProblemAnalyticsResponse,
)
from app.services.admin_service import AdminService
from app.utils.dependencies import require_admin
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/top-users", response_model=List[TopUserResponse])
async def get_top_users(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get top users by score (admin only)"""
    return await AdminService.get_top_users(db, limit)


@router.get("/stats", response_model=AdminStatsResponse)
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get platform statistics (admin only)"""
    return await AdminService.get_stats(db)


@router.get("/language-usage", response_model=List[LanguageUsageResponse])
async def get_language_usage(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get language usage statistics (admin only)"""
    return await AdminService.get_language_usage(db)


@router.get("/problem-analytics", response_model=List[ProblemAnalyticsResponse])
async def get_problem_analytics(
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Get problem analytics (admin only)"""
    return await AdminService.get_problem_analytics(db, limit)
