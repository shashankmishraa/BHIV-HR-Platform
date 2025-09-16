@echo off
echo ========================================
echo BHIV HR Platform - Deployment Test
echo ========================================
echo.

echo Testing all services...
echo.

echo 1. Gateway Health Check...
curl -s http://localhost:8000/health
if %errorlevel% equ 0 (
    echo ✓ Gateway: PASS
) else (
    echo ✗ Gateway: FAIL
)
echo.

echo 2. Database Connectivity...
curl -s -H "Authorization: Bearer myverysecureapikey123" http://localhost:8000/test-db
if %errorlevel% equ 0 (
    echo ✓ Database: PASS
) else (
    echo ✗ Database: FAIL
)
echo.

echo 3. Client Authentication...
curl -s -X POST http://localhost:8000/v1/client/login -H "Content-Type: application/json" -d "{\"client_id\": \"TECH001\", \"password\": \"demo123\"}"
if %errorlevel% equ 0 (
    echo ✓ Authentication: PASS
) else (
    echo ✗ Authentication: FAIL
)
echo.

echo 4. AI Agent Health...
curl -s http://localhost:9000/health
if %errorlevel% equ 0 (
    echo ✓ AI Agent: PASS
) else (
    echo ✗ AI Agent: FAIL
)
echo.

echo 5. Candidate Data...
curl -s http://localhost:8000/test-candidates
if %errorlevel% equ 0 (
    echo ✓ Candidates: PASS
) else (
    echo ✗ Candidates: FAIL
)
echo.

echo ========================================
echo Test Complete
echo ========================================
echo.
echo If all tests PASS, your deployment is ready!
echo If any tests FAIL, check the logs:
echo   docker-compose -f docker-compose.production.yml logs [service_name]
echo.
pause