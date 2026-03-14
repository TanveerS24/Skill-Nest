#!/bin/bash
# Spring Boot Backend Setup Script for Unix/Linux/Mac

set -e

echo ""
echo "========== SkillNest Spring Boot Backend Setup =========="
echo ""

# Check if Java is installed
if ! command -v java &> /dev/null; then
    echo "Error: Java is not installed. Please install Java 21 JDK."
    exit 1
fi

echo "[OK] Java is installed"
java -version

# Check if Maven is installed
if ! command -v mvn &> /dev/null; then
    echo "Error: Maven is not installed. Please install Maven 3.9+"
    exit 1
fi

echo "[OK] Maven is installed"
mvn -version

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp ".env.example" ".env"
    echo "[!] Please update .env with your configuration"
fi

# Build the project
echo ""
echo "Building Spring Boot project..."
mvn clean package -DskipTests

if [ $? -ne 0 ]; then
    echo "Error: Build failed"
    exit 1
fi

echo ""
echo "[OK] Build successful!"
echo ""
echo "========== Setup Complete =========="
echo ""
echo "To start the application:"
echo "  java -jar target/skillnest-backend-1.0.0.jar"
echo ""
echo "Or use Docker Compose from the root directory:"
echo "  docker-compose -f docker-compose-springboot.yml up -d"
echo ""
