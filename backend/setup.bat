@echo off
REM Spring Boot Backend Setup Script for Windows

echo.
echo ========== SkillNest Spring Boot Backend Setup ==========
echo.

REM Check if Java is installed
java -version >nul 2>&1
if errorlevel 1 (
    echo Error: Java is not installed. Please install Java 21 JDK.
    exit /b 1
)

echo [OK] Java is installed
java -version

REM Check if Maven is installed
mvn -version >nul 2>&1
if errorlevel 1 (
    echo Error: Maven is not installed. Please install Maven 3.9+
    exit /b 1
)

echo [OK] Maven is installed
mvn -version

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo Creating .env file...
    copy ".env.example" ".env"
    echo [!] Please update .env with your configuration
)

REM Build the project
echo.
echo Building Spring Boot project...
mvn clean package -DskipTests

if errorlevel 1 (
    echo Error: Build failed
    exit /b 1
)

echo.
echo [OK] Build successful!
echo.
echo ========== Setup Complete ==========
echo.
echo To start the application:
echo   java -jar target/skillnest-backend-1.0.0.jar
echo.
echo Or use Docker Compose from the root directory:
echo   docker-compose -f docker-compose-springboot.yml up -d
echo.
