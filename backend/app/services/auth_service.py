from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from ..models import User, UserRole, StudentProfile, HRProfile
from ..schemas import UserRegister
from ..core.security import get_password_hash, verify_password
import secrets

def create_user(db: Session, user_data: UserRegister) -> User:
    # Check if user exists
    existing_user = db.query(User).filter(User.email == user_data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        email=user_data.email,
        hashed_password=get_password_hash(user_data.password),
        role=user_data.role
    )
    db.add(user)
    db.flush()
    
    # Create profile based on role
    if user_data.role == UserRole.STUDENT:
        if not all([user_data.college, user_data.year, user_data.branch, user_data.target_role]):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Student registration requires college, year, branch, and target_role"
            )
        
        referral_code = secrets.token_urlsafe(8)
        initial_xp = 0
        
        # Process referral code if provided
        if user_data.referral_code:
            from ..services.card_service import process_referral_on_signup
            initial_xp = process_referral_on_signup(db, user_data.referral_code)
        
        student_profile = StudentProfile(
            user_id=user.id,
            name=user_data.name,
            college=user_data.college,
            year=user_data.year,
            branch=user_data.branch,
            target_role=user_data.target_role,
            referral_code=referral_code,
            total_xp=initial_xp
        )
        db.add(student_profile)
    
    elif user_data.role == UserRole.HR:
        if not user_data.company:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="HR registration requires company"
            )
        
        hr_profile = HRProfile(
            user_id=user.id,
            name=user_data.name,
            company=user_data.company,
            designation=user_data.designation
        )
        db.add(hr_profile)
    
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    return user

def get_user_by_email(db: Session, email: str) -> User:
    return db.query(User).filter(User.email == email).first()
