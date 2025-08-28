from auto_upload_resumes import AutoResumeUploader

# Upload existing processed candidates
uploader = AutoResumeUploader()
print("Uploading processed candidates to HR Platform...")
success = uploader.upload_to_platform(job_id=1)

if success:
    print("\nAll candidates uploaded! You can now:")
    print("1. Go to http://localhost:8501")
    print("2. Select 'View Top-5 Shortlist'") 
    print("3. Enter Job ID: 1")
    print("4. Click 'Generate Shortlist' to see your real candidates!")
else:
    print("Upload failed. Make sure the HR platform is running.")