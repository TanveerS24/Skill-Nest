from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class SubmissionCreate(BaseModel):
    problem_id: int
    code: str


class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    code: str
    detected_language: Optional[str]
    verdict: str
    runtime: Optional[float]
    memory: Optional[float]
    created_at: datetime

    class Config:
        from_attributes = True
