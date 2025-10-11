@echo off
echo BHIV HR Platform - Local Deployment
echo ====================================

cd /d "%~dp0\.."

echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker not found. Please install Docker Desktop.
    pause
    exit /b 1
)

echo Starting services...
docker-compose -f deployment\docker\docker-compose.production.yml up -d

echo Waiting for services to start...
timeout /t 30 /nobreak >nul

echo Checking service health...
curl -s http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo WARNING: Gateway service may still be starting...
) else (
    echo Gateway: HEALTHY
)

curl -s http://localhost:9000/health >nul 2>&1
if errorlevel 1 (
    echo WARNING: Agent service may still be starting...
) else (
    echo Agent: HEALTHY
)

echo.
echo Services started! Access URLs:
echo - Gateway API: http://localhost:8000/docs
echo - AI Agent: http://localhost:9000/docs  
echo - HR Portal: http://localhost:8501
echo - Client Portal: http://localhost:8502
echo.
echo To stop: docker-compose -f deployment\docker\docker-compose.production.yml down
pause