@echo off
echo ========================================
echo BHIV HR Platform - Render Schema Deploy
echo ========================================
echo.

cd /d "%~dp0"

echo Installing required dependencies...
pip install psycopg2-binary

echo.
echo Starting schema deployment to Render...
python deploy_schema_to_render.py

echo.
echo Deployment completed!
pause