# SkillNest - Production-Grade Multi-Language Coding Platform

A complete LeetCode-style coding platform with AI-powered language detection, Docker-based code execution, and comprehensive admin analytics.

## 🏗️ Architecture

### Tech Stack

**Frontend:**
- SvelteKit - Modern web framework
- TailwindCSS - Utility-first styling
- Monaco Editor - VS Code editor experience
- Svelte Stores - State management

**Backend:**
- FastAPI - High-performance Python API
- PostgreSQL - Robust relational database
- SQLAlchemy - Async ORM
- JWT - Secure authentication
- Docker - Isolated code execution

**AI/ML:**
- Ollama (llama3.2:3b) - Language detection
- ChromaDB - Vector database
- RAG - Retrieval-Augmented Generation

## 📁 Project Structure

```
Skill Nest/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLAlchemy models
│   │   │   ├── user.py      # User model with roles
│   │   │   ├── problem.py   # Problem model
│   │   │   └── submission.py # Submission with indexes
│   │   ├── schemas/         # Pydantic schemas
│   │   │   ├── user.py
│   │   │   ├── problem.py
│   │   │   ├── submission.py
│   │   │   └── admin.py     # Admin analytics schemas
│   │   ├── routers/         # API endpoints
│   │   │   ├── auth.py      # Authentication
│   │   │   ├── problems.py  # Problem CRUD
│   │   │   ├── submissions.py # Code submission
│   │   │   └── admin.py     # Admin endpoints (protected)
│   │   ├── services/        # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── submission_service.py
│   │   │   ├── execution_service.py  # Docker executor
│   │   │   ├── rag_service.py        # Language detection
│   │   │   └── admin_service.py      # Analytics
│   │   ├── utils/
│   │   │   ├── security.py  # JWT & password hashing
│   │   │   └── dependencies.py # Auth dependencies
│   │   ├── config.py        # Settings management
│   │   ├── database.py      # Async DB connection
│   │   └── main.py          # FastAPI app
│   ├── scripts/
│   │   └── seed.py          # Database seeding
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── lib/
│   │   │   ├── components/
│   │   │   │   ├── CodeEditor.svelte       # Monaco editor
│   │   │   │   ├── SubmissionResult.svelte
│   │   │   │   ├── LeaderboardTable.svelte
│   │   │   │   ├── AdminStatsCard.svelte
│   │   │   │   └── Navbar.svelte
│   │   │   ├── stores/
│   │   │   │   └── auth.js  # Auth state management
│   │   │   └── api.js       # API client
│   │   ├── routes/
│   │   │   ├── +page.svelte              # Home
│   │   │   ├── login/+page.svelte
│   │   │   ├── register/+page.svelte
│   │   │   ├── dashboard/+page.svelte
│   │   │   ├── problems/
│   │   │   │   ├── +page.svelte          # Problem list
│   │   │   │   └── [id]/+page.svelte     # Problem solver
│   │   │   └── admin/
│   │   │       ├── +layout.js            # Admin guard
│   │   │       ├── login/+page.svelte
│   │   │       └── dashboard/+page.svelte
│   │   └── app.css          # Tailwind imports
│   ├── package.json
│   ├── svelte.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
└── docker-compose.yml       # PostgreSQL service
```

## 🚀 Features

### User Features
- ✅ User registration and JWT authentication
- ✅ Browse coding problems by difficulty
- ✅ Monaco code editor with syntax highlighting
- ✅ Multi-language support (Python, C++, Java, JavaScript)
- ✅ AI-powered language detection using RAG
- ✅ Real-time code execution in isolated Docker containers
- ✅ Submission history tracking
- ✅ Score-based leaderboard
- ✅ Responsive UI with TailwindCSS

### Admin Features
- ✅ Role-based access control
- ✅ Protected admin dashboard
- ✅ **Analytics:**
  - Total users count
  - Total submissions
  - Acceptance rate
  - Daily submission count
  - Top 20 users by score
  - Most attempted problems
  - Language usage statistics
- ✅ Problem management (create problems)

### Security Features
- ✅ JWT authentication with role verification
- ✅ Password hashing with bcrypt
- ✅ Rate limiting (10 submissions/minute)
- ✅ Input size validation (50KB max)
- ✅ Isolated Docker execution (no network, resource limits)
- ✅ Non-root container execution
- ✅ Proper error handling

