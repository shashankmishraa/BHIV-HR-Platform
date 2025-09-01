import streamlit as st
import os
from pathlib import Path
import zipfile
import tempfile

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
    
    for i, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing {uploaded_file.name}...")
        
        # Save file to resume folder
        resume_path = Path("resume") / uploaded_file.name
        with open(resume_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        progress_bar.progress((i + 1) / len(uploaded_files))
    
    status_text.text("Processing complete!")
    st.success(f"Uploaded {len(uploaded_files)} files to resume folder")
    
    # Trigger processing
    if st.button("Extract Data from Uploaded Resumes"):
        trigger_resume_processing()

def process_zip_file(zip_file):
    """Process ZIP file containing resumes"""
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
            
            # Copy to resume folder
            for file_path in resume_files:
                filename = os.path.basename(file_path)
                dest_path = Path("resume") / filename
                
                with open(file_path, 'rb') as src, open(dest_path, 'wb') as dst:
                    dst.write(src.read())
            
            st.success(f"Extracted {len(resume_files)} files to resume folder")
            trigger_resume_processing()
        else:
            st.error("No resume files found in ZIP archive")

def scan_resume_folder():
    """Scan resume folder for new files"""
    resume_folder = Path("resume")
    if not resume_folder.exists():
        st.error("Resume folder not found")
        return
    
    resume_files = list(resume_folder.glob("*.pdf")) + list(resume_folder.glob("*.docx")) + list(resume_folder.glob("*.txt"))
    
    st.info(f"Found {len(resume_files)} resume files in folder")
    
    for file in resume_files[:10]:  # Show first 10
        st.write(f"📄 {file.name}")
    
    if len(resume_files) > 10:
        st.write(f"... and {len(resume_files) - 10} more files")
    
    if st.button("Process All Files in Folder"):
        trigger_resume_processing()

def trigger_resume_processing():
    """Trigger resume processing"""
    with st.spinner("Processing resumes..."):
        try:
            import subprocess
            result = subprocess.run(
                ["python", "tools/comprehensive_resume_extractor.py"],
                capture_output=True,
                text=True,
                cwd="."
            )
            
            if result.returncode == 0:
                st.success("✅ Resume processing completed!")
                st.text("Output:")
                st.code(result.stdout)
                
                # Trigger database sync
                sync_result = subprocess.run(
                    ["python", "tools/database_sync_manager.py"],
                    capture_output=True,
                    text=True,
                    cwd="."
                )
                
                if sync_result.returncode == 0:
                    st.success("✅ Database sync completed!")
                else:
                    st.error("❌ Database sync failed")
                    st.code(sync_result.stderr)
            else:
                st.error("❌ Resume processing failed")
                st.code(result.stderr)
                
        except Exception as e:
            st.error(f"Error: {str(e)}")