@echo off
echo ========================================
echo BHIV HR Platform - Week 2 Testing Script
echo Testing all ports: 8000, 8501, 8502, 9000, 5432
echo ========================================

echo.
echo [1/6] Checking if all services are running...
docker-compose -f docker-compose.production.yml ps

echo.
echo [2/6] Testing Port 8000 - Gateway API Health...
curl -s http://localhost:8000/health | findstr "week_2_complete"
if %errorlevel%==0 (
    echo ✅ Port 8000: Week 2 features detected
) else (
    echo ❌ Port 8000: Week 2 features not found
)

echo.
echo [3/6] Testing Port 8501 - HR Portal...
curl -s -o nul -w "%%{http_code}" http://localhost:8501 > temp_status.txt
set /p status=<temp_status.txt
if "%status%"=="200" (
    echo ✅ Port 8501: HR Portal responding
) else (
    echo ❌ Port 8501: HR Portal not responding
)
del temp_status.txt

echo.
echo [4/6] Testing Port 8502 - Client Portal...
curl -s -o nul -w "%%{http_code}" http://localhost:8502 > temp_status.txt
set /p status=<temp_status.txt
if "%status%"=="200" (
    echo ✅ Port 8502: Client Portal responding
) else (
    echo ❌ Port 8502: Client Portal not responding
)
del temp_status.txt

echo.
echo [5/6] Testing Port 9000 - AI Agent...
curl -s -o nul -w "%%{http_code}" http://localhost:9000/health > temp_status.txt
set /p status=<temp_status.txt
if "%status%"=="200" (
    echo ✅ Port 9000: AI Agent responding
) else (
    echo ❌ Port 9000: AI Agent not responding
)
del temp_status.txt

echo.
echo [6/6] Testing Port 5432 - Database...
docker exec bhivhraiplatform-db-1 pg_isready -U bhiv_user -d bhiv_hr > nul 2>&1
if %errorlevel%==0 (
    echo ✅ Port 5432: Database responding
) else (
    echo ❌ Port 5432: Database not responding
)

echo.
echo ========================================
echo Testing Week 2 Specific Features...
echo ========================================

echo.
echo Testing 2FA Demo Setup...
curl -s -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/v1/2fa/demo-setup | findstr "Demo Setup" > nul
if %errorlevel%==0 (
    echo ✅ 2FA Demo Setup: Working
) else (
    echo ❌ 2FA Demo Setup: Failed
)

echo.
echo Testing Password Policy...
curl -s -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/v1/password/policy | findstr "enterprise_password_policy" > nul
if %errorlevel%==0 (
    echo ✅ Password Policy: Working
) else (
    echo ❌ Password Policy: Failed
)

echo.
echo Testing Password Validation...
curl -s -X POST -H "Authorization: Bearer myverysecureapikey123" -H "Content-Type: application/json" -d "{\"password\":\"123456\"}" http://localhost:8000/v1/password/validate | findstr "valid" > nul
if %errorlevel%==0 (
    echo ✅ Password Validation: Working
) else (
    echo ❌ Password Validation: Failed
)

echo.
echo ========================================
echo Week 2 Testing Complete!
echo ========================================
echo.
echo Next Steps:
echo 1. Open http://localhost:8000/docs to test 2FA setup
echo 2. Open http://localhost:8502 to test client portal 2FA
echo 3. Install Google Authenticator for full 2FA testing
echo 4. Use the QR code from /v1/2fa/setup endpoint
echo.
echo For detailed testing: See WEEK_2_MULTI_PORT_TESTING.md
echo ========================================

pause