### Code Execution
- ✅ Docker-based sandboxing
- ✅ Memory limit: 256MB
- ✅ CPU limit: 0.5 cores
- ✅ Timeout: 2 seconds
- ✅ Network isolation
- ✅ Automatic cleanup
- ✅ Multiple verdicts:
  - Accepted
  - Wrong Answer
  - Runtime Error
  - Time Limit Exceeded
  - Memory Limit Exceeded

### Scoring System
- Easy: +10 points
- Medium: +20 points
- Hard: +40 points
- First-solve only (no duplicate points)

## 🛠️ Setup Instructions

### Prerequisites

```bash
# Required
- Python 3.11+
- Node.js 20+
- Docker Desktop
- PostgreSQL 15
- Git

# Install Ollama (for RAG)
# Windows: Download from https://ollama.ai
# Linux/Mac:
curl -fsSL https://ollama.com/install.sh | sh
```

### 1. Clone and Setup

```bash
cd "C:\Users\Tanveer\Vs Code\Skill Nest"
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your settings

# Start PostgreSQL
cd ..
docker-compose up -d

# Initialize database and seed data
cd backend
python scripts/seed.py
```

**Database will be seeded with:**
- Admin user: `admin@skillnest.com` / `admin123`
- 10 sample coding problems

### 3. Setup Ollama Models

```bash
# Pull required models
ollama pull llama3.2:3b-instruct-q4_K_M
ollama pull nomic-embed-text

# Verify models
ollama list
```

### 4. Pull Docker Images for Execution

```bash
docker pull python:3.11-slim
docker pull gcc:13
docker pull openjdk:17-slim
docker pull node:20-slim
```

### 5. Start Backend

```bash
cd backend
.\venv\Scripts\activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will run at: `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### 6. Frontend Setup

Open a new terminal:

```bash
cd "C:\Users\Tanveer\Vs Code\Skill Nest\frontend"

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: `http://localhost:5173`

## 📚 API Endpoints

### Authentication
```
POST   /api/v1/auth/register    - Register new user
POST   /api/v1/auth/login       - Login user
GET    /api/v1/auth/me          - Get current user
```

### Problems
```
GET    /api/v1/problems         - List all problems
GET    /api/v1/problems/{id}    - Get problem details
POST   /api/v1/problems         - Create problem (admin)
GET    /api/v1/problems/leaderboard - Get leaderboard
```

### Submissions
```
POST   /api/v1/submissions      - Submit code (rate limited)
GET    /api/v1/submissions/my-submissions - Get user history
GET    /api/v1/submissions/{id} - Get submission details
```

### Admin (Protected)
```
GET    /api/v1/admin/top-users         - Top 20 users
GET    /api/v1/admin/stats             - Platform statistics
GET    /api/v1/admin/language-usage    - Language breakdown
GET    /api/v1/admin/problem-analytics - Most attempted problems
```

All admin routes require:
- Valid JWT token
- User role = "admin"
- Returns 403 if not admin

## 🔐 Default Credentials

**Admin Account:**
- Email: `admin@skillnest.com`
- Password: `admin123`

**Test User:**
You can register any new user through the UI.

## 🎯 Usage Guide

### As a User:

1. **Register** at `/register`
2. **Login** at `/login`
3. **Browse problems** at `/problems`
4. **Solve a problem:**
   - Click on any problem
   - Write code in the Monaco editor
   - Select language (auto-detected via RAG)
   - Submit solution
   - View result instantly
5. **Check leaderboard** on dashboard
6. **View submission history** on dashboard

### As an Admin:

1. **Login** at `/admin/login` with admin credentials
2. **View dashboard** with:
   - User statistics
   - Submission metrics
   - Acceptance rates
   - Top performers
   - Problem analytics
   - Language usage
3. **Create problems** via API or extend UI

## 🧪 Testing the System

### Test Code Submission

**Python Example:**
```python
def two_sum(nums, target):
    seen = {}
    for i, num in enumerate(nums):
        if target - num in seen:
            return [seen[target - num], i]
        seen[num] = i
    return []

print(two_sum([2, 7, 11, 15], 9))
```

**JavaScript Example:**
```javascript
function twoSum(nums, target) {
    const seen = {};
    for (let i = 0; i < nums.length; i++) {
        const complement = target - nums[i];
        if (complement in seen) {
            return [seen[complement], i];
        }
        seen[nums[i]] = i;
    }
    return [];
}

console.log(twoSum([2, 7, 11, 15], 9));
```

## 🏗️ Production Deployment

### Environment Variables

Create `.env` file in backend:
```bash
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/db
SECRET_KEY=<generate-with-openssl-rand-hex-32>
DEBUG=False
```

