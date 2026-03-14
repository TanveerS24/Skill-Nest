# Spring Boot Backend Setup and Installation

## Prerequisites
- Java 21 JDK
- Maven 3.9+
- PostgreSQL 14+
- Redis 7+
- Docker (optional, for containerized setup)

## Installation Steps

### 1. Clone and Navigate
```bash
cd springboot-backend
```

### 2. Configure Database and Redis
```bash
# Copy and update environment file
cp .env.example .env

# Update with your database and Redis credentials
```

### 3. Build the Project
```bash
mvn clean package
```

### 4. Run the Application
```bash
java -jar target/skillnest-backend-1.0.0.jar
```

## Running with Docker Compose

```bash
# From root directory
docker-compose -f docker-compose-springboot.yml up -d
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get tokens
- `POST /api/auth/refresh` - Refresh access token

### Problems
- `GET /api/problems` - Get all problems (paginated)
- `GET /api/problems/{id}` - Get problem details
- `GET /api/problems/difficulty/{difficulty}` - Filter by difficulty
- `POST /api/problems` - Create problem (admin only)
- `PUT /api/problems/{id}` - Update problem (admin only)
- `DELETE /api/problems/{id}` - Delete problem (admin only)

### Submissions
- `POST /api/submissions` - Submit code
- `GET /api/submissions/user` - Get user submissions
- `GET /api/submissions/problem/{problemId}` - Get problem submissions
- `GET /api/submissions/{id}` - Get submission details

### Leaderboard
- `GET /api/leaderboard` - Get global leaderboard

## Testing

```bash
mvn test
```

## Docker Push (Optional)

```bash
docker build -t skillnest-backend:latest .
docker tag skillnest-backend:latest your-registry/skillnest-backend:latest
docker push your-registry/skillnest-backend:latest
```

## Migration from Python/FastAPI

See [MIGRATION_GUIDE.md](../MIGRATION_GUIDE.md) for detailed migration steps.
