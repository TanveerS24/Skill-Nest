from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from app.database import get_db
from app.models.problem import Problem
from app.models.user import User
from app.schemas.problem import ProblemResponse, ProblemCreate
from app.schemas.user import LeaderboardUser
from app.utils.dependencies import require_admin

router = APIRouter(prefix="/problems", tags=["problems"])


@router.get("", response_model=List[ProblemResponse])
async def get_problems(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
):
    """Get all problems"""
    result = await db.execute(
        select(Problem).offset(skip).limit(limit)
    )
    problems = result.scalars().all()
    return [ProblemResponse.model_validate(p) for p in problems]


@router.get("/{problem_id}", response_model=ProblemResponse)
async def get_problem(
    problem_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific problem"""
    result = await db.execute(
        select(Problem).where(Problem.id == problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found",
        )
    
    return ProblemResponse.model_validate(problem)


@router.post("", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
async def create_problem(
    problem_data: ProblemCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Create a new problem (admin only)"""
    problem = Problem(**problem_data.model_dump())
    db.add(problem)
    await db.commit()
    await db.refresh(problem)
    return ProblemResponse.model_validate(problem)


@router.get("/leaderboard", response_model=List[LeaderboardUser])
async def get_leaderboard(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
):
    """Get leaderboard (top users by score)"""
    result = await db.execute(
        select(User.id, User.email, User.score)
        .order_by(User.score.desc())
        .limit(limit)
    )
    users = result.all()
    return [
        LeaderboardUser(id=user.id, email=user.email, score=user.score)
        for user in users
    ]
