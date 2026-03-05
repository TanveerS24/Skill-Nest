# SkillNest - Multi-Language Coding Platform

<div align="center">

**A production-ready coding platform for solving Data Structure & Algorithm problems with Docker sandbox execution, AI code analysis, Redis caching, and dynamic leaderboards.**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-green.svg)](https://fastapi.tiangolo.com/)
[![SvelteKit](https://img.shields.io/badge/SvelteKit-2.0-orange.svg)](https://kit.svelte.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue.svg)](https://www.postgresql.org/)
[![Redis](https://img.shields.io/badge/Redis-7-red.svg)](https://redis.io/)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Database Structure](#database-structure)
- [Security Features](#security-features)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

SkillNest is a comprehensive coding platform designed for competitive programming and DSA practice. Users can:

- Solve coding problems in **Python, Java, C, and C++**
- Get **AI-powered code analysis** for security and complexity estimation
- Execute code in **isolated Docker containers** with resource limits
- View **real-time leaderboards** with multiple ranking options
- Track personal progress through an **analytics dashboard**

The platform supports anonymous browsing while requiring authentication for code submission.

---

## ✨ Features

### 🔐 Authentication System
- **JWT-based authentication** with access and refresh tokens
- Access token expires in 15 minutes
- Refresh token expires in 7 days (HttpOnly cookie)
- Role-based access control (User / Admin)

### 💻 Multi-Language Code Execution
- Support for **Python, Java, C, C++**
- Isolated Docker containers with:
  - No network access
  - CPU limit: 0.5 cores
  - Memory limit: 256MB (configurable)
  - PID limit: 64 processes
  - Read-only filesystem
  - Automatic timeout handling

### 🤖 AI Code Analysis
- Detects malicious patterns:
  - System calls (exec, eval, subprocess)
  - File operations
  - Network requests
  - Fork bombs
  - Infinite loops
- Estimates time and space complexity using AI (OpenAI API)
- Fallback analysis when AI unavailable

### 🏆 Dynamic Leaderboard System
- **Multiple ranking criteria:**
  - Total problems solved
  - Best average time complexity
  - Best average space complexity
  - Number of submissions per problem
- Complexity scoring:
  - O(1) = 1, O(log n) = 2, O(n) = 3, O(n log n) = 4, O(n²) = 5
- Real-time updates with Redis caching (5-minute TTL)

### ⚡ Redis Integration
- **Rate limiting:** 30 submissions per minute per user
- **Caching:**
  - Problem statements
  - Test cases
  - Leaderboard results
  - AI analysis results
- Future: Job queue for distributed execution

### 📊 Admin Dashboard
- Total user statistics
- Submission metrics
- Most attempted problems
- Language usage distribution
- Top performers leaderboard

### 🎨 Modern Frontend
- **SvelteKit** with TypeScript
- **TailwindCSS** for styling
- **Monaco Editor** for code editing
- Fully responsive design
- Real-time feedback
- Anonymous browsing support

---

## 🛠 Tech Stack

### Backend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.109 | Async REST API framework |
| **SQLAlchemy** | 2.0 | Async ORM for database |
| **PostgreSQL** | 15 | Primary database |
| **Redis** | 7 | Caching & rate limiting |
| **Docker SDK** | 7.0 | Container management |
| **Pydantic** | 2.5 | Data validation |
| **python-jose** | 3.3 | JWT handling |
| **passlib** | 1.7 | Password hashing |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **SvelteKit** | 2.0 | Frontend framework |
| **TypeScript** | 5.3 | Type safety |
| **TailwindCSS** | 3.4 | Styling |
| **Monaco Editor** | 0.45 | Code editor |
| **Vite** | 5.0 | Build tool |

### Infrastructure
- **Docker** & **Docker Compose** - Containerization
- **PostgreSQL** - Persistent data storage
- **Redis** - Caching layer
- **Nginx** (optional) - Reverse proxy

---

## 🏗 Architecture

```
┌─────────────────┐
│                 │
│   SvelteKit     │
│   Frontend      │◄─────┐
│                 │      │
└────────┬────────┘      │
         │               │
         │ HTTP/REST     │
         │               │
┌────────▼────────┐      │
│                 │      │
│   FastAPI       │      │
│   Backend       │      │
│                 │      │
└────┬─────┬──────┘      │
     │     │             │
     │     │             │
┌────▼──┐ ┌▼────────┐   │
│       │ │         │   │
│ PostgreSQL│ Redis │   │
│       │ │         │   │
└───────┘ └─────────┘   │
     │                  │
     │                  │
┌────▼──────────────┐   │
│                   │   │
│  Docker Engine    │   │
│  (Code Execution) │───┘
│                   │
└───────────────────┘
```

### Request Flow

1. **User submits code** → Frontend (SvelteKit)
2. **JWT validation** → FastAPI middleware
3. **Rate limit check** → Redis
4. **AI analysis** → External AI API (optional)
5. **Code execution** → Docker container
6. **Result storage** → PostgreSQL
7. **Cache update** → Redis
8. **Response** → Frontend

---

## 📦 Prerequisites

### Required Software
- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Python** 3.11+ (for local development)
- **Node.js** 20+ (for frontend development)
- **Git**

### Optional
- **OpenAI API Key** (for AI code analysis)
- **Kubernetes** (for production scaling)}

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd skillnest
```

### 2. Set Up Environment Variables

```bash
# Copy example env file
cp backend/.env.example backend/.env

# Edit backend/.env with your configuration
SECRET_KEY=your-secret-key-min-32-characters-long
AI_API_KEY=your-openai-api-key  # Optional
```

### 3. Pull Docker Images

```bash
# Backend will automatically pull these on first run
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull gcc:13-alpine
```

---

## ⚙️ Configuration

### Backend Configuration (`backend/.env`)

```env
# Database
DATABASE_URL=postgresql+asyncpg://skillnest:skillnest123@localhost:5432/skillnest_db

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-secret-key-change-this-in-production-min-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=7

# AI Service (Optional)
AI_API_KEY=sk-...your-openai-key
AI_API_URL=https://api.openai.com/v1/chat/completions

# Rate Limiting
RATE_LIMIT_SUBMISSIONS=30

# Execution Limits
DEFAULT_TIME_LIMIT=5
DEFAULT_MEMORY_LIMIT=256
```

### Frontend Configuration

The frontend uses environment variables prefixed with `PUBLIC_`:

```env
PUBLIC_API_URL=http://localhost:8000
```

---

## 🏃 Running the Application

### Option 1: Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down
```

Services will be available at:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs

### Option 2: Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start Docker-based services
docker-compose up -d postgres redis

# Run database migrations (create tables)
python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"

# Seed database with initial problems
python seed.py

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 📚 API Documentation

### Authentication Endpoints

#### POST `/auth/register`
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "user",
  "created_at": "2026-03-04T10:00:00"
}
```

#### POST `/auth/login`
Login and receive access token.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

Sets `refresh_token` HttpOnly cookie.

#### POST `/auth/refresh`
Refresh access token using refresh token cookie.

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

#### POST `/auth/logout`
Logout and clear refresh token.

#### GET `/auth/me`
Get current user information (requires authentication).

### Problems Endpoints

#### GET `/problems`
Get all problems (anonymous access allowed).

**Response:**
```json
[
  {
    "id": 1,
    "title": "Two Sum",
    "description": "...",
    "difficulty": "easy",
    "time_limit": 5,
    "memory_limit": 256,
    "created_at": "2026-03-04T10:00:00"
  }
]
```

#### GET `/problems/{id}`
Get problem details with non-hidden test cases.

#### POST `/problems`
Create new problem (admin only).

### Submissions Endpoints

#### POST `/submissions`
Submit code for a problem (requires authentication).

**Request:**
```json
{
  "problem_id": 1,
  "language": "python",
  "code": "def solution():\n    pass"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "problem_id": 1,
  "language": "python",
  "verdict": "Accepted",
  "runtime": 45.23,
  "memory": 12.5,
  "time_complexity": "O(n)",
  "space_complexity": "O(1)",
  "created_at": "2026-03-04T10:00:00"
}
```

#### GET `/submissions`
Get user submissions (requires authentication) or all submissions (anonymous).

#### GET `/submissions/{id}`
Get specific submission.

### Leaderboard Endpoints

#### GET `/leaderboard`
Get leaderboard with sorting options.

**Query Parameters:**
- `sort_by`: `solved` | `time` | `space` | `submissions`
- `problem_id`: Filter by problem (required for `submissions` sort)
- `limit`: Max entries (default: 100)

**Response:**
```json
[
  {
    "user_id": 1,
    "email": "user@example.com",
    "problems_solved": 5,
    "avg_time_complexity": 2.5,
    "avg_space_complexity": 2.0,
    "total_submissions": 12
  }
]
```

### Admin Endpoints

#### GET `/admin/dashboard`
Get admin dashboard statistics (admin only).

**Response:**
```json
{
  "total_users": 100,
  "total_submissions": 500,
  "accepted_submissions": 300,
  "most_attempted_problems": [...],
  "language_usage": {"python": 250, "java": 150, ...},
  "top_users": [...]
}
```

---

## 🗄 Database Structure

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(20) DEFAULT 'user',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Problems Table
```sql
CREATE TABLE problems (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) UNIQUE NOT NULL,
    description TEXT NOT NULL,
    difficulty VARCHAR(20),
    time_limit INTEGER DEFAULT 5,
    memory_limit INTEGER DEFAULT 256,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### TestCases Table
```sql
CREATE TABLE test_cases (
    id SERIAL PRIMARY KEY,
    problem_id INTEGER REFERENCES problems(id),
    input TEXT,
    expected_output TEXT,
    is_hidden BOOLEAN DEFAULT FALSE
);
```

### Submissions Table
```sql
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    problem_id INTEGER REFERENCES problems(id),
    language VARCHAR(20),
    code TEXT,
    verdict VARCHAR(50),
    runtime FLOAT,
    memory FLOAT,
    time_complexity VARCHAR(50),
    space_complexity VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 🔒 Security Features

### 1. Authentication
- Bcrypt password hashing
- JWT with expiration
- HttpOnly cookies for refresh tokens
- CORS configuration

### 2. Code Execution Sandbox
```python
docker run \
  --rm \
  --network none \
  --memory 256m \
  --cpus 0.5 \
  --pids-limit 64 \
  --read-only \
  image:tag
```

### 3. AI Code Analysis
Detects:
- Malicious system calls
- File operations
- Network requests
- Fork bombs
- Infinite loops (heuristic)

### 4. Rate Limiting
- 30 submissions per minute per user
- Tracked via Redis
- IP-based for anonymous users

### 5. Input Validation
- Pydantic models for all endpoints
- SQL injection prevention via ORM
- XSS protection in frontend

---

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Run Frontend Tests

```bash
cd frontend
npm run test
```

### Manual Testing

Use the provided demo accounts:
- **Admin:** admin@skillnest.com / admin123
- **User:** user@test.com / user123

---

## 🚢 Deployment

### Production Checklist

- [ ] Change `SECRET_KEY` to a strong random value
- [ ] Enable HTTPS (use Nginx with Let's Encrypt)
- [ ] Set `secure=True` for refresh token cookies
- [ ] Use production database credentials
- [ ] Configure proper CORS origins
- [ ] Set up monitoring (Prometheus/Grafana)
- [ ] Configure log aggregation
- [ ] Set up automated backups
- [ ] Use managed Redis (AWS ElastiCache, etc.)
- [ ] Configure CDN for frontend assets

### Docker Compose Production

```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  backend:
    image: skillnest-backend:latest
    environment:
      - SECRET_KEY=${SECRET_KEY}
      - DATABASE_URL=${DATABASE_URL}
    restart: always
```

### Kubernetes Deployment

```bash
# Apply Kubernetes manifests
kubectl apply -f k8s/

# Scale workers
kubectl scale deployment skillnest-backend --replicas=5
```

---

## 🐛 Troubleshooting

### Docker Container Issues

```bash
# Check running containers
docker ps

# View container logs
docker logs skillnest_backend

# Restart services
docker-compose restart

# Clean rebuild
docker-compose down -v
docker-compose build --no-cache
docker-compose up -d
```

### Database Connection Errors

```bash
# Check PostgreSQL is running
docker-compose ps postgres

# Connect to database
docker exec -it skillnest_postgres psql -U skillnest -d skillnest_db

# Check tables
\dt
```

### Redis Connection Errors

```bash
# Test Redis connection
docker exec -it skillnest_redis redis-cli ping

# Check keys
docker exec -it skillnest_redis redis-cli KEYS '*'
```

### Code Execution Failures

```bash
# Check Docker daemon
docker info

# Pull missing images
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull gcc:13-alpine

# Check container logs
docker logs <container_id>
```

---

## 🔄 Initial Data

The platform includes 6 seeded DSA problems:

1. **Two Sum** (Easy)
2. **Valid Parentheses** (Easy)
3. **Reverse Linked List** (Easy)
4. **Binary Search** (Easy)
5. **Merge Sorted Arrays** (Medium)
6. **Longest Substring Without Repeating Characters** (Medium)

Run `python seed.py` to populate the database.

---

## 📝 API Rate Limits

| Endpoint | Limit | Window |
|----------|-------|--------|
| `/submissions` (POST) | 30 | 1 minute |
| Other endpoints | Unlimited | - |

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- FastAPI for the excellent async framework
- SvelteKit for the modern frontend experience
- Monaco Editor by Microsoft
- Docker for containerization
- Redis for caching excellence

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Email: support@skillnest.dev

---

<div align="center">

**Built with ❤️ by distributed systems architects**

⭐ Star this repository if you find it helpful!

</div>