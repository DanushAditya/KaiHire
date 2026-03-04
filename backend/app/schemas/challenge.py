from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChallengeResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    challenge_type: str
    duration_days: int
    xp_reward: int
    pri_boost: int
    difficulty: str
    is_active: bool
    
    class Config:
        from_attributes = True

class ChallengeParticipationResponse(BaseModel):
    id: int
    challenge_id: int
    is_completed: bool
    progress: int
    started_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ChallengeEnroll(BaseModel):
    challenge_id: int

class ChallengeProgressUpdate(BaseModel):
    participation_id: int
    progress: int
