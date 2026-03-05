from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional
from app.models import Problem, TestCase
from app.redis_client import get_redis
import json


class CacheService:
    @staticmethod
    async def get_problem(db: AsyncSession, problem_id: int) -> Optional[dict]:
        """Get problem with caching"""
        redis_client = await get_redis()
        cache_key = f"problem:{problem_id}"
        
        # Check cache
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Query database
        result = await db.execute(
            select(Problem).where(Problem.id == problem_id)
        )
        problem = result.scalar_one_or_none()
        
        if not problem:
            return None
        
        problem_dict = {
            "id": problem.id,
            "title": problem.title,
            "description": problem.description,
            "difficulty": problem.difficulty.value,
            "time_limit": problem.time_limit,
            "memory_limit": problem.memory_limit,
        }
        
        # Cache for 1 hour
        await redis_client.setex(cache_key, 3600, json.dumps(problem_dict))
        
        return problem_dict
    
    @staticmethod
    async def get_test_cases(db: AsyncSession, problem_id: int, include_hidden: bool = False):
        """Get test cases with caching"""
        redis_client = await get_redis()
        cache_key = f"test_cases:{problem_id}:{include_hidden}"
        
        # Check cache
        cached = await redis_client.get(cache_key)
        if cached:
            return json.loads(cached)
        
        # Query database
        query = select(TestCase).where(TestCase.problem_id == problem_id)
        if not include_hidden:
            query = query.where(TestCase.is_hidden == False)
        
        result = await db.execute(query)
        test_cases = result.scalars().all()
        
        test_cases_list = [
            {
                "id": tc.id,
                "input": tc.input,
                "expected_output": tc.expected_output,
                "is_hidden": tc.is_hidden
            }
            for tc in test_cases
        ]
        
        # Cache for 1 hour
        await redis_client.setex(cache_key, 3600, json.dumps(test_cases_list))
        
        return test_cases_list
    
    @staticmethod
    async def invalidate_problem(problem_id: int):
        """Invalidate problem cache"""
        redis_client = await get_redis()
        await redis_client.delete(f"problem:{problem_id}")
        await redis_client.delete(f"test_cases:{problem_id}:True")
        await redis_client.delete(f"test_cases:{problem_id}:False")
