from sqlalchemy import Column, Integer, String, Text, Enum as SQLEnum
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class Difficulty(enum.Enum):
    Easy = "Easy"
    Medium = "Medium"
    Hard = "Hard"


class Problem(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    difficulty = Column(SQLEnum(Difficulty), nullable=False)
    description = Column(Text, nullable=False)
    time_limit = Column(Integer, default=2, nullable=False)  # seconds
    memory_limit = Column(Integer, default=256, nullable=False)  # MB

    # Relationships
    submissions = relationship("Submission", back_populates="problem")
