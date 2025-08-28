import os
import pandas as pd
import PyPDF2
import docx
import re
from pathlib import Path
import time
from datetime import datetime
import json

class ResumeProcessor:
    def __init__(self, resume_folder="resume", output_file="processed_candidates.csv"):
        self.resume_folder = resume_folder
        self.output_file = output_file
        self.processed_files = self.load_processed_files()
        
    def load_processed_files(self):
        """Load list of already processed files"""
        try:
            with open("processed_files.json", "r") as f:
                return set(json.load(f))
        except FileNotFoundError:
            return set()
    
    def save_processed_files(self):
        """Save list of processed files"""
        with open("processed_files.json", "w") as f:
            json.dump(list(self.processed_files), f)
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except Exception as e:
            print(f"Error reading DOCX {file_path}: {e}")
            return ""
    
    def extract_info_from_text(self, text, filename):
        """Extract key information from resume text"""
        # Clean text
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())
        
        # Extract name (first meaningful words, excluding common resume words)
        name = self.extract_name(text, filename)
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        email = emails[0] if emails else f"{name.lower().replace(' ', '.')}@email.com"
        
        # Extract phone
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        phone = phones[0] if phones else "+1-555-0000"
        
        # Estimate experience years
        experience_years = self.estimate_experience(text)
        
        # Generate CV URL (placeholder)
        cv_url = f"https://example.com/resumes/{filename}"
        
        return {
            'name': name,
            'email': email,
            'cv_url': cv_url,
            'phone': phone,
            'experience_years': experience_years,
            'status': 'applied'
        }
    
    def extract_name(self, text, filename):
        """Extract candidate name from text or filename"""
        # Try to get name from filename first
        name_from_file = Path(filename).stem
        name_from_file = re.sub(r'[_-]', ' ', name_from_file)
        name_from_file = re.sub(r'(?i)(resume|cv|curriculum|vitae)', '', name_from_file)
        name_from_file = name_from_file.strip()
        
        if len(name_from_file) > 3 and not name_from_file.isdigit():
            return name_from_file.title()
        
        # Try to extract from text
        lines = text.split('\n')[:5]  # Check first 5 lines
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 50:
                # Check if it looks like a name (2-4 words, mostly letters)
                words = line.split()
                if 2 <= len(words) <= 4 and all(word.replace('.', '').isalpha() for word in words):
                    return line.title()
        
        return name_from_file.title() if name_from_file else "Unknown Candidate"
    
    def estimate_experience(self, text):
        """Estimate years of experience from resume text"""
        # Look for experience patterns
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in\s*\w+',
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return int(matches[0])
        
        # Count graduation years to estimate experience
        current_year = datetime.now().year
        year_pattern = r'\b(19|20)\d{2}\b'
        years = [int(year) for year in re.findall(year_pattern, text)]
        
        if years:
            # Assume graduation year is the most recent year before current year
            grad_years = [year for year in years if 1990 <= year <= current_year]
            if grad_years:
                estimated_grad_year = max(grad_years)
                experience = max(0, current_year - estimated_grad_year - 1)
                return min(experience, 20)  # Cap at 20 years
        
        return 2  # Default to 2 years if can't determine
    
    def process_new_resumes(self):
        """Process all new resume files"""
        if not os.path.exists(self.resume_folder):
            print(f"Resume folder '{self.resume_folder}' not found!")
            return
        
        new_candidates = []
        resume_files = []
        
        # Get all resume files
        for ext in ['*.pdf', '*.docx', '*.doc']:
            resume_files.extend(Path(self.resume_folder).glob(ext))
        
        print(f"Found {len(resume_files)} resume files")
        
        for file_path in resume_files:
            filename = file_path.name
            
            # Skip if already processed
            if filename in self.processed_files:
                continue
            
            print(f"Processing: {filename}")
            
            # Extract text based on file type
            if filename.lower().endswith('.pdf'):
                text = self.extract_text_from_pdf(file_path)
            elif filename.lower().endswith(('.docx', '.doc')):
                text = self.extract_text_from_docx(file_path)
            else:
                continue
            
            if not text.strip():
                print(f"Could not extract text from {filename}")
                continue
            
            # Extract candidate information
            candidate_info = self.extract_info_from_text(text, filename)
            new_candidates.append(candidate_info)
            
            # Mark as processed
            self.processed_files.add(filename)
            
            print(f"Processed: {candidate_info['name']}")
        
        if new_candidates:
            # Create or update CSV
            df_new = pd.DataFrame(new_candidates)
            
            if os.path.exists(self.output_file):
                # Append to existing CSV
                df_existing = pd.read_csv(self.output_file)
                df_combined = pd.concat([df_existing, df_new], ignore_index=True)
                df_combined.drop_duplicates(subset=['name', 'email'], keep='last', inplace=True)
            else:
                df_combined = df_new
            
            # Save CSV
            df_combined.to_csv(self.output_file, index=False)
            self.save_processed_files()
            
            print(f"\nSuccessfully processed {len(new_candidates)} new resumes!")
            print(f"CSV saved as: {self.output_file}")
            print(f"Total candidates in CSV: {len(df_combined)}")
            
            return df_combined
        else:
            print("No new resumes to process.")
            return None
    
    def monitor_folder(self, interval=30):
        """Monitor folder for new resumes continuously"""
        print(f"Monitoring '{self.resume_folder}' folder for new resumes...")
        print(f"Check interval: {interval} seconds")
        print("Press Ctrl+C to stop monitoring\n")
        
        try:
            while True:
                self.process_new_resumes()
                print(f"Waiting {interval} seconds for new files...")
                time.sleep(interval)
        except KeyboardInterrupt:
            print("\nMonitoring stopped by user")

def main():
    processor = ResumeProcessor()
    
    print("BHIV Resume Processor")
    print("=" * 40)
    
    choice = input("Choose option:\n1. Process all new resumes now\n2. Monitor folder continuously\nEnter (1 or 2): ")
    
    if choice == "1":
        df = processor.process_new_resumes()
        if df is not None:
            print("\nPreview of processed candidates:")
            print(df[['name', 'email', 'experience_years']].head())
    elif choice == "2":
        processor.monitor_folder()
    else:
        print("Invalid choice. Processing once...")
        processor.process_new_resumes()

if __name__ == "__main__":
    main()