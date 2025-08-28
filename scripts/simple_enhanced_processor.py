import os
import pandas as pd
import PyPDF2
import docx
import re
from pathlib import Path
from datetime import datetime

class SimpleEnhancedProcessor:
    def __init__(self):
        self.resume_folder = "../resume"
        self.output_file = "../data/enhanced_candidates.csv"
        
    def extract_text_from_pdf(self, file_path):
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
    
    def extract_enhanced_info(self, text, filename):
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())
        
        # Basic extraction
        name = self.extract_name(text, filename)
        email = self.extract_email(text)
        phone = self.extract_phone(text)
        location = self.extract_location(text)
        skills = self.extract_skills(text)
        experience = self.estimate_experience(text)
        education = self.extract_education(text)
        
        return {
            'name': name,
            'email': email,
            'phone': phone,
            'location': location,
            'experience_years': experience,
            'education_level': education,
            'technical_skills': skills,
            'seniority_level': self.determine_seniority(experience),
            'cv_url': f"https://example.com/resumes/{filename}",
            'status': 'applied',
            'job_id': 1
        }
    
    def extract_name(self, text, filename):
        name_from_file = Path(filename).stem
        name_from_file = re.sub(r'[_-]', ' ', name_from_file)
        name_from_file = re.sub(r'(?i)(resume|cv)', '', name_from_file).strip()
        return name_from_file.title() if name_from_file else "Unknown"
    
    def extract_email(self, text):
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else "no-email@example.com"
    
    def extract_phone(self, text):
        phone_pattern = r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(phone_pattern, text)
        return phones[0] if phones else "+1-555-0000"
    
    def extract_location(self, text):
        cities = ['Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata']
        for city in cities:
            if city.lower() in text.lower():
                return city
        return "Not specified"
    
    def extract_skills(self, text):
        skills = []
        common_skills = ['Python', 'Java', 'JavaScript', 'React', 'SQL', 'AWS', 'Docker', 'Git']
        for skill in common_skills:
            if skill.lower() in text.lower():
                skills.append(skill)
        return ', '.join(skills[:8])
    
    def extract_education(self, text):
        if any(word in text.lower() for word in ['phd', 'doctorate']):
            return 'PhD'
        elif any(word in text.lower() for word in ['master', 'mba', 'm.tech']):
            return 'Masters'
        elif any(word in text.lower() for word in ['bachelor', 'b.tech', 'be']):
            return 'Bachelors'
        return 'Not specified'
    
    def estimate_experience(self, text):
        exp_pattern = r'(\d+)\+?\s*years?\s*(?:of\s*)?experience'
        matches = re.findall(exp_pattern, text.lower())
        if matches:
            return int(matches[0])
        
        current_year = datetime.now().year
        years = re.findall(r'\b(20\d{2})\b', text)
        if years:
            grad_year = max([int(y) for y in years if int(y) <= current_year])
            return max(0, current_year - grad_year - 1)
        return 2
    
    def determine_seniority(self, experience):
        if experience >= 8:
            return 'Senior'
        elif experience >= 4:
            return 'Mid-level'
        else:
            return 'Entry-level'
    
    def process_resumes(self):
        candidates = []
        resume_files = list(Path(self.resume_folder).glob('*.pdf'))
        
        print(f"Processing {len(resume_files)} resumes...")
        
        for file_path in resume_files:
            filename = file_path.name
            print(f"Processing: {filename}")
            
            text = self.extract_text_from_pdf(file_path)
            if text.strip():
                candidate_info = self.extract_enhanced_info(text, filename)
                candidates.append(candidate_info)
                print(f"  -> {candidate_info['name']} ({candidate_info['seniority_level']})")
        
        if candidates:
            df = pd.DataFrame(candidates)
            df.to_csv(self.output_file, index=False)
            print(f"\nSaved {len(candidates)} candidates to {self.output_file}")
            return df
        return None

if __name__ == "__main__":
    processor = SimpleEnhancedProcessor()
    processor.process_resumes()