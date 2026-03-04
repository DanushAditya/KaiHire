"""Service for generating professional readiness cards"""
from sqlalchemy.orm import Session
from ..models import StudentProfile, ResumeData
from typing import Dict
import secrets
import string

def generate_readiness_card_data(db: Session, student_id: int) -> Dict:
    """
    Generate professional readiness card data for a student
    Returns data that can be used to create a downloadable card
    """
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    
    if not student:
        return None
    
    resume_data = db.query(ResumeData).filter(ResumeData.student_id == student_id).first()
    
    # Get top skills
    top_skills = student.skills[:5] if student.skills else []
    
    # Determine strength areas based on assessments and scores
    strength_areas = determine_strength_areas(student, resume_data)
    
    # Determine improvement areas
    improvement_areas = determine_improvement_areas(student, resume_data)
    
    # Generate referral link if not exists
    if not student.referral_code:
        student.referral_code = generate_referral_code()
        db.commit()
    
    card_data = {
        "name": student.name,
        "college": student.college,
        "year": student.year,
        "branch": student.branch,
        "target_role": student.target_role,
        "pri_score": round(student.placement_readiness_index, 1),
        "sli_level": get_sli_level(student.skill_level_index),
        "current_streak": student.current_streak,
        "tier": student.tier,
        "total_xp": student.total_xp,
        "top_skills": top_skills,
        "strength_areas": strength_areas,
        "improvement_areas": improvement_areas,
        "referral_code": student.referral_code,
        "referral_link": f"https://kaihire.app/register?ref={student.referral_code}"
    }
    
    return card_data

def determine_strength_areas(student: StudentProfile, resume_data: ResumeData) -> list:
    """Determine student's strength areas"""
    strengths = []
    
    # Check PRI score
    if student.placement_readiness_index >= 70:
        strengths.append("High Placement Readiness")
    
    # Check streak
    if student.current_streak >= 7:
        strengths.append("Consistent Learner")
    
    # Check skills
    if student.skills and len(student.skills) >= 10:
        strengths.append("Diverse Skill Set")
    
    # Check resume quality
    if resume_data and resume_data.resume_quality_score >= 70:
        strengths.append("Strong Resume")
    
    # Check projects
    if resume_data and resume_data.extracted_projects and len(resume_data.extracted_projects) >= 3:
        strengths.append("Project Portfolio")
    
    # Check XP
    if student.total_xp >= 500:
        strengths.append("Active Participant")
    
    return strengths[:3]  # Return top 3

def determine_improvement_areas(student: StudentProfile, resume_data: ResumeData) -> list:
    """Determine areas for improvement"""
    improvements = []
    
    # Check PRI score
    if student.placement_readiness_index < 50:
        improvements.append("Boost Placement Readiness")
    
    # Check streak
    if student.current_streak < 3:
        improvements.append("Build Daily Consistency")
    
    # Check skills
    if not student.skills or len(student.skills) < 5:
        improvements.append("Expand Technical Skills")
    
    # Check resume
    if not resume_data or resume_data.resume_quality_score < 60:
        improvements.append("Enhance Resume Quality")
    
    # Check projects
    if not resume_data or not resume_data.extracted_projects or len(resume_data.extracted_projects) < 2:
        improvements.append("Add More Projects")
    
    return improvements[:3]  # Return top 3

def get_sli_level(sli_score: float) -> str:
    """Convert SLI score to level"""
    if sli_score >= 80:
        return "Expert"
    elif sli_score >= 60:
        return "Advanced"
    elif sli_score >= 40:
        return "Intermediate"
    elif sli_score >= 20:
        return "Beginner"
    else:
        return "Novice"

def generate_referral_code() -> str:
    """Generate unique referral code"""
    chars = string.ascii_uppercase + string.digits
    return ''.join(secrets.choice(chars) for _ in range(8))

def process_referral(db: Session, referral_code: str, new_student_id: int) -> bool:
    """
    Process referral when a new student signs up with a referral code
    Award bonus points to both users
    """
    # Find the referrer
    referrer = db.query(StudentProfile).filter(
        StudentProfile.referral_code == referral_code
    ).first()
    
    if not referrer:
        return False
    
    # Award bonus XP to referrer
    referrer.total_xp += 50
    
    # Award bonus XP to new student
    new_student = db.query(StudentProfile).filter(StudentProfile.id == new_student_id).first()
    if new_student:
        new_student.total_xp += 25
    
    db.commit()
    return True

def process_referral_on_signup(db: Session, referral_code: str) -> int:
    """
    Process referral during signup - returns initial XP for new user
    Awards bonus to referrer immediately
    """
    # Find the referrer
    referrer = db.query(StudentProfile).filter(
        StudentProfile.referral_code == referral_code
    ).first()
    
    if not referrer:
        return 0  # Invalid code, no bonus
    
    # Award bonus XP to referrer
    referrer.total_xp += 50
    db.commit()
    
    # Return bonus XP for new user
    return 25
