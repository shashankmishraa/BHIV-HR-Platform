@echo off
echo 🚀 BHIV HR Platform - Quick Deploy
echo ================================

REM Load environment variables
set DB_PASSWORD=bhiv_local_password_2025
set API_KEY_SECRET=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o
set JWT_SECRET=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA

echo 1. Stopping services...
docker-compose -f deployment\docker\docker-compose.production.yml down

echo 2. Cleaning Docker system...
docker system prune -a --volumes --force

echo 3. Building and starting services...
docker-compose -f deployment\docker\docker-compose.production.yml up -d --build

echo 4. Checking status...
timeout /t 30 /nobreak >nul
docker ps

echo ✅ Deployment completed!
echo Services available at:
echo - Gateway: http://localhost:8000
echo - Agent: http://localhost:9000
echo - HR Portal: http://localhost:8501
echo - Client Portal: http://localhost:8502