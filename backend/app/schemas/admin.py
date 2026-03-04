from pydantic import BaseModel
from typing import List


class TopUserResponse(BaseModel):
    id: int
    email: str
    score: int

    class Config:
        from_attributes = True


class AdminStatsResponse(BaseModel):
    total_users: int
    total_submissions: int
    accepted_submissions: int
    acceptance_rate: float
    submissions_today: int


class LanguageUsageResponse(BaseModel):
    language: str
    count: int


class ProblemAnalyticsResponse(BaseModel):
    problem_id: int
    problem_title: str
    submission_count: int
