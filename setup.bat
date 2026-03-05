@echo off
REM SkillNest Setup Script for Windows

echo ======================================================
echo Setting up SkillNest - Multi-Language Coding Platform
echo ======================================================
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Please start Docker and try again.
    exit /b 1
)

echo Docker is running
echo.

REM Create .env file if it doesn't exist
if not exist backend\.env (
    echo Creating backend\.env from .env.example...
    copy backend\.env.example backend\.env
    echo Please update backend\.env with your configuration
    echo.
)

REM Pull required Docker images
echo Pulling Docker images for code execution...
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull gcc:13-alpine
echo Docker images pulled successfully
echo.

REM Start services
echo Starting Docker services...
docker-compose up -d postgres redis
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul
echo Services are running
echo.

REM Setup backend
echo Setting up backend...
cd backend

REM Install Python dependencies
where python >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing Python dependencies...
    python -m venv venv
    call venv\Scripts\activate.bat
    pip install -r requirements.txt
    echo Backend dependencies installed
    
    REM Initialize database
    echo Initializing database...
    python -c "from app.database import init_db; import asyncio; asyncio.run(init_db())"
    
    REM Seed database
    echo Seeding database...
    python seed.py
    echo Database seeded with initial problems
) else (
    echo Python not found. Will initialize database in container.
)

cd ..

REM Setup frontend
echo Setting up frontend...
cd frontend

where npm >nul 2>&1
if %errorlevel% equ 0 (
    echo Installing frontend dependencies...
    npm install
    echo Frontend dependencies installed
) else (
    echo npm not found. Will install dependencies in container.
)

cd ..

REM Start all services
echo Starting all services...
docker-compose up -d
echo.
echo Setup complete!
echo.
echo ======================================================
echo Service URLs:
echo    Frontend:  http://localhost:5173
echo    Backend:   http://localhost:8000
echo    API Docs:  http://localhost:8000/docs
echo.
echo Demo credentials:
echo    Admin:     admin@skillnest.com / admin123
echo    User:      user@test.com / user123
echo.
echo To view logs:
echo    docker-compose logs -f
echo.
echo To stop services:
echo    docker-compose down
echo ======================================================
pause
