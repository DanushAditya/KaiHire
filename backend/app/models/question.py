from sqlalchemy import Column, Integer, String, JSON, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy import DateTime
from ..core.database import Base

class Question(Base):
    """MCQ questions for skill assessments"""
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False, index=True)  # DSA, ML, Web, Core, etc.
    role = Column(String(100), nullable=False, index=True)  # SDE, ML, Analyst, Core
    difficulty = Column(String(50), nullable=False, index=True)  # easy, medium, hard
    question_text = Column(Text, nullable=False)
    options = Column(JSON, nullable=False)  # List of 4 options
    correct_answer = Column(Integer, nullable=False)  # Index of correct option (0-3)
    explanation = Column(Text)
    points = Column(Integer, default=10)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
