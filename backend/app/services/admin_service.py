from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, cast, Date
from app.models.user import User
from app.models.submission import Submission
from app.models.problem import Problem
from app.schemas.admin import (
    TopUserResponse,
    AdminStatsResponse,
    LanguageUsageResponse,
    ProblemAnalyticsResponse,
)
from typing import List
from datetime import datetime, date


class AdminService:
    @staticmethod
    async def get_top_users(db: AsyncSession, limit: int = 20) -> List[TopUserResponse]:
        """Get top users by score"""
        result = await db.execute(
            select(User.id, User.email, User.score)
            .order_by(User.score.desc())
            .limit(limit)
        )
        users = result.all()
        return [
            TopUserResponse(id=user.id, email=user.email, score=user.score)
            for user in users
        ]
    
    @staticmethod
    async def get_stats(db: AsyncSession) -> AdminStatsResponse:
        """Get platform statistics"""
        # Total users
        total_users_result = await db.execute(select(func.count(User.id)))
        total_users = total_users_result.scalar()
        
        # Total submissions
        total_submissions_result = await db.execute(select(func.count(Submission.id)))
        total_submissions = total_submissions_result.scalar()
        
        # Accepted submissions
        accepted_result = await db.execute(
            select(func.count(Submission.id)).where(Submission.verdict == "Accepted")
        )
        accepted_submissions = accepted_result.scalar()
        
        # Acceptance rate
        acceptance_rate = (
            (accepted_submissions / total_submissions * 100)
            if total_submissions > 0
            else 0.0
        )
        
        # Submissions today
        today = date.today()
        today_result = await db.execute(
            select(func.count(Submission.id)).where(
                cast(Submission.created_at, Date) == today
            )
        )
        submissions_today = today_result.scalar()
        
        return AdminStatsResponse(
            total_users=total_users,
            total_submissions=total_submissions,
            accepted_submissions=accepted_submissions,
            acceptance_rate=round(acceptance_rate, 2),
            submissions_today=submissions_today,
        )
    
    @staticmethod
    async def get_language_usage(db: AsyncSession) -> List[LanguageUsageResponse]:
        """Get language usage statistics"""
        result = await db.execute(
            select(
                Submission.detected_language,
                func.count(Submission.id).label("count")
            )
            .where(Submission.detected_language.isnot(None))
            .group_by(Submission.detected_language)
            .order_by(func.count(Submission.id).desc())
        )
        
        usage = result.all()
        return [
            LanguageUsageResponse(language=lang, count=count)
            for lang, count in usage
        ]
    
    @staticmethod
    async def get_problem_analytics(
        db: AsyncSession, limit: int = 20
    ) -> List[ProblemAnalyticsResponse]:
        """Get problem analytics (most attempted problems)"""
        result = await db.execute(
            select(
                Problem.id,
                Problem.title,
                func.count(Submission.id).label("submission_count")
            )
            .join(Submission, Submission.problem_id == Problem.id)
            .group_by(Problem.id, Problem.title)
            .order_by(func.count(Submission.id).desc())
            .limit(limit)
        )
        
        analytics = result.all()
        return [
            ProblemAnalyticsResponse(
                problem_id=problem_id,
                problem_title=title,
                submission_count=count,
            )
            for problem_id, title, count in analytics
        ]
