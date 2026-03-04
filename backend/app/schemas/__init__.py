from .auth import UserRegister, UserLogin, Token, TokenData, UserResponse
from .student import (
    StudentProfileBase,
    StudentProfileUpdate,
    StudentProfileResponse,
    ResumeUploadResponse,
    SkillAssessmentCreate,
    SkillAssessmentResponse,
    PlanResponse,
    PlanTaskResponse,
    FriendRequest,
    FriendshipResponse,
)
from .challenge import (
    ChallengeResponse,
    ChallengeParticipationResponse,
    ChallengeEnroll,
    ChallengeProgressUpdate,
)

__all__ = [
    "UserRegister",
    "UserLogin",
    "Token",
    "TokenData",
    "UserResponse",
    "StudentProfileBase",
    "StudentProfileUpdate",
    "StudentProfileResponse",
    "ResumeUploadResponse",
    "SkillAssessmentCreate",
    "SkillAssessmentResponse",
    "PlanResponse",
    "PlanTaskResponse",
    "FriendRequest",
    "FriendshipResponse",
    "ChallengeResponse",
    "ChallengeParticipationResponse",
    "ChallengeEnroll",
    "ChallengeProgressUpdate",
]
