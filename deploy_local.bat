@echo off
echo ========================================
echo BHIV HR Platform - Local Deployment
echo ========================================
echo.

echo Step 1: Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker not found. Please install Docker Desktop.
    pause
    exit /b 1
)
echo ✓ Docker is available

echo.
echo Step 2: Stopping existing services...
docker-compose -f docker-compose.production.yml down >nul 2>&1
echo ✓ Stopped existing services

echo.
echo Step 3: Building and starting services...
echo This may take 2-3 minutes for first run...
docker-compose -f docker-compose.production.yml up --build -d

if %errorlevel% neq 0 (
    echo ERROR: Failed to start services
    pause
    exit /b 1
)

echo ✓ Services started successfully

echo.
echo Step 4: Waiting for services to be ready...
timeout /t 30 /nobreak >nul
echo ✓ Services should be ready

echo.
echo Step 5: Testing deployment...
echo Testing Gateway Health...
curl -s http://localhost:8000/health >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Gateway is responding
) else (
    echo ⚠ Gateway not ready yet, may need more time
)

echo.
echo ========================================
echo DEPLOYMENT COMPLETE
echo ========================================
echo.
echo Access URLs:
echo • API Gateway: http://localhost:8000/docs
echo • HR Portal:   http://localhost:8501
echo • Client Portal: http://localhost:8502
echo • AI Agent:    http://localhost:9000/docs
echo.
echo Test Credentials:
echo • Client ID: TECH001
echo • Password: demo123
echo • API Key: myverysecureapikey123
echo.
echo To view logs: docker-compose -f docker-compose.production.yml logs -f
echo To stop: docker-compose -f docker-compose.production.yml down
echo.
pause