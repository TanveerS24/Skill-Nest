from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from app.database import get_db
from app.schemas import ProblemResponse, ProblemDetail, ProblemCreate
from app.models import Problem, TestCase, User
from app.dependencies import get_optional_user, get_current_admin_user
from app.cache import CacheService

router = APIRouter(prefix="/problems", tags=["Problems"])


@router.get("", response_model=List[ProblemResponse])
async def get_problems(
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    """Get all problems (anonymous access allowed)"""
    result = await db.execute(select(Problem).order_by(Problem.id))
    problems = result.scalars().all()
    return problems


@router.get("/{problem_id}", response_model=ProblemDetail)
async def get_problem(
    problem_id: int,
    db: AsyncSession = Depends(get_db),
    user: Optional[User] = Depends(get_optional_user)
):
    """Get problem details with non-hidden test cases (anonymous access allowed)"""
    # Get problem from cache
    problem_dict = await CacheService.get_problem(db, problem_id)
    
    if not problem_dict:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    # Get non-hidden test cases
    test_cases = await CacheService.get_test_cases(db, problem_id, include_hidden=False)
    
    return {
        **problem_dict,
        "test_cases": test_cases
    }


@router.post("", response_model=ProblemResponse, status_code=status.HTTP_201_CREATED)
async def create_problem(
    problem_data: ProblemCreate,
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Create a new problem (admin only)"""
    # Check if problem with same title exists
    result = await db.execute(select(Problem).where(Problem.title == problem_data.title))
    existing = result.scalar_one_or_none()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Problem with this title already exists"
        )
    
    # Create problem
    problem = Problem(
        title=problem_data.title,
        description=problem_data.description,
        difficulty=problem_data.difficulty,
        time_limit=problem_data.time_limit,
        memory_limit=problem_data.memory_limit
    )
    
    db.add(problem)
    await db.flush()
    
    # Create test cases
    for tc_data in problem_data.test_cases:
        test_case = TestCase(
            problem_id=problem.id,
            input=tc_data.input,
            expected_output=tc_data.expected_output,
            is_hidden=tc_data.is_hidden
        )
        db.add(test_case)
    
    await db.commit()
    await db.refresh(problem)
    
    return problem
