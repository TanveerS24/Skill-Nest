#!/bin/bash

# SkillNest Setup Script
echo "🚀 Setting up SkillNest - Multi-Language Coding Platform"
echo "========================================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install docker-compose."
    exit 1
fi

echo "✅ docker-compose is available"
echo ""

# Create .env file if it doesn't exist
if [ ! -f backend/.env ]; then
    echo "📝 Creating backend/.env from .env.example..."
    cp backend/.env.example backend/.env
    echo "⚠️  Please update backend/.env with your configuration"
    echo ""
fi

# Pull required Docker images for code execution
echo "📦 Pulling Docker images for code execution..."
docker pull python:3.11-slim
docker pull openjdk:17-slim
docker pull gcc:13-alpine
echo "✅ Docker images pulled successfully"
echo ""

# Start services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis
echo "⏳ Waiting for services to be ready..."
sleep 10
echo "✅ Services are running"
echo ""

# Setup backend
echo "🔧 Setting up backend..."
cd backend

# Install Python dependencies (if running locally)
if command -v python3 &> /dev/null; then
    echo "📦 Installing Python dependencies..."
    python3 -m venv venv 2>/dev/null || true
    source venv/bin/activate 2>/dev/null || . venv/Scripts/activate 2>/dev/null
    pip install -r requirements.txt
    echo "✅ Backend dependencies installed"
    
    # Initialize database
    echo "🗄️  Initializing database..."
    python -c "
from app.database import init_db
import asyncio
asyncio.run(init_db())
print('Database initialized')
"
    
    # Seed database
    echo "🌱 Seeding database..."
    python seed.py
    echo "✅ Database seeded with initial problems"
else
    echo "⚠️  Python not found. Will initialize database in container."
fi

cd ..

# Setup frontend
echo "🎨 Setting up frontend..."
cd frontend

if command -v npm &> /dev/null; then
    echo "📦 Installing frontend dependencies..."
    npm install
    echo "✅ Frontend dependencies installed"
else
    echo "⚠️  npm not found. Will install dependencies in container."
fi

cd ..

# Start all services
echo "🚀 Starting all services..."
docker-compose up -d
echo ""
echo "✅ Setup complete!"
echo ""
echo "========================================================="
echo "📋 Service URLs:"
echo "   Frontend:  http://localhost:5173"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "👤 Demo credentials:"
echo "   Admin:     admin@skillnest.com / admin123"
echo "   User:      user@test.com / user123"
echo ""
echo "📝 To view logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 To stop services:"
echo "   docker-compose down"
echo "========================================================="
