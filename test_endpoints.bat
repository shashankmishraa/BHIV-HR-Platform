@echo off
echo 🧪 Testing Key Endpoints
echo =========================

set API_KEY=prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o

echo.
echo 1️⃣ Health Check:
curl -s http://localhost:8000/health

echo.
echo 2️⃣ Client Registration:
curl -X POST http://localhost:8000/v1/client/register ^
  -H "Content-Type: application/json" ^
  -d "{\"client_id\":\"TEST001\",\"company_name\":\"Test Corp\",\"contact_email\":\"test@corp.com\",\"password\":\"Test123!\"}"

echo.
echo 3️⃣ Candidate Registration:
curl -X POST http://localhost:8000/v1/candidate/register ^
  -H "Content-Type: application/json" ^
  -d "{\"name\":\"Jane Doe\",\"email\":\"jane@example.com\",\"password\":\"Pass123!\",\"technical_skills\":\"Python, React\"}"

echo.
echo 4️⃣ Create Job:
curl -X POST http://localhost:8000/v1/jobs ^
  -H "Authorization: Bearer %API_KEY%" ^
  -H "Content-Type: application/json" ^
  -d "{\"title\":\"Developer\",\"department\":\"Tech\",\"location\":\"Remote\",\"experience_level\":\"Mid\",\"requirements\":\"Python\",\"description\":\"Python developer\"}"

echo.
echo 5️⃣ Get Jobs:
curl -H "Authorization: Bearer %API_KEY%" http://localhost:8000/v1/jobs

echo.
echo 6️⃣ Get Candidates:
curl -H "Authorization: Bearer %API_KEY%" http://localhost:8000/v1/candidates

echo.
echo ✅ Endpoint testing completed!
pause