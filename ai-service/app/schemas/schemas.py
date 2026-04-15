from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from datetime import datetime


class TestCaseBase(BaseModel):
    input_data: str = Field(..., alias="input")
    expected_output: str = Field(..., alias="expected")


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseResponse(TestCaseBase):
    id: str
    is_sample: bool
    order_index: int

    class Config:
        from_attributes = True


class StarterCode(BaseModel):
    java: str = ""
    python: str = ""
    cpp: str = ""


class QuestionGenerateRequest(BaseModel):
    topic: str = Field(..., min_length=1, max_length=100)
    difficulty: str = Field(..., pattern="^(easy|medium|hard)$")


class QuestionGenerateResponse(BaseModel):
    question_id: str
    title: str
    description: str
    constraints: str
    examples: List[Dict[str, str]] = []
    test_cases: List[Dict[str, str]]
    starter_code: StarterCode


class QuestionDB(BaseModel):
    id: str
    title: str
    description: str
    constraints: Optional[str]
    topic: str
    difficulty: str
    created_at: datetime

    class Config:
        from_attributes = True


class CodeSubmitRequest(BaseModel):
    question_id: str
    language: str = Field(..., pattern="^(python|java|cpp|c\+\+)$")
    code: str = Field(..., min_length=1)


class TestCaseResult(BaseModel):
    input: str
    expected: str
    actual: str
    passed: bool


class CodeSubmitResponse(BaseModel):
    status: str
    results: List[TestCaseResult]
    execution_time_ms: Optional[float] = None
    stderr: Optional[str] = None


class CodeRunRequest(BaseModel):
    question_id: str
    language: str = Field(..., pattern="^(python|java|cpp|c\+\+)$")
    code: str = Field(..., min_length=1)


class SubmissionResult(BaseModel):
    test_case_id: str
    actual_output: Optional[str]
    passed: bool

    class Config:
        from_attributes = True


class SubmissionDB(BaseModel):
    id: str
    question_id: str
    language: str
    status: str
    execution_time_ms: Optional[float]
    created_at: datetime
    results: List[SubmissionResult]

    class Config:
        from_attributes = True


class HealthCheck(BaseModel):
    status: str
    version: str = "1.0.0"
    redis: str = "unknown"
