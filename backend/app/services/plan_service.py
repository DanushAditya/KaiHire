from sqlalchemy.orm import Session
from ..models import Plan, PlanTask, StudentProfile
from datetime import datetime

def generate_7_day_plan(db: Session, student: StudentProfile) -> Plan:
    """Generate personalized 7-day kickstart plan"""
    
    # Create plan
    plan = Plan(
        student_id=student.id,
        plan_type="7_day_kickstart",
        is_active=True
    )
    db.add(plan)
    db.flush()
    
    # Generate tasks based on target role
    tasks = get_tasks_for_role(student.target_role, plan.id, "7_day")
    
    for task in tasks:
        db.add(task)
    
    db.commit()
    db.refresh(plan)
    return plan

def generate_30_day_plan(db: Session, student: StudentProfile) -> Plan:
    """Generate advanced 30-day plan"""
    
    # Check if 7-day plan is completed
    seven_day_plan = db.query(Plan).filter(
        Plan.student_id == student.id,
        Plan.plan_type == "7_day_kickstart",
        Plan.is_completed == True
    ).first()
    
    if not seven_day_plan:
        return None
    
    # Create plan
    plan = Plan(
        student_id=student.id,
        plan_type="30_day_advanced",
        is_active=True
    )
    db.add(plan)
    db.flush()
    
    # Generate advanced tasks
    tasks = get_tasks_for_role(student.target_role, plan.id, "30_day")
    
    for task in tasks:
        db.add(task)
    
    db.commit()
    db.refresh(plan)
    return plan

def get_tasks_for_role(target_role: str, plan_id: int, plan_type: str) -> list:
    """Generate tasks based on target role"""
    
    tasks = []
    
    if plan_type == "7_day":
        if "SDE" in target_role.upper() or "SOFTWARE" in target_role.upper():
            tasks = [
                PlanTask(plan_id=plan_id, day=1, title="Complete DSA Basics Assessment", 
                        description="Test your knowledge on arrays and strings", task_type="assessment", xp_reward=20),
                PlanTask(plan_id=plan_id, day=2, title="Solve 5 Easy Problems", 
                        description="Practice basic problem solving", task_type="practice", xp_reward=15),
                PlanTask(plan_id=plan_id, day=3, title="Learn Time Complexity", 
                        description="Understand Big O notation", task_type="practice", xp_reward=15),
                PlanTask(plan_id=plan_id, day=4, title="Complete Sorting Assessment", 
                        description="Test sorting algorithms knowledge", task_type="assessment", xp_reward=20),
                PlanTask(plan_id=plan_id, day=5, title="Build Mini Project", 
                        description="Create a simple web app", task_type="practice", xp_reward=25),
                PlanTask(plan_id=plan_id, day=6, title="System Design Basics", 
                        description="Learn fundamental concepts", task_type="practice", xp_reward=20),
                PlanTask(plan_id=plan_id, day=7, title="Mock Interview Practice", 
                        description="Complete a mock coding round", task_type="challenge", xp_reward=30),
            ]
        elif "ML" in target_role.upper() or "DATA" in target_role.upper():
            tasks = [
                PlanTask(plan_id=plan_id, day=1, title="Python Basics Assessment", 
                        description="Test Python fundamentals", task_type="assessment", xp_reward=20),
                PlanTask(plan_id=plan_id, day=2, title="Learn NumPy & Pandas", 
                        description="Data manipulation basics", task_type="practice", xp_reward=15),
                PlanTask(plan_id=plan_id, day=3, title="Statistics Fundamentals", 
                        description="Probability and statistics", task_type="practice", xp_reward=15),
                PlanTask(plan_id=plan_id, day=4, title="ML Algorithms Assessment", 
                        description="Test ML concepts", task_type="assessment", xp_reward=20),
                PlanTask(plan_id=plan_id, day=5, title="Build Classification Model", 
                        description="Create a simple classifier", task_type="practice", xp_reward=25),
                PlanTask(plan_id=plan_id, day=6, title="Data Visualization", 
                        description="Learn matplotlib and seaborn", task_type="practice", xp_reward=20),
                PlanTask(plan_id=plan_id, day=7, title="Complete ML Project", 
                        description="End-to-end ML pipeline", task_type="challenge", xp_reward=30),
            ]
        else:
            # Generic plan
            tasks = [
                PlanTask(plan_id=plan_id, day=1, title="Profile Setup", 
                        description="Complete your profile", task_type="practice", xp_reward=10),
                PlanTask(plan_id=plan_id, day=2, title="Skill Assessment", 
                        description="Take initial assessment", task_type="assessment", xp_reward=20),
                PlanTask(plan_id=plan_id, day=3, title="Learn Core Concepts", 
                        description="Study fundamentals", task_type="practice", xp_reward=15),
                PlanTask(plan_id=plan_id, day=4, title="Practice Problems", 
                        description="Solve practice questions", task_type="practice", xp_reward=15),
                PlanTask(plan_id=plan_id, day=5, title="Build Project", 
                        description="Create a small project", task_type="practice", xp_reward=25),
                PlanTask(plan_id=plan_id, day=6, title="Advanced Topics", 
                        description="Explore advanced concepts", task_type="practice", xp_reward=20),
                PlanTask(plan_id=plan_id, day=7, title="Final Challenge", 
                        description="Complete comprehensive test", task_type="challenge", xp_reward=30),
            ]
    
    return tasks

def mark_task_complete(db: Session, task_id: int, student_id: int) -> PlanTask:
    """Mark a task as complete and award XP"""
    
    task = db.query(PlanTask).join(Plan).filter(
        PlanTask.id == task_id,
        Plan.student_id == student_id
    ).first()
    
    if not task or task.is_completed:
        return None
    
    task.is_completed = True
    task.completed_at = datetime.utcnow()
    
    # Award XP to student
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if student:
        student.total_xp += task.xp_reward
    
    # Check if plan is completed
    plan = task.plan
    all_tasks = db.query(PlanTask).filter(PlanTask.plan_id == plan.id).all()
    if all(t.is_completed for t in all_tasks):
        plan.is_completed = True
        plan.completed_at = datetime.utcnow()
    
    db.commit()
    db.refresh(task)
    return task
