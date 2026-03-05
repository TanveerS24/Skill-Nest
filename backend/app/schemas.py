from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, List
from app.models import UserRole, Difficulty, Verdict, Language


# User Schemas
class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str = Field(..., min_length=8)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    id: int
    role: UserRole
    created_at: datetime
    
    class Config:
        from_attributes = True


# Auth Schemas
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[UserRole] = None


# Problem Schemas
class TestCaseBase(BaseModel):
    input: str
    expected_output: str
    is_hidden: bool = False


class TestCaseCreate(TestCaseBase):
    pass


class TestCaseResponse(TestCaseBase):
    id: int
    problem_id: int
    
    class Config:
        from_attributes = True


class ProblemBase(BaseModel):
    title: str
    description: str
    difficulty: Difficulty
    time_limit: int = 5
    memory_limit: int = 256


class ProblemCreate(ProblemBase):
    test_cases: List[TestCaseCreate] = []


class ProblemResponse(ProblemBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class ProblemDetail(ProblemResponse):
    test_cases: List[TestCaseResponse] = []
    
    class Config:
        from_attributes = True


# Submission Schemas
class SubmissionCreate(BaseModel):
    problem_id: int
    language: Language
    code: str


class SubmissionResponse(BaseModel):
    id: int
    user_id: int
    problem_id: int
    language: Language
    code: str
    verdict: Verdict
    runtime: Optional[float]
    memory: Optional[float]
    time_complexity: Optional[str]
    space_complexity: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


# AI Analysis Schema
class AIAnalysisResult(BaseModel):
    is_safe: bool
    time_complexity: Optional[str] = None
    space_complexity: Optional[str] = None
    issues: List[str] = []


# Execution Results
class ExecutionResult(BaseModel):
    verdict: Verdict
    runtime: Optional[float] = None
    memory: Optional[float] = None
    output: Optional[str] = None
    error: Optional[str] = None


# Leaderboard Schemas
class LeaderboardEntry(BaseModel):
    user_id: int
    email: str
    problems_solved: int
    avg_time_complexity: float
    avg_space_complexity: float
    total_submissions: int
    
    class Config:
        from_attributes = True


# Admin Dashboard Schemas
class AdminStats(BaseModel):
    total_users: int
    total_submissions: int
    accepted_submissions: int
    most_attempted_problems: List[dict]
    language_usage: dict
    top_users: List[LeaderboardEntry]
