from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from typing import List, Optional
from ..core.database import get_db
from ..models import User, StudentProfile, HRProfile
from .deps import require_hr
import csv
import io

router = APIRouter(prefix="/hr", tags=["HR"])

@router.get("/profile")
def get_hr_profile(
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """Get HR profile"""
    profile = db.query(HRProfile).filter(HRProfile.user_id == current_user.id).first()
    if not profile:
        return {"error": "Profile not found"}
    
    return {
        "id": profile.id,
        "name": profile.name,
        "company": profile.company,
        "designation": profile.designation,
        "phone": profile.phone
    }

@router.get("/students")
def filter_students(
    college: Optional[str] = Query(None),
    branch: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    min_pri: Optional[float] = Query(None),
    target_role: Optional[str] = Query(None),
    min_sli: Optional[float] = Query(None),
    limit: int = Query(100, le=500),
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """Filter and search students"""
    query = db.query(StudentProfile)
    
    if college:
        query = query.filter(StudentProfile.college.ilike(f"%{college}%"))
    if branch:
        query = query.filter(StudentProfile.branch.ilike(f"%{branch}%"))
    if year:
        query = query.filter(StudentProfile.year == year)
    if min_pri:
        query = query.filter(StudentProfile.placement_readiness_index >= min_pri)
    if target_role:
        query = query.filter(StudentProfile.target_role.ilike(f"%{target_role}%"))
    if min_sli:
        query = query.filter(StudentProfile.skill_level_index >= min_sli)
    
    students = query.order_by(desc(StudentProfile.placement_readiness_index)).limit(limit).all()
    
    result = []
    for student in students:
        user = db.query(User).filter(User.id == student.user_id).first()
        result.append({
            "id": student.id,
            "name": student.name,
            "email": user.email if user else None,
            "college": student.college,
            "branch": student.branch,
            "year": student.year,
            "target_role": student.target_role,
            "placement_readiness_index": student.placement_readiness_index,
            "skill_level_index": student.skill_level_index,
            "current_streak": student.current_streak,
            "tier": student.tier,
            "skills": student.skills
        })
    
    return result

@router.get("/student/{student_id}")
def get_student_detail(
    student_id: int,
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """Get detailed student information"""
    student = db.query(StudentProfile).filter(StudentProfile.id == student_id).first()
    if not student:
        return {"error": "Student not found"}
    
    user = db.query(User).filter(User.id == student.user_id).first()
    
    return {
        "id": student.id,
        "name": student.name,
        "email": user.email if user else None,
        "college": student.college,
        "branch": student.branch,
        "year": student.year,
        "section": student.section,
        "target_role": student.target_role,
        "available_hours": student.available_hours,
        "skills": student.skills,
        "placement_readiness_index": student.placement_readiness_index,
        "skill_level_index": student.skill_level_index,
        "current_streak": student.current_streak,
        "longest_streak": student.longest_streak,
        "total_xp": student.total_xp,
        "tier": student.tier
    }

@router.get("/analytics")
def get_analytics(
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """Get analytics dashboard data"""
    
    # Total students
    total_students = db.query(func.count(StudentProfile.id)).scalar()
    
    # Average PRI
    avg_pri = db.query(func.avg(StudentProfile.placement_readiness_index)).scalar() or 0
    
    # Average streak
    avg_streak = db.query(func.avg(StudentProfile.current_streak)).scalar() or 0
    
    # Top colleges
    top_colleges = db.query(
        StudentProfile.college,
        func.count(StudentProfile.id).label('count')
    ).group_by(StudentProfile.college).order_by(desc('count')).limit(10).all()
    
    # Skill distribution
    skill_dist = {}
    students = db.query(StudentProfile).all()
    for student in students:
        for skill in student.skills:
            skill_dist[skill] = skill_dist.get(skill, 0) + 1
    
    # Top skills
    top_skills = sorted(skill_dist.items(), key=lambda x: x[1], reverse=True)[:10]
    
    # Tier distribution
    tier_dist = db.query(
        StudentProfile.tier,
        func.count(StudentProfile.id).label('count')
    ).group_by(StudentProfile.tier).all()
    
    return {
        "total_students": total_students,
        "average_pri": round(avg_pri, 2),
        "average_streak": round(avg_streak, 2),
        "top_colleges": [{"college": c[0], "count": c[1]} for c in top_colleges],
        "top_skills": [{"skill": s[0], "count": s[1]} for s in top_skills],
        "tier_distribution": [{"tier": t[0], "count": t[1]} for t in tier_dist]
    }

@router.get("/export")
def export_students(
    college: Optional[str] = Query(None),
    branch: Optional[str] = Query(None),
    year: Optional[int] = Query(None),
    min_pri: Optional[float] = Query(None),
    current_user: User = Depends(require_hr),
    db: Session = Depends(get_db)
):
    """Export students to CSV"""
    query = db.query(StudentProfile)
    
    if college:
        query = query.filter(StudentProfile.college.ilike(f"%{college}%"))
    if branch:
        query = query.filter(StudentProfile.branch.ilike(f"%{branch}%"))
    if year:
        query = query.filter(StudentProfile.year == year)
    if min_pri:
        query = query.filter(StudentProfile.placement_readiness_index >= min_pri)
    
    students = query.order_by(desc(StudentProfile.placement_readiness_index)).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Header
    writer.writerow([
        "Name", "Email", "College", "Branch", "Year", "Target Role",
        "PRI", "SLI", "Streak", "Tier", "Skills"
    ])
    
    # Data
    for student in students:
        user = db.query(User).filter(User.id == student.user_id).first()
        writer.writerow([
            student.name,
            user.email if user else "",
            student.college,
            student.branch,
            student.year,
            student.target_role,
            student.placement_readiness_index,
            student.skill_level_index,
            student.current_streak,
            student.tier,
            ", ".join(student.skills)
        ])
    
    output.seek(0)
    
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=students.csv"}
    )
