from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    challenge_type = Column(String(100), nullable=False)  # "DSA_SPRINT", "ML_SPRINT", "CORE_SPRINT"
    duration_days = Column(Integer, default=7)
    xp_reward = Column(Integer, default=100)
    pri_boost = Column(Integer, default=5)
    difficulty = Column(String(50), default="intermediate")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    participations = relationship("ChallengeParticipation", back_populates="challenge")

class ChallengeParticipation(Base):
    __tablename__ = "challenge_participations"
    
    id = Column(Integer, primary_key=True, index=True)
    challenge_id = Column(Integer, ForeignKey("challenges.id"))
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    is_completed = Column(Boolean, default=False)
    progress = Column(Integer, default=0)  # percentage
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    challenge = relationship("Challenge", back_populates="participations")
    student = relationship("StudentProfile", back_populates="challenges")
