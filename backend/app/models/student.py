from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, JSON, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base

class StudentProfile(Base):
    __tablename__ = "student_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String(255), nullable=False)
    college = Column(String(255), nullable=False)
    year = Column(Integer, nullable=False)
    branch = Column(String(255), nullable=False)
    section = Column(String(50))
    target_role = Column(String(100), nullable=False)
    available_hours = Column(Integer, default=10)
    skills = Column(JSON, default=list)
    
    # Scores
    skill_level_index = Column(Float, default=0.0)
    placement_readiness_index = Column(Float, default=0.0)
    
    # Gamification
    current_streak = Column(Integer, default=0)
    longest_streak = Column(Integer, default=0)
    last_activity_date = Column(DateTime(timezone=True))
    total_xp = Column(Integer, default=0)
    tier = Column(String(50), default="Beginner")
    
    # Referral
    referral_code = Column(String(50), unique=True, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    user = relationship("User", back_populates="student_profile")
    resume_data = relationship("ResumeData", back_populates="student", uselist=False)
    assessments = relationship("SkillAssessment", back_populates="student")
    plans = relationship("Plan", back_populates="student")
    challenges = relationship("ChallengeParticipation", back_populates="student")
    sent_friend_requests = relationship("Friendship", foreign_keys="Friendship.student_id", back_populates="student")
    received_friend_requests = relationship("Friendship", foreign_keys="Friendship.friend_id", back_populates="friend")

class ResumeData(Base):
    __tablename__ = "resume_data"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"), unique=True)
    file_path = Column(String(500))
    extracted_name = Column(String(255))
    extracted_skills = Column(JSON, default=list)
    extracted_projects = Column(JSON, default=list)
    extracted_experience = Column(JSON, default=list)
    resume_quality_score = Column(Float, default=0.0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("StudentProfile", back_populates="resume_data")

class SkillAssessment(Base):
    __tablename__ = "skill_assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    category = Column(String(100), nullable=False)
    difficulty = Column(String(50), nullable=False)
    score = Column(Float, nullable=False)
    total_questions = Column(Integer, nullable=False)
    correct_answers = Column(Integer, nullable=False)
    time_taken = Column(Integer)  # in seconds
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("StudentProfile", back_populates="assessments")

class Plan(Base):
    __tablename__ = "plans"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    plan_type = Column(String(50), nullable=False)  # "7_day_kickstart" or "30_day_advanced"
    is_active = Column(Boolean, default=True)
    is_completed = Column(Boolean, default=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    student = relationship("StudentProfile", back_populates="plans")
    tasks = relationship("PlanTask", back_populates="plan")

class PlanTask(Base):
    __tablename__ = "plan_tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    plan_id = Column(Integer, ForeignKey("plans.id"))
    day = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    task_type = Column(String(50))  # "assessment", "challenge", "practice"
    is_completed = Column(Boolean, default=False)
    completed_at = Column(DateTime(timezone=True))
    xp_reward = Column(Integer, default=10)
    
    # Relationships
    plan = relationship("Plan", back_populates="tasks")

class Friendship(Base):
    __tablename__ = "friendships"
    
    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("student_profiles.id"))
    friend_id = Column(Integer, ForeignKey("student_profiles.id"))
    status = Column(String(50), default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    student = relationship("StudentProfile", foreign_keys=[student_id], back_populates="sent_friend_requests")
    friend = relationship("StudentProfile", foreign_keys=[friend_id], back_populates="received_friend_requests")
