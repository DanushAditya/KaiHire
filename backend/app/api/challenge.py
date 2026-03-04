from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import User, StudentProfile, Challenge, ChallengeParticipation
from ..schemas import ChallengeResponse, ChallengeParticipationResponse, ChallengeEnroll, ChallengeProgressUpdate
from ..services.streak_service import update_streak
from ..services.score_service import update_student_tier, calculate_placement_readiness_index
from datetime import datetime
from .deps import require_student

router = APIRouter(prefix="/challenges", tags=["Challenges"])

@router.get("/", response_model=List[ChallengeResponse])
def get_challenges(db: Session = Depends(get_db)):
    """Get all active challenges"""
    challenges = db.query(Challenge).filter(Challenge.is_active == True).all()
    return challenges

@router.post("/enroll", response_model=ChallengeParticipationResponse)
def enroll_challenge(
    enrollment: ChallengeEnroll,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Enroll in a challenge"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Check if already enrolled
    existing = db.query(ChallengeParticipation).filter(
        ChallengeParticipation.challenge_id == enrollment.challenge_id,
        ChallengeParticipation.student_id == profile.id
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Already enrolled in this challenge")
    
    # Create participation
    participation = ChallengeParticipation(
        challenge_id=enrollment.challenge_id,
        student_id=profile.id
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)
    
    # Update streak
    update_streak(db, profile.id)
    
    return participation

@router.get("/my-challenges", response_model=List[ChallengeParticipationResponse])
def get_my_challenges(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get all challenges for current student"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    participations = db.query(ChallengeParticipation).filter(
        ChallengeParticipation.student_id == profile.id
    ).all()
    return participations

@router.put("/progress", response_model=ChallengeParticipationResponse)
def update_progress(
    progress_data: ChallengeProgressUpdate,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Update challenge progress"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    participation = db.query(ChallengeParticipation).filter(
        ChallengeParticipation.id == progress_data.participation_id,
        ChallengeParticipation.student_id == profile.id
    ).first()
    
    if not participation:
        raise HTTPException(status_code=404, detail="Participation not found")
    
    participation.progress = progress_data.progress
    
    # Check if completed
    if progress_data.progress >= 100 and not participation.is_completed:
        participation.is_completed = True
        participation.completed_at = datetime.utcnow()
        
        # Award XP and PRI boost
        challenge = db.query(Challenge).filter(Challenge.id == participation.challenge_id).first()
        if challenge:
            profile.total_xp += challenge.xp_reward
            profile.placement_readiness_index = min(
                profile.placement_readiness_index + challenge.pri_boost,
                100.0
            )
        
        # Update tier
        update_student_tier(db, profile)
    
    db.commit()
    db.refresh(participation)
    
    # Update streak
    update_streak(db, profile.id)
    
    return participation
