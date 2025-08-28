import pandas as pd
import httpx
import time
from resume_processor import ResumeProcessor

class AutoResumeUploader:
    def __init__(self, api_base="http://localhost:8000", api_key="myverysecureapikey123"):
        self.api_base = api_base
        self.headers = {"X-API-KEY": api_key}
        self.processor = ResumeProcessor()
    
    def upload_to_platform(self, csv_file="processed_candidates.csv", job_id=1):
        """Upload processed candidates to BHIV HR Platform"""
        try:
            # Read CSV
            df = pd.read_csv(csv_file)
            print(f"Found {len(df)} candidates in CSV")
            
            # Convert to API format
            candidates = []
            for _, row in df.iterrows():
                candidate = {
                    "name": str(row['name']),
                    "email": str(row['email']),
                    "cv_url": str(row['cv_url']),
                    "phone": str(row.get('phone', '')),
                    "experience_years": int(row.get('experience_years', 2)),
                    "status": str(row.get('status', 'applied')),
                    "job_id": job_id
                }
                candidates.append(candidate)
            
            # Upload to platform
            response = httpx.post(
                f"{self.api_base}/v1/candidates/bulk",
                json={"candidates": candidates},
                headers=self.headers,
                timeout=30.0
            )
            
            if response.status_code == 200:
                result = response.json()
                print(f"Successfully uploaded {result.get('count', len(candidates))} candidates to Job ID: {job_id}")
                return True
            else:
                print(f"Upload failed: {response.text}")
                return False
                
        except Exception as e:
            print(f"Error uploading: {str(e)}")
            return False
    
    def process_and_upload(self, job_id=1):
        """Process new resumes and upload to platform"""
        print("Processing new resumes...")
        df = self.processor.process_new_resumes()
        
        if df is not None and len(df) > 0:
            print(f"Uploading {len(df)} candidates to HR Platform...")
            success = self.upload_to_platform(job_id=job_id)
            if success:
                print("Complete! Candidates are now available for AI matching.")
            return success
        else:
            print("No new resumes to process.")
            return True
    
    def monitor_and_auto_upload(self, job_id=1, interval=60):
        """Monitor folder and auto-upload new resumes"""
        print(f"Auto-monitoring mode: Job ID {job_id}, Check every {interval}s")
        print("Press Ctrl+C to stop\n")
        
        try:
            while True:
                self.process_and_upload(job_id)
                print(f"Waiting {interval} seconds...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nAuto-upload stopped")

def main():
    uploader = AutoResumeUploader()
    
    print("BHIV Auto Resume Uploader")
    print("=" * 40)
    
    # Get job ID
    try:
        job_id = int(input("Enter Job ID to upload candidates to (default: 1): ") or "1")
    except ValueError:
        job_id = 1
    
    choice = input(f"\nChoose option:\n1. Process & upload once (Job ID: {job_id})\n2. Monitor & auto-upload continuously\n3. Just upload existing CSV\nEnter (1, 2, or 3): ")
    
    if choice == "1":
        uploader.process_and_upload(job_id)
    elif choice == "2":
        uploader.monitor_and_auto_upload(job_id)
    elif choice == "3":
        uploader.upload_to_platform(job_id=job_id)
    else:
        print("Invalid choice. Processing once...")
        uploader.process_and_upload(job_id)

if __name__ == "__main__":
    main()