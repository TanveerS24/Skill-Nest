from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.database import get_db
from app.schemas.submission import SubmissionCreate, SubmissionResponse
from app.services.submission_service import SubmissionService
from app.utils.dependencies import get_current_user
from app.models.user import User
from app.config import settings

router = APIRouter(prefix="/submissions", tags=["submissions"])

limiter = Limiter(key_func=get_remote_address)
submission_service = SubmissionService()


@router.post(
    "",
    response_model=SubmissionResponse,
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit(settings.RATE_LIMIT_SUBMISSIONS)
async def submit_code(
    request: Request,
    submission_data: SubmissionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Submit code for a problem"""
    
    # Validate code size
    if len(submission_data.code) > settings.MAX_CODE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Code size exceeds maximum limit of {settings.MAX_CODE_SIZE} bytes",
        )
    
    try:
        submission = await submission_service.create_and_execute_submission(
            db=db,
            user_id=current_user.id,
            submission_data=submission_data,
        )
        
        return SubmissionResponse.model_validate(submission)
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Submission failed: {str(e)}",
        )


@router.get("/my-submissions", response_model=List[SubmissionResponse])
async def get_my_submissions(
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current user's submission history"""
    submissions = await submission_service.get_user_submissions(
        db=db,
        user_id=current_user.id,
        limit=limit,
    )
    
    return [SubmissionResponse.model_validate(s) for s in submissions]


@router.get("/{submission_id}", response_model=SubmissionResponse)
async def get_submission(
    submission_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get a specific submission"""
    from sqlalchemy import select
    from app.models.submission import Submission
    
    result = await db.execute(
        select(Submission).where(Submission.id == submission_id)
    )
    submission = result.scalar_one_or_none()
    
    if not submission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Submission not found",
        )
    
    # Only allow user to see their own submissions (or admin)
    if submission.user_id != current_user.id and current_user.role.value != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied",
        )
    
    return SubmissionResponse.model_validate(submission)
