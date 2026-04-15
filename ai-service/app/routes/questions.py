from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.db.base import get_db
from app.schemas.schemas import (
    QuestionGenerateRequest,
    QuestionGenerateResponse,
    QuestionDB
)
from app.services.question_service import QuestionService
from app.core.logging import logger

router = APIRouter(prefix="/questions", tags=["questions"])


@router.post("/generate", response_model=QuestionGenerateResponse)
async def generate_question(
    request: QuestionGenerateRequest,
    db: Session = Depends(get_db)
):
    """Generate a new DSA question using RAG."""
    try:
        service = QuestionService(db)
        question = await service.generate_question(
            topic=request.topic,
            difficulty=request.difficulty
        )
        return QuestionGenerateResponse(**question)
    except Exception as e:
        logger.error(f"Failed to generate question: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{question_id}")
async def get_question(
    question_id: str,
    db: Session = Depends(get_db)
):
    """Get a question by ID."""
    service = QuestionService(db)
    question = service.get_question(question_id)

    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    return question


@router.get("")
async def list_questions(
    topic: Optional[str] = None,
    difficulty: Optional[str] = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    """List questions with optional filters."""
    service = QuestionService(db)
    questions = service.list_questions(
        topic=topic,
        difficulty=difficulty,
        limit=limit,
        offset=offset
    )
    return {"questions": questions, "total": len(questions)}
