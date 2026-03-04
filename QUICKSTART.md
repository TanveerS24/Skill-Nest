# ⚡ Quick Start Guide

Get SkillNest running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.11+ installed
- [ ] Node.js 20+ installed
- [ ] Docker Desktop running
- [ ] Ollama installed

## Step-by-Step Setup

### 1. Start PostgreSQL (30 seconds)

```powershell
cd "C:\Users\Tanveer\Vs Code\Skill Nest"
docker-compose up -d
```

### 2. Backend Setup (2 minutes)

```powershell
cd backend

# Create virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env

# Seed database (creates admin user + 10 problems)
python scripts\seed.py

# Start backend
uvicorn app.main:app --reload
```

✅ Backend running at: http://localhost:8000

### 3. Setup Ollama Models (1 minute)

Open a new PowerShell terminal:

```powershell
ollama pull llama3.2:3b-instruct-q4_K_M
ollama pull nomic-embed-text
```

### 4. Frontend Setup (90 seconds)

Open a new PowerShell terminal:

```powershell
cd "C:\Users\Tanveer\Vs Code\Skill Nest\frontend"

# Install dependencies
npm install

# Start frontend
npm run dev
```

✅ Frontend running at: http://localhost:5173

### 5. Pull Docker Images for Code Execution

Open a new PowerShell terminal:

```powershell
docker pull python:3.11-slim
docker pull node:20-slim
docker pull gcc:13
docker pull openjdk:17-slim
```

## Test It Out!

### Test Admin Access

1. Go to http://localhost:5173/admin/login
2. Login with:
   - Email: `admin@skillnest.com`
   - Password: `admin123`
3. View the admin dashboard

### Test User Flow

1. Go to http://localhost:5173/register
2. Create a new account
3. Browse problems at `/problems`
4. Click on "Two Sum" problem
5. Write this Python solution:

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

6. Click "Submit Solution"
7. See verdict: **Accepted** ✅
8. Your score increased by 10 points!

## Verify Everything is Working

Check these URLs:

- ✅ Frontend: http://localhost:5173
- ✅ Backend: http://localhost:8000
- ✅ API Docs: http://localhost:8000/docs
- ✅ Health Check: http://localhost:8000/health

## Common Issues

### "Connection refused" on PostgreSQL
```powershell
# Check if container is running
docker ps

# If not, start it
docker-compose up -d
```

### Ollama model not found
```powershell
# Check installed models
ollama list

# If missing, pull them
ollama pull llama3.2:3b-instruct-q4_K_M
ollama pull nomic-embed-text
```

### Monaco Editor not loading
```powershell
cd frontend
rm -rf node_modules
npm install
```

### Docker execution failing
```powershell
# Make sure Docker Desktop is running
# Then pull the language images again
docker pull python:3.11-slim
```

## What's Next?

- Try different languages (Python, JavaScript, C++, Java)
- Solve all 10 sample problems
- Check the leaderboard
- View your submission history
- Create new problems (as admin)
- Explore the admin dashboard analytics

## Architecture Overview

```
┌─────────────────────────────────────────────────────┐
│                    User / Admin                      │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│              SvelteKit Frontend                      │
│  (Monaco Editor, TailwindCSS, Svelte Stores)        │
└───────────────────────┬─────────────────────────────┘
                        │ HTTP/REST
                        ▼
┌─────────────────────────────────────────────────────┐
│               FastAPI Backend                        │
│  ┌──────────────────────────────────────────────┐  │
│  │  Auth │ Problems │ Submissions │ Admin       │  │
│  └──────────────────────────────────────────────┘  │
│  ┌──────────────────────────────────────────────┐  │
│  │  RAG Service    │   Execution Service        │  │
│  │  (Ollama+Chroma)│   (Docker Sandbox)        │  │
│  └──────────────────────────────────────────────┘  │
└─────────┬────────────────────────────┬──────────────┘
          │                            │
          ▼                            ▼
┌──────────────────┐        ┌──────────────────────┐
│   PostgreSQL     │        │   Docker Engine      │
│   (User Data)    │        │   (Code Execution)   │
└──────────────────┘        └──────────────────────┘
```

## Key Features Implemented

✅ **User System**
- JWT authentication
- Role-based access (user/admin)
- Score tracking
- Submission history

✅ **Code Execution**
- Multi-language support
- Docker sandboxing
- Resource limits
- Multiple verdicts

✅ **AI Integration**
- RAG-based language detection
- Ollama LLM
- ChromaDB vector store

✅ **Admin Dashboard**
- User analytics
- Submission metrics
- Language usage stats
- Problem analytics

✅ **Security**
- Rate limiting
- Input validation
- Isolated execution
- JWT expiration

## Support

Check the main [README.md](README.md) for:
- Full API documentation
- Detailed architecture
- Advanced configuration
- Troubleshooting guide
- Production deployment

---

**Happy Coding! 🚀**
