from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from ..core.database import get_db
from ..models import User, StudentProfile, Friendship
from ..schemas import FriendRequest, FriendshipResponse
from .deps import require_student

router = APIRouter(prefix="/friends", tags=["Friends"])

@router.post("/request", status_code=status.HTTP_201_CREATED)
def send_friend_request(
    request_data: FriendRequest,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Send friend request"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    # Find friend by email
    friend_user = db.query(User).filter(User.email == request_data.friend_email).first()
    if not friend_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    friend_profile = db.query(StudentProfile).filter(StudentProfile.user_id == friend_user.id).first()
    if not friend_profile:
        raise HTTPException(status_code=404, detail="Friend is not a student")
    
    # Check if already friends or request exists
    existing = db.query(Friendship).filter(
        ((Friendship.student_id == profile.id) & (Friendship.friend_id == friend_profile.id)) |
        ((Friendship.student_id == friend_profile.id) & (Friendship.friend_id == profile.id))
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Friend request already exists")
    
    # Create friendship
    friendship = Friendship(
        student_id=profile.id,
        friend_id=friend_profile.id,
        status="pending"
    )
    db.add(friendship)
    db.commit()
    
    return {"message": "Friend request sent"}

@router.get("/requests", response_model=List[dict])
def get_friend_requests(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get pending friend requests"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    requests = db.query(Friendship).filter(
        Friendship.friend_id == profile.id,
        Friendship.status == "pending"
    ).all()
    
    result = []
    for req in requests:
        sender = db.query(StudentProfile).filter(StudentProfile.id == req.student_id).first()
        sender_user = db.query(User).filter(User.id == sender.user_id).first()
        result.append({
            "id": req.id,
            "sender_name": sender.name,
            "sender_email": sender_user.email,
            "created_at": req.created_at
        })
    
    return result

@router.post("/accept/{friendship_id}")
def accept_friend_request(
    friendship_id: int,
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Accept friend request"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    friendship = db.query(Friendship).filter(
        Friendship.id == friendship_id,
        Friendship.friend_id == profile.id,
        Friendship.status == "pending"
    ).first()
    
    if not friendship:
        raise HTTPException(status_code=404, detail="Friend request not found")
    
    friendship.status = "accepted"
    
    # Award bonus XP to both users
    profile.total_xp += 10
    friend = db.query(StudentProfile).filter(StudentProfile.id == friendship.student_id).first()
    if friend:
        friend.total_xp += 10
    
    db.commit()
    
    return {"message": "Friend request accepted"}

@router.get("/list", response_model=List[dict])
def get_friends(
    current_user: User = Depends(require_student),
    db: Session = Depends(get_db)
):
    """Get list of friends"""
    profile = db.query(StudentProfile).filter(StudentProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    friendships = db.query(Friendship).filter(
        ((Friendship.student_id == profile.id) | (Friendship.friend_id == profile.id)),
        Friendship.status == "accepted"
    ).all()
    
    result = []
    for friendship in friendships:
        friend_id = friendship.friend_id if friendship.student_id == profile.id else friendship.student_id
        friend = db.query(StudentProfile).filter(StudentProfile.id == friend_id).first()
        friend_user = db.query(User).filter(User.id == friend.user_id).first()
        
        result.append({
            "id": friend.id,
            "name": friend.name,
            "email": friend_user.email,
            "college": friend.college,
            "target_role": friend.target_role,
            "placement_readiness_index": friend.placement_readiness_index,
            "current_streak": friend.current_streak,
            "tier": friend.tier
        })
    
    return result
