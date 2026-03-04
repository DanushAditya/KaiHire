from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import engine, Base
from .api import auth, student, leaderboard, hr, assessment, card, plan, ai

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="KaiHire API",
    description="AI Placement Copilot & Talent Radar",
    version="1.0.0"
)

# CORS middleware - must be added before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Include routers
app.include_router(auth.router)
app.include_router(student.router)
app.include_router(leaderboard.router)
app.include_router(hr.router)
app.include_router(assessment.router)
app.include_router(card.router)
app.include_router(plan.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {
        "message": "Welcome to KaiHire API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}
