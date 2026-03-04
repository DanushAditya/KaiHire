from sqlalchemy.orm import Session
from ..models import StudentProfile, ResumeData, SkillAssessment, PlanTask, ChallengeParticipation

def calculate_placement_readiness_index(db: Session, student_id: int) -> float:
    """
    Calculate PRI based on multiple factors:
    - Resume Quality (20%)
    - Skill Test Score (30%)
    - Project Depth (20%)
    - Streak Consistency (15%)
    - Challenge Participation (15%)
    """
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not student:
        return 0.0
    
    # Resume Quality (20%)
    resume_score = 0.0
    resume_data = db.query(ResumeData).filter(ResumeData.student_id == student_id).first()
    if resume_data:
        resume_score = (resume_data.resume_quality_score / 100) * 20
    
    # Skill Test Score (30%)
    skill_score = 0.0
    assessments = db.query(SkillAssessment).filter(SkillAssessment.student_id == student_id).all()
    if assessments:
        avg_assessment_score = sum(a.score for a in assessments) / len(assessments)
        skill_score = (avg_assessment_score / 100) * 30
    
    # Project Depth (20%)
    project_score = 0.0
    if resume_data and resume_data.extracted_projects:
        num_projects = len(resume_data.extracted_projects)
        project_score = min(num_projects * 7, 20)
    
    # Streak Consistency (15%)
    streak_score = 0.0
    if student.current_streak > 0:
        streak_score = min(student.current_streak * 2, 15)
    
    # Challenge Participation (15%)
    challenge_score = 0.0
    completed_challenges = db.query(ChallengeParticipation).filter(
        ChallengeParticipation.student_id == student_id,
        ChallengeParticipation.is_completed == True
    ).count()
    challenge_score = min(completed_challenges * 5, 15)
    
    total_pri = resume_score + skill_score + project_score + streak_score + challenge_score
    return round(total_pri, 2)

def calculate_skill_level_index(db: Session, student_id: int) -> float:
    """
    Calculate SLI based on assessment performance
    """
    assessments = db.query(SkillAssessment).filter(SkillAssessment.student_id == student_id).all()
    
    if not assessments:
        return 0.0
    
    # Weight by difficulty
    difficulty_weights = {
        "easy": 1.0,
        "medium": 1.5,
        "hard": 2.0
    }
    
    weighted_sum = 0.0
    total_weight = 0.0
    
    for assessment in assessments:
        weight = difficulty_weights.get(assessment.difficulty, 1.0)
        weighted_sum += assessment.score * weight
        total_weight += weight
    
    if total_weight == 0:
        return 0.0
    
    sli = (weighted_sum / total_weight)
    return round(sli, 2)

def update_student_tier(db: Session, student: StudentProfile):
    """Update student tier based on XP"""
    xp = student.total_xp
    
    if xp < 100:
        tier = "Beginner"
    elif xp < 300:
        tier = "Explorer"
    elif xp < 600:
        tier = "Achiever"
    elif xp < 1000:
        tier = "Pro"
    else:
        tier = "Elite"
    
    student.tier = tier
    db.commit()
