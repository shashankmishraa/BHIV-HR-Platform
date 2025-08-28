@echo off
echo ========================================
echo    BHIV Resume Monitor - Auto Upload
echo ========================================
echo.
echo This will monitor the 'resume' folder for new files
echo and automatically process and upload them to Job ID: 1
echo.
echo Press Ctrl+C to stop monitoring
echo.
pause

python -c "
from auto_upload_resumes import AutoResumeUploader
uploader = AutoResumeUploader()
uploader.monitor_and_auto_upload(job_id=1, interval=30)
"