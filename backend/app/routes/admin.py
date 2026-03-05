from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.database import get_db
from app.schemas import AdminStats, LeaderboardEntry
from app.models import User, Submission, Problem, Verdict
from app.dependencies import get_current_admin_user
from app.leaderboard import LeaderboardService

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.get("/dashboard", response_model=AdminStats)
async def get_admin_dashboard(
    db: AsyncSession = Depends(get_db),
    admin: User = Depends(get_current_admin_user)
):
    """Get admin dashboard statistics (admin only)"""
    
    # Total users
    total_users_result = await db.execute(select(func.count(User.id)))
    total_users = total_users_result.scalar()
    
    # Total submissions
    total_submissions_result = await db.execute(select(func.count(Submission.id)))
    total_submissions = total_submissions_result.scalar()
    
    # Accepted submissions
    accepted_submissions_result = await db.execute(
        select(func.count(Submission.id)).where(Submission.verdict == Verdict.ACCEPTED)
    )
    accepted_submissions = accepted_submissions_result.scalar()
    
    # Most attempted problems
    most_attempted_query = select(
        Problem.id,
        Problem.title,
        func.count(Submission.id).label("attempt_count")
    ).select_from(Problem).join(
        Submission, Problem.id == Submission.problem_id
    ).group_by(
        Problem.id, Problem.title
    ).order_by(
        func.count(Submission.id).desc()
    ).limit(10)
    
    most_attempted_result = await db.execute(most_attempted_query)
    most_attempted_problems = [
        {
            "problem_id": row.id,
            "title": row.title,
            "attempts": row.attempt_count
        }
        for row in most_attempted_result.all()
    ]
    
    # Language usage statistics
    language_usage_query = select(
        Submission.language,
        func.count(Submission.id).label("count")
    ).group_by(
        Submission.language
    )
    
    language_usage_result = await db.execute(language_usage_query)
    language_usage = {
        row.language.value: row.count
        for row in language_usage_result.all()
    }
    
    # Top users
    top_users = await LeaderboardService.get_leaderboard(
        db=db,
        sort_by="solved",
        limit=10
    )
    
    return AdminStats(
        total_users=total_users,
        total_submissions=total_submissions,
        accepted_submissions=accepted_submissions,
        most_attempted_problems=most_attempted_problems,
        language_usage=language_usage,
        top_users=top_users
    )
