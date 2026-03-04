from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List
from ..core.database import get_db
from ..models import StudentProfile

router = APIRouter(prefix="/leaderboard", tags=["Leaderboard"])

@router.get("/class")
def get_class_leaderboard(
    college: str = Query(...),
    branch: str = Query(...),
    year: int = Query(...),
    section: str = Query(None),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db)
):
    """Get class leaderboard"""
    query = db.query(StudentProfile).filter(
        StudentProfile.college == college,
        StudentProfile.branch == branch,
        StudentProfile.year == year
    )
    
    if section:
        query = query.filter(StudentProfile.section == section)
    
    students = query.order_by(desc(StudentProfile.placement_readiness_index)).limit(limit).all()
    
    result = []
    for idx, student in enumerate(students, 1):
        result.append({
            "rank": idx,
            "name": student.name,
            "target_role": student.target_role,
            "placement_readiness_index": student.placement_readiness_index,
            "skill_level_index": student.skill_level_index,
            "current_streak": student.current_streak,
            "tier": student.tier,
            "total_xp": student.total_xp
        })
    
    return result

@router.get("/branch")
def get_branch_leaderboard(
    college: str = Query(...),
    branch: str = Query(...),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db)
):
    """Get branch leaderboard"""
    students = db.query(StudentProfile).filter(
        StudentProfile.college == college,
        StudentProfile.branch == branch
    ).order_by(desc(StudentProfile.placement_readiness_index)).limit(limit).all()
    
    result = []
    for idx, student in enumerate(students, 1):
        result.append({
            "rank": idx,
            "name": student.name,
            "year": student.year,
            "target_role": student.target_role,
            "placement_readiness_index": student.placement_readiness_index,
            "skill_level_index": student.skill_level_index,
            "current_streak": student.current_streak,
            "tier": student.tier
        })
    
    return result

@router.get("/college")
def get_college_leaderboard(
    college: str = Query(...),
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db)
):
    """Get college leaderboard"""
    students = db.query(StudentProfile).filter(
        StudentProfile.college == college
    ).order_by(desc(StudentProfile.placement_readiness_index)).limit(limit).all()
    
    result = []
    for idx, student in enumerate(students, 1):
        result.append({
            "rank": idx,
            "name": student.name,
            "branch": student.branch,
            "year": student.year,
            "target_role": student.target_role,
            "placement_readiness_index": student.placement_readiness_index,
            "skill_level_index": student.skill_level_index,
            "current_streak": student.current_streak,
            "tier": student.tier
        })
    
    return result
