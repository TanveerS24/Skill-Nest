from pydantic import BaseModel
from typing import Optional


class ProblemCreate(BaseModel):
    title: str
    difficulty: str  # Easy, Medium, Hard
    description: str
    time_limit: int = 2
    memory_limit: int = 256


class ProblemResponse(BaseModel):
    id: int
    title: str
    difficulty: str
    description: str
    time_limit: int
    memory_limit: int

    class Config:
        from_attributes = True