### Build and Deploy

```bash
# Backend
cd backend
docker build -t skillnest-backend .
docker run -p 8000:8000 --env-file .env skillnest-backend

# Frontend
cd frontend
npm run build
docker build -t skillnest-frontend .
docker run -p 3000:3000 skillnest-frontend
```

## 🔧 Advanced Configuration

### Adjust Resource Limits

Edit `backend/app/config.py`:
```python
DOCKER_MEMORY_LIMIT = "512m"  # Increase memory
DOCKER_CPU_LIMIT = 1.0        # More CPU
EXECUTION_TIMEOUT = 5         # Longer timeout
```

### Add More Languages

1. Update `LANGUAGE_CONFIGS` in `backend/app/services/execution_service.py`
2. Add language docs to `LANGUAGE_DOCS` in `backend/app/services/rag_service.py`
3. Pull required Docker image

### Custom Rate Limits

Edit `backend/app/config.py`:
```python
RATE_LIMIT_SUBMISSIONS = "20/minute"  # More submissions
```

## 📊 Database Schema

**Users Table:**
- Includes role (user/admin) for RBAC
- Score tracking for leaderboard
- Indexed on score for fast queries

**Submissions Table:**
- Indexed on user_id and problem_id
- Detected language stored
- Runtime and memory metrics
- Timestamp for daily analytics

**Indexes:**
- `idx_submission_user_id` - Fast user history
- `idx_submission_problem_id` - Problem analytics
- `users.score DESC` - Leaderboard queries

## 🐛 Troubleshooting

### Docker Permission Error
```bash
# Windows: Ensure Docker Desktop is running
# Linux: Add user to docker group
sudo usermod -aG docker $USER
```

### Ollama Connection Failed
```bash
# Check Ollama is running
ollama list

# Restart Ollama service
# Windows: Restart from Task Manager
# Linux: sudo systemctl restart ollama
```

### Database Connection Error
```bash
# Check PostgreSQL container
docker ps

# Restart database
docker-compose restart postgres
```

### Frontend Monaco Editor Not Loading
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 📈 Performance Considerations

- **Database**: Indexes on high-query columns
- **Code Execution**: Containers cleaned immediately after use
- **Rate Limiting**: Prevents abuse
- **Async/Await**: Non-blocking I/O throughout
- **Connection Pooling**: PostgreSQL pool (10 connections, 20 overflow)

## 🔒 Security Best Practices

✅ **Implemented:**
- JWT with expiration
- Password hashing (bcrypt)
- Role-based access control
- Docker network isolation
- Rate limiting
- Input validation
- Resource limits

⚠️ **Production Recommendations:**
- Use HTTPS
- Rotate SECRET_KEY regularly
- Enable CORS only for trusted origins
- Set up monitoring and logging
- Regular security audits
- Keep dependencies updated

## 🤝 Contributing

This is a complete production-ready system. To extend:

1. Add more problem test cases
2. Implement problem tags/categories
3. Add social features (comments, discussions)
4. Implement contest mode
5. Add code templates
6. Extend RAG with more languages

## 📝 License

This project is created for educational purposes.

## 🙏 Acknowledgments

- **FastAPI** - Modern Python web framework
- **SvelteKit** - Reactive frontend framework
- **Monaco Editor** - VS Code editor
- **Ollama** - Local LLM inference
- **Docker** - Containerization

---

## 🎓 Technical Deep Dive

### RAG Language Detection Flow

1. User submits code
2. Code embedding generated via `nomic-embed-text`
3. Vector similarity search in ChromaDB
4. Top 3 language docs retrieved
5. LLM (llama3.2) classifies with context
6. Fallback to heuristics if needed

### Docker Execution Pipeline

1. Code written to temporary file
2. Container spawned with:
   - Mounted code volume (read-only)
   - No network access
   - Memory/CPU limits
   - Non-root user
3. Code executed with timeout
4. Metrics captured (runtime, memory)
5. Container removed immediately
6. Verdict determined and stored

### Admin Analytics Queries

All optimized with proper indexes:
- **Top Users**: `ORDER BY score DESC LIMIT 20`
- **Acceptance Rate**: Aggregated count with filter
- **Daily Count**: Date casting with timezone
- **Language Usage**: GROUP BY with count
- **Problem Analytics**: JOIN with aggregation

---

**Built with ❤️ for productive coding practice**

For questions or issues, check the API documentation at `/docs` when running the backend.
