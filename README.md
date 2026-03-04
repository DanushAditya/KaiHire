# KaiHire – AI Placement Copilot & Talent Radar

A production-ready full-stack campus placement ecosystem platform with dual login for students and HR professionals. Built with modern technologies and best practices for scalability and maintainability.

## 🚀 Features

### Student Features

#### 📄 Resume Intelligence
- PDF resume upload and parsing
- Automatic extraction of skills, projects, and experience
- Resume quality scoring (0-100)
- Intelligent insights and improvement suggestions
- Auto-fill profile from resume data

#### 🎯 Smart Profile System
- Comprehensive profile with college, year, branch, section
- Target role selection (SDE, ML Engineer, Analyst, Core, etc.)
- Available hours per week tracking
- Multi-select skills with chip UI
- Real-time profile completion tracking

#### 📊 Skill Assessment Engine
- Internal MCQ-based assessment system
- 50+ questions across multiple categories:
  - Data Structures & Algorithms
  - Python Programming
  - Machine Learning
  - Web Development
  - Database Management
- Adaptive difficulty based on performance
- Role-specific question filtering
- Timed assessments (10 minutes)
- Detailed performance analytics

#### 📈 Dual Scoring System
- **Placement Readiness Index (PRI)**: 0-100 score based on:
  - Resume Quality (20%)
  - Skill Test Score (30%)
  - Project Depth (20%)
  - Streak Consistency (15%)
  - Challenge Participation (15%)
- **Skill Level Index (SLI)**: Weighted assessment performance
  - Difficulty-based weighting
  - Category-wise tracking
  - Progressive improvement tracking

#### 🎓 Personalized Learning Plans
- **7-Day Kickstart Plan**:
  - Role-specific tasks
  - Daily structured activities
  - XP rewards for completion
  - Progress tracking
- **30-Day Advanced Plan**:
  - Unlocked after 7-day completion
  - Advanced challenges
  - Deep-dive topics
  - Career preparation

#### 🎮 Gamification System
- **Daily Streak Tracking**:
  - Increment on daily activity
  - Reset on missed days
  - Milestone badges at 7, 30, 100 days
  - Longest streak records
- **XP & Tier System**:
  - Beginner (0-100 XP)
  - Explorer (100-300 XP)
  - Achiever (300-600 XP)
  - Pro (600-1000 XP)
  - Elite (1000+ XP)
- **Unlock System**:
  - Progressive feature unlocking
  - Advanced analytics access
  - Profile frames and badges
  - Resume insights

#### 👥 Social Features
- **Friend System**:
  - Add friends by email or referral code
  - Compare PRI scores
  - View friend streaks
  - Challenge participation comparison
- **Leaderboards**:
  - Class leaderboard
  - Branch leaderboard
  - College-wide leaderboard
  - Real-time ranking updates
  - Cached for performance

#### 🏆 7-Day Challenges
- Role-based challenge types:
  - DSA Sprint
  - ML Sprint
  - Core Concepts Sprint
  - Web Development Sprint
- XP points and badges
- PRI boost on completion
- Progress tracking
- Completion certificates

#### 💳 Professional Readiness Card
- Downloadable digital card featuring:
  - Name, college, and target role
  - PRI and SLI scores
  - Current streak and tier
  - Top 5 skills
  - Strength areas
  - Improvement suggestions
  - Unique referral code
- Share with friends
- Challenge friends feature

#### 🔗 Referral System
- Unique referral code for each student
- Bonus XP for both referrer and referee:
  - Referrer: +50 XP
  - New user: +25 XP
- Track referral statistics
- Leaderboard for top referrers

### HR Features

#### 🎯 Advanced Talent Filtering
- Filter by:
  - College
  - Branch
  - Year
  - PRI threshold
  - Skill level
  - Target role
  - Minimum streak
- Multi-criteria search
- Saved filter presets

#### 📊 Analytics Dashboard
- **Top Performers**:
  - Top 100 students by PRI
  - Skill distribution charts
  - Activity heatmaps
- **Metrics**:
  - Total active students
  - Average PRI by branch
  - Skill coverage analysis
  - Engagement statistics
- **Visualizations**:
  - Recharts-based graphs
  - Interactive charts
  - Exportable reports

