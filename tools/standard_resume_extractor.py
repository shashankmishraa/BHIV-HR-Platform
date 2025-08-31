import os
import pandas as pd
import PyPDF2
import docx
import re
from pathlib import Path

class StandardResumeExtractor:
    def __init__(self, resume_folder="resume", output_csv="data/standard_candidates.csv"):
        self.resume_folder = resume_folder
        self.output_csv = output_csv
        
    def extract_text(self, file_path):
        """Extract text from PDF or DOCX"""
        try:
            if file_path.suffix.lower() == '.pdf':
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                doc = docx.Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs])
        except:
            return ""
        return ""
    
    def extract_name(self, text, filename):
        """Extract name from filename or text"""
        # Clean filename
        name = Path(filename).stem
        name = re.sub(r'[_-]', ' ', name)
        name = re.sub(r'(?i)(resume|cv|curriculum)', '', name)
        name = re.sub(r'\(\d+\)', '', name).strip()
        
        if len(name) > 2 and not name.isdigit():
            return name.title()
        
        # Extract from text first lines
        lines = text.split('\n')[:3]
        for line in lines:
            line = line.strip()
            if 3 < len(line) < 40 and len(line.split()) <= 3:
                if all(word.replace('.', '').isalpha() for word in line.split()):
                    return line.title()
        
        return name.title() if name else "Unknown"
    
    def extract_email(self, text):
        """Extract email"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)
        return emails[0] if emails else ""
    
    def extract_phone(self, text):
        """Extract phone number"""
        patterns = [
            r'\+91[-\s]?\d{10}',
            r'\+\d{1,3}[-\s]?\d{10,14}',
            r'\d{10}'
        ]
        for pattern in patterns:
            phones = re.findall(pattern, text)
            if phones:
                return phones[0]
        return ""
    
    def extract_skills(self, text):
        """Extract technical skills"""
        skills_list = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins',
            'Git', 'HTML', 'CSS', 'Bootstrap', 'jQuery',
            'Machine Learning', 'AI', 'Data Science', 'Tableau', 'Power BI'
        ]
        
        found_skills = []
        text_lower = text.lower()
        for skill in skills_list:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return '; '.join(found_skills[:8])
    
    def extract_experience(self, text):
        """Extract years of experience"""
        patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'experience\s*:?\s*(\d+)\+?\s*years?'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                return int(matches[0])
        
        # Estimate from years mentioned
        years = re.findall(r'\b(20\d{2})\b', text)
        if years:
            years = [int(y) for y in years if 2000 <= int(y) <= 2024]
            if years:
                return max(0, 2024 - min(years))
        
        return 0
    
    def extract_education(self, text):
        """Extract highest education"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['phd', 'ph.d', 'doctorate']):
            return 'PhD'
        elif any(word in text_lower for word in ['master', 'mba', 'm.tech', 'ms', 'ma']):
            return 'Masters'
        elif any(word in text_lower for word in ['bachelor', 'b.tech', 'be', 'bs', 'ba']):
            return 'Bachelors'
        elif any(word in text_lower for word in ['diploma', 'associate']):
            return 'Diploma'
        
        return 'Not Specified'
    
    def extract_location(self, text):
        """Extract location"""
        cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune',
            'New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Boston', 'Seattle'
        ]
        
        for city in cities:
            if city.lower() in text.lower():
                return city
        
        # Look for state patterns
        state_pattern = r'([A-Z][a-z]+,\s*[A-Z]{2})'
        matches = re.findall(state_pattern, text)
        if matches:
            return matches[0]
        
        return 'Not Specified'
    
    def extract_designation(self, text):
        """Extract job designation"""
        designations = [
            'Software Engineer', 'Senior Software Engineer', 'Lead Engineer',
            'Data Scientist', 'Data Analyst', 'Machine Learning Engineer',
            'Full Stack Developer', 'Frontend Developer', 'Backend Developer',
            'Product Manager', 'Project Manager', 'Team Lead',
            'DevOps Engineer', 'Cloud Engineer', 'System Administrator'
        ]
        
        text_lower = text.lower()
        for designation in designations:
            if designation.lower() in text_lower:
                return designation
        
        # Generic patterns
        if 'engineer' in text_lower:
            return 'Software Engineer'
        elif 'developer' in text_lower:
            return 'Developer'
        elif 'analyst' in text_lower:
            return 'Analyst'
        elif 'manager' in text_lower:
            return 'Manager'
        
        return 'Not Specified'
    
    def process_resumes(self):
        """Process all resumes and create standardized CSV"""
        if not os.path.exists(self.resume_folder):
            print(f"Resume folder not found: {self.resume_folder}")
            return
        
        candidates = []
        resume_files = []
        
        # Get all resume files
        for ext in ['*.pdf', '*.docx', '*.doc']:
            resume_files.extend(Path(self.resume_folder).glob(ext))
        
        print(f"Processing {len(resume_files)} resume files...")
        
        for file_path in resume_files:
            filename = file_path.name
            print(f"Processing: {filename}")
            
            text = self.extract_text(file_path)
            if not text.strip():
                print(f"  - Could not extract text")
                continue
            
            # Extract standardized fields
            candidate = {
                'id': len(candidates) + 1,
                'name': self.extract_name(text, filename),
                'email': self.extract_email(text),
                'phone': self.extract_phone(text),
                'location': self.extract_location(text),
                'designation': self.extract_designation(text),
                'skills': self.extract_skills(text),
                'experience_years': self.extract_experience(text),
                'education': self.extract_education(text),
                'resume_file': filename,
                'status': 'Active'
            }
            
            candidates.append(candidate)
            print(f"  - {candidate['name']} | {candidate['designation']} | {candidate['experience_years']}y | {candidate['education']}")
        
        if candidates:
            # Create output directory
            os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
            
            # Save to CSV
            df = pd.DataFrame(candidates)
            df.to_csv(self.output_csv, index=False)
            
            print(f"\nSUCCESS: Processed {len(candidates)} candidates")
            print(f"Output: {self.output_csv}")
            
            # Show summary
            print(f"\nSummary:")
            print(f"- With Email: {df['email'].notna().sum()}")
            print(f"- With Phone: {df['phone'].notna().sum()}")
            print(f"- Avg Experience: {df['experience_years'].mean():.1f} years")
            print(f"- Education Levels: {df['education'].value_counts().to_dict()}")
            
            return df
        
        print("No resumes processed successfully")
        return None

def main():
    extractor = StandardResumeExtractor()
    extractor.process_resumes()

if __name__ == "__main__":
    main()