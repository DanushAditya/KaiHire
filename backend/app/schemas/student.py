from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class StudentProfileBase(BaseModel):
    name: str
    college: str
    year: int
    branch: str
    section: Optional[str] = None
    target_role: str
    available_hours: int = 10
    skills: List[str] = []

class StudentProfileUpdate(BaseModel):
    name: Optional[str] = None
    college: Optional[str] = None
    year: Optional[int] = None
    branch: Optional[str] = None
    section: Optional[str] = None
    target_role: Optional[str] = None
    available_hours: Optional[int] = None
    skills: Optional[List[str]] = None

class StudentProfileResponse(StudentProfileBase):
    id: int
    user_id: int
    skill_level_index: float
    placement_readiness_index: float
    current_streak: int
    longest_streak: int
    total_xp: int
    tier: str
    referral_code: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class ResumeUploadResponse(BaseModel):
    extracted_name: Optional[str]
    extracted_skills: List[str]
    extracted_projects: List[dict]
    extracted_experience: List[dict]
    resume_quality_score: float

class SkillAssessmentCreate(BaseModel):
    category: str
    difficulty: str

class SkillAssessmentResponse(BaseModel):
    id: int
    category: str
    difficulty: str
    score: float
    total_questions: int
    correct_answers: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class PlanResponse(BaseModel):
    id: int
    plan_type: str
    is_active: bool
    is_completed: bool
    started_at: datetime
    
    class Config:
        from_attributes = True

class PlanTaskResponse(BaseModel):
    id: int
    day: int
    title: str
    description: Optional[str]
    task_type: str
    is_completed: bool
    xp_reward: int
    
    class Config:
        from_attributes = True

class FriendRequest(BaseModel):
    friend_email: str

class FriendshipResponse(BaseModel):
    id: int
    friend_name: str
    friend_email: str
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True
