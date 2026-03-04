# 🏛️ Architecture Documentation

## System Overview

SkillNest is a production-grade, distributed coding platform built with modern microservices patterns, AI integration, and enterprise security practices.

## Architecture Layers

### 1. Presentation Layer (Frontend)

**Technology**: SvelteKit + TailwindCSS + Monaco Editor

**Components**:
```
┌─────────────────────────────────────────────────┐
│              SvelteKit Application               │
│  ┌───────────────────────────────────────────┐  │
│  │  Pages (Routes)                           │  │
│  │  - Home, Login, Register                  │  │
│  │  - Dashboard, Problems, Problem Detail    │  │
│  │  - Admin Login, Admin Dashboard           │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │  Components                               │  │
│  │  - CodeEditor (Monaco)                    │  │
│  │  - SubmissionResult                       │  │
│  │  - LeaderboardTable                       │  │
│  │  - AdminStatsCard                         │  │
│  │  - Navbar                                 │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │  State Management                         │  │
│  │  - Auth Store (JWT + User)               │  │
│  │  - API Client (Fetch wrapper)            │  │
│  └───────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────┐  │
│  │  Route Guards                             │  │
│  │  - Admin layout guard (role check)       │  │
│  │  - Auth verification                      │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

**Key Design Decisions**:
- **SvelteKit**: Chosen for minimal runtime, reactive state, and easy SSR
- **Stores**: Persistent auth state using localStorage
- **Monaco Editor**: Full IDE experience in browser
- **TailwindCSS**: Rapid UI development with utility classes
- **Route Protection**: Layout-based guards with role checking

### 2. Application Layer (Backend API)

**Technology**: FastAPI + Python 3.11

**Architecture Pattern**: Clean Architecture with Service Layer

```
┌─────────────────────────────────────────────────────────┐
│                   FastAPI Application                    │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │               Routers (Controllers)                 │ │
│  │  ┌──────────┬───────────┬────────────┬──────────┐ │ │
│  │  │   Auth   │ Problems  │ Submissions│  Admin   │ │ │
│  │  └──────────┴───────────┴────────────┴──────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │              Middleware & Dependencies              │ │
│  │  - CORS                                            │ │
│  │  - Rate Limiter (SlowAPI)                         │ │
│  │  - Auth Dependencies (JWT verification)           │ │
│  │  - Role Guards (require_admin)                    │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │                 Service Layer                       │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │  AuthService                                  │ │ │
│  │  │  - User registration                          │ │ │
│  │  │  - Authentication                             │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │  SubmissionService                            │ │ │
│  │  │  - Create submission                          │ │ │
│  │  │  - Execute code (via ExecutionService)       │ │ │
│  │  │  - Detect language (via RAGService)          │ │ │
│  │  │  - Update user score                          │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │  ExecutionService                             │ │ │
│  │  │  - Docker container orchestration            │ │ │
│  │  │  - Language-specific execution               │ │ │
│  │  │  - Verdict determination                     │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │  RAGService                                   │ │ │
│  │  │  - Language detection with LLM               │ │ │
│  │  │  - Vector similarity search                  │ │ │
│  │  │  - Fallback heuristics                       │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  │  ┌──────────────────────────────────────────────┐ │ │
│  │  │  AdminService                                 │ │ │
│  │  │  - Analytics queries                          │ │ │
│  │  │  - Aggregation computations                  │ │ │
│  │  └──────────────────────────────────────────────┘ │ │
│  └────────────────────────────────────────────────────┘ │
│                           │                              │
│                           ▼                              │
│  ┌────────────────────────────────────────────────────┐ │
│  │            Data Access Layer (ORM)                  │ │
│  │  - SQLAlchemy Models                               │ │
│  │  - Async Session Management                        │ │
│  │  - Database Migrations                             │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

**Design Patterns**:
- **Service Layer**: Business logic separated from routes
- **Dependency Injection**: FastAPI's DI for DB sessions, auth
- **Repository Pattern**: Implicit through SQLAlchemy
- **Async/Await**: Non-blocking I/O throughout

### 3. Data Layer

**Primary Database**: PostgreSQL 15

**Schema Design**:

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    password_hash VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'user',  -- user | admin
    score INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_users_score ON users(score DESC);

-- Problems table
CREATE TABLE problems (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    difficulty VARCHAR NOT NULL,  -- Easy | Medium | Hard
    description TEXT NOT NULL,
    time_limit INTEGER DEFAULT 2,
    memory_limit INTEGER DEFAULT 256
);

