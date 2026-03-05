from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from typing import List
from app.database import get_db
from app.schemas import SubmissionCreate, SubmissionResponse
from app.models import Submission, Problem, TestCase, User, Verdict
from app.dependencies import get_current_user, get_optional_user
from app.ai_analyzer import analyzer
from app.execution import executor
from app.leaderboard import LeaderboardService
from app.cache import CacheService

router = APIRouter(prefix="/submissions", tags=["Submissions"])


@router.post("", response_model=SubmissionResponse, status_code=status.HTTP_201_CREATED)
async def submit_code(
    submission_data: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Submit code for a problem (authenticated users only)"""
    # Get problem
    result = await db.execute(
        select(Problem).where(Problem.id == submission_data.problem_id)
    )
    problem = result.scalar_one_or_none()
    
    if not problem:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problem not found"
        )
    
    # AI Analysis
    ai_result = await analyzer.analyze_code(
        submission_data.code,
        submission_data.language
    )
    
    if not ai_result.is_safe:
        # Create submission with unsafe verdict
        submission = Submission(
            user_id=current_user.id,
            problem_id=problem.id,
            language=submission_data.language,
            code=submission_data.code,
            verdict=Verdict.UNSAFE_CODE,
            time_complexity=None,
            space_complexity=None
        )
        db.add(submission)
        await db.commit()
        await db.refresh(submission)
        
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsafe code detected: {', '.join(ai_result.issues)}"
        )
    
    # Get all test cases (including hidden)
    test_cases_data = await CacheService.get_test_cases(db, problem.id, include_hidden=True)
    
    # Execute code against all test cases
    all_passed = True
    total_runtime = 0.0
    max_memory = 0.0
    final_verdict = Verdict.ACCEPTED
    
    for tc_data in test_cases_data:
        exec_result = await executor.execute_code(
            code=submission_data.code,
            language=submission_data.language,
            test_input=tc_data["input"],
            time_limit=problem.time_limit,
            memory_limit=problem.memory_limit
        )
        
        # Check verdict
        if exec_result.verdict != Verdict.ACCEPTED:
            all_passed = False
            final_verdict = exec_result.verdict
            break
        
        # Check output
        if exec_result.output != tc_data["expected_output"].strip():
            all_passed = False
            final_verdict = Verdict.WRONG_ANSWER
            break
        
        # Track metrics
        if exec_result.runtime:
            total_runtime += exec_result.runtime
        if exec_result.memory:
            max_memory = max(max_memory, exec_result.memory)
    
    # Calculate average runtime
    avg_runtime = total_runtime / len(test_cases_data) if test_cases_data else 0
    
    # Create submission
    submission = Submission(
        user_id=current_user.id,
        problem_id=problem.id,
        language=submission_data.language,
        code=submission_data.code,
        verdict=final_verdict,
        runtime=avg_runtime if all_passed else None,
        memory=max_memory if all_passed else None,
        time_complexity=ai_result.time_complexity if all_passed else None,
        space_complexity=ai_result.space_complexity if all_passed else None
    )
    
    db.add(submission)
    await db.commit()
    await db.refresh(submission)
    
    # Invalidate leaderboard cache
    await LeaderboardService.invalidate_cache()
    
    return submission


@router.get("", response_model=List[SubmissionResponse])
async def get_submissions(
    problem_id: int = None,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_optional_user)
):
    """Get submissions (anonymous can view all, authenticated can view own)"""
    if user:
        # Get user's own submissions
        query = select(Submission).where(Submission.user_id == user.id)
        if problem_id:
            query = query.where(Submission.problem_id == problem_id)
        query = query.order_by(Submission.created_at.desc()).limit(100)
    else:
        # Anonymous: get all submissions (without code)
        query = select(Submission)
        if problem_id:
            query = query.where(Submission.problem_id == problem_id)
        query = query.order_by(Submission.created_at.desc()).limit(100)
    
    result = await db.execute(query)
    submissions = result.scalars().all()
    
    return submissions


@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: int,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_optional_user)
):
    """Get specific submission"""
    result = await db.execute(
        select(Submission).where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found"
        )
    
    # Only owner can view their submission details
    if user and submission.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied"
        )
    
    return submission
