"""Seed script to populate question bank for assessments"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.database import SessionLocal
from app.models import Question

def seed_questions():
    db = SessionLocal()
    
    # DSA Questions for SDE role
    dsa_questions = [
        # Easy
        {
            "category": "DSA",
            "role": "SDE",
            "difficulty": "easy",
            "question_text": "What is the time complexity of accessing an element in an array by index?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
            "correct_answer": 0,
            "explanation": "Array access by index is constant time O(1) operation",
            "points": 10
        },
        {
            "category": "DSA",
            "role": "SDE",
            "difficulty": "easy",
            "question_text": "Which data structure uses LIFO (Last In First Out) principle?",
            "options": ["Queue", "Stack", "Array", "Linked List"],
            "correct_answer": 1,
            "explanation": "Stack follows LIFO principle",
            "points": 10
        },
        {
            "category": "DSA",
            "role": "SDE",
            "difficulty": "easy",
            "question_text": "What is the best case time complexity of Binary Search?",
            "options": ["O(1)", "O(log n)", "O(n)", "O(n log n)"],
            "correct_answer": 0,
            "explanation": "Best case is when element is found at middle in first comparison",
            "points": 10
        },
        
        # Medium
        {
            "category": "DSA",
            "role": "SDE",
            "difficulty": "medium",
            "question_text": "What is the time complexity of QuickSort in average case?",
            "options": ["O(n)", "O(n log n)", "O(n^2)", "O(log n)"],
            "correct_answer": 1,
            "explanation": "QuickSort has O(n log n) average case complexity",
            "points": 15
        },
        {
            "category": "DSA",
            "role": "SDE",
            "difficulty": "medium",
            "question_text": "Which algorithm is used to find shortest path in weighted graph?",
            "options": ["BFS", "DFS", "Dijkstra's", "Binary Search"],
            "correct_answer": 2,
            "explanation": "Dijkstra's algorithm finds shortest path in weighted graphs",
            "points": 15
        },
        {
            "category": "DSA",
            "role": "SDE",
            "difficulty": "medium",
            "question_text": "What is the space complexity of recursive Fibonacci?",
            "options": ["O(1)", "O(n)", "O(log n)", "O(n^2)"],
            "correct_answer": 1,
            "explanation": "Recursive Fibonacci uses O(n) space for call stack",
            "points": 15
        },
        
        # Hard
        {
            "category": "DSA",
            "role": "SDE",
            "difficulty": "hard",
            "question_text": "What is the time complexity of finding LCA in a Binary Tree using Tarjan's algorithm?",
            "options": ["O(n)", "O(log n)", "O(n log n)", "O(1)"],
            "correct_answer": 0,
            "explanation": "Tarjan's LCA algorithm runs in O(n) time",
            "points": 20
        },
        {
            "category": "DSA",
            "role": "SDE",
            "difficulty": "hard",
            "question_text": "Which data structure is best for implementing LRU Cache?",
            "options": ["Array", "HashMap + Doubly Linked List", "Binary Tree", "Stack"],
            "correct_answer": 1,
            "explanation": "LRU Cache is efficiently implemented using HashMap and Doubly Linked List",
            "points": 20
        },
    ]
    
    # Python/Programming Questions
    python_questions = [
        {
            "category": "Python",
            "role": "ML",
            "difficulty": "easy",
            "question_text": "Which of the following is mutable in Python?",
            "options": ["Tuple", "String", "List", "Integer"],
            "correct_answer": 2,
            "explanation": "Lists are mutable in Python",
            "points": 10
        },
        {
            "category": "Python",
            "role": "ML",
            "difficulty": "easy",
            "question_text": "What is the output of: print(type([]))?",
            "options": ["<class 'tuple'>", "<class 'list'>", "<class 'dict'>", "<class 'set'>"],
            "correct_answer": 1,
            "explanation": "[] creates an empty list",
            "points": 10
        },
        {
            "category": "Python",
            "role": "ML",
            "difficulty": "medium",
            "question_text": "What is a decorator in Python?",
            "options": [
                "A function that modifies another function",
                "A class method",
                "A type of loop",
                "A data structure"
            ],
            "correct_answer": 0,
            "explanation": "Decorators are functions that modify the behavior of other functions",
            "points": 15
        },
        {
            "category": "Python",
            "role": "ML",
            "difficulty": "medium",
            "question_text": "What is the difference between '==' and 'is' in Python?",
            "options": [
                "No difference",
                "== checks value, is checks identity",
                "is checks value, == checks identity",
                "Both check identity"
            ],
            "correct_answer": 1,
            "explanation": "== compares values, is compares object identity",
            "points": 15
        },
    ]
    
    # Machine Learning Questions
    ml_questions = [
        {
            "category": "Machine Learning",
            "role": "ML",
            "difficulty": "easy",
            "question_text": "What is supervised learning?",
            "options": [
                "Learning without labels",
                "Learning with labeled data",
                "Reinforcement learning",
                "Unsupervised clustering"
            ],
            "correct_answer": 1,
            "explanation": "Supervised learning uses labeled training data",
            "points": 10
        },
        {
            "category": "Machine Learning",
            "role": "ML",
            "difficulty": "medium",
            "question_text": "What is overfitting in machine learning?",
            "options": [
                "Model performs well on training and test data",
                "Model performs poorly on both training and test data",
                "Model performs well on training but poorly on test data",
                "Model performs poorly on training but well on test data"
            ],
            "correct_answer": 2,
            "explanation": "Overfitting occurs when model memorizes training data but fails to generalize",
            "points": 15
        },
        {
            "category": "Machine Learning",
            "role": "ML",
            "difficulty": "medium",
            "question_text": "Which algorithm is used for classification?",
            "options": ["Linear Regression", "Logistic Regression", "K-Means", "PCA"],
            "correct_answer": 1,
            "explanation": "Logistic Regression is a classification algorithm",
            "points": 15
        },
        {
            "category": "Machine Learning",
            "role": "ML",
            "difficulty": "hard",
            "question_text": "What is the vanishing gradient problem?",
            "options": [
                "Gradients become too large",
                "Gradients become very small in deep networks",
                "No gradients are computed",
                "Gradients are always zero"
            ],
            "correct_answer": 1,
            "explanation": "Vanishing gradient problem occurs when gradients become very small in deep networks",
            "points": 20
        },
    ]
    
    # Web Development Questions
    web_questions = [
        {
            "category": "Web Development",
            "role": "SDE",
            "difficulty": "easy",
            "question_text": "What does HTTP stand for?",
            "options": [
                "HyperText Transfer Protocol",
                "High Transfer Text Protocol",
                "HyperText Transmission Protocol",
                "High Text Transfer Protocol"
            ],
            "correct_answer": 0,
            "explanation": "HTTP stands for HyperText Transfer Protocol",
            "points": 10
        },
        {
            "category": "Web Development",
            "role": "SDE",
            "difficulty": "medium",
            "question_text": "What is REST API?",
            "options": [
                "A database",
                "An architectural style for web services",
                "A programming language",
                "A frontend framework"
            ],
            "correct_answer": 1,
            "explanation": "REST is an architectural style for designing web services",
            "points": 15
        },
        {
            "category": "Web Development",
            "role": "SDE",
            "difficulty": "medium",
            "question_text": "What is the purpose of CORS?",
            "options": [
                "To style web pages",
                "To allow cross-origin requests",
                "To compress data",
                "To encrypt data"
            ],
            "correct_answer": 1,
            "explanation": "CORS (Cross-Origin Resource Sharing) allows cross-origin HTTP requests",
            "points": 15
        },
    ]
    
    # Database Questions
    db_questions = [
        {
            "category": "Database",
            "role": "SDE",
            "difficulty": "easy",
            "question_text": "What does SQL stand for?",
            "options": [
                "Structured Query Language",
                "Simple Query Language",
                "Standard Query Language",
                "System Query Language"
            ],
            "correct_answer": 0,
            "explanation": "SQL stands for Structured Query Language",
            "points": 10
        },
        {
            "category": "Database",
            "role": "SDE",
            "difficulty": "medium",
            "question_text": "What is a primary key?",
            "options": [
                "A key that can be null",
                "A unique identifier for a record",
                "A foreign key reference",
                "An index"
            ],
            "correct_answer": 1,
            "explanation": "Primary key uniquely identifies each record in a table",
            "points": 15
        },
        {
            "category": "Database",
            "role": "SDE",
            "difficulty": "medium",
            "question_text": "What is normalization in databases?",
            "options": [
                "Backing up data",
                "Organizing data to reduce redundancy",
                "Encrypting data",
                "Indexing data"
            ],
            "correct_answer": 1,
            "explanation": "Normalization organizes data to minimize redundancy",
            "points": 15
        },
    ]
    
    # Combine all questions
    all_questions = (
        dsa_questions + 
        python_questions + 
        ml_questions + 
        web_questions + 
        db_questions
    )
    
    # Add questions to database
    for q_data in all_questions:
        question = Question(**q_data)
        db.add(question)
    
    db.commit()
    print(f"✓ Seeded {len(all_questions)} questions successfully!")
    db.close()

if __name__ == "__main__":
    print("Seeding question bank...")
    seed_questions()
    print("Done!")
