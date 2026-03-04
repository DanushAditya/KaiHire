"""
Seed script to populate database with sample data
Run with: python seed_data.py
"""
from app.core.database import SessionLocal, engine, Base
from app.models import User, UserRole, StudentProfile, Challenge, Question
from app.core.security import get_password_hash
import secrets

def seed_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Create sample challenges
        challenges = [
            Challenge(
                title="DSA Sprint - 7 Days",
                description="Master data structures and algorithms in 7 days",
                challenge_type="DSA_SPRINT",
                duration_days=7,
                xp_reward=150,
                pri_boost=10,
                difficulty="intermediate",
                is_active=True
            ),
            Challenge(
                title="ML Fundamentals Sprint",
                description="Learn machine learning basics in one week",
                challenge_type="ML_SPRINT",
                duration_days=7,
                xp_reward=150,
                pri_boost=10,
                difficulty="intermediate",
                is_active=True
            ),
            Challenge(
                title="Core Engineering Concepts",
                description="Strengthen your core engineering knowledge",
                challenge_type="CORE_SPRINT",
                duration_days=7,
                xp_reward=150,
                pri_boost=10,
                difficulty="intermediate",
                is_active=True
            ),
        ]
        
        for challenge in challenges:
            existing = db.query(Challenge).filter(Challenge.title == challenge.title).first()
            if not existing:
                db.add(challenge)
        
        # Create sample questions
        questions = [
            Question(
                category="DSA",
                difficulty="easy",
                question_text="What is the time complexity of binary search?",
                options=["O(n)", "O(log n)", "O(n^2)", "O(1)"],
                correct_answer=1,
                explanation="Binary search divides the search space in half each time",
                tags=["algorithms", "complexity"]
            ),
            Question(
                category="DSA",
                difficulty="medium",
                question_text="Which data structure uses LIFO principle?",
                options=["Queue", "Stack", "Tree", "Graph"],
                correct_answer=1,
                explanation="Stack follows Last In First Out principle",
                tags=["data-structures"]
            ),
            Question(
                category="ML",
                difficulty="easy",
                question_text="What is supervised learning?",
                options=[
                    "Learning without labels",
                    "Learning with labeled data",
                    "Reinforcement learning",
                    "Unsupervised clustering"
                ],
                correct_answer=1,
                explanation="Supervised learning uses labeled training data",
                tags=["machine-learning", "basics"]
            ),
        ]
        
        for question in questions:
            existing = db.query(Question).filter(
                Question.question_text == question.question_text
            ).first()
            if not existing:
                db.add(question)
        
        db.commit()
        print("✓ Database seeded successfully!")
        print("✓ Created sample challenges")
        print("✓ Created sample questions")
        
    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
