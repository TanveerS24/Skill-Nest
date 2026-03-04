from sqlalchemy import Column, Integer, String, Text, DateTime, Float, ForeignKey, Index
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database import Base


class Submission(Base):
    __tablename__ = "submissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id"), nullable=False)
    code = Column(Text, nullable=False)
    detected_language = Column(String, nullable=True)
    verdict = Column(String, nullable=False)  # Accepted, Wrong Answer, etc.
    runtime = Column(Float, nullable=True)  # milliseconds
    memory = Column(Float, nullable=True)  # MB
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")

    __table_args__ = (
        Index("idx_submission_user_id", "user_id"),
        Index("idx_submission_problem_id", "problem_id"),
    )
