from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models.user import UserRole

class UserRegister(BaseModel):
    email: EmailStr
    password: str
    role: UserRole
    name: str
    
    # Student specific
    college: Optional[str] = None
    year: Optional[int] = None
    branch: Optional[str] = None
    target_role: Optional[str] = None
    referral_code: Optional[str] = None
    
    # HR specific
    company: Optional[str] = None
    designation: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = None

class UserResponse(BaseModel):
    id: int
    email: str
    role: UserRole
    is_active: bool
    
    class Config:
        from_attributes = True
