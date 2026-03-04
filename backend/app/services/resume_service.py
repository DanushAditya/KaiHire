import PyPDF2
import re
from typing import Dict, List
from io import BytesIO

def parse_resume(file_content: bytes, filename: str) -> Dict:
    """
    Simulates resume parsing logic.
    In production, you might use ML models or external APIs.
    """
    try:
        # Extract text from PDF
        pdf_reader = PyPDF2.PdfReader(BytesIO(file_content))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Simple extraction logic
        extracted_data = {
            "extracted_name": extract_name(text),
            "extracted_skills": extract_skills(text),
            "extracted_projects": extract_projects(text),
            "extracted_experience": extract_experience(text),
            "resume_quality_score": calculate_resume_quality(text)
        }
        
        return extracted_data
    except Exception as e:
        return {
            "extracted_name": None,
            "extracted_skills": [],
            "extracted_projects": [],
            "extracted_experience": [],
            "resume_quality_score": 0.0
        }

def extract_name(text: str) -> str:
    """Extract name from resume text"""
    lines = text.split('\n')
    # Assume name is in first few lines
    for line in lines[:5]:
        line = line.strip()
        if len(line) > 3 and len(line) < 50 and not any(char.isdigit() for char in line):
            return line
    return "Unknown"

def extract_skills(text: str) -> List[str]:
    """Extract skills from resume"""
    common_skills = [
        "Python", "Java", "JavaScript", "C++", "React", "Node.js", "Django",
        "FastAPI", "SQL", "MongoDB", "Machine Learning", "Deep Learning",
        "Data Structures", "Algorithms", "Git", "Docker", "AWS", "Azure",
        "HTML", "CSS", "TypeScript", "Angular", "Vue", "Flask", "PostgreSQL"
    ]
    
    found_skills = []
    text_lower = text.lower()
    
    for skill in common_skills:
        if skill.lower() in text_lower:
            found_skills.append(skill)
    
    return found_skills

def extract_projects(text: str) -> List[Dict]:
    """Extract projects from resume"""
    projects = []
    
    # Look for project section
    if "project" in text.lower():
        # Simple heuristic: find lines after "project" keyword
        lines = text.split('\n')
        in_project_section = False
        current_project = None
        
        for line in lines:
            line = line.strip()
            if "project" in line.lower() and len(line) < 50:
                in_project_section = True
                continue
            
            if in_project_section and line and len(line) > 10:
                if current_project is None or len(line) < 100:
                    current_project = {"title": line, "description": ""}
                    projects.append(current_project)
                else:
                    if current_project:
                        current_project["description"] += " " + line
                
                if len(projects) >= 3:
                    break
    
    return projects[:3]

def extract_experience(text: str) -> List[Dict]:
    """Extract experience from resume"""
    experience = []
    
    # Look for experience section
    if "experience" in text.lower() or "internship" in text.lower():
        lines = text.split('\n')
        in_exp_section = False
        current_exp = None
        
        for line in lines:
            line = line.strip()
            if ("experience" in line.lower() or "internship" in line.lower()) and len(line) < 50:
                in_exp_section = True
                continue
            
            if in_exp_section and line and len(line) > 10:
                if current_exp is None or len(line) < 100:
                    current_exp = {"role": line, "description": ""}
                    experience.append(current_exp)
                else:
                    if current_exp:
                        current_exp["description"] += " " + line
                
                if len(experience) >= 2:
                    break
    
    return experience[:2]

def calculate_resume_quality(text: str) -> float:
    """Calculate resume quality score"""
    score = 0.0
    
    # Length check
    if len(text) > 500:
        score += 20
    
    # Has contact info
    if re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text):
        score += 15
    
    # Has phone number
    if re.search(r'\b\d{10}\b', text):
        score += 10
    
    # Has sections
    sections = ["education", "experience", "project", "skill"]
    for section in sections:
        if section in text.lower():
            score += 10
    
    # Has technical skills
    if len(extract_skills(text)) > 3:
        score += 15
    
    return min(score, 100.0)
