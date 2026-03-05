from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Enum as SQLAEnum, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.database import Base


class UserRole(str, enum.Enum):
    USER = "user"
    ADMIN = "admin"


class Difficulty(str, enum.Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class Verdict(str, enum.Enum):
    ACCEPTED = "Accepted"
    WRONG_ANSWER = "Wrong Answer"
    RUNTIME_ERROR = "Runtime Error"
    TIME_LIMIT_EXCEEDED = "Time Limit Exceeded"
    MEMORY_LIMIT_EXCEEDED = "Memory Limit Exceeded"
    COMPILATION_ERROR = "Compilation Error"
    UNSAFE_CODE = "Unsafe Code"


class Language(str, enum.Enum):
    PYTHON = "python"
    JAVA = "java"
    C = "c"
    CPP = "cpp"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(SQLAEnum(UserRole), default=UserRole.USER, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    submissions = relationship("Submission", back_populates="user", cascade="all, delete-orphan")


class Problem(Base):
    __tablename__ = "problems"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=False)
    difficulty = Column(SQLAEnum(Difficulty), nullable=False, index=True)
    time_limit = Column(Integer, default=5, nullable=False)  # seconds
    memory_limit = Column(Integer, default=256, nullable=False)  # MB
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    test_cases = relationship("TestCase", back_populates="problem", cascade="all, delete-orphan")
    submissions = relationship("Submission", back_populates="problem", cascade="all, delete-orphan")


class TestCase(Base):
    __tablename__ = "test_cases"
    
    id = Column(Integer, primary_key=True, index=True)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    input = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)
    is_hidden = Column(Boolean, default=False, nullable=False)
    
    problem = relationship("Problem", back_populates="test_cases")


class Submission(Base):
    __tablename__ = "submissions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    problem_id = Column(Integer, ForeignKey("problems.id", ondelete="CASCADE"), nullable=False)
    language = Column(SQLAEnum(Language), nullable=False)
    code = Column(Text, nullable=False)
    verdict = Column(SQLAEnum(Verdict), nullable=False)
    runtime = Column(Float, nullable=True)  # milliseconds
    memory = Column(Float, nullable=True)  # MB
    time_complexity = Column(String(50), nullable=True)
    space_complexity = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    user = relationship("User", back_populates="submissions")
    problem = relationship("Problem", back_populates="submissions")
