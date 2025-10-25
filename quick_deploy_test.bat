@echo off
echo 🚀 BHIV HR Platform - Quick Local Deploy & Test
echo ================================================

echo.
echo 📋 Step 1: Starting Docker Services...
docker-compose -f deployment\docker\docker-compose.production.yml up -d

echo.
echo ⏳ Waiting for services to start (30 seconds)...
timeout /t 30 /nobreak

echo.
echo 📋 Step 2: Testing Health Endpoints...
curl -s http://localhost:8000/health
echo.
curl -s http://localhost:9000/health

echo.
echo 📋 Step 3: Testing Client Registration...
curl -X POST http://localhost:8000/v1/client/register ^
  -H "Content-Type: application/json" ^
  -d "{\"client_id\":\"TESTCLIENT01\",\"company_name\":\"Test Company Ltd\",\"contact_email\":\"admin@testcompany.com\",\"password\":\"SecurePass123!\"}"

echo.
echo 📋 Step 4: Testing Client Login...
curl -X POST http://localhost:8000/v1/client/login ^
  -H "Content-Type: application/json" ^
  -d "{\"client_id\":\"TESTCLIENT01\",\"password\":\"SecurePass123!\"}"

echo.
echo 📋 Step 5: Creating Job...
curl -X POST http://localhost:8000/v1/jobs ^
  -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Senior Python Developer\",\"department\":\"Engineering\",\"location\":\"San Francisco, CA\",\"experience_level\":\"Senior\",\"requirements\":\"Python, FastAPI, PostgreSQL\",\"description\":\"Senior Python developer needed\"}"

echo.
echo 📋 Step 6: Testing Candidate Registration...
curl -X POST http://localhost:8000/v1/candidate/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"John Smith\",\"email\":\"john.smith@example.com\",\"password\":\"CandidatePass123!\",\"phone\":\"+1-555-0123\",\"location\":\"San Francisco, CA\",\"experience_years\":5,\"technical_skills\":\"Python, FastAPI, PostgreSQL\"}"

echo.
echo 📋 Step 7: Getting Jobs List...
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" ^
     http://localhost:8000/v1/jobs

echo.
echo 🌐 Portal URLs:
echo    Client Portal: http://localhost:8502
echo    HR Portal: http://localhost:8501  
echo    Candidate Portal: http://localhost:8503
echo.
echo ✅ Local deployment and basic testing completed!
echo    Check the portal URLs above to continue testing
pause