#### 👤 Student Detail View
- Complete profile information
- Resume download
- Skill assessment history
- Consistency graphs
- Challenge completion status
- Project portfolio
- Contact information

#### 📥 Export Functionality
- CSV export of filtered students
- Customizable columns
- Bulk data download
- Integration-ready format

## 🛠️ Tech Stack

### Frontend
- **React 18** with Vite for fast development
- **Material-UI (MUI) v5** for professional UI components
- **React Router v6** for navigation
- **Axios** for API communication
- **Recharts** for data visualization
- **Framer Motion** for smooth animations
- **Dark/Light mode** toggle

### Backend
- **FastAPI** for high-performance API
- **MySQL** for robust data storage
- **SQLAlchemy ORM** for database operations
- **JWT Authentication** with bcrypt password hashing
- **Pydantic** for data validation
- **Python-Jose** for JWT tokens
- **PyPDF2** for resume parsing

### Architecture
- RESTful API design
- Role-based access control (RBAC)
- Dependency injection pattern
- Service layer architecture
- Modular folder structure
- Environment-based configuration

## 📁 Project Structure

```
kaihire/
├── backend/
│   ├── app/
│   │   ├── api/              # API route handlers
│   │   │   ├── auth.py       # Authentication endpoints
│   │   │   ├── student.py    # Student endpoints
│   │   │   ├── assessment.py # Assessment endpoints
│   │   │   ├── plan.py       # Learning plan endpoints
│   │   │   ├── card.py       # Readiness card endpoints
│   │   │   ├── challenge.py  # Challenge endpoints
│   │   │   ├── friends.py    # Friend system endpoints
│   │   │   ├── leaderboard.py# Leaderboard endpoints
│   │   │   └── hr.py         # HR endpoints
│   │   ├── core/             # Core configuration
│   │   │   ├── config.py     # Settings management
│   │   │   ├── database.py   # Database connection
│   │   │   └── security.py   # Security utilities
│   │   ├── models/           # SQLAlchemy models
│   │   │   ├── user.py       # User model
│   │   │   ├── student.py    # Student models
│   │   │   ├── hr.py         # HR model
│   │   │   ├── challenge.py  # Challenge models
│   │   │   └── question.py   # Question model
│   │   ├── schemas/          # Pydantic schemas
│   │   │   ├── auth.py       # Auth schemas
│   │   │   ├── student.py    # Student schemas
│   │   │   └── challenge.py  # Challenge schemas
│   │   ├── services/         # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── resume_service.py
│   │   │   ├── score_service.py
│   │   │   ├── plan_service.py
│   │   │   ├── streak_service.py
│   │   │   ├── question_service.py
│   │   │   └── card_service.py
│   │   └── main.py           # FastAPI application
│   ├── requirements.txt      # Python dependencies
│   ├── seed_data.py          # Database seeding
│   ├── seed_questions.py     # Question bank seeding
│   └── .env.example          # Environment template
└── frontend/
    ├── src/
    │   ├── components/       # Reusable components
    │   │   ├── Layout.jsx
    │   │   └── ReadinessCard.jsx
    │   ├── pages/            # Page components
    │   │   ├── Login.jsx
    │   │   ├── Register.jsx
    │   │   ├── student/      # Student pages
    │   │   │   ├── Dashboard.jsx
    │   │   │   ├── Profile.jsx
    │   │   │   ├── Assessment.jsx
    │   │   │   ├── Plan.jsx
    │   │   │   ├── Challenges.jsx
    │   │   │   ├── Friends.jsx
    │   │   │   └── Leaderboard.jsx
    │   │   └── hr/           # HR pages
    │   │       ├── Dashboard.jsx
    │   │       ├── TalentList.jsx
    │   │       └── Analytics.jsx
    │   ├── services/         # API services
    │   │   └── api.js
    │   ├── App.jsx           # Main app component
    │   └── main.jsx          # Entry point
    ├── package.json          # Node dependencies
    └── vite.config.js        # Vite configuration
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Node.js 16 or higher
- MySQL 8.0 or higher

### Backend Setup

1. **Navigate to backend directory**:
```bash
cd backend
```

2. **Create virtual environment**:
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Setup MySQL database**:
```sql
CREATE DATABASE kaihire;
```

5. **Configure environment variables**:
```bash
cp .env.example .env
```

Edit `.env`:
```env
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/kaihire
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DEBUG=True
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

