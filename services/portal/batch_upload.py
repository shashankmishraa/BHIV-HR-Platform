import streamlit as st
import os
from pathlib import Path
import zipfile
import tempfile
import httpx
import json

def show_batch_upload():
    """Batch resume upload interface"""
    st.header("📁 Batch Resume Upload")
    
    upload_method = st.radio("Upload Method", ["Individual Files", "Zip Archive", "Folder Scan"])
    
    if upload_method == "Individual Files":
        uploaded_files = st.file_uploader(
            "Choose resume files",
            type=['pdf', 'docx', 'doc', 'txt'],
            accept_multiple_files=True,
            help="Select multiple resume files to upload"
        )
        
        if uploaded_files:
            st.success(f"Selected {len(uploaded_files)} files")
            
            if st.button("Process All Resumes"):
                process_uploaded_files(uploaded_files)
    
    elif upload_method == "Zip Archive":
        zip_file = st.file_uploader("Upload ZIP file containing resumes", type=['zip'])
        
        if zip_file:
            if st.button("Extract and Process"):
                process_zip_file(zip_file)
    
    elif upload_method == "Folder Scan":
        st.info("📂 Folder Scan Mode")
        st.write("This will scan the resume/ folder for new files")
        
        if st.button("Scan Resume Folder"):
            scan_resume_folder()

def process_uploaded_files(uploaded_files):
    """Process individual uploaded files"""
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    try:
        # Ensure resume folder exists with proper permissions
        resume_folder = Path("/app/resume")
        resume_folder.mkdir(parents=True, exist_ok=True)
        
        for i, uploaded_file in enumerate(uploaded_files):
            status_text.text(f"Processing {uploaded_file.name}...")
            
            # Save file to resume folder
            resume_path = resume_folder / uploaded_file.name
            with open(resume_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            progress_bar.progress((i + 1) / len(uploaded_files))
        
        status_text.text("Files uploaded successfully!")
        st.success(f"Uploaded {len(uploaded_files)} files to resume folder")
        
        # Auto-trigger processing
        if st.button("Extract Data and Upload to Database", use_container_width=True):
            trigger_resume_processing()
            
    except Exception as e:
        st.error(f"Upload failed: {str(e)}")
        st.info("Try using smaller files or check file permissions")

def process_zip_file(zip_file):
    """Process ZIP file containing resumes"""
    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract ZIP
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Find resume files
            resume_files = []
            for root, dirs, files in os.walk(temp_dir):
                for file in files:
                    if file.lower().endswith(('.pdf', '.docx', '.doc', '.txt')):
                        resume_files.append(os.path.join(root, file))
            
            if resume_files:
                st.success(f"Found {len(resume_files)} resume files in ZIP")
                
                # Ensure resume folder exists
                resume_folder = Path("/app/resume")
                resume_folder.mkdir(parents=True, exist_ok=True)
                
                # Copy to resume folder
                for file_path in resume_files:
                    filename = os.path.basename(file_path)
                    dest_path = resume_folder / filename
                    
                    with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
                        dst.write(src.read())
                
                st.success(f"Extracted {len(resume_files)} files to resume folder")
                
                if st.button("Extract Data and Upload to Database", use_container_width=True):
                    trigger_resume_processing()
            else:
                st.error("No resume files found in ZIP archive")
                
    except Exception as e:
        st.error(f"ZIP processing failed: {str(e)}")

def scan_resume_folder():
    """Scan resume folder for new files"""
    resume_folder = Path("/app/resume")
    
    try:
        resume_folder.mkdir(parents=True, exist_ok=True)
        resume_files = list(resume_folder.glob("*.pdf")) + list(resume_folder.glob("*.docx")) + list(resume_folder.glob("*.txt"))
        
        st.info(f"Found {len(resume_files)} resume files in folder")
        
        for file in resume_files[:10]:  # Show first 10
            st.write(f"📄 {file.name}")
        
        if len(resume_files) > 10:
            st.write(f"... and {len(resume_files) - 10} more files")
        
        if st.button("Extract Data and Upload All Files", use_container_width=True):
            trigger_resume_processing()
            
    except Exception as e:
        st.error(f"Folder scan failed: {str(e)}")

def trigger_resume_processing():
    """Trigger resume processing and upload to API"""
    import httpx
    import os
    
    API_BASE = os.getenv("GATEWAY_URL", "http://gateway:8000")
    API_KEY = os.getenv("API_KEY_SECRET", "myverysecureapikey123")
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    with st.spinner("Processing resumes and uploading to database..."):
        try:
            # First run resume extraction
            import subprocess
            result = subprocess.run(
                ["python", "/app/tools/comprehensive_resume_extractor.py"],
                capture_output=True,
                text=True,
                cwd="/app"
            )
            
            if result.returncode == 0:
                st.success("✅ Resume extraction completed!")
                
                # Now read the extracted data and upload via API
                import json
                from pathlib import Path
                
                # Check if extracted data file exists
                data_file = Path("/app/data/extracted_candidates.json")
                if data_file.exists():
                    with open(data_file, 'r') as f:
                        candidates_data = json.load(f)
                    
                    if candidates_data:
                        # Upload to API
                        response = httpx.post(
                            f"{API_BASE}/v1/candidates/bulk",
                            json={"candidates": candidates_data},
                            headers=headers,
                            timeout=30.0
                        )
                        
                        if response.status_code == 200:
                            result_data = response.json()
                            st.success(f"✅ Successfully uploaded {result_data.get('candidates_inserted', 0)} candidates to database!")
                            st.info("📊 Candidates are now available for AI matching and search")
                        else:
                            st.error(f"❌ API upload failed: {response.text}")
                    else:
                        st.warning("⚠️ No candidate data extracted from resumes")
                else:
                    st.warning("⚠️ No extracted data file found. Please check resume extraction process.")
            else:
                st.error("❌ Resume processing failed")
                st.code(result.stderr)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")