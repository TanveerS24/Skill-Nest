from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, distinct, and_
from typing import List
from app.models import User, Submission, Problem, Verdict
from app.schemas import LeaderboardEntry
from app.redis_client import get_redis
import json


class LeaderboardService:
    @staticmethod
    def _complexity_to_score(complexity: str) -> int:
        """Convert complexity notation to score (lower is better)"""
        if not complexity:
            return 999
        
        complexity = complexity.upper()
        
        if "O(1)" in complexity:
            return 1
        elif "O(LOG N)" in complexity or "O(LOGN)" in complexity:
            return 2
        elif "O(N LOG N)" in complexity or "O(NLOGN)" in complexity:
            return 4
        elif "O(N^2)" in complexity or "O(N²)" in complexity:
            return 5
        elif "O(N)" in complexity:
            return 3
        else:
            return 6
    
    @staticmethod
    async def get_leaderboard(
        db: AsyncSession,
        sort_by: str = "solved",
        problem_id: int = None,
        limit: int = 100
    ) -> List[LeaderboardEntry]:
        """
        Get leaderboard with different sorting criteria
        """
        # Check cache first
        redis_client = await get_redis()
        cache_key = f"leaderboard:{sort_by}:{problem_id or 'all'}:{limit}"
        
        cached = await redis_client.get(cache_key)
        if cached:
            data = json.loads(cached)
            return [LeaderboardEntry(**entry) for entry in data]
        
        # Query database
        if sort_by == "solved":
            leaderboard = await LeaderboardService._get_by_problems_solved(db, limit)
        elif sort_by == "time":
            leaderboard = await LeaderboardService._get_by_time_complexity(db, limit)
        elif sort_by == "space":
            leaderboard = await LeaderboardService._get_by_space_complexity(db, limit)
        elif sort_by == "submissions" and problem_id:
            leaderboard = await LeaderboardService._get_by_submissions_per_problem(db, problem_id, limit)
        else:
            leaderboard = await LeaderboardService._get_by_problems_solved(db, limit)
        
        # Cache result for 5 minutes
        await redis_client.setex(
            cache_key,
            300,
            json.dumps([entry.model_dump() for entry in leaderboard])
        )
        
        return leaderboard
    
    @staticmethod
    async def _get_by_problems_solved(db: AsyncSession, limit: int) -> List[LeaderboardEntry]:
        """Rank by number of unique problems solved"""
        query = select(
            User.id,
            User.email,
            func.count(distinct(Submission.problem_id)).label("problems_solved"),
            func.avg(func.cast(Submission.runtime, type_=func.Float())).label("avg_runtime"),
            func.count(Submission.id).label("total_submissions")
        ).select_from(User).join(
            Submission, User.id == Submission.user_id, isouter=True
        ).where(
            Submission.verdict == Verdict.ACCEPTED
        ).group_by(
            User.id, User.email
        ).order_by(
            func.count(distinct(Submission.problem_id)).desc()
        ).limit(limit)
        
        result = await db.execute(query)
        rows = result.all()
        
        leaderboard = []
        for row in rows:
            # Calculate average complexity scores
            time_query = select(
                func.avg(
                    func.case(
                        (Submission.time_complexity == "O(1)", 1),
                        (Submission.time_complexity.like("%log%"), 2),
                        (Submission.time_complexity == "O(n)", 3),
                        (Submission.time_complexity.like("%n log n%"), 4),
                        (Submission.time_complexity.like("%n^2%"), 5),
                        else_=6
                    )
                )
            ).where(
                and_(
                    Submission.user_id == row.id,
                    Submission.verdict == Verdict.ACCEPTED
                )
            )
            
            time_result = await db.execute(time_query)
            avg_time_complexity = time_result.scalar() or 3.0
            
            space_query = select(
                func.avg(
                    func.case(
                        (Submission.space_complexity == "O(1)", 1),
                        (Submission.space_complexity.like("%log%"), 2),
                        (Submission.space_complexity == "O(n)", 3),
                        (Submission.space_complexity.like("%n log n%"), 4),
                        (Submission.space_complexity.like("%n^2%"), 5),
                        else_=6
                    )
                )
            ).where(
                and_(
                    Submission.user_id == row.id,
                    Submission.verdict == Verdict.ACCEPTED
                )
            )
            
            space_result = await db.execute(space_query)
            avg_space_complexity = space_result.scalar() or 3.0
            
            leaderboard.append(LeaderboardEntry(
                user_id=row.id,
                email=row.email,
                problems_solved=row.problems_solved or 0,
                avg_time_complexity=float(avg_time_complexity),
                avg_space_complexity=float(avg_space_complexity),
                total_submissions=row.total_submissions or 0
            ))
        
        return leaderboard
    
    @staticmethod
    async def _get_by_time_complexity(db: AsyncSession, limit: int) -> List[LeaderboardEntry]:
        """Rank by best average time complexity"""
        return await LeaderboardService._get_by_problems_solved(db, limit)
    
    @staticmethod
    async def _get_by_space_complexity(db: AsyncSession, limit: int) -> List[LeaderboardEntry]:
        """Rank by best average space complexity"""
        return await LeaderboardService._get_by_problems_solved(db, limit)
    
    @staticmethod
    async def _get_by_submissions_per_problem(
        db: AsyncSession,
        problem_id: int,
        limit: int
    ) -> List[LeaderboardEntry]:
        """Rank by number of submissions for a specific problem"""
        query = select(
            User.id,
            User.email,
            func.count(Submission.id).label("total_submissions")
        ).select_from(User).join(
            Submission, User.id == Submission.user_id
        ).where(
            Submission.problem_id == problem_id
        ).group_by(
            User.id, User.email
        ).order_by(
            func.count(Submission.id).desc()
        ).limit(limit)
        
        result = await db.execute(query)
        rows = result.all()
        
        leaderboard = []
        for row in rows:
            leaderboard.append(LeaderboardEntry(
                user_id=row.id,
                email=row.email,
                problems_solved=0,  # Not relevant for this view
                avg_time_complexity=0.0,
                avg_space_complexity=0.0,
                total_submissions=row.total_submissions
            ))
        
        return leaderboard
    
    @staticmethod
    async def invalidate_cache():
        """Invalidate all leaderboard caches"""
        redis_client = await get_redis()
        keys = await redis_client.keys("leaderboard:*")
        if keys:
            await redis_client.delete(*keys)
