"""
AI-powered endpoints using Ollama
Provides intelligent features for students
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict
from ..core.database import get_db
from ..api.deps import require_student
from ..models import User, StudentProfile, ResumeData
from ..services.ai_service import ai_service
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI Features"])

class ProjectIdeaRequest(BaseModel):
    target_role: str = None

class CareerGuidanceRequest(BaseModel):
    include_salary: bool = True

class InterviewQuestionsRequest(BaseModel):
    target_role: str
    difficulty: str = "medium"
    count: int = 10

@router.post("/resume/analyze")
def analyze_resume_ai(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    AI-powered resume analysis
    Provides detailed insights and recommendations
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    resume_data = db.query(ResumeData).filter(ResumeData.student_id == student.id).first()
    if not resume_data:
        raise HTTPException(status_code=404, detail="No resume uploaded")
    
    # Prepare resume data for AI analysis
    resume_dict = {
        "extracted_name": resume_data.extracted_name,
        "extracted_skills": resume_data.extracted_skills or [],
        "extracted_projects": resume_data.extracted_projects or [],
        "extracted_experience": resume_data.extracted_experience or []
    }
    
    analysis = ai_service.analyze_resume_advanced(resume_dict)
    
    return {
        "analysis": analysis,
        "message": "AI analysis complete"
    }

@router.post("/plan/generate")
def generate_ai_plan(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered personalized learning plan
    Based on student profile and goals
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Prepare student data
    student_data = {
        "target_role": student.target_role,
        "skills": student.skills or [],
        "available_hours": student.available_hours,
        "pri_score": student.placement_readiness_index,
        "weak_areas": ["DSA", "System Design"]  # Can be determined from assessments
    }
    
    # Generate AI plan
    plan = ai_service.generate_personalized_plan(student_data)
    
    return {
        "plan": plan,
        "message": "AI-powered plan generated successfully"
    }

@router.post("/interview-questions")
def generate_interview_questions_post(
    request: InterviewQuestionsRequest,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Generate AI-powered interview questions (POST endpoint)
    Tailored to role and difficulty
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    target_role = request.target_role or student.target_role
    
    # Generate questions using AI
    questions = ai_service.generate_interview_questions(
        target_role, 
        request.difficulty, 
        request.count
    )
    
    return {
        "questions": questions,
        "role": target_role,
        "difficulty": request.difficulty,
        "count": len(questions)
    }

@router.get("/interview/questions")
def get_interview_questions(
    role: str = None,
    difficulty: str = "medium",
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Get AI-generated interview questions
    Tailored to role and difficulty
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    target_role = role or student.target_role
    
    # Generate questions
    questions = ai_service.generate_interview_questions(target_role, difficulty)
    
    return {
        "questions": questions,
        "role": target_role,
        "difficulty": difficulty
    }

@router.get("/skills/gap-analysis")
def analyze_skill_gaps(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Analyze skill gaps for target role
    Provides learning roadmap
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Prepare profile data
    profile_data = {
        "skills": student.skills or [],
        "pri_score": student.placement_readiness_index,
        "target_role": student.target_role
    }
    
    # Analyze gaps
    analysis = ai_service.analyze_skill_gaps(profile_data, student.target_role)
    
    return {
        "analysis": analysis,
        "current_skills": student.skills,
        "target_role": student.target_role
    }

@router.post("/projects/ideas")
def get_project_ideas(
    request: ProjectIdeaRequest = None,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Get AI-generated project ideas
    Based on skills and target role
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    target_role = request.target_role if request else student.target_role
    skills = student.skills or []
    
    # Generate project ideas
    projects = ai_service.generate_project_ideas(skills, target_role)
    
    return {
        "projects": projects,
        "message": "Project ideas generated successfully"
    }

@router.post("/career/guidance")
def get_career_guidance(
    request: CareerGuidanceRequest = CareerGuidanceRequest(),
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Get personalized career guidance
    Based on profile and market trends
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Prepare student data
    student_data = {
        "target_role": student.target_role,
        "skills": student.skills or [],
        "year": student.year,
        "pri_score": student.placement_readiness_index,
        "college": student.college,
        "branch": student.branch
    }
    
    # Get career guidance
    guidance = ai_service.provide_career_guidance(student_data)
    
    return {
        "guidance": guidance,
        "message": "Career guidance generated successfully"
    }

@router.get("/mentor/chat")
def ai_mentor_chat(
    question: str,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Chat with AI mentor
    Get answers to career and technical questions
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    system_prompt = f"""You are a helpful career mentor for {student.name}, 
    a {student.year} year {student.branch} student targeting {student.target_role} roles.
    Provide concise, actionable advice."""
    
    # Generate response
    response = ai_service._generate(question, system_prompt)
    
    return {
        "question": question,
        "response": response,
        "mentor_context": {
            "student_name": student.name,
            "target_role": student.target_role,
            "year": student.year
        }
    }

@router.get("/recommendations/daily")
def get_daily_recommendations(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """
    Get daily personalized recommendations
    Based on current progress and goals
    """
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not student:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    recommendations = {
        "focus_area": "Data Structures & Algorithms",
        "daily_goal": "Solve 3 medium-level problems",
        "suggested_topics": ["Binary Search", "Two Pointers", "Sliding Window"],
        "motivation": f"You're on a {student.current_streak} day streak! Keep it going!",
        "quick_wins": [
            "Review yesterday's problems",
            "Watch one system design video",
            "Update LinkedIn profile"
        ],
        "resources": [
            {"title": "LeetCode Daily Challenge", "type": "practice"},
            {"title": "System Design Primer", "type": "reading"},
            {"title": "Mock Interview", "type": "practice"}
        ]
    }
    
    return {
        "recommendations": recommendations,
        "date": "today",
        "personalized_for": student.name
    }
