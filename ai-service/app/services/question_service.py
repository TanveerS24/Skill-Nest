from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.db.models import Question, TestCase, Submission, SubmissionResult
from app.rag.vector_store import vector_store
from app.rag.ollama_client import ollama_client
from app.utils.cache import redis_cache
from app.core.logging import logger
import json


class QuestionService:
    def __init__(self, db: Session):
        self.db = db

    async def generate_question(
        self,
        topic: str,
        difficulty: str
    ) -> Dict[str, Any]:
        """Generate a new DSA question using RAG."""

        # Check cache first
        cache_key = redis_cache.get_generation_cache_key(topic, difficulty)
        cached = redis_cache.get(cache_key)
        if cached:
            logger.info(f"Returning cached question for {topic}/{difficulty}")
            return cached

        # Retrieve similar questions for context
        similar_questions = await vector_store.retrieve_similar_questions(
            topic=topic,
            difficulty=difficulty,
            n_results=3
        )

        # Generate new question using LLM
        question_data = await ollama_client.generate_dsa_question(
            topic=topic,
            difficulty=difficulty,
            similar_questions=similar_questions
        )

        # Store in database
        question = Question(
            title=question_data["title"],
            description=question_data["description"],
            constraints=question_data.get("constraints", ""),
            topic=topic,
            difficulty=difficulty
        )
        self.db.add(question)
        self.db.flush()

        # Store test cases
        for i, tc in enumerate(question_data["test_cases"][:10]):
            test_case = TestCase(
                question_id=question.id,
                input_data=tc.get("input", ""),
                expected_output=tc.get("output", ""),
                is_sample=(i < 2),
                order_index=i
            )
            self.db.add(test_case)

        self.db.commit()

        # Add to vector store
        await vector_store.add_question(
            question_id=question.id,
            title=question_data["title"],
            description=question_data["description"],
            topic=topic,
            difficulty=difficulty
        )

        # Prepare response
        starter_code = question_data.get("starter_code", {})
        response = {
            "question_id": question.id,
            "title": question_data["title"],
            "description": question_data["description"],
            "constraints": question_data.get("constraints", ""),
            "examples": question_data.get("examples", []),
            "test_cases": [
                {"input": tc.get("input", ""), "output": tc.get("output", "")}
                for tc in question_data["test_cases"][:10]
            ],
            "starter_code": {
                "java": starter_code.get("java", ""),
                "python": starter_code.get("python", ""),
                "cpp": starter_code.get("cpp", "")
            }
        }

        # Cache the result
        redis_cache.set(cache_key, response, expire=3600)
        redis_cache.set(
            redis_cache.get_question_cache_key(question.id),
            response,
            expire=7200
        )

        return response

    def get_question(self, question_id: str) -> Optional[Dict[str, Any]]:
        """Get question by ID."""

        # Check cache first
        cache_key = redis_cache.get_question_cache_key(question_id)
        cached = redis_cache.get(cache_key)
        if cached:
            return cached

        question = self.db.query(Question).filter(Question.id == question_id).first()
        if not question:
            return None

        test_cases = self.db.query(TestCase).filter(
            TestCase.question_id == question_id
        ).order_by(TestCase.order_index).all()

        response = {
            "question_id": question.id,
            "title": question.title,
            "description": question.description,
            "constraints": question.constraints,
            "topic": question.topic,
            "difficulty": question.difficulty,
            "examples": [],
            "test_cases": [
                {"input": tc.input_data, "output": tc.expected_output}
                for tc in test_cases if tc.is_sample
            ],
            "test_cases_full": [
                {"input": tc.input_data, "output": tc.expected_output}
                for tc in test_cases
            ],
            "starter_code": {"java": "", "python": "", "cpp": ""}
        }

        redis_cache.set(cache_key, response, expire=7200)
        return response

    def get_test_cases(self, question_id: str, only_samples: bool = False) -> List[Dict[str, str]]:
        """Get test cases for a question."""
        query = self.db.query(TestCase).filter(TestCase.question_id == question_id)
        if only_samples:
            query = query.filter(TestCase.is_sample == True)

        test_cases = query.order_by(TestCase.order_index).all()
        return [
            {"input": tc.input_data, "expected_output": tc.expected_output}
            for tc in test_cases
        ]

    def store_submission(
        self,
        question_id: str,
        language: str,
        code: str,
        status: str,
        results: List[Dict[str, Any]],
        execution_time_ms: Optional[float] = None
    ) -> str:
        """Store submission in database."""
        submission = Submission(
            question_id=question_id,
            language=language,
            code=code,
            status=status,
            execution_time_ms=execution_time_ms
        )
        self.db.add(submission)
        self.db.flush()

        # Store results
        for result in results:
            sr = SubmissionResult(
                submission_id=submission.id,
                test_case_id=result.get("test_case_id", ""),
                actual_output=result.get("actual"),
                passed=result.get("passed", False),
                execution_time_ms=result.get("execution_time_ms")
            )
            self.db.add(sr)

        self.db.commit()
        return submission.id

    def list_questions(
        self,
        topic: Optional[str] = None,
        difficulty: Optional[str] = None,
        limit: int = 10,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """List questions with optional filters."""
        query = self.db.query(Question)

        if topic:
            query = query.filter(Question.topic == topic)
        if difficulty:
            query = query.filter(Question.difficulty == difficulty)

        questions = query.order_by(desc(Question.created_at)).offset(offset).limit(limit).all()

        return [
            {
                "question_id": q.id,
                "title": q.title,
                "topic": q.topic,
                "difficulty": q.difficulty,
                "created_at": q.created_at.isoformat()
            }
            for q in questions
        ]
