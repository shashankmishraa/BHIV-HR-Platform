import os
import pandas as pd
import PyPDF2
import re
from pathlib import Path
from datetime import datetime

class PDFToCSVConverter:
    def __init__(self, pdf_folder="resume", output_csv="data/candidates.csv"):
        self.pdf_folder = pdf_folder
        self.output_csv = output_csv
        
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
    
    def extract_name(self, text, filename):
        """Extract candidate name with improved logic"""
        # Clean filename first
        name_from_file = Path(filename).stem
        name_from_file = re.sub(r'[_-]', ' ', name_from_file)
        name_from_file = re.sub(r'(?i)(resume|cv|curriculum|vitae)', '', name_from_file)
        name_from_file = name_from_file.strip()
        
        # If filename has a good name, use it
        if len(name_from_file) > 3 and not name_from_file.isdigit():
            return name_from_file.title()
        
        # Extract from text - look at first few lines
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if 5 < len(line) < 50:
                words = line.split()
                if 2 <= len(words) <= 4 and all(word.replace('.', '').isalpha() for word in words):
                    return line.title()
        
        return name_from_file.title() if name_from_file else "Unknown Candidate"
    
    def extract_email(self, text):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else ""
    
    def extract_phone(self, text):
        """Extract phone number"""
        phone_patterns = [
            r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\+?\d{10,15}',
            r'\(\d{3}\)\s?\d{3}-?\d{4}'
        ]
        
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return ""
    
    def extract_location(self, text):
        """Extract location"""
        # Look for city, state patterns
        location_patterns = [
            r'([A-Z][a-z]+,\s*[A-Z]{2}(?:\s+\d{5})?)',
            r'([A-Z][a-z]+\s+[A-Z][a-z]+,\s*[A-Z]{2})',
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].strip()
        
        # Common cities
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 
                 'San Francisco', 'Boston', 'Seattle', 'Austin', 'Denver',
                 'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai']
        
        for city in cities:
            if city.lower() in text.lower():
                return city
        
        return ""
    
    def extract_skills(self, text):
        """Extract basic skills"""
        # Common technical skills
        common_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle',
            'AWS', 'Azure', 'Docker', 'Kubernetes', 'Git',
            'Machine Learning', 'AI', 'Data Science', 'Analytics'
        ]
        
        skills = []
        text_lower = text.lower()
        for skill in common_skills:
            if skill.lower() in text_lower:
                skills.append(skill)
        
        return ', '.join(skills[:10])  # Limit to 10 skills
    
    def extract_experience_years(self, text):
        """Extract years of experience"""
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return int(matches[0])
        
        # Estimate from graduation year
        current_year = datetime.now().year
        year_pattern = r'\b(19|20)\d{2}\b'
        years = [int(year) for year in re.findall(year_pattern, text)]
        
        if years:
            grad_years = [year for year in years if 1990 <= year <= current_year]
            if grad_years:
                estimated_grad_year = max(grad_years)
                experience = max(0, current_year - estimated_grad_year - 1)
                return min(experience, 25)
        
        return 0
    
    def extract_education(self, text):
        """Extract education level"""
        education_keywords = {
            'PhD': ['phd', 'ph.d', 'doctorate', 'doctoral'],
            'Masters': ['masters', 'master', 'm.s', 'ms', 'm.a', 'ma', 'mba'],
            'Bachelors': ['bachelor', 'bachelors', 'b.s', 'bs', 'b.a', 'ba', 'b.tech'],
            'Associates': ['associate', 'associates', 'diploma'],
            'High School': ['high school', 'secondary', '12th']
        }
        
        text_lower = text.lower()
        for level, keywords in education_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        return ""
    
    def extract_job_title(self, text):
        """Extract current/recent job title"""
        # Look for common job titles
        title_patterns = [
            r'(?i)(software engineer|developer|programmer|data scientist|analyst|manager|director|lead|senior|architect)',
            r'(?i)(product manager|project manager|consultant|specialist|coordinator)'
        ]
        
        for pattern in title_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0].title()
        
        return ""
    
    def convert_pdfs_to_csv(self):
        """Convert all PDFs to CSV with enhanced extraction"""
        if not os.path.exists(self.pdf_folder):
            print(f"PDF folder '{self.pdf_folder}' not found!")
            return
        
        candidates = []
        pdf_files = list(Path(self.pdf_folder).glob('*.pdf'))
        
        print(f"Found {len(pdf_files)} PDF files")
        print("Converting PDFs to CSV with enhanced extraction...")
        
        for pdf_file in pdf_files:
            filename = pdf_file.name
            print(f"Processing: {filename}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_file)
            if not text.strip():
                print(f"Could not extract text from {filename}")
                continue
            
            # Extract candidate information
            candidate_data = {
                'name': self.extract_name(text, filename),
                'email': self.extract_email(text),
                'phone': self.extract_phone(text),
                'location': self.extract_location(text),
                'skills': self.extract_skills(text),
                'experience_years': self.extract_experience_years(text),
                'education_level': self.extract_education(text),
                'job_title': self.extract_job_title(text),
                'cv_url': f"https://example.com/resumes/{filename}",
                'status': 'applied',
                'resume_filename': filename,
                'processed_date': datetime.now().isoformat()
            }
            
            candidates.append(candidate_data)
            print(f"Extracted: {candidate_data['name']} - {candidate_data['job_title']} - {candidate_data['experience_years']} years")
        
        if candidates:
            # Ensure output directory exists
            os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
            
            # Create CSV
            df = pd.DataFrame(candidates)
            df.to_csv(self.output_csv, index=False)
            
            print(f"\nSuccessfully converted {len(candidates)} PDFs to CSV!")
            print(f"Output file: {self.output_csv}")
            print(f"Total candidates: {len(df)}")
            
            # Show preview
            print("\nPreview:")
            print(df[['name', 'job_title', 'experience_years', 'education_level', 'skills']].head())
            
            return df
        else:
            print("No PDFs processed successfully.")
            return None

def main():
    """Main function to run PDF to CSV conversion"""
    converter = PDFToCSVConverter()
    
    print("BHIV PDF to CSV Converter")
    print("=" * 40)
    print("Converting PDF resumes to structured CSV data...")
    
    df = converter.convert_pdfs_to_csv()
    
    if df is not None:
        print(f"\nConversion complete!")
        print(f"Fields extracted:")
        print("   - Basic: name, email, phone, location")
        print("   - Professional: job_title, experience_years, skills")
        print("   - Education: education_level")
        print("   - System: cv_url, status, resume_filename")

if __name__ == "__main__":
    main()