-- Submissions table
CREATE TABLE submissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    problem_id INTEGER REFERENCES problems(id),
    code TEXT NOT NULL,
    detected_language VARCHAR,
    verdict VARCHAR NOT NULL,  -- Accepted, Wrong Answer, etc.
    runtime FLOAT,  -- milliseconds
    memory FLOAT,   -- MB
    created_at TIMESTAMP DEFAULT NOW()
);
CREATE INDEX idx_submission_user_id ON submissions(user_id);
CREATE INDEX idx_submission_problem_id ON submissions(problem_id);
```

**Indexing Strategy**:
- `users.score DESC` - Fast leaderboard queries
- `submissions.user_id` - Quick user history lookup
- `submissions.problem_id` - Problem analytics
- `submissions.created_at` - Time-based queries

**Query Optimization**:
- Connection pooling (10 base, 20 overflow)
- Async queries prevent blocking
- Proper indexes on foreign keys
- Aggregations use database-level operations

### 4. Execution Layer

**Technology**: Docker Engine

**Isolation Strategy**:

```
┌─────────────────────────────────────────────────┐
│            ExecutionService                      │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         Docker Container Lifecycle               │
│                                                  │
│  1. Create temp directory                       │
│  2. Write code to file                          │
│  3. Spawn container with:                       │
│     - Volume mount (read-only)                  │
│     - Network: none (--network none)            │
│     - Memory: 256MB (--memory 256m)             │
│     - CPU: 0.5 cores (--cpus 0.5)               │
│     - User: nobody (non-root)                   │
│     - Timeout: 2 seconds                        │
│  4. Execute code                                │
│  5. Capture stdout/stderr                       │
│  6. Get metrics (runtime, memory)               │
│  7. Determine verdict                           │
│  8. Stop & remove container                     │
│  9. Clean temp files                            │
└─────────────────────────────────────────────────┘
```

**Language Configurations**:

| Language   | Base Image            | Compile Step | Execute Step |
|------------|-----------------------|--------------|--------------|
| Python     | python:3.11-slim      | None         | python file.py |
| JavaScript | node:20-slim          | None         | node file.js |
| C++        | gcc:13                | g++ compile  | ./executable |
| Java       | openjdk:17-slim       | javac compile| java Main |

**Verdicts**:
- **Accepted**: Exit code 0, expected output
- **Wrong Answer**: Exit code 0, wrong output
- **Runtime Error**: Non-zero exit code
- **Time Limit Exceeded**: Timeout reached
- **Memory Limit Exceeded**: OOM kill

**Security Measures**:
- No network access
- Read-only code mount
- Resource limits enforced
- Non-root execution
- Immediate cleanup

### 5. AI/ML Layer

**Technology**: Ollama + ChromaDB

**RAG Pipeline**:

```
┌──────────────────────────────────────────────────┐
│              User Submits Code                    │
└────────────────────┬─────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────┐
│              RAGService                           │
│                                                   │
│  Step 1: Generate Code Embedding                 │
│  ┌────────────────────────────────────────────┐  │
│  │  Ollama Embedding API                      │  │
│  │  Model: nomic-embed-text                   │  │
│  │  Input: First 1000 chars of code          │  │
│  │  Output: 768-dim vector                    │  │
│  └────────────────────────────────────────────┘  │
│                     │                             │
│                     ▼                             │
│  Step 2: Vector Similarity Search                │
│  ┌────────────────────────────────────────────┐  │
│  │  ChromaDB Query                            │  │
│  │  - Search in language_docs collection      │  │
│  │  - Return top 3 similar docs               │  │
│  │  - Languages: Python, C++, Java, JS        │  │
│  └────────────────────────────────────────────┘  │
│                     │                             │
│                     ▼                             │
│  Step 3: LLM Classification                      │
│  ┌────────────────────────────────────────────┐  │
│  │  Ollama Generate API                       │  │
│  │  Model: llama3.2:3b-instruct-q4_K_M        │  │
│  │  Prompt: Code + Retrieved docs context    │  │
│  │  Output: Language name + confidence        │  │
│  └────────────────────────────────────────────┘  │
│                     │                             │
│                     ▼                             │
│  Step 4: Fallback Heuristics (if LLM fails)     │
│  ┌────────────────────────────────────────────┐  │
│  │  - Check for "def " → Python               │  │
│  │  - Check for "public class" → Java         │  │
│  │  - Check for "#include" → C++              │  │
│  │  - Check for "function" → JavaScript       │  │
│  └────────────────────────────────────────────┘  │
│                     │                             │
│                     ▼                             │
│          Return: {language, confidence}          │
└──────────────────────────────────────────────────┘
```

**Language Documentation Embeddings**:
- Pre-embedded during initialization
- Stored in ChromaDB
- Contains syntax patterns and examples
- Updated when new languages added

**Why RAG?**:
- **Accuracy**: Context-aware classification
- **Explainability**: See similar documents
- **Extensibility**: Add languages by adding docs
- **Fallback**: Heuristics if AI fails

### 6. Security Architecture

**Authentication Flow**:

```
┌─────────────────────────────────────────────────┐
│         User Login Request                       │
│         POST /api/v1/auth/login                  │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         AuthService.authenticate_user            │
│  1. Query user by email                         │
│  2. Verify password (bcrypt)                    │
│  3. Return user or None                         │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         create_access_token()                    │
│  1. Prepare payload: {sub: user_id}            │
│  2. Add expiration (24 hours)                   │
│  3. Sign with SECRET_KEY (HS256)                │
│  4. Return JWT token                            │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         Return Token + User Info                 │
│         Frontend stores in localStorage          │
└─────────────────────────────────────────────────┘
```

**Authorization Flow** (Protected Endpoints):

```
┌─────────────────────────────────────────────────┐
│    Request to Protected Endpoint                 │
│    Header: Authorization: Bearer <token>         │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         get_current_user() dependency            │
│  1. Extract token from header                   │
│  2. Verify signature                            │
│  3. Check expiration                            │
│  4. Extract user_id from payload                │
│  5. Query database for user                     │
│  6. Return User object                          │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│   For Admin Routes: require_admin() dependency  │
│  1. Call get_current_user()                     │
│  2. Check if user.role == 'admin'               │
│  3. Raise 403 if not admin                      │
│  4. Return user if admin                        │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         Execute Route Handler                    │
└─────────────────────────────────────────────────┘
```

**Security Layers**:

1. **Authentication**: JWT with signature verification
2. **Authorization**: Role-based access control (RBAC)
3. **Rate Limiting**: 10 submissions/minute per IP
4. **Input Validation**: Pydantic schemas, size limits
5. **Execution Isolation**: Docker sandboxing
6. **Password Security**: Bcrypt hashing
7. **CORS**: Restricted origins
8. **Error Handling**: No sensitive data in errors

### 7. Monitoring & Observability

**Health Checks**:
- `/health` - Service availability
- Database connection check
- Docker daemon connectivity

**Metrics** (Available via Admin Dashboard):
- Total users
- Total submissions
- Acceptance rate
- Daily submission count
- Language usage distribution
- Problem popularity

**Logging**:
- FastAPI request logs
- Execution errors captured
- RAG service fallbacks logged

## Data Flow Diagrams

### Submission Flow (Complete)

```
User writes code in Monaco Editor
         │
         ▼
