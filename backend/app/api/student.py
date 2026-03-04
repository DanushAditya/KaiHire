from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import User, StudentProfile, ResumeData, SkillAssessment, Plan, PlanTask
from ..schemas import (
    StudentProfileResponse,
    StudentProfileUpdate,
    ResumeUploadResponse,
    SkillAssessmentCreate,
    SkillAssessmentResponse,
    PlanResponse,
    PlanTaskResponse,
)
from ..services.resume_service import parse_resume
from ..services.score_service import (
    calculate_placement_readiness_index,
    calculate_skill_level_index,
    update_student_tier
)
from ..services.plan_service import generate_7_day_plan, generate_30_day_plan, mark_task_complete
from ..services.streak_service import update_streak
from .deps import require_student

router = APIRouter(prefix="/student", tags=["Student"])

@router.get("/profile", response_model=StudentProfileResponse)
def get_profile(current_user: User = Depends(require_student), db: Session = Depends(get_db)):
    """Get student profile"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/profile", response_model=StudentProfileResponse)
def update_profile(
    profile_data: StudentProfileUpdate,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Update student profile"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Update fields
    for field, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, field, value)
    
    db.commit()
    db.refresh(profile)
    
    # Update streak
    update_streak(db, profile.id)
    
    return profile

@router.post("/resume/upload", response_model=ResumeUploadResponse)
async def upload_resume(
    file: UploadFile = File(...),
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Upload and parse resume"""
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Read file content
    content = await file.read()
    
    # Parse resume
    parsed_data = parse_resume(content, file.filename)
    
    # Save or update resume data
    resume_data = db.query(ResumeData).filter(ResumeData.student_id == profile.id).first()
    if resume_data:
        resume_data.extracted_name = parsed_data["extracted_name"]
        resume_data.extracted_skills = parsed_data["extracted_skills"]
        resume_data.extracted_projects = parsed_data["extracted_projects"]
        resume_data.extracted_experience = parsed_data["extracted_experience"]
        resume_data.resume_quality_score = parsed_data["resume_quality_score"]
    else:
        resume_data = ResumeData(
            student_id=profile.id,
            file_path=f"resumes/{current_user.id}_{file.filename}",
            **parsed_data
        )
        db.add(resume_data)
    
    db.commit()
    
    # Recalculate PRI
    profile.placement_readiness_index = calculate_placement_readiness_index(db, profile.id)
    db.commit()
    
    # Update streak
    update_streak(db, profile.id)
    
    return parsed_data

@router.post("/assessment", response_model=SkillAssessmentResponse)
def create_assessment(
    assessment_data: SkillAssessmentCreate,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Create a skill assessment (simplified - in production would include questions)"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Simulate assessment (in production, this would involve actual questions)
    import random
    total_questions = 10
    correct_answers = random.randint(5, 10)
    score = (correct_answers / total_questions) * 100
    
    assessment = SkillAssessment(
        student_id=profile.id,
        category=assessment_data.category,
        difficulty=assessment_data.difficulty,
        score=score,
        total_questions=total_questions,
        correct_answers=correct_answers
    )
    db.add(assessment)
    db.commit()
    db.refresh(assessment)
    
    # Update scores
    profile.skill_level_index = calculate_skill_level_index(db, profile.id)
    profile.placement_readiness_index = calculate_placement_readiness_index(db, profile.id)
    db.commit()
    
    # Update streak
    update_streak(db, profile.id)
    
    return assessment

@router.get("/assessments", response_model=List[SkillAssessmentResponse])
def get_assessments(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get all assessments for current student"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    assessments = db.query(SkillAssessment).filter(SkillAssessment.student_id == profile.id).all()
    return assessments

@router.post("/plan/generate", response_model=PlanResponse)
def generate_plan(
    plan_type: str,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Generate personalized learning plan"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    if plan_type == "7_day":
        plan = generate_7_day_plan(db, profile)
    elif plan_type == "30_day":
        plan = generate_30_day_plan(db, profile)
        if not plan:
            raise HTTPException(status_code=400, detail="Complete 7-day plan first")
    else:
        raise HTTPException(status_code=400, detail="Invalid plan type")
    
    return plan

@router.get("/plans", response_model=List[PlanResponse])
def get_plans(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get all plans for current student"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    plans = db.query(Plan).filter(Plan.student_id == profile.id).all()
    return plans

@router.get("/plan/{plan_id}/tasks", response_model=List[PlanTaskResponse])
def get_plan_tasks(
    plan_id: int,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get tasks for a specific plan"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Verify plan belongs to student
    plan = db.query(Plan).filter(Plan.id == plan_id, Plan.student_id == profile.id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    
    tasks = db.query(PlanTask).filter(PlanTask.plan_id == plan_id).order_by(PlanTask.day).all()
    return tasks

@router.post("/task/{task_id}/complete", response_model=PlanTaskResponse)
def complete_task(
    task_id: int,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Mark a task as complete"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    task = mark_task_complete(db, task_id, profile.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or already completed")
    
    # Update tier and streak
    update_student_tier(db, profile)
    update_streak(db, profile.id)
    
    # Recalculate PRI
    profile.placement_readiness_index = calculate_placement_readiness_index(db, profile.id)
    db.commit()
    
    return task
