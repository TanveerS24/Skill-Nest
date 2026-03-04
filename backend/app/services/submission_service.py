from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.submission import Submission
from app.models.user import User
from app.models.problem import Problem, Difficulty
from app.schemas.submission import SubmissionCreate
from app.services.execution_service import ExecutionService
from app.services.rag_service import RAGService


class SubmissionService:
    def __init__(self):
        self.execution_service = ExecutionService()
        self.rag_service = RAGService()
    
    async def create_and_execute_submission(
        self,
        db: AsyncSession,
        user_id: int,
        submission_data: SubmissionCreate,
    ) -> Submission:
        """Create and execute a code submission"""
        
        # Detect language using RAG
        detection = await self.rag_service.detect_language(submission_data.code)
        detected_language = detection["language"]
        
        # Execute code
        execution_result = await self.execution_service.execute_code(
            code=submission_data.code,
            language=detected_language,
        )
        
        # Create submission record
        submission = Submission(
            user_id=user_id,
            problem_id=submission_data.problem_id,
            code=submission_data.code,
            detected_language=detected_language,
            verdict=execution_result.verdict,
            runtime=execution_result.runtime,
            memory=execution_result.memory,
        )
        
        db.add(submission)
        
        # Update user score if accepted
        if execution_result.verdict == "Accepted":
            await self._update_user_score(db, user_id, submission_data.problem_id)
        
        await db.commit()
        await db.refresh(submission)
        
        return submission
    
    async def _update_user_score(
        self, db: AsyncSession, user_id: int, problem_id: int
    ):
        """Update user score based on problem difficulty"""
        # Check if user already solved this problem
        result = await db.execute(
            select(Submission)
            .where(
                Submission.user_id == user_id,
                Submission.problem_id == problem_id,
                Submission.verdict == "Accepted",
            )
            .limit(1)
        )
        
        # If this is the first accepted submission for this problem
        previous_accepted = result.scalar_one_or_none()
        if previous_accepted and previous_accepted.id != previous_accepted.id:
            return  # Already solved, don't add points again
        
        # Get problem difficulty
        problem_result = await db.execute(
            select(Problem).where(Problem.id == problem_id)
        )
        problem = problem_result.scalar_one_or_none()
        
        if not problem:
            return
        
        # Calculate score based on difficulty
        score_map = {
            Difficulty.Easy: 10,
            Difficulty.Medium: 20,
            Difficulty.Hard: 40,
        }
        
        points = score_map.get(problem.difficulty, 0)
        
        # Update user score
        user_result = await db.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        
        if user:
            user.score += points
            await db.commit()
    
    async def get_user_submissions(
        self, db: AsyncSession, user_id: int, limit: int = 50
    ):
        """Get user's submission history"""
        result = await db.execute(
            select(Submission)
            .where(Submission.user_id == user_id)
            .order_by(Submission.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()
