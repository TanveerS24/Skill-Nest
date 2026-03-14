# SkillNest - Multi-Language Coding Platform

<div align="center">

**A production-ready coding platform for solving Data Structure & Algorithm problems with Docker sandbox execution, Redis caching, JWT authentication, and dynamic leaderboards.**

[![Java](https://img.shields.io/badge/Java-21-orange.svg)](https://www.oracle.com/java/)
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2-green.svg)](https://spring.io/projects/spring-boot)
[![SvelteKit](https://img.shields.io/badge/SvelteKit-2.0-orange.svg)](https://kit.svelte.dev/)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)](https://www.postgresql.org/)
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
| **Spring Boot** | 3.2.0 | REST API framework |
| **Spring Data JPA** | 3.2.0 | ORM with Hibernate |
| **Spring Security** | 3.2.0 | Authorization & authentication |
| **PostgreSQL** | 16 | Primary database |
| **Redis** | 7 | Caching & leaderboard ranking |
| **Docker Java SDK** | 3.3.4 | Container management for code execution |
| **JJWT** | 0.12.3 | JWT token handling |
| **Lombok** | 1.18.30 | Code generation utilities |

### Frontend
| Technology | Version | Purpose |
|-----------|---------|---------|
| **SvelteKit** | 2.0 | Frontend framework |
| **TypeScript** | 5.3 | Type safety |
| **TailwindCSS** | 3.4 | Styling |
| **Monaco Editor** | 0.45 | Code editor |
| **Vite** | 5.0 | Build tool |

### Infrastructure
- **Docker** & **Docker Compose** - Containerization & orchestration
- **PostgreSQL 16** - Persistent data storage with connection pooling
- **Redis 7** - Caching layer for leaderboards & rankings
- **Nginx** (optional) - Reverse proxy for production
- **Java 21 JDK** - Runtime environment

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
│   Spring Boot   │      │
│   Backend       │      │
│   (Java 21)     │      │
│                 │      │
└────┬─────┬──────┘      │
     │     │             │
     │     │             │
┌────▼──┐ ┌▼────────┐   │
│       │ │         │   │
│PostgreSQL│ Redis │   │
│  (JPA)  │(Caching)   │
└───────┘ └─────────┘   │
     │                  │
     │                  │
┌────▼──────────────┐   │
│                   │   │
│  Docker Engine    │   │
│  (Code Execution) │───┘
│  (docker-java)    │
│                   │
└───────────────────┘
```

### Request Flow

1. **User submits code** → Frontend redirects to Spring Boot (SvelteKit)
2. **JWT validation** → Spring Security filter
3. **Code execution** → Docker container orchestration via docker-java SDK
4. **Result storage** → PostgreSQL via Spring Data JPA/Hibernate
5. **Leaderboard cache** → Redis via Spring Data Redis (@Cacheable)
6. **Response** → REST controller returns JSON response

---

## 📦 Prerequisites

### Required Software
- **Docker** (20.10+) and **Docker Compose** (2.0+)
- **Java 21 JDK** (for local development and building)
- **Maven** 3.9+ (build tool)
- **Node.js** 20+ (for frontend development)
- **Git**
- **PostgreSQL 16** (can run via Docker)
- **Redis 7** (can run via Docker)

### Optional
- **Kubernetes** (for production scaling)
- **Nginx** (for reverse proxy)

---

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd skillnest
```

### 2. Verify Prerequisites

```bash
# Verify Java 21 is installed
java -version

# Verify Maven is installed
mvn -version

# Verify Docker is installed
docker --version
```

### 3. Configure Backend Environment

Edit `backend/src/main/resources/application.properties`:

```properties
# Server Configuration
server.port=8080
server.servlet.context-path=/api

# Database Configuration
spring.datasource.url=jdbc:postgresql://localhost:5432/skillnest_db
spring.datasource.username=skillnest
spring.datasource.password=skillnest123
spring.jpa.hibernate.ddl-auto=update
spring.jpa.show-sql=false

# Redis Configuration
spring.data.redis.host=localhost
spring.data.redis.port=6379
spring.cache.type=redis

# JWT Configuration
jwt.secret=your-secret-key-change-this-in-production-minimum-32-characters-long
jwt.expiration-ms=900000  # 15 minutes
jwt.refresh-expiration-ms=604800000  # 7 days

# Docker Configuration
docker.host=unix:///var/run/docker.sock  # On Windows: tcp://localhost:2375

# CORS Configuration
cors.allowed-origins=http://localhost:5173,http://localhost:3000
```

### 4. Pull Required Docker Images

```bash
# These will be automatically pulled when code execution is needed
docker pull python:3.11-slim
docker pull openjdk:21-slim
docker pull gcc:13
docker pull ubuntu:22.04  # For C++ compilation
```

---

## 🏃 Running the Application

### Option 1: Using Docker Compose (Recommended)

```bash
# Start all services (PostgreSQL, Redis, Spring Boot Backend, SvelteKit Frontend)
docker-compose -f docker-compose-springboot.yml up -d

# View logs
docker-compose -f docker-compose-springboot.yml logs -f

# Stop all services
docker-compose -f docker-compose-springboot.yml down
```

Services will be available at:
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8080/api
- **Health Check:** http://localhost:8080/api/health

### Option 2: Local Development

#### Backend (Spring Boot)

```bash
cd backend

# Build the project
mvn clean package

# Install dependencies
mvn install

# Start PostgreSQL and Redis (if not already running)
docker-compose up -d postgres redis

# Run Spring Boot application
mvn spring-boot:run

# OR run the JAR directly
java -jar target/skilnest-1.0.0.jar
```

#### Frontend (SvelteKit)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Access at http://localhost:5173
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
**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "tokenType": "Bearer",
  "refreshToken": "eyJhbGciOiJIUzI1NiIs..."
}
```

Includes `refreshToken` in secure HttpOnly cookie.

#### POST `/auth/refresh`
Refresh access token using refresh token from cookie.

**Response:**
```json
{
  "accessToken": "eyJhbGciOiJIUzI1NiIs...",
  "tokenType": "Bearer"
}
```

#### GET `/auth/me`
Get current user information (requires authentication).

**Response:**
```json
{
  "id": 1,
  "email": "user@example.com",
  "role": "USER",
  "createdAt": "2026-03-04T10:00:00Z"
}
```

### Problems Endpoints

#### GET `/problems`
Get all problems with pagination (anonymous access allowed).

**Query Parameters:**
- `page`: Page number (0-indexed)
- `size`: Results per page (default: 20)
- `sort`: Sort criteria

**Response:**
```json
{
  "content": [
    {
      "id": 1,
      "title": "Two Sum",
      "description": "...",
      "difficulty": "EASY",
      "timeLimit": 5,
      "memoryLimit": 256,
      "createdAt": "2026-03-04T10:00:00Z"
    }
  ],
  "totalElements": 50,
  "totalPages": 3,
  "currentPage": 0,
  "pageSize": 20
}
```

#### GET `/problems/{id}`
Get problem details with non-hidden test cases and submission details.

#### POST `/problems`
Create new problem (admin only).

### Submissions Endpoints

#### POST `/submissions`
Submit code for a problem (requires authentication).

**Request:**
```json
{
  "problemId": 1,
  "language": "PYTHON",
  "code": "def solution():\n    pass"
}
```

**Response:**
```json
{
  "id": 1,
  "userId": 1,
  "problemId": 1,
  "language": "PYTHON",
  "verdict": "ACCEPTED",
  "runtime": 45.23,
  "memory": 12.5,
  "output": "Test passed",
  "createdAt": "2026-03-04T10:00:00Z"
}
```

#### GET `/submissions`
Get user submissions with pagination (requires authentication).

#### GET `/submissions/problem/{problemId}`
Get all submissions for a specific problem.

### Leaderboard Endpoints

#### GET `/leaderboard`
Get leaderboard with user rankings.

**Response:**
```json
[
  {
    "userId": 1,
    "email": "user@example.com",
    "problemsSolved": 5,
    "totalSubmissions": 12,
    "rank": 1
  }
]
```

### Admin Endpoints

#### GET `/admin/all-testcases/{problemId}`
Get all test cases including hidden ones (admin only).
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
- Spring Validation annotations across all DTOs
- SQL injection prevention via Spring Data JPA (JPQL/Native Query parameterization)
- XSS protection in frontend with proper encoding

---

## 🧪 Testing

### Run Backend Tests (JUnit 5)

```bash
cd backend

# Run all tests
mvn test

# Run specific test clase
mvn test -Dtest=AuthServiceTest

# Run with coverage
mvn test jacoco:report
```

### Run Frontend Tests

```bash
cd frontend
npm run test
```

### Manual Testing

Use the provided demo accounts:
- **Admin:** admin@skillnest.com / password123
- **User:** user@test.com / password123

---

## 🚢 Deployment

### Production Checklist

- [ ] Change `jwt.secret` to a strong random value (min 32 characters)
- [ ] Enable HTTPS (use Nginx with Let's Encrypt or cloud loadbalancer)
- [ ] Set `server.ssl.enabled=true` in application.properties
- [ ] Use production database credentials
- [ ] Configure proper CORS origins in SecurityConfig.java
- [ ] Set up monitoring (Spring Boot Actuator, Prometheus)
- [ ] Configure log aggregation (ELK stack)
- [ ] Set up automated database backups
- [ ] Use managed Redis service (AWS ElastiCache, Azure Redis)
- [ ] Configure CDN/Object storage for static assets

### Docker Production Build

```bash
# Build production JAR
mvn clean package -DskipTests=true

# Build Docker image
docker build -t skillnest-backend:latest -f backend/Dockerfile .

# Run production container
docker run -d \
  --name skillnest-backend \
  -e DATABASE_URL=jdbc:postgresql://prod-db:5432/skillnest \
  -e REDIS_HOST=prod-redis \
  -p 8080:8080 \
  skillnest-backend:latest
```

### Kubernetes Deployment

```bash
# Deploy to Kubernetes cluster
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Scale application
kubectl scale deployment skillnest-backend --replicas=3 -n skillnest

# Monitor deployment
kubectl logs -f deployment/skillnest-backend -n skillnest
```

---

## 🐛 Troubleshooting

### Spring Boot Application Issues

```bash
# Check if port 8080 is already in use
lsof -i :8080  # On Windows: netstat -ano | findstr :8080

# Check application logs
tail -f backend/logs/application.log

# Check application health
curl http://localhost:8080/api/health
```

### Database Connection Errors

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Connect to database
docker exec -it skillnest-postgres psql -U skillnest -d skillnest_db

# Verify tables were created
\dt

# Check Hibernate logs
# Set spring.jpa.show-sql=true in application.properties
```

### Redis Connection Errors

```bash
# Test Redis connection
docker exec -it skillnest-redis redis-cli ping

# Check Redis keys
docker exec -it skillnest-redis redis-cli KEYS '*'

# Clear Redis cache if needed
docker exec -it skillnest-redis redis-cli FLUSHALL
```

### Code Execution Failures

```bash
# Check Docker daemon is running
docker info

# Pull required execution images
docker pull python:3.11-slim
docker pull openjdk:21-slim
docker pull gcc:13
docker pull ubuntu:22.04

# Check Docker socket permissions (Linux)
ls -la /var/run/docker.sock

# Check container execution logs
docker logs <container_id>
```

### Compilation/Build Errors

```bash
# Clean rebuild
mvn clean install

# Skip tests for faster build
mvn clean package -DskipTests=true

# Check Java version
java -version

# Check Maven version
mvn -version
```

---

## 🔄 Initial Data

The platform includes 6 seeded DSA problems accessible via:
- `/api/problems` endpoint after application starts
- Problems include: Two Sum, Valid Parentheses, Reverse Linked List, Binary Search, Merge Sorted Arrays, Longest Substring

To add custom problems:
- Use POST `/api/problems` endpoint (admin only)
- Include title, description, difficulty, and test cases
- Test cases can be marked as hidden for hidden test suite

---

## 📝 API Rate Limits

| Endpoint | Limit | Window | Notes |
|----------|-------|--------|-------|
| `/submissions` (POST) | Per problem | Per minute | Prevents spam submissions |
| Other endpoints | Unlimited | - | Read-only endpoints not rate-limited |

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

- Spring Boot for the robust backend framework
- Spring Security for comprehensive authentication
- Spring Data JPA for elegant ORM
- SvelteKit for the modern frontend
- Monaco Editor by Microsoft
- Docker for secure containerization
- Redis for high-performance caching

---

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [CONTRIBUTING.md](CONTRIBUTING.md) file
- Review [troubleshooting](#-troubleshooting) section

---

<div align="center">

**Built with ❤️ using Java Spring Boot & SvelteKit**

⭐ Star this repository if you find it helpful!

Powered by Spring Boot • PostgreSQL • Docker • Redis

</div>