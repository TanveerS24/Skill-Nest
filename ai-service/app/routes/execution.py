from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.base import get_db
from app.schemas.schemas import (
    CodeSubmitRequest,
    CodeSubmitResponse,
    CodeRunRequest,
    TestCaseResult
)
from app.execution.code_executor import CodeExecutor
from app.services.question_service import QuestionService
from app.core.logging import logger
from typing import List

router = APIRouter(prefix="/execute", tags=["execution"])


def normalize_language(language: str) -> str:
    """Normalize language name."""
    lang = language.lower().strip()
    if lang in ["c++", "cxx"]:
        return "cpp"
    if lang in ["py", "python3"]:
        return "python"
    return lang


@router.post("/submit", response_model=CodeSubmitResponse)
async def submit_code(
    request: CodeSubmitRequest,
    db: Session = Depends(get_db)
):
    """Submit code for evaluation. Stores result in database."""
    try:
        service = QuestionService(db)

        # Get question and test cases
        question = service.get_question(request.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        test_cases = service.get_test_cases(request.question_id, only_samples=False)
        if not test_cases:
            raise HTTPException(status_code=404, detail="No test cases found for question")

        # Execute code
        language = normalize_language(request.language)
        executor = CodeExecutor()
        execution_result = executor.execute(
            language=language,
            code=request.code,
            test_cases=test_cases
        )

        # Format results
        results: List[TestCaseResult] = []
        for i, res in enumerate(execution_result["results"]):
            results.append(TestCaseResult(
                input=res["input"],
                expected=res["expected"],
                actual=res["actual"],
                passed=res["passed"]
            ))

        # Store submission
        total_time = execution_result.get("total_execution_time_ms", 0)
        submission_id = service.store_submission(
            question_id=request.question_id,
            language=language,
            code=request.code,
            status=execution_result["status"],
            results=execution_result["results"],
            execution_time_ms=total_time
        )

        logger.info(f"Submission {submission_id} stored with status {execution_result['status']}")

        return CodeSubmitResponse(
            status=execution_result["status"],
            results=results,
            execution_time_ms=total_time,
            stderr=execution_result.get("stderr")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Code submission failed: {e}")
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")


@router.post("/run")
async def run_code(
    request: CodeRunRequest,
    db: Session = Depends(get_db)
):
    """Run code without storing submission."""
    try:
        service = QuestionService(db)

        # Get question and sample test cases only
        question = service.get_question(request.question_id)
        if not question:
            raise HTTPException(status_code=404, detail="Question not found")

        # Get only sample test cases for preview
        test_cases = service.get_test_cases(request.question_id, only_samples=True)
        if not test_cases:
            # Fallback to first 2 test cases if no samples marked
            all_cases = service.get_test_cases(request.question_id, only_samples=False)
            test_cases = all_cases[:2] if len(all_cases) >= 2 else all_cases

        # Execute code
        language = normalize_language(request.language)
        executor = CodeExecutor()
        execution_result = executor.execute(
            language=language,
            code=request.code,
            test_cases=test_cases
        )

        # Format results
        results = [
            TestCaseResult(
                input=res["input"],
                expected=res["expected"],
                actual=res["actual"],
                passed=res["passed"]
            )
            for res in execution_result["results"]
        ]

        return CodeSubmitResponse(
            status=execution_result["status"],
            results=results,
            execution_time_ms=execution_result.get("total_execution_time_ms"),
            stderr=execution_result.get("stderr")
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Code execution failed: {e}")
        raise HTTPException(status_code=500, detail=f"Execution failed: {str(e)}")
