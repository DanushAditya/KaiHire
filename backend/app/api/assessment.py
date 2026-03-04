"""Assessment and question endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..api.deps import require_student
from ..models import User, SkillAssessment, StudentProfile
from ..services.question_service import QuestionService
from ..services.score_service import calculate_skill_level_index, calculate_placement_readiness_index, update_student_tier
from pydantic import BaseModel

router = APIRouter(prefix="/assessment", tags=["assessment"])

class StartAssessmentRequest(BaseModel):
    category: str
    role: str
    difficulty: str = "medium"

class QuestionResponse(BaseModel):
    id: int
    question_text: str
    options: List[str]
    difficulty: str

class SubmitAssessmentRequest(BaseModel):
    category: str
    role: str
    difficulty: str
    answers: dict  # {question_id: answer_index}
    time_taken: int  # seconds

@router.post("/start")
def start_assessment(
    request: StartAssessmentRequest,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Start a new assessment and get questions"""
    
    # Get student profile
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    # Get questions (adaptive based on previous performance)
    previous_assessments = db.query(SkillAssessment).filter(
        SkillAssessment.student_id == student.id,
        SkillAssessment.category == request.category
    ).order_by(SkillAssessment.created_at.desc()).first()
    
    previous_score = previous_assessments.score if previous_assessments else None
    
    questions = QuestionService.get_adaptive_questions(
        db, request.category, request.role, previous_score, count=10
    )
    
    if not questions:
        raise HTTPException(status_code=404, detail="No questions available for this category")
    
    # Return questions without correct answers
    return {
        "questions": [
            {
                "id": q.id,
                "question_text": q.question_text,
                "options": q.options,
                "difficulty": q.difficulty
            }
            for q in questions
        ],
        "total_questions": len(questions),
        "time_limit": 600  # 10 minutes
    }

@router.post("/submit")
def submit_assessment(
    request: SubmitAssessmentRequest,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Submit assessment answers and get automatic evaluation with detailed feedback"""
    
    # Get student profile
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    # Get questions to validate answers
    question_ids = [int(qid) for qid in request.answers.keys()]
    from ..models import Question
    questions = db.query(Question).filter(Question.id.in_(question_ids)).all()
    
    # Calculate score with detailed feedback
    result = QuestionService.calculate_assessment_score(request.answers, questions)
    
    # Generate detailed feedback for each question
    detailed_results = []
    for question in questions:
        user_answer_index = request.answers.get(str(question.id))
        is_correct = user_answer_index == question.correct_answer
        
        detailed_results.append({
            "question_id": question.id,
            "question_text": question.question_text,
            "user_answer": question.options[user_answer_index] if user_answer_index is not None else "Not answered",
            "correct_answer": question.options[question.correct_answer],
            "is_correct": is_correct,
            "explanation": question.explanation if hasattr(question, 'explanation') else None
        })
    
    # Save assessment
    assessment = SkillAssessment(
        student_id=student.id,
        category=request.category,
        difficulty=request.difficulty,
        score=result["score"],
        total_questions=result["total"],
        correct_answers=result["correct"],
        time_taken=request.time_taken
    )
    db.add(assessment)
    
    # Award XP based on performance
    base_xp = int(result["score"] / 10) * 5  # 5 XP per 10% score
    bonus_xp = 0
    
    # Bonus XP for perfect score
    if result["score"] == 100:
        bonus_xp += 50
    
    # Bonus XP for fast completion (under 5 minutes)
    if request.time_taken < 300:
        bonus_xp += 25
    
    total_xp = base_xp + bonus_xp
    student.total_xp += total_xp
    
    # Recalculate SLI and PRI automatically
    student.skill_level_index = calculate_skill_level_index(db, student.id)
    student.placement_readiness_index = calculate_placement_readiness_index(db, student.id)
    
    # Update tier automatically
    update_student_tier(db, student)
    
    # Update streak if assessment taken today
    from datetime import datetime, timedelta
    today = datetime.now().date()
    last_activity = student.last_activity_date
    
    if last_activity:
        if last_activity == today:
            pass  # Already counted today
        elif last_activity == today - timedelta(days=1):
            student.current_streak += 1
            student.longest_streak = max(student.longest_streak, student.current_streak)
        else:
            student.current_streak = 1
    else:
        student.current_streak = 1
    
    student.last_activity_date = today
    
    db.commit()
    db.refresh(student)
    
    return {
        "score": result["score"],
        "correct": result["correct"],
        "total": result["total"],
        "xp_earned": total_xp,
        "base_xp": base_xp,
        "bonus_xp": bonus_xp,
        "new_sli": student.skill_level_index,
        "new_pri": student.placement_readiness_index,
        "tier": student.tier,
        "current_streak": student.current_streak,
        "detailed_results": detailed_results,
        "message": get_performance_message(result["score"]),
        "improvements": get_improvement_suggestions(result["score"], request.category)
    }

@router.get("/history")
def get_assessment_history(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get student's assessment history"""
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    assessments = db.query(SkillAssessment).filter(
        SkillAssessment.student_id == student.id
    ).order_by(SkillAssessment.created_at.desc()).all()
    
    return {
        "assessments": [
            {
                "id": a.id,
                "category": a.category,
                "difficulty": a.difficulty,
                "score": a.score,
                "correct_answers": a.correct_answers,
                "total_questions": a.total_questions,
                "time_taken": a.time_taken,
                "created_at": a.created_at
            }
            for a in assessments
        ]
    }

def get_performance_message(score: float) -> str:
    """Get motivational message based on score"""
    if score >= 90:
        return "Outstanding! You're mastering this topic!"
    elif score >= 75:
        return "Great job! Keep up the excellent work!"
    elif score >= 60:
        return "Good effort! A bit more practice will make you perfect!"
    elif score >= 40:
        return "Nice try! Review the concepts and try again!"
    else:
        return "Keep learning! Practice makes perfect!"

def get_improvement_suggestions(score: float, category: str) -> list:
    """Get personalized improvement suggestions based on performance"""
    suggestions = []
    
    if score < 60:
        suggestions.append(f"Review {category} fundamentals")
        suggestions.append("Practice more questions in this category")
        suggestions.append("Watch tutorial videos on this topic")
    elif score < 80:
        suggestions.append(f"Focus on advanced {category} concepts")
        suggestions.append("Try harder difficulty questions")
        suggestions.append("Work on time management")
    else:
        suggestions.append("Excellent! Try a different category")
        suggestions.append("Challenge yourself with harder questions")
        suggestions.append("Help others learn this topic")
    
    return suggestions
