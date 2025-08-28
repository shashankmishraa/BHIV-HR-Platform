@echo off
echo ========================================
echo    BHIV Resume Processor
echo ========================================
echo.

echo Installing required packages...
pip install -r resume_requirements.txt

echo.
echo Starting resume processor...
python resume_processor.py

pause