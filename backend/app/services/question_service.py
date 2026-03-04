"""Service for managing assessment questions"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Dict
from ..models import Question
import random

class QuestionService:
    """Handles question retrieval and adaptive difficulty"""
    
    @staticmethod
    def get_questions_for_assessment(
        db: Session,
        category: str,
        role: str,
        difficulty: str = "medium",
        count: int = 10
    ) -> List[Question]:
        """Get random questions for assessment"""
        questions = db.query(Question).filter(
            Question.category == category,
            Question.role == role,
            Question.difficulty == difficulty,
            Question.is_active == True
        ).all()
        
        # Return random sample
        if len(questions) > count:
            return random.sample(questions, count)
        return questions
    
    @staticmethod
    def get_adaptive_questions(
        db: Session,
        category: str,
        role: str,
        previous_score: float = None,
        count: int = 10
    ) -> List[Question]:
        """Get randomized questions with adaptive difficulty based on previous performance"""
        
        # Determine difficulty based on previous score
        if previous_score is None:
            difficulty = "medium"
        elif previous_score >= 80:
            difficulty = "hard"
        elif previous_score >= 50:
            difficulty = "medium"
        else:
            difficulty = "easy"
        
        # Try exact match first with random ordering
        questions = db.query(Question).filter(
            Question.category == category,
            Question.role == role,
            Question.difficulty == difficulty,
            Question.is_active == True
        ).order_by(func.random()).limit(count).all()
        
        # If no exact match, try with just category (randomized)
        if not questions:
            questions = db.query(Question).filter(
                Question.category == category,
                Question.difficulty == difficulty,
                Question.is_active == True
            ).order_by(func.random()).limit(count).all()
        
        # If still no match, try with just role (randomized)
        if not questions:
            questions = db.query(Question).filter(
                Question.role == role,
                Question.difficulty == difficulty,
                Question.is_active == True
            ).order_by(func.random()).limit(count).all()
        
        # If still no match, return any questions with that difficulty (randomized)
        if not questions:
            questions = db.query(Question).filter(
                Question.difficulty == difficulty,
                Question.is_active == True
            ).order_by(func.random()).limit(count).all()
        
        # Last resort: return any active questions (randomized)
        if not questions:
            questions = db.query(Question).filter(
                Question.is_active == True
            ).order_by(func.random()).limit(count).all()
        
        return questions
    
    @staticmethod
    def calculate_assessment_score(
        answers: Dict[int, int],
        questions: List[Question]
    ) -> Dict:
        """Calculate score from user answers"""
        correct = 0
        total = len(questions)
        
        for question in questions:
            # Handle both string and int keys from frontend
            user_answer = answers.get(str(question.id)) or answers.get(question.id)
            if user_answer is not None and user_answer == question.correct_answer:
                correct += 1
        
        score = (correct / total * 100) if total > 0 else 0
        
        return {
            "score": round(score, 2),
            "correct": correct,
            "total": total,
            "percentage": round(score, 2)
        }
