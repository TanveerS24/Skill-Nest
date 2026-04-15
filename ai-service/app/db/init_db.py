from app.db.base import engine, Base
from app.db.models import Question, TestCase, Submission, SubmissionResult


def init_db():
    Base.metadata.create_all(bind=engine)
