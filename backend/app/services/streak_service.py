from sqlalchemy.orm import Session
from ..models import StudentProfile
from datetime import datetime, timedelta

def update_streak(db: Session, student_id: int):
    """Update student's daily streak"""
    
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not student:
        return
    
    now = datetime.utcnow()
    last_activity = student.last_activity_date
    
    if last_activity is None:
        # First activity
        student.current_streak = 1
        student.longest_streak = 1
        student.last_activity_date = now
    else:
        # Check if activity is on a different day
        days_diff = (now.date() - last_activity.date()).days
        
        if days_diff == 0:
            # Same day, no change
            pass
        elif days_diff == 1:
            # Consecutive day
            student.current_streak += 1
            if student.current_streak > student.longest_streak:
                student.longest_streak = student.current_streak
            student.last_activity_date = now
        else:
            # Streak broken
            student.current_streak = 1
            student.last_activity_date = now
    
    db.commit()

def check_streak_milestone(student: StudentProfile) -> dict:
    """Check if student reached streak milestone"""
    
    milestones = {
        7: {"reward": "7-Day Warrior", "xp": 50},
        30: {"reward": "Monthly Champion", "xp": 200},
        100: {"reward": "Centurion", "xp": 500}
    }
    
    if student.current_streak in milestones:
        return milestones[student.current_streak]
    
    return None