Click "Submit Solution"
         │
         ▼
Frontend validates code size
         │
         ▼
POST /api/v1/submissions
         │
         ▼
Rate limiter check (10/min)
         │
         ▼
JWT verification (get_current_user)
         │
         ▼
SubmissionService.create_and_execute_submission()
         │
         ├─────────────────────────────────┐
         │                                  │
         ▼                                  ▼
RAGService.detect_language()    ExecutionService.execute_code()
         │                                  │
         ├─ Embed code                     ├─ Create temp dir
         ├─ Query ChromaDB                 ├─ Write code to file
         ├─ Ask LLM                         ├─ Spawn Docker container
         └─ Return language                ├─ Execute with timeout
                                           ├─ Capture output & metrics
                                           └─ Return ExecutionResult
         │                                  │
         └─────────────────┬────────────────┘
                           │
                           ▼
         Create Submission record in DB
                           │
                           ▼
         If verdict == "Accepted":
           ├─ Check if first solve
           ├─ Get problem difficulty
           ├─ Award points (Easy:10, Med:20, Hard:40)
           └─ Update user.score
                           │
                           ▼
         Commit transaction
                           │
                           ▼
         Return SubmissionResponse
                           │
                           ▼
         Frontend displays result
         Frontend updates user score in navbar
```

### Admin Analytics Flow

```
Admin visits /admin/dashboard
         │
         ▼
