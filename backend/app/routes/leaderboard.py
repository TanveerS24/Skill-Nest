from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.database import get_db
from app.schemas import LeaderboardEntry
from app.leaderboard import LeaderboardService
from app.dependencies import get_optional_user
from app.models import User

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])


@router.get("", response_model=List[LeaderboardEntry])
async def get_leaderboard(
    sort_by: str = Query("solved", regex="^(solved|time|space|submissions)$"),
    problem_id: Optional[int] = None,
    limit: int = Query(100, ge=1, le=1000),
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    """
    Get leaderboard with various sorting options (anonymous access allowed)
    
    - **sort_by**: 'solved', 'time', 'space', or 'submissions'
    - **problem_id**: Required when sort_by='submissions'
    - **limit**: Maximum number of entries to return
    """
    if sort_by == "submissions" and not problem_id:
        return []
    
    leaderboard = await LeaderboardService.get_leaderboard(
        db=db,
        sort_by=sort_by,
        problem_id=problem_id,
        limit=limit
    )
    
    return leaderboard
