"""
AI Service using Ollama for advanced features
Provides intelligent resume analysis, personalized recommendations, and more
"""

import ollama
from typing import Dict, List, Optional
import json
from ..core.config import settings

class AIService:
    """Service for AI-powered features using Ollama"""
    
    def __init__(self):
        self.enabled = getattr(settings, 'OLLAMA_ENABLED', 'True').lower() == 'true'
        self.model = getattr(settings, 'OLLAMA_MODEL', 'llama2')
        self.base_url = getattr(settings, 'OLLAMA_BASE_URL', 'http://localhost:11434')
    
    def _generate(self, prompt: str, system_prompt: str = None) -> str:
        """Generate response from Ollama"""
        if not self.enabled:
            return self._fallback_response(prompt)
        
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            response = ollama.chat(
                model=self.model,
                messages=messages
            )
            return response['message']['content']
        except Exception as e:
            print(f"Ollama error: {e}")
            return self._fallback_response(prompt)
    
    def _fallback_response(self, prompt: str) -> str:
        """Fallback when Ollama is not available"""
        return "AI service temporarily unavailable. Using rule-based analysis."
    
    def analyze_resume_advanced(self, resume_data: Dict) -> Dict:
        """
        Advanced resume analysis using AI
        Provides detailed insights, suggestions, and scoring
        """
        system_prompt = """You are an expert career counselor and resume analyst. 
        Analyze resumes and provide actionable feedback to help students improve their job prospects.
        Be specific, constructive, and encouraging."""
        
        prompt = f"""Analyze this student's resume and provide detailed feedback:

Name: {resume_data.get('extracted_name', 'Not provided')}
Skills: {', '.join(resume_data.get('extracted_skills', []))}
Projects: {len(resume_data.get('extracted_projects', []))} projects
Experience: {len(resume_data.get('extracted_experience', []))} experiences

Provide analysis in this JSON format:
{{
    "overall_score": <0-100>,
    "strengths": [<list of 3-5 specific strengths>],
    "improvements": [<list of 3-5 specific improvements>],
    "missing_skills": [<list of recommended skills to add>],
    "ats_score": <0-100, how well it passes ATS systems>,
    "recommendations": [<list of 3-5 actionable recommendations>]
}}"""
        
        response = self._generate(prompt, system_prompt)
        
        try:
            # Try to parse JSON response
            analysis = json.loads(response)
        except:
            # Fallback to rule-based analysis
            analysis = self._rule_based_resume_analysis(resume_data)
        
        return analysis
    
    def _rule_based_resume_analysis(self, resume_data: Dict) -> Dict:
        """Rule-based fallback for resume analysis"""
        skills = resume_data.get('extracted_skills', [])
        projects = resume_data.get('extracted_projects', [])
        experience = resume_data.get('extracted_experience', [])
        
        score = min(100, len(skills) * 3 + len(projects) * 10 + len(experience) * 15)
        
        strengths = []
        if len(skills) >= 10:
            strengths.append("Strong technical skill set")
        if len(projects) >= 3:
            strengths.append("Good project portfolio")
        if len(experience) >= 2:
            strengths.append("Relevant work experience")
        
        improvements = []
        if len(skills) < 8:
            improvements.append("Add more technical skills")
        if len(projects) < 2:
            improvements.append("Include more projects")
        if not experience:
            improvements.append("Add internship or work experience")
        
        return {
            "overall_score": score,
            "strengths": strengths or ["Resume uploaded successfully"],
            "improvements": improvements or ["Keep building your profile"],
            "missing_skills": ["Cloud Computing", "System Design", "Testing"],
            "ats_score": 75,
            "recommendations": [
                "Quantify achievements with numbers",
                "Use action verbs in descriptions",
                "Tailor resume for target role"
            ]
        }
    
    def generate_personalized_plan(self, student_data: Dict) -> Dict:
        """
        Generate AI-powered personalized learning plan
        Based on student's profile, goals, and weak areas
        """
        system_prompt = """You are an expert career coach specializing in tech placements.
        Create personalized, actionable learning plans for students based on their profile."""
        
        prompt = f"""Create a personalized 7-day learning plan for this student:

Target Role: {student_data.get('target_role', 'SDE')}
Current Skills: {', '.join(student_data.get('skills', []))}
Available Hours/Week: {student_data.get('available_hours', 10)}
Current PRI Score: {student_data.get('pri_score', 0)}
Weak Areas: {', '.join(student_data.get('weak_areas', ['DSA', 'System Design']))}

Create a JSON response with 7 days of tasks:
{{
    "plan_title": "<motivating title>",
    "plan_description": "<brief description>",
    "days": [
        {{
            "day": 1,
            "title": "<task title>",
            "description": "<detailed description>",
            "duration_hours": <1-3>,
            "resources": ["<resource 1>", "<resource 2>"],
            "success_criteria": "<how to know you completed it>"
        }}
    ]
}}"""
        
        response = self._generate(prompt, system_prompt)
        
        try:
            plan = json.loads(response)
        except:
            plan = self._rule_based_plan(student_data)
        
        return plan
    
    def _rule_based_plan(self, student_data: Dict) -> Dict:
        """Rule-based fallback for plan generation"""
        target_role = student_data.get('target_role', 'SDE').upper()
        
        if 'SDE' in target_role or 'SOFTWARE' in target_role:
            days = [
                {
                    "day": 1,
                    "title": "Master Array & String Fundamentals",
                    "description": "Learn core array and string manipulation techniques",
                    "duration_hours": 2,
                    "resources": ["LeetCode Easy Problems", "GeeksforGeeks Arrays"],
                    "success_criteria": "Solve 5 easy problems"
                },
                {
                    "day": 2,
                    "title": "Two Pointer Technique",
                    "description": "Master the two-pointer approach for array problems",
                    "duration_hours": 2,
                    "resources": ["Two Pointer Pattern Guide"],
                    "success_criteria": "Solve 3 two-pointer problems"
                },
                {
                    "day": 3,
                    "title": "Hash Maps & Sets",
                    "description": "Learn when and how to use hash-based data structures",
                    "duration_hours": 2,
                    "resources": ["Hash Map Tutorial"],
                    "success_criteria": "Solve 4 hash map problems"
                },
                {
                    "day": 4,
                    "title": "Recursion Basics",
                    "description": "Understand recursive thinking and base cases",
                    "duration_hours": 2,
                    "resources": ["Recursion Visualizer"],
                    "success_criteria": "Solve 3 recursion problems"
                },
                {
                    "day": 5,
                    "title": "Sorting Algorithms",
                    "description": "Learn and implement common sorting algorithms",
                    "duration_hours": 2,
                    "resources": ["Sorting Visualizations"],
                    "success_criteria": "Implement 3 sorting algorithms"
                },
                {
                    "day": 6,
                    "title": "Binary Search Mastery",
                    "description": "Master binary search and its variations",
                    "duration_hours": 2,
                    "resources": ["Binary Search Guide"],
                    "success_criteria": "Solve 4 binary search problems"
                },
                {
                    "day": 7,
                    "title": "Mock Interview Practice",
                    "description": "Complete a timed mock coding interview",
                    "duration_hours": 2,
                    "resources": ["Mock Interview Platform"],
                    "success_criteria": "Complete 2 medium problems in 45 minutes"
                }
            ]
        else:
            days = [
                {
                    "day": i,
                    "title": f"Day {i} Learning Task",
                    "description": f"Focus on {target_role} fundamentals",
                    "duration_hours": 2,
                    "resources": ["Online Resources"],
                    "success_criteria": "Complete daily task"
                }
                for i in range(1, 8)
            ]
        
        return {
            "plan_title": f"7-Day {target_role} Kickstart Plan",
            "plan_description": "Personalized plan to boost your placement readiness",
            "days": days
        }
    
    def generate_interview_questions(self, role: str, difficulty: str = "medium") -> List[Dict]:
        """
        Generate AI-powered interview questions
        Tailored to role and difficulty level
        """
        system_prompt = """You are an expert technical interviewer.
        Generate realistic, high-quality interview questions."""
        
        prompt = f"""Generate 5 {difficulty} level interview questions for a {role} role.

Return JSON format:
{{
    "questions": [
        {{
            "question": "<question text>",
            "type": "<technical/behavioral/system-design>",
            "hints": ["<hint 1>", "<hint 2>"],
            "key_points": ["<key point 1>", "<key point 2>"]
        }}
    ]
}}"""
        
        response = self._generate(prompt, system_prompt)
        
        try:
            result = json.loads(response)
            return result.get('questions', [])
        except:
            return self._rule_based_questions(role, difficulty)
    
    def _rule_based_questions(self, role: str, difficulty: str) -> List[Dict]:
        """Rule-based fallback for question generation"""
        questions = [
            {
                "question": f"Explain your approach to solving complex {role} problems",
                "type": "technical",
                "hints": ["Think about problem-solving methodology", "Consider edge cases"],
                "key_points": ["Clear communication", "Systematic approach"]
            },
            {
                "question": "Describe a challenging project you worked on",
                "type": "behavioral",
                "hints": ["Use STAR method", "Focus on your contribution"],
                "key_points": ["Problem identification", "Solution implementation", "Results"]
            }
        ]
        return questions
    
    def analyze_skill_gaps(self, student_profile: Dict, target_role: str) -> Dict:
        """
        Analyze skill gaps between current profile and target role
        Provide specific recommendations
        """
        system_prompt = """You are a career advisor specializing in tech recruitment.
        Analyze skill gaps and provide actionable advice."""
        
        current_skills = student_profile.get('skills', [])
        
        prompt = f"""Analyze skill gaps for this student:

Current Skills: {', '.join(current_skills)}
Target Role: {target_role}
Current PRI: {student_profile.get('pri_score', 0)}

Provide JSON response:
{{
    "critical_gaps": [<list of must-have skills missing>],
    "nice_to_have": [<list of beneficial skills>],
    "learning_priority": [<ordered list of what to learn first>],
    "estimated_timeline": "<realistic timeline to fill gaps>",
    "recommended_resources": [<specific learning resources>]
}}"""
        
        response = self._generate(prompt, system_prompt)
        
        try:
            analysis = json.loads(response)
        except:
            analysis = {
                "critical_gaps": ["System Design", "Data Structures"],
                "nice_to_have": ["Cloud Computing", "Docker"],
                "learning_priority": ["DSA Fundamentals", "System Design Basics", "Projects"],
                "estimated_timeline": "3-4 months with consistent practice",
                "recommended_resources": ["LeetCode", "System Design Primer", "Project Ideas"]
            }
        
        return analysis
    
    def generate_project_ideas(self, skills: List[str], target_role: str) -> List[Dict]:
        """
        Generate personalized project ideas
        Based on current skills and target role
        """
        system_prompt = """You are a tech mentor helping students build impressive portfolios.
        Suggest practical, resume-worthy project ideas."""
        
        prompt = f"""Suggest 3 project ideas for a student:

Current Skills: {', '.join(skills)}
Target Role: {target_role}

Return JSON:
{{
    "projects": [
        {{
            "title": "<project name>",
            "description": "<what it does>",
            "difficulty": "<beginner/intermediate/advanced>",
            "duration": "<estimated time>",
            "technologies": [<list of techs to use>],
            "learning_outcomes": [<what they'll learn>],
            "resume_impact": "<why it's impressive>"
        }}
    ]
}}"""
        
        response = self._generate(prompt, system_prompt)
        
        try:
            result = json.loads(response)
            return result.get('projects', [])
        except:
            return self._rule_based_projects(target_role)
    
    def _rule_based_projects(self, target_role: str) -> List[Dict]:
        """Rule-based fallback for project ideas"""
        if 'SDE' in target_role.upper():
            return [
                {
                    "title": "Task Management API",
                    "description": "RESTful API with authentication and CRUD operations",
                    "difficulty": "intermediate",
                    "duration": "1-2 weeks",
                    "technologies": ["FastAPI", "PostgreSQL", "JWT"],
                    "learning_outcomes": ["API design", "Database modeling", "Authentication"],
                    "resume_impact": "Shows backend development skills"
                },
                {
                    "title": "Real-time Chat Application",
                    "description": "WebSocket-based chat with rooms and notifications",
                    "difficulty": "intermediate",
                    "duration": "2-3 weeks",
                    "technologies": ["React", "WebSocket", "Node.js"],
                    "learning_outcomes": ["Real-time communication", "State management"],
                    "resume_impact": "Demonstrates full-stack capabilities"
                }
            ]
        return []
    
    def provide_career_guidance(self, student_data: Dict) -> Dict:
        """
        Provide personalized career guidance
        Based on student's profile, interests, and market trends
        """
        system_prompt = """You are an experienced career counselor in the tech industry.
        Provide realistic, actionable career advice."""
        
        prompt = f"""Provide career guidance for this student:

Profile:
- Target Role: {student_data.get('target_role')}
- Skills: {', '.join(student_data.get('skills', []))}
- Year: {student_data.get('year')}
- PRI Score: {student_data.get('pri_score', 0)}

Provide JSON response:
{{
    "career_path": "<recommended career trajectory>",
    "immediate_actions": [<list of actions for next 30 days>],
    "long_term_goals": [<list of 6-12 month goals>],
    "industry_insights": "<current market trends>",
    "salary_expectations": "<realistic salary range>",
    "companies_to_target": [<list of suitable companies>]
}}"""
        
        response = self._generate(prompt, system_prompt)
        
        try:
            guidance = json.loads(response)
        except:
            guidance = {
                "career_path": "Software Development → Senior Developer → Tech Lead",
                "immediate_actions": [
                    "Complete 50 DSA problems",
                    "Build 2 portfolio projects",
                    "Practice system design"
                ],
                "long_term_goals": [
                    "Master full-stack development",
                    "Contribute to open source",
                    "Build strong GitHub profile"
                ],
                "industry_insights": "High demand for full-stack developers",
                "salary_expectations": "₹4-8 LPA for freshers",
                "companies_to_target": ["Startups", "Product Companies", "Service Companies"]
            }
        
        return guidance

# Global AI service instance
ai_service = AIService()
