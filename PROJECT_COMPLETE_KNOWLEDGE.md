# SkillNest - Complete Technical Knowledge & Architecture Guide

**Version:** 1.0.0  
**Project Type:** Multi-Language Coding Platform  
**Date:** 2026-04-27

---

## 📋 Table of Contents

1. [Project Overview](#project-overview)
2. [Problem Statement & Solution](#problem-statement--solution)
3. [Technology Stack](#technology-stack)
4. [Complete Architecture](#complete-architecture)
5. [Database Schema & Models](#database-schema--models)
6. [Core Business Logic](#core-business-logic)
7. [API Endpoints & Flow](#api-endpoints--flow)
8. [Authentication & Security](#authentication--security)
9. [Code Execution Pipeline](#code-execution-pipeline)
10. [Leaderboard System](#leaderboard-system)
11. [File Structure Deep Dive](#file-structure-deep-dive)
12. [Key Algorithms & Patterns](#key-algorithms--patterns)
13. [Data Flow Diagrams](#data-flow-diagrams)

---

## Project Overview

### What is SkillNest?

SkillNest is a **production-ready, cloud-native competitive programming platform** that allows users to:

- ✅ Solve Data Structure & Algorithm (DSA) problems in **4 languages** (Python, Java, C, C++)
- ✅ Submit code for execution in **isolated Docker containers** with resource limits
- ✅ Get **real-time feedback** on test cases (passed/failed)
- ✅ View **AI-powered code analysis** (complexity estimation, security scanning)
- ✅ Track performance through **dynamic, multi-criteria leaderboards**
- ✅ Access **admin dashboard** for platform analytics
- ✅ Browse problems **anonymously** without login

### Key Differentiators

1. **Multi-Language Support**: Python, Java, C, C++ with language-specific execution
2. **Sandbox Execution**: Docker containers with CPU/Memory/PID limits for security
3. **AI Integration**: OpenAI-powered complexity analysis and malicious code detection
4. **Redis Caching**: 5-minute TTL leaderboard caching + rate limiting (30 submissions/min)
5. **JWT Authentication**: 15-min access token + 7-day refresh token with HttpOnly cookies
6. **Real-time Leaderboards**: 4 ranking criteria (problems solved, avg time complexity, avg space complexity, submission count)

---

## Problem Statement & Solution

### The Problem

Competitive programming learners need a platform that:
1. Provides a safe, isolated environment for code execution
2. Supports multiple programming languages
3. Gives instant feedback on code correctness
4. Analyzes code quality (complexity, security)
5. Motivates learning through transparent rankings
6. Handles high server loads efficiently

### The Solution

SkillNest solves this through:

| Problem | Solution |
|---------|----------|
| **Code Safety** | Docker containers with resource limits (0.5 CPU, 256MB RAM, read-only FS, no network) |
| **Multi-Language** | Docker images for Python, Java, C, C++ with language-specific runners |
| **Instant Feedback** | Real-time test case execution against visible + hidden test cases |
| **Quality Analysis** | AI-powered complexity estimation (O(1) to O(n²)) + malicious pattern detection |
| **Motivation** | Redis-cached leaderboards with multiple ranking criteria |
| **High Availability** | Horizontal scaling via Docker Compose, rate limiting against abuse, connection pooling |

---

## Technology Stack

### Backend Services

| Layer | Technology | Reason | Version |
|-------|-----------|--------|----------|
| **API Framework** | Spring Boot | Enterprise-grade, battle-tested REST framework | 3.2.0 |
| **Language** | Java | Performance, type safety, rich ecosystem | 21 (LTS) |
| **ORM** | Spring Data JPA + Hibernate | Automatic SQL generation, relationship mapping | 3.2.0 |
| **Database** | PostgreSQL | ACID compliance, complex queries, JSON support | 16 |
| **Cache Layer** | Redis | In-memory caching, rate limiting, pub/sub | 7 |
| **Container Control** | Docker Java SDK | Programmatic Docker API for code execution | 3.3.4 |
| **Authentication** | JJWT | JWT token generation/validation | 0.12.3 |
| **Build Tool** | Maven | Dependency management, multi-module support | 3.9+ |

### AI Service

| Component | Technology | Purpose | Version |
|-----------|-----------|---------|----------|
| **Framework** | FastAPI | Lightweight async API, auto-documentation | 0.109.0 |
| **Server** | Uvicorn | ASGI server for FastAPI | 0.27.0 |
| **ORM** | SQLAlchemy | Python-based ORM for DB operations | 2.0.25 |
| **DB Driver** | Psycopg2 | PostgreSQL dialect for SQLAlchemy | 2.9.9 |
| **Cache Client** | Redis-py | Redis connection pooling and commands | 5.0.1 |
| **Embeddings** | ChromaDB | Vector embeddings for RAG (Retrieval-Augmented Generation) | 0.4.22 |
| **HTTP Client** | Httpx | Async HTTP requests for external APIs | 0.26.0 |
| **Validation** | Pydantic | Data validation using Python type hints | 2.5.3 |

### Frontend

| Component | Technology | Purpose | Version |
|-----------|-----------|---------|----------|
| **Framework** | SvelteKit | Modern, fast web framework with file-based routing | 2.0 |
| **Language** | TypeScript | Type-safe JavaScript | 5.3.3 |
| **Styling** | Tailwind CSS | Utility-first CSS framework | 3.4.0 |
| **Code Editor** | Monaco Editor | VS Code's editor component | 0.45.0 |
| **Build Tool** | Vite | Lightning-fast build tool and dev server | 5.0.0 |
| **CSS Processing** | PostCSS | CSS transformation pipeline | 8.4.32 |

### Infrastructure

- **Containerization**: Docker + Docker Compose
- **Orchestration**: Docker Compose (development), Kubernetes-ready (production)
- **Database Connection Pooling**: HikariCP (Spring Boot default)
- **Reverse Proxy** (Optional): Nginx for production load balancing
- **Monitoring** (Future): ELK Stack, Prometheus, Grafana

---

## Complete Architecture

### System Design Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                          USER BROWSER                               │
│   (Chrome, Firefox, Safari accessing http://localhost:5173)         │
└────────────────────────────┬────────────────────────────────────────┘
                             │ HTTP/WebSocket
                             │
        ┌────────────────────▼────────────────────┐
        │     SvelteKit Frontend (Vite)          │
        │  - React to user interactions          │
        │  - Monaco Editor for code input        │
        │  - Real-time leaderboard updates       │
        │  Port: 5173                            │
        └────────────────────┬────────────────────┘
                             │ REST API Calls
                             │
   ┌─────────────────────────▼─────────────────────────┐
   │     Spring Boot API Gateway (Java 21)            │
   │  Port: 8080 (/api endpoint)                      │
   │                                                   │
   │  ┌───────────────────────────────────────────┐   │
   │  │ JWT Security Filter                       │   │
   │  │ - Validate Authorization header           │   │
   │  │ - Extract user ID from token              │   │
   │  │ - Rate limiting (30 req/min)              │   │
   │  └───────────────────────────────────────────┘   │
   │                                                   │
   │  ┌─────────────────────────────────────────┐     │
   │  │ Controllers                             │     │
   │  │ - UserController (auth/profile)         │     │
   │  │ - ProblemController (browse problems)   │     │
   │  │ - SubmissionController (submit code)    │     │
   │  │ - LeaderboardController (rankings)      │     │
   │  │ - AdminController (stats/analytics)     │     │
   │  └──────────┬──────────────────────────────┘     │
   │             │                                     │
   │  ┌──────────▼────────────────────────────────┐   │
   │  │ Services (Business Logic)                │   │
   │  │ - AuthenticationService (JWT/password)  │   │
   │  │ - SubmissionService (execution logic)   │   │
   │  │ - CodeExecutionService (Docker API)     │   │
   │  │ - LeaderboardService (ranking calc)     │   │
   │  │ - AnalyticsService (admin stats)        │   │
   │  └──────────┬──────────────────────────────┘   │
   │             │                                    │
   └─────────────┼────────────────────────────────────┘
                 │
        ┌────────┴──────────┬──────────────┐
        │                   │              │
        ▼                   ▼              ▼
   ┌─────────────┐   ┌──────────────┐  ┌────────────────┐
   │ PostgreSQL  │   │  Redis       │  │ Docker Engine  │
   │    16       │   │    7         │  │                │
   │             │   │              │  │ ┌────────────┐ │
   │ Tables:     │   │ Cache:       │  │ │ Python     │ │
   │ - users     │   │ - Problem    │  │ │ Container  │ │
   │ - problems  │   │ - Test cases │  │ └────────────┘ │
   │ - test_cases│   │ - Leaderboard   │ │ ┌────────────┐ │
   │ - submissions   │ - User stats  │  │ │ Java       │ │
   │ - analytics    │ - Submission  │  │ │ Container  │ │
   │             │   │   results    │  │ └────────────┘ │
   │ Indexes:    │   │              │  │ ┌────────────┐ │
   │ - idx_created_at │  TTL: 5min  │  │ │ C/C++      │ │
   │ - idx_user_problem       │  │ Container  │ │
   │ - idx_difficulty    │              │ └────────────┘ │
   │             │   │              │  │                │
   └─────────────┘   └──────────────┘  └────────────────┘
        │                   │              
        │                   │              
        └─────────────┬─────────────┘
                      │
        ┌─────────────▼──────────────────┐
        │   FastAPI AI Service (Python)   │
        │   Port: 8000 (/docs for API)   │
        │                                │
        │ Routes:                         │
        │ - /execute/run (dry run)       │
        │ - /execute/submit (final)      │
        │ - /generate (AI questions)     │
        │ - /health (status check)       │
        └─────────────┬──────────────────┘
                      │
                      ▼
           ┌──────────────────┐
           │   SQLAlchemy     │
           │   ORM (Python)   │
           └────────┬─────────┘
                    │
        ┌───────────▼──────────────┐
        │   PostgreSQL (AI DB)     │
        │                          │
        │ Tables:                  │
        │ - questions (DSA)        │
        │ - test_cases            │
        │ - submissions (RAG DB)  │
        │ - submission_results    │
        └──────────────────────────┘
```

### Request Flow: Code Submission

```
┌─────────────────────────────────────────────────────────────────┐
│ STEP 1: User Interface (Frontend)                               │
│ - User selects problem, chooses language, writes code          │
│ - Clicks "Submit"                                               │
│ - Frontend collects: { problemId, code, language }             │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 2: HTTP POST /api/submissions                             │
│ - SvelteKit frontend sends POST request with JWT in header     │
│ - Headers: Authorization: Bearer eyJhbGc...                    │
│ - Body: { problemId: 5, language: "python", code: "..." }     │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 3: Spring Boot Security Filter                            │
│ - JwtAuthenticationFilter intercepts request                   │
│ - Validates JWT token expiration and signature                │
│ - Extracts userId from token claims                           │
│ - Sets SecurityContext (user ID: 42)                          │
│ - Rate limit check: user 42 < 30 submissions/min ✓            │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 4: SubmissionController.submitCode()                      │
│ - @PostMapping endpoint receives request                       │
│ - Extracts userId (42) from Authentication object             │
│ - Validates SubmissionCreateDto (JSON parsing)                │
│ - Delegates to SubmissionService.submitCode()                 │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 5: SubmissionService.submitCode()                         │
│ - Fetch User entity from DB by ID (42)                        │
│ - Fetch Problem entity from DB by problemId (5)               │
│ - Fetch ALL TestCases for problem (visible + hidden)          │
│ - Initialize: finalVerdict=ACCEPTED, totalRuntime=0, maxMemory=0  │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 6: Test Case Loop (foreach TestCase)                      │
│ - For each test case (visible and hidden):                    │
│   - Call CodeExecutionService.executeCode()                   │
│   - Pass: code, language, input, timeLimit, memoryLimit       │
│   - Receive: ExecutionResult { verdict, output, runtime, etc} │
│                                                                │
│ Execution Results Scenarios:                                   │
│ ┌─────────────────────────────────────────────────────┐       │
│ │ 1. ACCEPTED: Output matches expected               │       │
│ │    - totalRuntime += result.getRuntime()           │       │
│ │    - if (result.getMemory() > maxMemory)          │       │
│ │        maxMemory = result.getMemory()             │       │
│ │                                                     │       │
│ │ 2. WRONG_ANSWER: Output doesn't match             │       │
│ │    - finalVerdict = WRONG_ANSWER                  │       │
│ │    - BREAK LOOP (don't test hidden cases)         │       │
│ │                                                     │       │
│ │ 3. TIME_LIMIT_EXCEEDED: > 5 seconds               │       │
│ │    - finalVerdict = TIME_LIMIT_EXCEEDED           │       │
│ │    - BREAK LOOP                                   │       │
│ │                                                     │       │
│ │ 4. MEMORY_LIMIT_EXCEEDED: > 256 MB                │       │
│ │    - finalVerdict = MEMORY_LIMIT_EXCEEDED         │       │
│ │    - BREAK LOOP                                   │       │
│ │                                                     │       │
│ │ 5. RUNTIME_ERROR: Segmentation fault, NULL ref   │       │
│ │    - finalVerdict = RUNTIME_ERROR                 │       │
│ │    - BREAK LOOP                                   │       │
│ └─────────────────────────────────────────────────────┘       │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 7: Create Submission Entity                               │
│ - Build Submission object                                      │
│ - Set verdict (ACCEPTED, WRONG_ANSWER, etc.)                  │
│ - Calculate average runtime: totalRuntime / testCases.size()  │
│ - Set max memory used                                         │
│ - Persist to PostgreSQL                                       │
│                                                                │
│ SQL: INSERT INTO submissions                                  │
│      (user_id, problem_id, language, code, verdict,          │
│       runtime, memory, created_at)                            │
│      VALUES (42, 5, 'python', '...', 'ACCEPTED', ...)        │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 8: Invalidate Cache                                       │
│ - DELETE Redis key: leaderboard:*                             │
│   (Leaderboard will recalculate on next request)              │
│ - DELETE Redis key: user:42:stats                             │
│   (User stats will refresh)                                   │
│ - This triggers leaderboard recalculation with new data       │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 9: Return Response (SubmissionResponseDto)                │
│ - HTTP 201 CREATED                                             │
│ - Body: {                                                      │
│     "id": 1001,                                               │
│     "userId": 42,                                             │
│     "problemId": 5,                                           │
│     "language": "python",                                     │
│     "code": "...",                                            │
│     "verdict": "ACCEPTED",                                    │
│     "runtime": 0.234,                                         │
│     "memory": 15.6,                                           │
│     "timeComplexity": "O(n)",                                 │
│     "spaceComplexity": "O(1)",                                │
│     "createdAt": "2026-04-27T10:30:00"                       │
│   }                                                            │
└────────────────┬────────────────────────────────────────────────┘
                 │
┌────────────────▼────────────────────────────────────────────────┐
│ STEP 10: Frontend Updates UI                                   │
│ - Display "ACCEPTED ✓" in green                               │
│ - Show execution time: 234ms                                  │
│ - Show memory used: 15.6 MB                                   │
│ - Refresh leaderboard (fetch new rankings)                    │
│ - Update user dashboard                                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## Database Schema & Models

### ER Diagram

```
┌──────────────────────┐
│      USERS           │
├──────────────────────┤
│ id (PK)              │
│ email (UNIQUE)       │
│ password (hashed)    │
│ role (USER/ADMIN)    │
│ created_at           │
└───────────┬──────────┘
            │
            │ (1 to many)
            │
            ▼
┌──────────────────────┐
│   SUBMISSIONS        │
├──────────────────────┤
│ id (PK)              │
│ user_id (FK)         │
│ problem_id (FK)      │
│ language             │
│ code (TEXT)          │
│ verdict              │
│ runtime              │
│ memory               │
│ time_complexity      │
│ space_complexity     │
│ created_at           │
└──────────────────────┘
            │
            │ (has many)
            │
            ▼
┌──────────────────────┐
│   PROBLEMS           │
├──────────────────────┤
│ id (PK)              │
│ title (UNIQUE)       │
│ description (TEXT)   │
│ difficulty           │
│ time_limit (sec)     │
│ memory_limit (MB)    │
│ created_at           │
└──────────┬───────────┘
           │
           │ (1 to many)
           │
           ▼
┌──────────────────────┐
│   TEST_CASES         │
├──────────────────────┤
│ id (PK)              │
│ problem_id (FK)      │
│ input (TEXT)         │
│ expected_output      │
│ is_hidden (BOOL)     │
│ order_index          │
│ is_sample (BOOL)     │
└──────────────────────┘
```

### Detailed Schema

#### Users Table
```sql
CREATE TABLE users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,  -- bcrypt hashed
    role ENUM('USER', 'ADMIN') DEFAULT 'USER',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_email (email)
);
```

**Java Entity:**
```java
@Entity
@Table(name = "users")
@Data
@Builder
public class User implements UserDetails {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Email
    @Column(unique = true, nullable = false)
    private String email;
    
    @Column(nullable = false)
    private String password;
    
    @Enumerated(EnumType.STRING)
    @Builder.Default
    private UserRole role = UserRole.USER;
    
    @Column(updatable = false)
    private LocalDateTime createdAt;
    
    @OneToMany(mappedBy = "user", cascade = CascadeType.ALL)
    private List<Submission> submissions;
    
    // UserDetails implementations
    @Override
    public Collection<? extends GrantedAuthority> getAuthorities() {
        return Collections.singletonList(
            new SimpleGrantedAuthority("ROLE_" + role.name())
        );
    }
    
    @Override
    public String getUsername() {
        return this.email;
    }
    
    @Override
    public boolean isAccountNonExpired() {
        return true;
    }
    
    @Override
    public boolean isAccountNonLocked() {
        return true;
    }
    
    @Override
    public boolean isCredentialsNonExpired() {
        return true;
    }
    
    @Override
    public boolean isEnabled() {
        return true;
    }
}
```

#### Problems Table
```sql
CREATE TABLE problems (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    difficulty ENUM('EASY', 'MEDIUM', 'HARD') NOT NULL,
    time_limit INT DEFAULT 5,  -- seconds
    memory_limit INT DEFAULT 256,  -- MB
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_difficulty (difficulty),
    INDEX idx_title (title)
);
```

**Sample Data:**
```sql
INSERT INTO problems (title, difficulty, description) VALUES
('Two Sum', 'EASY', 'Given an array of integers, find two numbers that add up to target'),
('Valid Parentheses', 'EASY', 'Check if brackets, braces, and parentheses are balanced'),
('Binary Search', 'MEDIUM', 'Implement binary search on sorted array'),
('Longest Substring', 'MEDIUM', 'Find longest substring without repeating characters'),
('Word Ladder', 'HARD', 'Transform word to another using dictionary');
```

#### Test Cases Table
```sql
CREATE TABLE test_cases (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    problem_id BIGINT NOT NULL,
    input TEXT NOT NULL,
    expected_output TEXT NOT NULL,
    is_hidden BOOLEAN DEFAULT FALSE,
    is_sample BOOLEAN DEFAULT FALSE,
    order_index INT DEFAULT 0,
    FOREIGN KEY (problem_id) REFERENCES problems(id),
    INDEX idx_problem (problem_id)
);
```

**Sample Data (Two Sum Problem):**
```sql
INSERT INTO test_cases (problem_id, input, expected_output, is_hidden, is_sample) VALUES
(1, '[2,7,11,15]\n9', '[0,1]', FALSE, TRUE),
(1, '[3,2,4]\n6', '[1,2]', FALSE, TRUE),
(1, '[3,3]\n6', '[0,1]', TRUE, FALSE);  -- Hidden test case
```

#### Submissions Table
```sql
CREATE TABLE submissions (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    problem_id BIGINT NOT NULL,
    language ENUM('PYTHON', 'JAVA', 'CPP', 'C') NOT NULL,
    code LONGTEXT NOT NULL,
    verdict ENUM('ACCEPTED', 'WRONG_ANSWER', 'TIME_LIMIT_EXCEEDED', 
                 'MEMORY_LIMIT_EXCEEDED', 'RUNTIME_ERROR') NOT NULL,
    runtime DECIMAL(10,2),  -- milliseconds
    memory DECIMAL(10,2),   -- MB
    time_complexity VARCHAR(50),  -- O(n), O(log n), etc.
    space_complexity VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (problem_id) REFERENCES problems(id),
    INDEX idx_created_at (created_at),
    INDEX idx_user_problem (user_id, problem_id)
);
```

**Verdict Enum:**
```java
public enum Verdict {
    ACCEPTED,              // All test cases passed
    WRONG_ANSWER,          // Output doesn't match expected
    TIME_LIMIT_EXCEEDED,   // Execution > 5 seconds
    MEMORY_LIMIT_EXCEEDED, // Memory usage > 256 MB
    RUNTIME_ERROR          // Crash, segfault, null pointer, etc.
}
```

---

## Core Business Logic

### 1. Authentication Flow

#### JWT Token Generation

```java
// JwtTokenProvider.java
@Component
public class JwtTokenProvider {
    
    @Value("${JWT_SECRET_KEY:skillnest-secret-key-change-in-production}")
    private String secretKey;
    
    @Value("${JWT_ACCESS_TOKEN_EXPIRATION:900}")  // 15 minutes in seconds
    private long accessTokenExpiration;
    
    @Value("${JWT_REFRESH_TOKEN_EXPIRATION:604800}")  // 7 days in seconds
    private long refreshTokenExpiration;
    
    public String generateAccessToken(Long userId) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + accessTokenExpiration * 1000);
        
        return Jwts.builder()
                .setSubject(userId.toString())
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(SignatureAlgorithm.HS512, secretKey)
                .compact();
    }
    
    public String generateRefreshToken(Long userId) {
        Date now = new Date();
        Date expiryDate = new Date(now.getTime() + refreshTokenExpiration * 1000);
        
        return Jwts.builder()
                .setSubject(userId.toString())
                .claim("type", "refresh")
                .setIssuedAt(now)
                .setExpiration(expiryDate)
                .signWith(SignatureAlgorithm.HS512, secretKey)
                .compact();
    }
    
    public Long getUserIdFromToken(String token) {
        Claims claims = Jwts.parser()
                .setSigningKey(secretKey)
                .parseClaimsJws(token)
                .getBody();
        
        return Long.parseLong(claims.getSubject());
    }
    
    public boolean validateToken(String token) {
        try {
            Jwts.parser()
                .setSigningKey(secretKey)
                .parseClaimsJws(token);
            return true;
        } catch (JwtException | IllegalArgumentException e) {
            return false;
        }
    }
}
```

**Flow Diagram:**
```
Login Request (email, password)
         ▼
   ┌─────────────────────────┐
   │ Find User by Email      │
   │ (DB Query)              │
   └────────────┬────────────┘
                ▼
   ┌─────────────────────────┐
   │ Verify Password         │
   │ BCrypt.verify()         │
   │ match?                  │
   └────────────┬────────────┘
                │
        ┌───────┴───────┐
        │ YES           │ NO
        ▼               ▼
    ┌───────┐   ┌──────────────┐
    │Generate   │ 401 Unauthorized
    │Tokens     │
    │- Access  └──────────────┘
    │- Refresh 
    └────┬─────┘
         ▼
    ┌──────────────────────┐
    │ Return Tokens:       │
    │ - Access: JWT        │
    │ - Refresh: Cookie    │
    │   (HttpOnly, Secure) │
    └──────────────────────┘
```

#### JWT Validation Flow (Every Request)

```java
// JwtAuthenticationFilter.java
@Component
public class JwtAuthenticationFilter extends OncePerRequestFilter {
    
    @Autowired
    private JwtTokenProvider tokenProvider;
    
    @Override
    protected void doFilterInternal(
            HttpServletRequest request,
            HttpServletResponse response,
            FilterChain filterChain) throws ServletException, IOException {
        
        try {
            String token = getTokenFromRequest(request);
            
            if (token != null && tokenProvider.validateToken(token)) {
                Long userId = tokenProvider.getUserIdFromToken(token);
                
                // Create Authentication object
                Authentication authentication = 
                    new UsernamePasswordAuthenticationToken(
                        userId, 
                        null, 
                        getAuthorities(userId)
                    );
                
                SecurityContextHolder.getContext()
                    .setAuthentication(authentication);
            }
        } catch (Exception ex) {
            logger.error("Could not set user authentication", ex);
        }
        
        filterChain.doFilter(request, response);
    }
    
    private String getTokenFromRequest(HttpServletRequest request) {
        String bearerToken = request.getHeader("Authorization");
        if (bearerToken != null && bearerToken.startsWith("Bearer ")) {
            return bearerToken.substring(7);
        }
        return null;
    }
}
```

### 2. Code Execution Pipeline

#### Docker Container Management

```java
// CodeExecutionService.java
@Service
public class CodeExecutionService {
    
    @Autowired
    private DockerClient dockerClient;
    
    public ExecutionResult executeCode(
            String code,
            Language language,
            String input,
            int timeLimitSeconds,
            int memoryLimitMB) {
        
        try {
            // 1. Create container from appropriate image
            String imageId = getImageForLanguage(language);
            // imageId examples:
            // - python:3.11-slim
            // - openjdk:21-slim
            // - gcc:latest (for C/C++)
            
            // 2. Create container config
            ContainerConfig containerConfig = new ContainerConfig()
                    .withImage(imageId)
                    .withHostConfig(new HostConfig()
                        .withMemory(memoryLimitMB * 1024 * 1024L)  // Convert MB to bytes
                        .withCpuPeriod(100000L)
                        .withCpuQuota(50000L)  // 0.5 cores
                        .withPidsLimit(64L)
                        .withReadonlyRootfs(true)  // Read-only filesystem
                        .withNetworkMode("none")  // No network access
                    )
                    .withCmd(getRunCommand(language, code))
                    .withStdinOpen(true)
                    .withAttachStdin(true)
                    .withAttachStdout(true)
                    .withAttachStderr(true);
            
            // 3. Create container
            CreateContainerResponse container = 
                dockerClient.createContainerCmd(imageId)
                    .withHostConfig(containerConfig.getHostConfig())
                    // ... other configs
                    .exec();
            
            // 4. Start container
            dockerClient.startContainerCmd(container.getId()).exec();
            
            // 5. Execute code with timeout
            ExecutorService executor = Executors.newSingleThreadExecutor();
            Future<ExecResult> future = executor.submit(() -> 
                dockerClient.execStartCmd(
                    dockerClient.execCreateCmd(container.getId())
                        .withCmd("sh", "-c", getExecutionCommand(language, code))
                        .withAttachStdout(true)
                        .withAttachStderr(true)
                        .exec()
                        .getId()
                )
                .exec(new ResultCallback.Adapter<Frame>() {
                    // Handle output
                })
            );
            
            // 6. Wait with timeout (5 seconds + buffer)
            ExecResult result = future.get(timeLimitSeconds + 2, TimeUnit.SECONDS);
            
            // 7. Compare output
            ExecutionResult executionResult = compareOutputs(
                result.getStdout(),
                expectedOutput,
                timeLimitSeconds,
                memoryLimitMB
            );
            
            return executionResult;
            
        } catch (TimeoutException e) {
            return ExecutionResult.builder()
                .verdict(Verdict.TIME_LIMIT_EXCEEDED)
                .stderr("Execution exceeded " + timeLimitSeconds + " seconds")
                .build();
        } catch (Exception e) {
            return ExecutionResult.builder()
                .verdict(Verdict.RUNTIME_ERROR)
                .stderr(e.getMessage())
                .build();
        } finally {
            // 8. Clean up container
            try {
                dockerClient.stopContainerCmd(container.getId()).exec();
                dockerClient.removeContainerCmd(container.getId()).exec();
            } catch (Exception e) {
                logger.error("Failed to cleanup container", e);
            }
        }
    }
    
    private String[] getRunCommand(Language language, String code) {
        switch (language) {
            case PYTHON:
                return new String[]{"python3", "-c", code};
            case JAVA:
                return new String[]{"java", "-cp", ".", "Solution"};
            case CPP:
                return new String[]{"g++", "-o", "solution", "-", "&&", "./solution"};
            case C:
                return new String[]{"gcc", "-o", "solution", "-", "&&", "./solution"};
        }
    }
}
```

**Execution Flow Visualization:**

```
Code Received (Python, Java, C, C++)
         │
         ▼
    Pull Docker Image
    (if not exists)
    │
    ├─ openjdk:21-slim (for Java)
    ├─ python:3.11-slim (for Python)
    ├─ gcc:latest (for C/C++)
    │
    ▼
Create Container with Constraints:
├─ Memory: 256 MB
├─ CPU: 0.5 cores
├─ PID Limit: 64 processes
├─ Network: Disabled
├─ Filesystem: Read-only (except /tmp)
│
▼
Copy Code + Input into Container
│
▼
Execute Code (timeout: 5 sec + buffer)
│
    Record:
    ├─ Stdout (actual output)
    ├─ Stderr (error messages)
    ├─ Exit code
    ├─ Execution time
    ├─ Memory used
    │
    ▼
Compare Outputs:
    ├─ actual_output == expected_output?
    │   │
    │   ├─ YES → Verdict: ACCEPTED
    │   │
    │   └─ NO → Verdict: WRONG_ANSWER
    │
    ├─ Execution time > 5 sec?
    │   └─ YES → Verdict: TIME_LIMIT_EXCEEDED
    │
    ├─ Memory > 256 MB?
    │   └─ YES → Verdict: MEMORY_LIMIT_EXCEEDED
    │
    ├─ Exit code != 0?
    │   └─ YES → Verdict: RUNTIME_ERROR
    │
    ▼
Cleanup Container (stop + remove)
│
▼
Return ExecutionResult
```

### 3. Leaderboard & Ranking System

#### Leaderboard Calculation Logic

```java
// LeaderboardService.java
@Service
public class LeaderboardService {
    
    @Autowired
    private SubmissionRepository submissionRepository;
    
    @Autowired
    private RedisTemplate<String, Object> redisTemplate;
    
    private static final int CACHE_TTL_MINUTES = 5;
    
    @Cacheable(value = "leaderboard", 
               cacheManager = "redisCacheManager",
               unless = "#result == null")
    public List<LeaderboardEntryDto> getLeaderboard(String sortBy) {
        
        // sortBy options:
        // - "problems_solved" (default)
        // - "avg_time_complexity"
        // - "avg_space_complexity"
        // - "total_submissions"
        
        List<User> allUsers = userRepository.findAll();
        List<LeaderboardEntryDto> entries = new ArrayList<>();
        
        for (User user : allUsers) {
            // Count accepted problems
            long acceptedProblems = submissionRepository
                .countByUserIdAndVerdict(user.getId(), Verdict.ACCEPTED);
            
            // Get all accepted submissions
            List<Submission> acceptedSubmissions = submissionRepository
                .findByUserIdAndVerdict(user.getId(), Verdict.ACCEPTED);
            
            // Calculate average time complexity
            double avgTimeComplexity = calculateAverageComplexity(
                acceptedSubmissions,
                "timeComplexity"
            );
            
            // Calculate average space complexity
            double avgSpaceComplexity = calculateAverageComplexity(
                acceptedSubmissions,
                "spaceComplexity"
            );
            
            // Count total submissions
            long totalSubmissions = submissionRepository
                .countByUserId(user.getId());
            
            entries.add(LeaderboardEntryDto.builder()
                .userId(user.getId())
                .email(user.getEmail())
                .problemsSolved(acceptedProblems)
                .totalSubmissions(totalSubmissions)
                .avgTimeComplexity(avgTimeComplexity)
                .avgSpaceComplexity(avgSpaceComplexity)
                .build());
        }
        
        // Sort based on criteria
        switch (sortBy) {
            case "avg_time_complexity":
                entries.sort(Comparator
                    .comparingDouble(LeaderboardEntryDto::getAvgTimeComplexity)
                    .thenComparing(LeaderboardEntryDto::getProblemsSolved, 
                                 Comparator.reverseOrder()));
                break;
                
            case "avg_space_complexity":
                entries.sort(Comparator
                    .comparingDouble(LeaderboardEntryDto::getAvgSpaceComplexity)
                    .thenComparing(LeaderboardEntryDto::getProblemsSolved, 
                                 Comparator.reverseOrder()));
                break;
                
            case "total_submissions":
                entries.sort(Comparator
                    .comparingLong(LeaderboardEntryDto::getTotalSubmissions)
                    .reversed());
                break;
                
            case "problems_solved":  // default
            default:
                entries.sort(Comparator
                    .comparingLong(LeaderboardEntryDto::getProblemsSolved)
                    .reversed()
                    .thenComparing(LeaderboardEntryDto::getEmail));
                break;
        }
        
        // Add rank
        int rank = 1;
        for (LeaderboardEntryDto entry : entries) {
            entry.setRank(rank++);
        }
        
        // Cache for 5 minutes in Redis
        redisTemplate.opsForValue()
            .set("leaderboard:" + sortBy, entries, 
                 Duration.ofMinutes(CACHE_TTL_MINUTES));
        
        return entries;
    }
    
    private double calculateAverageComplexity(
            List<Submission> submissions,
            String complexityType) {
        
        // Complexity scoring system
        Map<String, Double> complexityScore = new HashMap<>();
        complexityScore.put("O(1)", 1.0);
        complexityScore.put("O(log n)", 2.0);
        complexityScore.put("O(n)", 3.0);
        complexityScore.put("O(n log n)", 4.0);
        complexityScore.put("O(n²)", 5.0);
        complexityScore.put("O(n³)", 6.0);
        complexityScore.put("O(2^n)", 7.0);
        complexityScore.put("O(n!)", 8.0);
        
        double sum = 0;
        for (Submission submission : submissions) {
            String complexity = complexityType.equals("timeComplexity") ?
                submission.getTimeComplexity() :
                submission.getSpaceComplexity();
            
            sum += complexityScore.getOrDefault(complexity, 5.0);
        }
        
        return submissions.isEmpty() ? 0 : sum / submissions.size();
    }
}
```

**Leaderboard Cache Mechanism:**

```
GET /api/leaderboard?sortBy=problems_solved
         │
         ▼
┌─────────────────────────────────┐
│ Check Redis Cache               │
│ Key: leaderboard:problems_solved│
└────────┬────────────────────────┘
         │
    ┌────┴───────┐
    │ CACHE HIT? │
    └────┬───────┘
         │
    ┌────┴─────────────────┐
    │ YES               NO │
    ▼                      ▼
  Return            ┌──────────────────┐
  Cached            │ Query DB:        │
  Results           │ - All users      │
    │               │ - Submissions    │
    │               │ - Test complexities
    │               └────────┬─────────┘
    │                        │
    │                        ▼
    │               ┌──────────────────────┐
    │               │ Calculate:           │
    │               │ - Problems solved    │
    │               │ - Avg time complex   │
    │               │ - Avg space complex  │
    │               │ - Total submissions  │
    │               └────────┬─────────────┘
    │                        │
    │                        ▼
    │               ┌──────────────────────┐
    │               │ Sort by criteria     │
    │               │ Add rank            │
    │               └────────┬─────────────┘
    │                        │
    │                        ▼
    │               ┌──────────────────────┐
    │               │ Cache in Redis       │
    │               │ TTL: 5 minutes      │
    │               └────────┬─────────────┘
    │                        │
    └────────────────┬───────┘
                     │
                     ▼
            Return Results to Client
```

---

## API Endpoints & Flow

### Authentication Endpoints

```
POST /api/auth/register
├─ Payload: { email, password }
├─ Validation: email format, password strength
├─ Response (201):
│  {
│    "token": "eyJhbGc...",
│    "refreshToken": "eyJhbGc...",
│    "userId": 5,
│    "email": "user@test.com"
│  }
└─ Errors: 400 (validation), 409 (email exists)

POST /api/auth/login
├─ Payload: { email, password }
├─ Process:
│  1. Find user by email
│  2. Verify BCrypt password
│  3. Generate JWT tokens
├─ Response (200):
│  {
│    "token": "eyJhbGc...",
│    "refreshToken": "eyJhbGc...",  // HttpOnly cookie
│    "userId": 5,
│    "email": "user@test.com",
│    "role": "USER"
│  }
└─ Errors: 401 (invalid credentials), 404 (user not found)

POST /api/auth/refresh
├─ Headers: Authorization: Bearer <accessToken>
├─ Process:
│  1. Validate refresh token in HttpOnly cookie
│  2. Generate new access token (15 min expiry)
├─ Response (200):
│  { "token": "eyJhbGc..." }
└─ Errors: 401 (unauthorized), 403 (forbidden)

POST /api/auth/logout
├─ Headers: Authorization: Bearer <token>
├─ Process:
│  1. Clear refresh token cookie
│  2. Blacklist token (optional)
├─ Response (200): { "message": "Logged out successfully" }
└─ Errors: 401 (unauthorized)
```

### Problem Endpoints

```
GET /api/problems
├─ Query Params:
│  - page: 0 (default)
│  - size: 10 (default)
│  - difficulty: EASY, MEDIUM, HARD (optional)
│  - sort: title, difficulty, createdAt (optional)
├─ Auth: Optional (no login required for browsing)
├─ Response (200):
│  {
│    "content": [
│      {
│        "id": 1,
│        "title": "Two Sum",
│        "difficulty": "EASY",
│        "description": "Find two numbers that add up to target",
│        "timeLimit": 5,
│        "memoryLimit": 256
│      }
│    ],
│    "totalElements": 6,
│    "totalPages": 1,
│    "number": 0,
│    "size": 10
│  }
└─ Errors: 400 (invalid params)

GET /api/problems/{id}
├─ Auth: Optional (browse without login)
├─ Response (200):
│  {
│    "id": 1,
│    "title": "Two Sum",
│    "description": "...",
│    "difficulty": "EASY",
│    "timeLimit": 5,
│    "memoryLimit": 256,
│    "testCases": [  // Only visible test cases
│      {
│        "input": "[2,7,11,15]\n9",
│        "expectedOutput": "[0,1]",
│        "isSample": true
│      }
│    ]
│  }
└─ Errors: 404 (problem not found)

GET /api/admin/problems/{id}/test-cases
├─ Auth: Required (ADMIN role)
├─ Response (200):
│  {
│    "visible": [...],
│    "hidden": [...]  // Only for admins
│  }
└─ Errors: 403 (forbidden)
```

### Submission Endpoints

```
POST /api/submissions
├─ Auth: Required
├─ Payload:
│  {
│    "problemId": 1,
│    "language": "python",
│    "code": "def twoSum(nums, target):\n  ..."
│  }
├─ Rate Limit: 30 submissions/minute per user
├─ Process:
│  1. Validate JWT token
│  2. Check rate limit (Redis)
│  3. Fetch problem and test cases
│  4. Execute code against each test case
│  5. Save submission to DB
│  6. Invalidate leaderboard cache
├─ Response (201):
│  {
│    "id": 1001,
│    "userId": 42,
│    "problemId": 1,
│    "language": "python",
│    "code": "...",
│    "verdict": "ACCEPTED",
│    "runtime": 0.234,  // milliseconds
│    "memory": 15.6,    // MB
│    "timeComplexity": "O(n)",
│    "spaceComplexity": "O(1)",
│    "createdAt": "2026-04-27T10:30:00"
│  }
└─ Errors: 
   - 401 (unauthorized)
   - 403 (rate limit exceeded)
   - 404 (problem not found)
   - 400 (invalid code/language)

GET /api/submissions/user?page=0&size=10
├─ Auth: Required
├─ Response (200):
│  {
│    "content": [
│      { /* submission object */ },
│      { /* submission object */ }
│    ],
│    "totalElements": 25,
│    "totalPages": 3,
│    "number": 0
│  }
└─ Errors: 401 (unauthorized)

GET /api/submissions/{id}
├─ Auth: Required (user can view own submission)
├─ Response (200): { /* submission object */ }
└─ Errors: 401, 404

GET /api/submissions/problem/{problemId}?page=0&size=10
├─ Auth: Optional (public leaderboard)
├─ Response (200):
│  {
│    "content": [
│      { /* submission by user 1 */ },
│      { /* submission by user 2 */ }
│    ],
│    "totalElements": 150
│  }
└─ Errors: 404 (problem not found)
```

### Leaderboard Endpoints

```
GET /api/leaderboard?sortBy=problems_solved
├─ Query Params:
│  - sortBy: problems_solved (default)
│            avg_time_complexity
│            avg_space_complexity
│            total_submissions
├─ Auth: Optional
├─ Cache: 5-minute Redis TTL
├─ Response (200):
│  [
│    {
│      "rank": 1,
│      "userId": 42,
│      "email": "user@test.com",
│      "problemsSolved": 6,
│      "totalSubmissions": 15,
│      "avgTimeComplexity": 2.5,
│      "avgSpaceComplexity": 1.2
│    },
│    {
│      "rank": 2,
│      "userId": 43,
│      "email": "another@test.com",
│      "problemsSolved": 5,
│      "totalSubmissions": 12,
│      "avgTimeComplexity": 3.1,
│      "avgSpaceComplexity": 1.8
│    }
│  ]
└─ Errors: None (always returns array)
```

### Admin Endpoints

```
GET /api/admin/stats
├─ Auth: Required (ADMIN role)
├─ Response (200):
│  {
│    "totalUsers": 150,
│    "totalSubmissions": 3450,
│    "acceptedSubmissions": 1200,
│    "rejectedSubmissions": 2250,
│    "averageAcceptanceRate": 34.8,
│    "languageUsage": {
│      "python": 1200,
│      "java": 800,
│      "cpp": 1100,
│      "c": 350
│    },
│    "topProblems": [
│      {
│        "problemId": 1,
│        "title": "Two Sum",
│        "attempts": 250,
│        "acceptances": 180
│      }
│    ],
│    "topUsers": [
│      { "userId": 42, "email": "...", "solved": 6 }
│    ]
│  }
└─ Errors: 403 (forbidden)

POST /api/admin/problems
├─ Auth: Required (ADMIN role)
├─ Payload:
│  {
│    "title": "New Problem",
│    "description": "...",
│    "difficulty": "MEDIUM",
│    "timeLimit": 5,
│    "memoryLimit": 256,
│    "testCases": [
│      { "input": "...", "expectedOutput": "...", "isHidden": false }
│    ]
│  }
├─ Response (201): { /* problem object */ }
└─ Errors: 403, 400
```

---

## Authentication & Security

### Security Features

#### 1. JWT Token Strategy

```
┌──────────────────────────────────────────────────────┐
│ JWT Token Structure                                  │
├──────────────────────────────────────────────────────┤
│ Header:                                              │
│ {                                                    │
│   "alg": "HS512",                                   │
│   "typ": "JWT"                                      │
│ }                                                    │
│                                                      │
│ Payload:                                             │
│ {                                                    │
│   "sub": "42",           ← User ID                  │
│   "iat": 1682524800,     ← Issued At               │
│   "exp": 1682525700      ← Expiration (900 sec)    │
│ }                                                    │
│                                                      │
│ Signature:                                           │
│ HMACSHA512(                                          │
│   base64UrlEncode(header) + "." +                  │
│   base64UrlEncode(payload),                        │
│   secretKey                                         │
│ )                                                    │
└──────────────────────────────────────────────────────┘
```

#### 2. Token Flow

```
Client                          Server
  │                              │
  ├──── POST /login ────────────>│
  │     {email, password}        │
  │                              ├─ Hash password with BCrypt
  │                              ├─ Compare with stored hash
  │                              ├─ If match: generate tokens
  │                              │
  │<───── 200 OK ────────────────┤
  │ {                            │
  │   "token": "eyJhbGc...",    │ Access Token (15 min)
  │   "refreshToken": "..."      │ Refresh Token (7 days)
  │ }                            │ in HttpOnly cookie
  │                              │
  ├─ Store token in memory      │
  ├─ Store refresh in HttpOnly  │
  │                              │
  │                              │
  │--- 10 minutes pass ---       │
  │                              │
  ├──── POST /resource ─────────>│
  │ Authorization: Bearer ...    │
  │                              ├─ Extract token from header
  │                              ├─ Verify signature with secret
  │                              ├─ Check expiration
  │                              ├─ Extract user ID
  │                              │
  │<───── 200 Success ───────────┤
  │                              │
  │                              │
  │--- 5 more minutes pass ---   │
  │ (token now expired)          │
  │                              │
  ├──── POST /resource ─────────>│
  │ Authorization: Bearer ...    │
  │ (now expired)                │
  │                              ├─ Token expired!
  │<───── 401 Unauthorized ──────┤
  │                              │
  │ (Client catches 401)         │
  │                              │
  ├──── POST /refresh ──────────>│
  │ (HttpOnly cookie sent       │
  │  automatically)              │
  │                              ├─ Validate refresh token
  │                              ├─ Generate new access token
  │                              │
  │<───── 200 OK ────────────────┤
  │ { "token": "eyJhbGc..." }   │ New access token
  │                              │
  └─ Retry failed request       │
```

#### 3. Password Security

```java
// PasswordEncoder Configuration
@Configuration
public class SecurityConfig {
    
    @Bean
    public PasswordEncoder passwordEncoder() {
        return new BCryptPasswordEncoder(12);  // Strength: 12
    }
}

// During Registration:
String rawPassword = "myPassword123!";
String hashedPassword = passwordEncoder.encode(rawPassword);
// Output: $2a$12$R9h/cIPz0gi.URNNGJVS.OPST9/PgBkqquzi.Ss7KIUgO2t0jKMUe

// During Login:
boolean isMatch = passwordEncoder.matches(
    loginPassword,
    storedHashedPassword
);
```

#### 4. CORS Configuration

```java
@Configuration
public class CorsConfig implements WebMvcConfigurer {
    
    @Override
    public void addCorsMappings(CorsRegistry registry) {
        registry.addMapping("/api/**")
                .allowedOrigins("http://localhost:5173")
                .allowedMethods("GET", "POST", "PUT", "DELETE", "OPTIONS")
                .allowedHeaders("Content-Type", "Authorization")
                .allowCredentials(true)
                .maxAge(3600);
    }
}
```

#### 5. Rate Limiting Implementation

```java
// Rate Limiting via Redis
@Component
public class RateLimitInterceptor extends HandlerInterceptorAdapter {
    
    @Autowired
    private RedisTemplate<String, Integer> redisTemplate;
    
    private static final int MAX_SUBMISSIONS = 30;
    private static final long WINDOW_MINUTES = 1;
    
    @Override
    public boolean preHandle(
            HttpServletRequest request,
            HttpServletResponse response,
            Object handler) throws Exception {
        
        if (request.getRequestURI().startsWith("/api/submissions")) {
            Long userId = getUserIdFromToken(request);
            String key = "rate_limit:submissions:" + userId;
            
            Integer submissions = redisTemplate.opsForValue().get(key);
            
            if (submissions == null) {
                redisTemplate.opsForValue()
                    .set(key, 1, Duration.ofMinutes(WINDOW_MINUTES));
            } else if (submissions >= MAX_SUBMISSIONS) {
                response.setStatus(HttpStatus.TOO_MANY_REQUESTS.value());
                response.getWriter().write("Rate limit exceeded");
                return false;
            } else {
                redisTemplate.opsForValue()
                    .increment(key);
            }
        }
        
        return true;
    }
}
```

---

## Code Execution Pipeline

### Multi-Language Code Execution

Each language requires different handling:

#### Python Execution

```python
# ai-service/app/execution/code_executor.py
import subprocess
import tempfile
import os
from typing import Tuple

class PythonExecutor:
    
    def execute(
        self,
        code: str,
        test_input: str,
        time_limit: int = 5,
        memory_limit: int = 256
    ) -> Tuple[str, str, bool]:
        
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.py',
            delete=False
        ) as f:
            f.write(code)
            script_path = f.name
        
        try:
            # Execute with subprocess
            process = subprocess.Popen(
                ['python3', script_path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=time_limit
            )
            
            stdout, stderr = process.communicate(
                input=test_input,
                timeout=time_limit
            )
            
            return stdout, stderr, process.returncode == 0
            
        except subprocess.TimeoutExpired:
            process.kill()
            return "", "TIME_LIMIT_EXCEEDED", False
        except Exception as e:
            return "", str(e), False
        finally:
            if os.path.exists(script_path):
                os.remove(script_path)
```

#### Java Execution

```java
// Java compilation & execution in Docker
docker run --rm \
  --memory=256m \
  --cpus=0.5 \
  --pids-limit=64 \
  openjdk:21-slim \
  bash -c "
    cat > Solution.java << 'EOF'
public class Solution {
    public int[] twoSum(int[] nums, int target) {
        // ... implementation
    }
}
EOF
    javac Solution.java && \
    echo '${INPUT}' | java Solution
  "
```

### Verdict Determination Logic

```
Flow Analysis for Test Case Execution:
┌─────────────────────────────────┐
│ Execute Code in Container       │
└─────┬───────────────────────────┘
      │
      ▼
┌────────────────────────────────────────┐
│ Capture: stdout, stderr, exit_code    │
│          execution_time, memory_used  │
└────┬─────────────────────────────────┘
     │
     ▼
┌─── Verdict Decision Tree ──┐
│                            │
├─ exit_code != 0          │ RUNTIME_ERROR
│   (crash/error)          │
│                          │
├─ execution_time > 5s     │ TIME_LIMIT_EXCEEDED
│                          │
├─ memory_used > 256MB     │ MEMORY_LIMIT_EXCEEDED
│                          │
├─ stdout != expected      │ WRONG_ANSWER
│   (output mismatch)      │
│                          │
├─ All checks pass         │ ACCEPTED
│                          │
└──────────────────────────┘
```

---

## Leaderboard System

### Ranking Criteria Explanation

| Criterion | Calculation | Example |
|-----------|-------------|---------|
| **Problems Solved** | Count(Submit verdict=ACCEPTED) | User solved 6 problems |
| **Avg Time Complexity** | Mean(time_complexity_score) | Avg O(n log n) = score 4 |
| **Avg Space Complexity** | Mean(space_complexity_score) | Avg O(1) = score 1 |
| **Total Submissions** | Count(All Submissions) | 25 total attempts |

### Complexity Scoring

```java
Map<String, Double> complexityScores = {
    "O(1)"      → 1.0,   // Constant
    "O(log n)"  → 2.0,   // Logarithmic
    "O(n)"      → 3.0,   // Linear
    "O(n log n)"→ 4.0,   // Linearithmic
    "O(n²)"     → 5.0,   // Quadratic
    "O(n³)"     → 6.0,   // Cubic
    "O(2^n)"    → 7.0,   // Exponential
    "O(n!)"     → 8.0    // Factorial
};
```

### Cache Invalidation

When a user submits code:
1. Submission is saved to DB
2. Redis keys deleted:
   - `leaderboard:*` (all leaderboard sorts)
   - `user:{userId}:stats`
3. Next leaderboard request recalculates from fresh DB data
4. Result cached for 5 minutes

---

## File Structure Deep Dive

### Backend File Organization

```
springboot-backend/
│
├── src/main/java/com/skillnest/
│   │
│   ├── SkillNestApplication.java
│   │   └─ Main Spring Boot application entry point
│   │     - @SpringBootApplication annotation
│   │     - main() method ← JVM starts here
│   │
│   ├── config/
│   │   ├─ SecurityConfig.java
│   │   │  └─ JWT filter chain setup
│   │   │     Password encoder bean
│   │   │     CORS configuration
│   │   │
│   │   ├─ CacheConfig.java
│   │   │  └─ Redis connection factory
│   │   │     Cache manager setup
│   │   │
│   │   └─ DockerConfig.java
│   │      └─ Docker client bean creation
│   │
│   ├── controller/
│   │   ├─ UserController.java
│   │   │  └─ POST /register
│   │   │     POST /login
│   │   │     GET /profile (auth required)
│   │   │
│   │   ├─ ProblemController.java
│   │   │  └─ GET /problems (paginated)
│   │   │     GET /problems/{id}
│   │   │
│   │   ├─ SubmissionController.java
│   │   │  └─ POST /submissions (auth required, rate limited)
│   │   │     GET /submissions/user (auth required)
│   │   │     GET /submissions/{id} (auth required)
│   │   │     GET /submissions/problem/{id}
│   │   │
│   │   ├─ LeaderboardController.java
│   │   │  └─ GET /leaderboard (cached)
│   │   │
│   │   └─ AdminController.java
│   │      └─ GET /admin/stats (admin only)
│   │         POST /admin/problems (admin only)
│   │
│   ├── service/
│   │   ├─ AuthenticationService.java
│   │   │  ├─ registerUser(): validate, hash password, save
│   │   │  ├─ loginUser(): authenticate, generate tokens
│   │   │  └─ refreshToken(): validate + generate new JWT
│   │   │
│   │   ├─ UserService.java
│   │   │  └─ getUserProfile()
│   │   │     updateProfile()
│   │   │
│   │   ├─ ProblemService.java
│   │   │  └─ getAllProblems()
│   │   │     getProblemById()
│   │   │     getVisibleTestCases()
│   │   │
│   │   ├─ SubmissionService.java  ← CRITICAL LOGIC
│   │   │  ├─ submitCode() {
│   │   │  │   for each test case:
│   │   │  │     execute code via Docker
│   │   │  │     check verdict
│   │   │  │     if not accepted: break
│   │   │  │   save submission
│   │   │  │   invalidate cache
│   │   │  │ }
│   │   │  ├─ getUserSubmissions()
│   │   │  └─ getSubmission()
│   │   │
│   │   ├─ CodeExecutionService.java  ← DOCKER INTEGRATION
│   │   │  ├─ executeCode() {
│   │   │  │   create Docker container
│   │   │  │   set memory/cpu limits
│   │   │  │   execute code with timeout
│   │   │  │   compare output vs expected
│   │   │  │   return verdict
│   │   │  │ }
│   │   │  └─ handles Python, Java, C, C++
│   │   │
│   │   ├─ LeaderboardService.java
│   │   │  ├─ getLeaderboard() @Cached
│   │   │  ├─ calculateRankings()
│   │   │  └─ calculateComplexity()
│   │   │
│   │   └─ AnalyticsService.java
│   │      └─ Admin dashboard statistics
│   │
│   ├── entity/
│   │   ├─ User.java
│   │   │  @Entity @Table(name = "users")
│   │   │  Fields: id, email, password, role, createdAt
│   │   │  Implements UserDetails
│   │   │  OneToMany relationship with Submission
│   │   │
│   │   ├─ Problem.java
│   │   │  @Entity @Table(name = "problems")
│   │   │  Fields: id, title, description, difficulty, limits
│   │   │  Indexes: difficulty, title
│   │   │  OneToMany: testCases, submissions
│   │   │
│   │   ├─ TestCase.java
│   │   │  @Entity @Table(name = "test_cases")
│   │   │  Fields: id, input, expectedOutput, isHidden
│   │   │  ManyToOne: problem
│   │   │
│   │   ├─ Submission.java
│   │   │  @Entity @Table(name = "submissions")  
│   │   │  Fields: id, code, verdict, runtime, memory
│   │   │  ManyToOne: user, problem
│   │   │  Indexes: createdAt, (userId, problemId) composite
│   │   │
│   │   ├─ Language.java (enum)
│   │   │  PYTHON, JAVA, CPP, C
│   │   │
│   │   ├─ Verdict.java (enum)
│   │   │  ACCEPTED
│   │   │  WRONG_ANSWER
│   │   │  TIME_LIMIT_EXCEEDED
│   │   │  MEMORY_LIMIT_EXCEEDED
│   │   │  RUNTIME_ERROR
│   │   │
│   │   ├─ UserRole.java (enum)
│   │   │  USER, ADMIN
│   │   │
│   │   └─ Difficulty.java (enum)
│   │      EASY, MEDIUM, HARD
│   │
│   ├── repository/
│   │   ├─ UserRepository.java
│   │   │  extends JpaRepository
│   │   │  findByEmail(), existsByEmail()
│   │   │
│   │   ├─ ProblemRepository.java
│   │   │  extends JpaRepository
│   │   │  findByDifficulty(), findAll()
│   │   │
│   │   ├─ TestCaseRepository.java
│   │   │  extends JpaRepository
│   │   │  findByProblemId()
│   │   │  findByProblemIdAndIsHidden()
│   │   │
│   │   ├─ SubmissionRepository.java  ← Database queries
│   │   │  extends JpaRepository
│   │   │  findByUserId()
│   │   │  findByProblemId()
│   │   │  countByUserIdAndVerdict()
│   │   │  findFirstByUserIdAndProblemIdOrderByCreatedAtDesc()
│   │   │
│   │   └─ (Spring Data generates SQL at runtime)
│   │
│   ├── dto/
│   │   ├─ UserRegisterDto.java  ← Request validation
│   │   │  { email, password }
│   │   │
│   │   ├─ UserLoginDto.java
│   │   │  { email, password }
│   │   │
│   │   ├─ SubmissionCreateDto.java  ← Submission request
│   │   │  { problemId, language, code }
│   │   │
│   │   ├─ SubmissionResponseDto.java ← Submission response
│   │   │  { id, userId, problemId, language, code,
│   │   │    verdict, runtime, memory, complexity, createdAt }
│   │   │
│   │   ├─ ProblemDto.java
│   │   ├─ TestCaseDto.java
│   │   └─ LeaderboardEntryDto.java
│   │      { rank, userId, email, problemsSolved,
│   │        totalSubmissions, avgTimeComplexity, ... }
│   │
│   ├── exception/
│   │   ├─ ResourceNotFoundException.java
│   │   ├─ ValidationException.java
│   │   ├─ UnauthorizedException.java
│   │   └─ GlobalExceptionHandler.java
│   │      @ControllerAdvice
│   │      @ExceptionHandler methods
│   │
│   └── security/
│       ├─ JwtTokenProvider.java
│       │  generateAccessToken()
│       │  generateRefreshToken()
│       │  validateToken()
│       │  getUserIdFromToken()
│       │
│       └─ JwtAuthenticationFilter.java
│          ← extends OncePerRequestFilter
│          doFilterInternal() {
│            extract token from Authorization: Bearer
│            validate signature & expiration
│            extract user ID
│            set SecurityContext
│          }
│
├── src/main/resources/
│   ├── application.properties
│   │  spring.datasource.url=jdbc:postgresql://localhost:5432/skillnest
│   │  spring.red.host=redis
│   │  spring.redis.port=6379
│   │  server.port=8080
│   │
│   └── application-h2.properties (for testing)
│
└── pom.xml (Maven config)
   <dependencies>
     spring-boot-starter-web
     spring-boot-starter-data-jpa
     spring-boot-starter-security
     spring-boot-starter-data-redis
     postgresql driver
     jjwt
     docker-java-sdk
   </dependencies>
```

### Frontend File Organization

```
frontend/
│
├── src/
│   ├── app.html
│   │  └─ Main HTML shell
│   │     <div id="app"></div>
│   │
│   ├── app.css
│   │  └─ Global styles
│   │     @tailwind imports
│   │
│   ├── routes/
│   │  │  ← File-based routing (SvelteKit feature)
│   │  │
│   │  ├── +layout.svelte
│   │  │  └─ Root layout
│   │  │     Navigation bar
│   │  │     Footer
│   │  │     Applied to all pages
│   │  │
│   │  ├── +page.svelte
│   │  │  └─ Home page (http://localhost:5173/)
│   │  │     Hero section
│   │  │     Quick stats
│   │  │     Links to problems/leaderboard
│   │  │
│   │  ├── login/
│   │  │  └── +page.svelte
│   │  │     Form: email, password
│   │  │     POST /auth/login
│   │  │     Store JWT in memory
│   │  │
│   │  ├── register/
│   │  │  └── +page.svelte
│   │  │     Form: email, password, confirm
│   │  │     POST /auth/register
│   │  │
│   │  ├── problems/
│   │  │  ├── +page.svelte
│   │  │  │  Grid/List view of all problems
│   │  │  │  GET /problems (paginated)
│   │  │  │  Filter by difficulty
│   │  │  │  No auth required
│   │  │  │
│   │  │  └── [id]/
│   │  │     └── +page.svelte
│   │  │        Problem detail page
│   │  │        GET /problems/{id}
│   │  │        Display description
│   │  │        Show visible test cases
│   │  │        Monaco code editor (if logged in)
│   │  │        Submit button → POST /submissions
│   │  │
│   │  ├── leaderboard/
│   │  │  └── +page.svelte
│   │  │     Leaderboard table
│   │  │     GET /leaderboard?sortBy=...
│   │  │     Tabs to switch ranking criteria
│   │  │     No auth required
│   │  │
│   │  ├── dashboard/
│   │  │  └── +page.svelte
│   │  │     (Auth required)
│   │  │     User stats
│   │  │     Recent submissions
│   │  │     Accepted rate
│   │  │
│   │  ├── profile/
│   │  │  └── +page.svelte
│   │  │     User profile info
│   │  │     Settings
│   │  │
│   │  └── teacher/ (admin routes)
│   │     └── dashboard/
│   │        └── +page.svelte
│   │           Admin statistics
│   │           Create new problems
│   │           Manage users
│   │
│   ├── lib/
│   │  │
│   │  ├── api/
│   │  │  └── client.ts
│   │  │     ← API client configuration
│   │  │     Axios/fetch wrapper
│   │  │     Interceptors for JWT
│   │  │     Base URL: http://localhost:8080/api
│   │  │
│   │  ├── components/
│   │  │  ├─ CodeEditor.svelte
│   │  │  │  Monaco editor component
│   │  │  │  Language selection
│   │  │  │  Code input area
│   │  │  │  Props: { code, language, onChange, onSubmit }
│   │  │  │
│   │  │  ├─ ProblemCard.svelte
│   │  │  │  Problem preview card
│   │  │  │  Difficulty badge
│   │  │  │  Title + description snippet
│   │  │  │
│   │  │  ├─ LeaderboardTable.svelte
│   │  │  │  Table with rankings
│   │  │  │  Sortable columns
│   │  │  │
│   │  │  └─ TeacherStats.svelte
│   │  │     Admin dashboard stats
│   │  │
│   │  ├── stores/
│   │  │  ├─ authStore.ts (Svelte store)
│   │  │  │  Shared state: token, user, isLoggedIn
│   │  │  │  Methods: login(), logout(), refreshToken()
│   │  │  │
│   │  │  ├─ userStore.ts
│   │  │  │  User profile state
│   │  │  │
│   │  │  └─ leaderboardStore.ts
│   │  │     Leaderboard cache + state
│   │  │
│   │  └── types.ts
│   │     TypeScript interface definitions
│   │     User, Problem, Submission, Leaderboard, etc.
│   │
│   └── hooks.server.ts
│      Server-side hooks
│      Handle GET requests before route
│
├── vite.config.ts (Vite build config)
├── svelte.config.js (SvelteKit config)
├── tailwind.config.js (Tailwind setup)
├── postcss.config.cjs (CSS processing)
└── package.json (npm dependencies)
```

### AI Service File Organization

```
ai-service/
│
├── app/
│   │
│   ├── main.py
│   │  └─ FastAPI app initialization
│   │     @app = FastAPI()
│   │     Include routers
│   │     Middleware setup
│   │
│   ├── core/
│   │  ├─ config.py
│   │  │  Configuration management
│   │  │  DATABASE_URL, REDIS_URL, etc.
│   │  │  Environment variables
│   │  │
│   │  ├─ logging.py
│   │  │  Logging setup
│   │  │  Log format, level, handlers
│   │  │
│   │  └─ constants.py
│   │     Constants for complexity scoring
│   │
│   ├── db/
│   │  ├─ base.py
│   │  │  SQLAlchemy engine creation
│   │  │  Base ORM class
│   │  │  Session factory
│   │  │
│   │  ├─ models.py
│   │  │  SQLAlchemy ORM models
│   │  │  Question, TestCase, Submission, SubmissionResult
│   │  │  Relationships and indexes
│   │  │
│   │  └─ init_db.py
│   │     Create tables on startup
│   │     Base.metadata.create_all()
│   │
│   ├── execution/
│   │  └─ code_executor.py
│   │     Execute code (Python, Java, C, C++)
│   │     subprocess module
│   │     Timeout handling
│   │     Output parsing
│   │
│   ├── rag/  ← Retrieval-Augmented Generation
│   │  ├─ ollama_client.py
│   │  │  Connect to Ollama AI model
│   │  │  Generate questions
│   │  │  Analyze code
│   │  │
│   │  └─ vector_store.py
│   │     ChromaDB embeddings
│   │     Store question embeddings
│   │     Similarity search
│   │
│   ├── routes/
│   │  ├─ execution.py  ← Main code execution routes
│   │  │  POST /execute/run (dry run)
│   │  │  POST /execute/submit (final)
│   │  │
│   │  ├─ questions.py
│   │  │  POST /generate (AI generate questions)
│   │  │  GET /questions/{id}
│   │  │
│   │  └─ health.py
│   │     GET /health (status check)
│   │
│   ├── schemas/
│   │  └─ schemas.py
│   │     Pydantic models for validation
│   │     CodeSubmitRequest,CodeSubmitResponse
│   │     TestCaseResult
│   │     QuestionGenerateRequest
│   │
│   ├── services/
│   │  └─ question_service.py
│   │     Business logic for questions
│   │
│   └── utils/
│      └─ cache.py
│         Redis cache management
│         Set/get cache
│         Cache invalidation
│
├── requirements.txt
│  fastapi, uvicorn, sqlalchemy
│  psycopg2-binary, redis, chromadb
│  pydantic, python-dotenv
│
├── Dockerfile
│  FROM python:3.11-slim
│  Copy code
│  pip install -r requirements.txt
│  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
│
├── docker-compose.yml
└── entrypoint.sh
```

---

## Key Algorithms & Patterns

### 1. Test Case Execution Algorithm

```pseudocode
function submitCode(userId, problemId, code, language):
    user ← getUser(userId)
    problem ← getProblem(problemId)
    testCases ← getAllTestCases(problemId)  // visible + hidden
    
    finalVerdict ← ACCEPTED
    totalRuntime ← 0
    maxMemory ← 0
    
    FOR EACH testCase IN testCases:
        input ← testCase.input
        expected ← testCase.expectedOutput
        
        result ← executeInDocker(
            code, 
            language, 
            input,
            problem.timeLimit,
            problem.memoryLimit
        )
        
        actual ← result.stdout
        totalRuntime += result.executionTime
        maxMemory ← max(maxMemory, result.memory)
        
        IF actual != expected:
            finalVerdict ← WRONG_ANSWER
            BREAK  // Stop on first failure
        ELSE IF result.executionTime > timeLimit:
            finalVerdict ← TIME_LIMIT_EXCEEDED
            BREAK
        ELSE IF result.memory > memoryLimit:
            finalVerdict ← MEMORY_LIMIT_EXCEEDED
            BREAK
        ELSE IF result.exitCode != 0:
            finalVerdict ← RUNTIME_ERROR
            BREAK
        END IF
    END FOR
    
    submission ← newSubmission(
        user, 
        problem, 
        code, 
        language,
        finalVerdict,
        totalRuntime / testCases.size(),
        maxMemory
    )
    
    saveToDatabase(submission)
    invalidateLeaderboardCache()
    
    RETURN submissionResponse(submission)
END function
```

### 2. Leaderboard Ranking Algorithm

```pseudocode
function calculateLeaderboard(sortBy):
    users ← getAllUsers()
    entries ← []
    
    FOR EACH user IN users:
        acceptedSubmissions ← findAcceptedSubmissions(user.id)
        
        entry ← {
            userId: user.id,
            email: user.email,
            problemsSolved: COUNT(acceptedSubmissions),
            totalSubmissions: COUNT(allSubmissions),
            avgTimeComplexity: AVERAGE(acceptedSubmissions.timeComplexity),
            avgSpaceComplexity: AVERAGE(acceptedSubmissions.spaceComplexity)
        }
        
        entries.add(entry)
    END FOR
    
    CASE sortBy:
        "problems_solved":
            SORT entries BY problemsSolved DESC, email ASC
            
        "avg_time_complexity":
            SORT entries BY avgTimeComplexity ASC, problemsSolved DESC
            
        "avg_space_complexity":
            SORT entries BY avgSpaceComplexity ASC, problemsSolved DESC
            
        "total_submissions":
            SORT entries BY totalSubmissions DESC
    END CASE
    
    rank ← 1
    FOR EACH entry IN entries:
        entry.rank ← rank
        rank += 1
    END FOR
    
    CACHE entries IN Redis FOR 5 MINUTES
    
    RETURN entries
END function
```

### 3. Docker Container Lifecycle

```pseudocode
function executeCodeInDocker(code, language, input, timeLimit, memoryLimit):
    imageId ← getDockerImage(language)
    // imageId = "python:3.11-slim", "openjdk:21-slim", etc.
    
    // Create container config
    config ← {
        image: imageId,
        memory: memoryLimit * 1024 * 1024,  // bytes
        cpuQuota: 50000,  // 0.5 cores
        pidsLimit: 64,
        readonlyRootfs: true,
        networkMode: "none"
    }
    
    container ← dockerClient.createContainer(config)
    START_TIME ← getCurrentTime()
    
    TRY:
        dockerClient.startContainer(container.id)
        
        output ← executeWithTimeout(
            container.id,
            code,
            input,
            timeLimit + 2 SECONDS
        )
        
        EXECUTION_TIME ← getCurrentTime() - START_TIME
        EXIT_CODE ← getContainerExitCode(container.id)
        MEMORY_USED ← getMemoryStats(container.id)
        
    CATCH TimeoutException:
        dockerClient.killContainer(container.id)
        RETURN { verdict: TIME_LIMIT_EXCEEDED, ... }
        
    FINALLY:
        dockerClient.stopContainer(container.id)
        dockerClient.removeContainer(container.id)
    END TRY
    
    RESULT ← {
        stdout: output,
        executionTime: EXECUTION_TIME,
        memory: MEMORY_USED,
        exitCode: EXIT_CODE
    }
    
    RETURN RESULT
END function
```

---

## Data Flow Diagrams

### Complete Request/Response Cycle

```
1. USER ACTION (Frontend)
   └─ User writes Python code, clicks "Submit"
   
2. API REQUEST (Frontend → Backend)
   └─ POST http://localhost:8080/api/submissions
      Headers: Authorization: Bearer eyJhbGc...
      Body: { problemId: 5, language: "python", code: "..." }
   
3. SECURITY (Spring Boot)
   └─ JwtAuthenticationFilter
      ├─ Extract token from Authorization header
      ├─ Validate signature with HMAC512
      ├─ Check token expiration
      └─ Set userId (42) in SecurityContext
   
4. RATE LIMITING (Redis)
   └─ Check: rate_limit:submissions:42
      ├─ Current: 5 submissions
      ├─ Limit: 30 per minute
      └─ Status: PASS
   
5. CONTROLLER (SubmissionController)
   └─ submitCode() endpoint
      ├─ Receive SubmissionCreateDto
      ├─ Validate JSON structure
      └─ Call SubmissionService.submitCode()
   
6. SERVICE LOGIC (SubmissionService)
   └─ submitCode(userId=42, problemId=5, ...)
      ├─ Query: User.findById(42) from PostgreSQL
      ├─ Query: Problem.findById(5) from PostgreSQL
      ├─ Query: TestCase.findByProblemId(5) from PostgreSQL
      │
      ├─ FOR EACH TestCase:
      │  ├─ Test 1: Input="[2,7,11,15]\n9"
      │  │  ├─ Call CodeExecutionService.executeCode()
      │  │  │
      │  │  └─ Docker Execution (below)
      │  │
      │  ├─ Test 2: Input="[3,2,4]\n6"
      │  │  └─ Docker Execution
      │  │
      │  └─ Test 3: Input="[3,3]\n6" (hidden)
      │     └─ Docker Execution
      │
      └─ Save Submission to PostgreSQL
         └─ INSERT INTO submissions VALUES (...)
   
7. DOCKER EXECUTION (CodeExecutionService)
   └─ FOR EACH test case:
      ├─ Create Docker container
      │  └─ Docker image: python:3.11-slim
      │     Memory: 256 MB
      │     CPU: 0.5 cores
      │     PID Limit: 64
      │
      ├─ Copy code + input into container
      ├─ Execute: python3 -c "user_code < input"
      ├─ Capture: stdout, stderr, exit code
      ├─ Measure: execution time, memory used
      │
      ├─ COMPARE OUTPUTS
      │  ├─ actual_stdout vs expected_output?
      │  ├─ execution_time > 5 sec?
      │  ├─ memory > 256 MB?
      │  └─ exit_code != 0?
      │
      ├─ SET VERDICT
      │  ├─ Test 1: ACCEPTED (output matches)
      │  ├─ Test 2: ACCEPTED (output matches)
      │  └─ Test 3: ACCEPTED (output matches)
      │
      └─ Cleanup: Stop + Remove docker container
   
8. RESULT AGGREGATION (SubmissionService)
   └─ All tests passed
      ├─ finalVerdict = ACCEPTED
      ├─ averageRuntime = (234 + 245 + 239) / 3 = 239 ms
      ├─ maxMemory = 18.5 MB
      └─ timeComplexity = "O(n)"  (from AI analysis)
   
9. CACHE INVALIDATION (Redis)
   └─ RedisTemplate.delete("leaderboard:*")
      └─ Next leaderboard request will recalculate
   
10. SAVE TO DATABASE (PostgreSQL)
    └─ INSERT INTO submissions
       (user_id, problem_id, language, code, verdict,
        runtime, memory, time_complexity, created_at)
       VALUES (42, 5, 'python', '...', 'ACCEPTED',
               239.0, 18.5, 'O(n)', NOW())
   
11. RESPONSE (Spring Boot → Frontend)
    └─ HTTP 201 CREATED
       {
         "id": 1001,
         "userId": 42,
         "problemId": 5,
         "language": "python",
         "code": "...",
         "verdict": "ACCEPTED",
         "runtime": 239.0,
         "memory": 18.5,
         "timeComplexity": "O(n)",
         "spaceComplexity": "O(1)",
         "createdAt": "2026-04-27T10:30:00"
       }
   
12. FRONTEND UPDATE (SvelteKit)
    └─ Display response
       ├─ Show "✓ ACCEPTED" in green
       ├─ Display "Runtime: 239ms"
       ├─ Display "Memory: 18.5MB"
       ├─ Update user stats (problemsSolved++, totalSubmissions++)
       └─ Refresh leaderboard (GET /leaderboard)
```

### Architecture Components Interaction

```
┌────────────────────────────────────────────────────────────────┐
│                      EXTERNAL SYSTEMS                          │
└────────────────────────────────────────────────────────────────┘
         │                    │                       │
         │                    │                       │
    ┌────▼──────┐    ┌────────▼──────┐    ┌──────────▼────┐
    │ PostgreSQL│    │    Redis      │    │ Docker Engine │
    │     16    │    │      7        │    │   (Container) │
    │           │    │               │    │               │
    │ Tables:   │    │ Cache:        │    │ Images:       │
    │ - users   │    │ - leaderboard │    │ - python:3.11 │
    │ - problems│    │ - rate limit  │    │ - java:21     │
    │ - subm.   │    │ - stats       │    │ - gcc:latest  │
    └────┬──────┘    └───────┬───────┘    └────────┬──────┘
         │                   │                     │
         └──────────┬────────┴────────┬────────────┘
                    │                 │
    ┌───────────────▼─────────────────▼──────────────────┐
    │       SPRING BOOT BACKEND (Java 21)                │
    │         Port: 8080 (/api)                          │
    │                                                    │
    │  ┌─────────────────────────────────────────────┐   │
    │  │ JwtAuthenticationFilter                     │   │
    │  │ - Validate JWT tokens                       │   │
    │  │ - Extract userId                           │   │
    │  │ - Set SecurityContext                       │   │
    │  └─────────────────────────────────────────────┘   │
    │                                                    │
    │  ┌─────────────────────────────────────────────┐   │
    │  │ Controllers                                 │   │
    │  │ - UserController                           │   │
    │  │ - ProblemController                        │   │
    │  │ - SubmissionController ← MAIN LOGIC        │   │
    │  │ - LeaderboardController                    │   │
    │  │ - AdminController                          │   │
    │  └──────────────┬────────────────────────────┘    │
    │                 │                                  │
    │  ┌──────────────▼────────────────────────────┐    │
    │  │ Services                                  │    │
    │  │ - SubmissionService                      │    │
    │  │   {submitCode, execute, save, invalidate}│    │
    │  │ - CodeExecutionService                   │    │
    │  │   {Docker API integration}               │    │
    │  │ - LeaderboardService                     │    │
    │  │   {calculate rankings, cache}            │    │
    │  │ - AuthenticationService                  │    │
    │  │   {JWT, password hashing}                │    │
    │  └──────────────┬───────────────────────────┘    │
    │                 │                                  │
    │  ┌──────────────▼────────────────────────────┐    │
    │  │ Repositories (Spring Data JPA)           │    │
    │  │ - UserRepository                         │    │
    │  │ - ProblemRepository                      │    │
    │  │ - SubmissionRepository                   │    │
    │  │ - TestCaseRepository                     │    │
    │  │ (Auto-generate SQL from method names)    │    │
    │  └──────────────┬───────────────────────────┘    │
    │                 │                                  │
    │  ┌──────────────▼────────────────────────────┐    │
    │  │ Entities (Hibernate ORM)                 │    │
    │  │ - User, Problem, TestCase               │    │
    │  │ - Submission, Verdict, Language         │    │
    │  │ (Maps to PostgreSQL tables)              │    │
    │  └──────────────────────────────────────────┘    │
    │                                                    │
    └───────────────┬────────────────────────────────────┘
                    │
    ┌───────────────▼────────────────────────────────┐
    │   SVELTEKIT FRONTEND (TypeScript)              │
    │   Port: 5173                                   │
    │                                                │
    │  ┌─────────────────────────────────────────┐   │
    │  │ Routes/Pages                            │   │
    │  │ - /problems (browse)                    │   │
    │  │ - /problems/[id] (solve)                │   │
    │  │ - /leaderboard (rankings)               │   │
    │  │ - /dashboard (user stats)               │   │
    │  │ - /teacher/dashboard (admin)            │   │
    │  └─────────────────────────────────────────┘   │
    │                                                │
    │  ┌─────────────────────────────────────────┐   │
    │  │ Components                              │   │
    │  │ - CodeEditor (Monaco)                   │   │
    │  │ - LeaderboardTable                      │   │
    │  │ - ProblemCard                           │   │
    │  │ - TeacherStats                          │   │
    │  └─────────────────────────────────────────┘   │
    │                                                │
    │  ┌─────────────────────────────────────────┐   │
    │  │ Stores (Svelte store subscription)      │   │
    │  │ - authStore {token, user}               │   │
    │  │ - userStore {profile}                   │   │
    │  │ - leaderboardStore {rankings, cache}    │   │
    │  └─────────────────────────────────────────┘   │
    │                                                │
    │  ┌─────────────────────────────────────────┐   │
    │  │ API Client (axios/fetch)                │   │
    │  │ - Base URL: http://localhost:8080/api  │   │
    │  │ - Interceptor: Add JWT to headers      │   │
    │  │ - Error handler: Refresh token logic   │   │
    │  └─────────────────────────────────────────┘   │
    │                                                │
    └────────────────────────────────────────────────┘
                    │
    ┌───────────────▼────────────────────────────────┐
    │   FASTAPI AI SERVICE (Python)                  │
    │   Port: 8000 (/docs)                           │
    │                                                │
    │  ┌─────────────────────────────────────────┐   │
    │  │ Routes                                  │   │
    │  │ - /execute/run (dry run)               │   │
    │  │ - /execute/submit (final)              │   │
    │  │ - /generate (AI questions)             │   │
    │  │ - /health (checks)                     │   │
    │  └─────────────────────────────────────────┘   │
    │                                                │
    │  ┌─────────────────────────────────────────┐   │
    │  │ Code Executor                           │   │
    │  │ - Python: subprocess                    │   │
    │  │ - Java/C/C++: Docker                    │   │
    │  │ - Timeout handling                      │   │
    │  │ - Output parsing                        │   │
    │  └─────────────────────────────────────────┘   │
    │                                                │
    │  ┌─────────────────────────────────────────┐   │
    │  │ RAG Engine (ChromaDB, Ollama)          │   │
    │  │ - Generate AI questions                │   │
    │  │ - Analyze code complexity              │   │
    │  │ - Vector embeddings storage            │   │
    │  └─────────────────────────────────────────┘   │
    │                                                │
    └────────────────────────────────────────────────┘
```

---

## Summary

This comprehensive document covers:

✅ **Architecture**: Multi-tier microservices design  
✅ **Database**: PostgreSQL with optimized indexes  
✅ **Cache**: Redis for leaderboard and rate limiting  
✅ **Security**: JWT tokens, password hashing, Docker sandboxing  
✅ **Code Execution**: Docker containerization with resource limits  
✅ **Leaderboard**: Multi-criteria ranking with 5-min cache  
✅ **File Structure**: Complete directory organization  
✅ **API Endpoints**: All REST endpoints documented  
✅ **Data Flow**: Step-by-step request/response cycles  
✅ **Business Logic**: Algorithms and decision trees  

---

**End of Document**

*This is a living document. Update with latest features and architectural changes as the project evolves.*
