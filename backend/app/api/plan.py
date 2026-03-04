"""Learning plan endpoints"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.database import get_db
from ..api.deps import require_student
from ..models import User, StudentProfile, Plan, PlanTask
from ..services.plan_service import generate_7_day_plan, generate_30_day_plan, mark_task_complete

router = APIRouter(prefix="/plan", tags=["plan"])

@router.post("/generate/7-day")
def create_7_day_plan(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Generate personalized 7-day kickstart plan"""
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    # Check if already has an active 7-day plan
    existing_plan = db.query(Plan).filter(
        Plan.student_id == student.id,
        Plan.plan_type == "7_day_kickstart",
        Plan.is_active == True
    ).first()
    
    if existing_plan:
        raise HTTPException(status_code=400, detail="You already have an active 7-day plan")
    
    plan = generate_7_day_plan(db, student)
    
    return {
        "message": "7-day kickstart plan generated successfully!",
        "plan_id": plan.id,
        "plan_type": plan.plan_type,
        "total_tasks": len(plan.tasks)
    }

@router.post("/generate/30-day")
def create_30_day_plan(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Generate advanced 30-day plan (requires 7-day completion)"""
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    plan = generate_30_day_plan(db, student)
    
    if not plan:
        raise HTTPException(
            status_code=400, 
            detail="Complete your 7-day kickstart plan first to unlock the 30-day plan"
        )
    
    return {
        "message": "30-day advanced plan unlocked!",
        "plan_id": plan.id,
        "plan_type": plan.plan_type,
        "total_tasks": len(plan.tasks)
    }

@router.get("/my-plans")
def get_my_plans(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get all plans for current student"""
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    plans = db.query(Plan).filter(Plan.student_id == student.id).all()
    
    return {
        "plans": [
            {
                "id": p.id,
                "plan_type": p.plan_type,
                "is_active": p.is_active,
                "is_completed": p.is_completed,
                "started_at": p.started_at,
                "completed_at": p.completed_at,
                "tasks": [
                    {
                        "id": t.id,
                        "day": t.day,
                        "title": t.title,
                        "description": t.description,
                        "task_type": t.task_type,
                        "is_completed": t.is_completed,
                        "completed_at": t.completed_at,
                        "xp_reward": t.xp_reward
                    }
                    for t in p.tasks
                ],
                "progress": calculate_plan_progress(p)
            }
            for p in plans
        ]
    }

@router.post("/task/{task_id}/complete")
def complete_task(
    task_id: int,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Mark a task as complete"""
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    task = mark_task_complete(db, task_id, student.id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found or already completed")
    
    # Check if plan is completed
    plan = task.plan
    plan_completed = plan.is_completed
    
    db.refresh(student)
    
    response = {
        "message": "Task completed!",
        "xp_earned": task.xp_reward,
        "new_total_xp": student.total_xp,
        "tier": student.tier
    }
    
    if plan_completed:
        response["plan_completed"] = True
        response["bonus_message"] = "Congratulations! You completed the entire plan!"
        if plan.plan_type == "7_day_kickstart":
            response["unlock_message"] = "You can now unlock the 30-day advanced plan!"
    
    return response

@router.get("/task/{task_id}")
def get_task_details(
    task_id: int,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get detailed information about a specific task"""
    
    student = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    
    task = db.query(PlanTask).join(Plan).filter(
        PlanTask.id == task_id,
        Plan.student_id == student.id
    ).first()
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "id": task.id,
        "day": task.day,
        "title": task.title,
        "description": task.description,
        "task_type": task.task_type,
        "is_completed": task.is_completed,
        "completed_at": task.completed_at,
        "xp_reward": task.xp_reward,
        "plan_type": task.plan.plan_type
    }

def calculate_plan_progress(plan: Plan) -> dict:
    """Calculate plan completion progress"""
    total_tasks = len(plan.tasks)
    completed_tasks = sum(1 for t in plan.tasks if t.is_completed)
    
    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "percentage": round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
    }