6. **Seed database**:
```bash
python seed_data.py
python seed_questions.py
```

7. **Run backend server**:
```bash
uvicorn app.main:app --reload
```

Backend will be available at: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Frontend Setup

1. **Navigate to frontend directory**:
```bash
cd frontend
```

2. **Install dependencies**:
```bash
npm install
```

3. **Run development server**:
```bash
npm run dev
```

Frontend will be available at: http://localhost:5173

## 📚 API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Key Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login user
- `GET /auth/me` - Get current user

#### Student
- `GET /student/profile` - Get student profile
- `PUT /student/profile` - Update profile
- `POST /student/resume/upload` - Upload resume

#### Assessment
- `POST /assessment/start` - Start new assessment
- `POST /assessment/submit` - Submit assessment
- `GET /assessment/history` - Get assessment history

#### Plans
- `POST /plan/generate/7-day` - Generate 7-day plan
- `POST /plan/generate/30-day` - Generate 30-day plan
- `GET /plan/my-plans` - Get all plans
- `POST /plan/task/{id}/complete` - Complete task

#### Card
- `GET /card/generate` - Generate readiness card
- `POST /card/referral/apply` - Apply referral code
- `GET /card/referral/stats` - Get referral stats

#### Challenges
- `GET /challenges/` - Get all challenges
- `POST /challenges/enroll` - Enroll in challenge
- `GET /challenges/my-challenges` - Get enrolled challenges

#### Friends
- `POST /friends/request` - Send friend request
- `GET /friends/requests` - Get pending requests
- `POST /friends/accept/{id}` - Accept request
- `GET /friends/list` - Get friends list

#### Leaderboard
- `GET /leaderboard/class` - Class leaderboard
- `GET /leaderboard/branch` - Branch leaderboard
- `GET /leaderboard/college` - College leaderboard

#### HR
- `GET /hr/students` - Filter students
- `GET /hr/student/{id}` - Get student details
- `GET /hr/analytics` - Get analytics
- `GET /hr/export` - Export CSV

## 🧪 Testing

### Test Accounts

After running `seed_data.py`, you can use:

**Student Account**:
- Email: student@test.com
- Password: password123

**HR Account**:
- Email: hr@test.com
- Password: password123

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment instructions including:
- Server setup
- MySQL configuration
- Nginx setup
- SSL certificates
- Docker deployment
- Cloud platform deployment (AWS, Heroku)
- Monitoring and maintenance

## 🔒 Security Features

- JWT-based authentication
- Password hashing with bcrypt
- Role-based access control
- CORS configuration
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection
- Environment-based secrets
- Rate limiting ready

## 📊 Database Schema

### Key Tables
- `users` - User authentication
- `student_profiles` - Student information
- `hr_profiles` - HR information
- `resume_data` - Parsed resume data
- `skill_assessments` - Assessment records
- `questions` - Question bank
- `plans` - Learning plans
- `plan_tasks` - Plan tasks
- `challenges` - Available challenges
- `challenge_participations` - Student enrollments
- `friendships` - Friend connections

## 🎨 UI/UX Features

- Clean, modern Material Design
- Responsive layout (mobile, tablet, desktop)
- Dark/Light mode toggle
- Smooth animations with Framer Motion
- Loading states and error handling
- Toast notifications
- Progress indicators
- Interactive charts and graphs

## 🔧 Development

### Code Quality
- Modular architecture
- Clean code principles
- Proper error handling
- Comprehensive comments
- Type hints (Python)
- PropTypes (React)

### Best Practices
- RESTful API design
- Separation of concerns
- DRY principle
- SOLID principles
- Dependency injection
- Environment configuration

## 📝 License

MIT License - See LICENSE file for details

## 👥 Contributors

Built by a team of final-year engineering students as a production-ready campus placement platform.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions:
- GitHub Issues: [Create an issue](https://github.com/yourusername/kaihire/issues)
- Email: support@kaihire.com

## 🙏 Acknowledgments

- FastAPI for the amazing web framework
- Material-UI for beautiful components
- MySQL for robust data storage
- All open-source contributors

---

Made with ❤️ for campus placements
