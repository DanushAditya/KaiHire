"""Professional Readiness Card endpoints"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..api.deps import require_student
from ..models import User
from ..services.card_service import generate_readiness_card_data
from pydantic import BaseModel

router = APIRouter(prefix="/card", tags=["card"])

class ReferralRequest(BaseModel):
    referral_code: str

@router.get("/generate")
def generate_card(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Generate professional readiness card data"""
    
    from ..models import StudentProfile
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    card_data = generate_readiness_card_data(db, student.id)
    
    if not card_data:
        return {"error": "Unable to generate card"}
    
    return {
        "card": card_data,
        "message": "Card generated successfully"
    }

@router.post("/referral/apply")
def apply_referral(
    request: ReferralRequest,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Apply referral code for bonus points"""
    
    from ..models import StudentProfile
    from ..services.card_service import process_referral
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    if student.total_xp > 25:  
        return {"error": "Referral code can only be applied once during registration"}
    
    success = process_referral(db, request.referral_code, student.id)
    
    if success:
        db.refresh(student)
        return {
            "success": True,
            "message": "Referral applied! You earned 25 XP!",
            "new_xp": student.total_xp
        }
    else:
        return {
            "success": False,
            "error": "Invalid referral code"
        }

@router.get("/referral/stats")
def get_referral_stats(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get referral statistics"""
    
    from ..models import StudentProfile
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    

    referrals_count = db.query(StudentProfile).filter(
        StudentProfile.referral_code == student.referral_code
    ).count() - 1 
    
    return {
        "referral_code": student.referral_code,
        "total_referrals": max(0, referrals_count),
        "xp_earned_from_referrals": max(0, referrals_count) * 50
    }
