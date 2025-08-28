@echo off
echo ========================================
echo    BHIV HR Platform - Local Setup
echo ========================================
echo.

echo Installing Python dependencies...
echo.

echo [1/3] Installing Gateway dependencies...
cd gateway
pip install -r requirements.txt
cd ..

echo [2/3] Installing Portal dependencies...
cd portal  
pip install -r requirements.txt
cd ..

echo [3/3] Installing Agent dependencies...
cd agent
pip install -r requirements.txt
cd ..

echo.
echo ========================================
echo    Starting Services (Local Mode)
echo ========================================
echo.
echo Starting PostgreSQL is required separately
echo You can use Docker for just the database:
echo   docker run -d --name bhiv-db -p 5432:5432 -e POSTGRES_USER=bhiv_user -e POSTGRES_PASSWORD=bhiv_pass -e POSTGRES_DB=bhiv_hr postgres:15-alpine
echo.
echo Then run these commands in separate terminals:
echo   1. Gateway:  cd gateway ^&^& uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
echo   2. Portal:   cd portal ^&^& streamlit run app.py --server.port=8501 --server.address=0.0.0.0  
echo   3. Agent:    cd agent ^&^& uvicorn app:app --host 0.0.0.0 --port 9000
echo.
pause