Check role (require_admin guard)
         │
         ▼
Make parallel API calls:
  ├─ GET /api/v1/admin/stats
  ├─ GET /api/v1/admin/top-users
  ├─ GET /api/v1/admin/language-usage
  └─ GET /api/v1/admin/problem-analytics
         │
         ▼
Each endpoint queries database:
  ├─ Stats: Aggregate counts & rates
  ├─ Top Users: ORDER BY score DESC LIMIT 20
  ├─ Language Usage: GROUP BY language
  └─ Problem Analytics: JOIN + GROUP BY
         │
         ▼
Return aggregated data
         │
         ▼
Frontend renders:
  ├─ Stats cards
  ├─ Top users table
  ├─ Problem analytics table
  └─ Language usage grid
```

## Scalability Considerations

### Current Architecture (Single Server)
- Suitable for: 100-1000 concurrent users
- Bottleneck: Code execution (Docker containers)

### Horizontal Scaling Strategy

```
┌──────────────────────────────────────────────────┐
│              Load Balancer (Nginx)                │
└────────────┬─────────────────────┬────────────────┘
             │                     │
             ▼                     ▼
┌─────────────────────┐  ┌─────────────────────┐
│  FastAPI Instance 1  │  │  FastAPI Instance 2  │
└──────────┬──────────┘  └──────────┬───────────┘
           │                         │
           └───────────┬─────────────┘
                       │
                       ▼
           ┌────────────────────────┐
           │   Shared PostgreSQL     │
           └────────────────────────┘
```

**For Heavy Load**:
- Add message queue (RabbitMQ/Redis) for submissions
- Separate execution workers
- Shared storage for code (S3/NFS)
- Redis for session storage
- Database read replicas

### Performance Optimizations

**Already Implemented**:
- ✅ Database connection pooling
- ✅ Async I/O (non-blocking)
- ✅ Proper indexes
- ✅ Rate limiting
- ✅ Container cleanup

**Future Enhancements**:
- Caching (Redis) for:
  - Leaderboard
  - Problem list
  - User profiles
- CDN for frontend assets
- Database query optimization
- Code execution queue

## Technology Choices Rationale

| Component | Technology | Why? |
|-----------|-----------|------|
| Frontend | SvelteKit | Minimal bundle, reactive, fast |
| Backend | FastAPI | Async, fast, auto docs, type hints |
| Database | PostgreSQL | ACID, relations, JSON support, mature |
| Auth | JWT | Stateless, scalable, standard |
| Execution | Docker | Isolation, multi-language, security |
| AI | Ollama | Local inference, privacy, no API costs |
| Vector DB | ChromaDB | Embedded, easy setup, Python-friendly |
| Styling | TailwindCSS | Rapid development, consistent design |
| Editor | Monaco | Full IDE features, popular |

## Deployment Architecture

### Development
```
localhost:5173 (Frontend)
localhost:8000 (Backend)
localhost:5432 (PostgreSQL)
localhost:11434 (Ollama)
```

### Production (Recommended)
```
┌────────────────────────────────────────┐
│          Cloud Provider (AWS)           │
│                                         │
│  ┌──────────────────────────────────┐  │
│  │  Application Load Balancer        │  │
│  │  (HTTPS, SSL Termination)         │  │
│  └───────────┬──────────────────────┘  │
│              │                          │
│       ┌──────┴──────┐                  │
│       │             │                   │
│       ▼             ▼                   │
│  ┌─────────┐  ┌─────────┐             │
│  │ Backend │  │ Backend │             │
│  │   ECS   │  │   ECS   │             │
│  └────┬────┘  └────┬────┘             │
│       │            │                   │
│       └──────┬─────┘                   │
│              │                          │
│              ▼                          │
│       ┌────────────┐                   │
│       │    RDS     │                   │
│       │ PostgreSQL │                   │
│       └────────────┘                   │
│                                         │
│       ┌────────────┐                   │
│       │     S3     │                   │
│       │ (Frontend) │                   │
│       └────────────┘                   │
└────────────────────────────────────────┘
```

---

**This architecture provides**:
- ✅ Scalability
- ✅ Security
- ✅ Maintainability
- ✅ Observability
- ✅ Performance
- ✅ Extensibility
