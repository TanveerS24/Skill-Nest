import uuid
from datetime import datetime
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Integer, Boolean, Float
from sqlalchemy.orm import relationship
from app.db.base import Base


def generate_uuid():
    return str(uuid.uuid4())


class Question(Base):
    __tablename__ = "questions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    constraints = Column(Text, nullable=True)
    topic = Column(String(100), nullable=False, index=True)
    difficulty = Column(String(20), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    test_cases = relationship("TestCase", back_populates="question", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="question", cascade="all, delete-orphan")


class TestCase(Base):
    __tablename__ = "test_cases"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False, index=True)
    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_sample = Column(Boolean, default=False)
    order_index = Column(Integer, nullable=False)

    question = relationship("Question", back_populates="test_cases")


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    question_id = Column(String(36), ForeignKey("questions.id"), nullable=False, index=True)
    language = Column(String(20), nullable=False)
    code = Column(Text, nullable=False)
    status = Column(String(20), nullable=False)
    execution_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    question = relationship("Question", back_populates="submissions")
    results = relationship("SubmissionResult", back_populates="submission", cascade="all, delete-orphan")


class SubmissionResult(Base):
    __tablename__ = "submission_results"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    submission_id = Column(String(36), ForeignKey("submissions.id"), nullable=False, index=True)
    test_case_id = Column(String(36), ForeignKey("test_cases.id"), nullable=False)
    actual_output = Column(Text, nullable=True)
    passed = Column(Boolean, nullable=False)
    execution_time_ms = Column(Float, nullable=True)

    submission = relationship("Submission", back_populates="results")
