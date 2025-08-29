import os
import pandas as pd
import PyPDF2
import re
from pathlib import Path
from datetime import datetime

class CleanResumeProcessor:
    def __init__(self):
        self.resume_folder = "resume"
        self.output_file = "data/clean_candidates.csv"
        
    def extract_text_from_pdf(self, file_path):
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text.strip()
        except Exception as e:
            print(f"Error reading PDF {file_path}: {e}")
            return ""
    
    def clean_text(self, text):
        # Clean and normalize text
        text = re.sub(r'\s+', ' ', text)  # Multiple spaces to single
        text = re.sub(r'[^\w\s@.+()-]', ' ', text)  # Keep only alphanumeric and basic chars
        return text.strip()
    
    def extract_name(self, text, filename):
        text_lines = text.split('\n')[:5]  # First 5 lines only
        
        # Look for name patterns in first few lines
        for line in text_lines:
            line = line.strip()
            # Skip lines with common resume words
            if any(word in line.lower() for word in ['resume', 'cv', 'curriculum', 'email', 'phone', 'address']):
                continue
            
            # Look for 2-3 word names
            words = line.split()
            if 2 <= len(words) <= 3 and all(word.isalpha() and len(word) > 1 for word in words):
                if all(len(word) < 15 for word in words):  # Reasonable name length
                    return ' '.join(words).title()
        
        # Fallback to filename
        name = Path(filename).stem
        name = re.sub(r'[_-]', ' ', name)
        name = re.sub(r'(?i)(resume|cv|\d+|\(\d+\))', '', name).strip()
        if name:
            return ' '.join(name.split()[:2]).title()
        
        return "Unknown Candidate"
    
    def extract_email(self, text):
        # Simple, reliable email extraction
        email_pattern = r'\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b'
        emails = re.findall(email_pattern, text)
        
        # Filter valid emails
        for email in emails:
            email = email.lower()
            if not any(fake in email for fake in ['example', 'test', 'sample', 'dummy']):
                return email
        
        return "email@notprovided.com"
    
    def extract_phone(self, text):
        # Indian phone number patterns
        patterns = [
            r'\+91[\s-]?\d{10}',  # +91 9876543210
            r'\+91[\s-]?\d{5}[\s-]?\d{5}',  # +91 98765 43210
            r'(?<!\d)\d{10}(?!\d)',  # 9876543210
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text)
            if matches:
                phone = re.sub(r'[\s-]', '', matches[0])
                if phone.startswith('+91'):
                    return phone
                elif len(phone) == 10 and phone[0] in '6789':  # Valid Indian mobile start
                    return f'+91{phone}'
        
        return "Phone not available"
    
    def extract_location(self, text):
        # Major Indian cities
        cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Pune', 'Kolkata',
            'Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur', 'Nagpur', 'Indore',
            'Thane', 'Bhopal', 'Visakhapatnam', 'Patna', 'Vadodara', 'Ghaziabad',
            'Ludhiana', 'Agra', 'Nashik', 'Faridabad', 'Meerut', 'Rajkot', 'Varanasi',
            'Srinagar', 'Aurangabad', 'Dhanbad', 'Amritsar', 'Allahabad', 'Ranchi',
            'Howrah', 'Coimbatore', 'Jabalpur', 'Gwalior', 'Vijayawada', 'Jodhpur',
            'Madurai', 'Raipur', 'Kota', 'Guwahati', 'Chandigarh', 'Solapur',
            'Hubli', 'Bareilly', 'Moradabad', 'Mysore', 'Gurgaon', 'Aligarh',
            'Jalandhar', 'Tiruchirappalli', 'Bhubaneswar', 'Salem', 'Warangal',
            'Guntur', 'Bhiwandi', 'Saharanpur', 'Gorakhpur', 'Bikaner', 'Amravati',
            'Noida', 'Jamshedpur', 'Bhilai', 'Cuttack', 'Firozabad', 'Kochi',
            'Nellore', 'Bhavnagar', 'Dehradun', 'Durgapur', 'Asansol', 'Rourkela',
            'Nanded', 'Kolhapur', 'Ajmer', 'Akola', 'Gulbarga', 'Jamnagar', 'Ujjain'
        ]
        
        text_lower = text.lower()
        for city in cities:
            if city.lower() in text_lower:
                return city
        
        return "India"
    
    def extract_skills(self, text):
        # Core technical skills
        skills_db = {
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
            'HTML', 'CSS', 'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis',
            'AWS', 'Azure', 'Docker', 'Kubernetes', 'Git', 'Linux', 'Windows',
            'Machine Learning', 'AI', 'Data Science', 'Pandas', 'NumPy',
            'TensorFlow', 'PyTorch', 'Tableau', 'Power BI', 'Excel',
            'Android', 'iOS', 'React Native', 'Flutter'
        }
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skills_db:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return ', '.join(found_skills[:8]) if found_skills else 'Basic Computer Skills'
    
    def extract_education(self, text):
        text_lower = text.lower()
        
        # Education patterns
        if any(word in text_lower for word in ['phd', 'ph.d', 'doctorate']):
            return 'PhD'
        elif any(word in text_lower for word in ['mba', 'm.b.a']):
            return 'MBA'
        elif any(word in text_lower for word in ['m.tech', 'mtech', 'master']):
            return 'Masters'
        elif any(word in text_lower for word in ['b.tech', 'btech', 'bachelor', 'be', 'b.e']):
            return 'Bachelors'
        elif any(word in text_lower for word in ['diploma', 'polytechnic']):
            return 'Diploma'
        elif any(word in text_lower for word in ['12th', 'xii', 'intermediate']):
            return '12th Pass'
        
        return 'Graduate'
    
    def estimate_experience(self, text):
        text_lower = text.lower()
        
        # Look for explicit experience mentions
        exp_patterns = [
            r'(\d+)\s*years?\s*(?:of\s*)?experience',
            r'experience\s*:?\s*(\d+)\s*years?',
            r'(\d+)\s*yrs?\s*experience'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                years = int(matches[0])
                return min(years, 10)  # Cap at 10 years
        
        # Estimate from graduation year
        current_year = datetime.now().year
        grad_years = re.findall(r'20(\d{2})', text)
        
        if grad_years:
            years = [int(f'20{y}') for y in grad_years if 2010 <= int(f'20{y}') <= current_year]
            if years:
                grad_year = max(years)  # Most recent year
                exp = current_year - grad_year - 1
                return max(0, min(exp, 8))
        
        # Keyword-based estimation
        if any(word in text_lower for word in ['fresher', 'fresh graduate', 'entry']):
            return 0
        elif any(word in text_lower for word in ['junior', 'associate']):
            return 1
        elif any(word in text_lower for word in ['senior', 'lead']):
            return 4
        
        return 2  # Default
    
    def determine_seniority(self, experience):
        if experience >= 6:
            return 'Senior'
        elif experience >= 3:
            return 'Mid-level'
        elif experience >= 1:
            return 'Junior'
        else:
            return 'Entry-level'
    

    
    def generate_summary(self, name, experience, skills, education):
        if experience == 0:
            return f"{education} graduate with skills in {skills.split(', ')[0] if skills != 'Basic Computer Skills' else 'technology'}"
        else:
            primary_skill = skills.split(', ')[0] if skills != 'Basic Computer Skills' else 'software development'
            return f"{experience} years experienced {education} professional specializing in {primary_skill}"
    
    def process_resumes(self):
        candidates = []
        resume_files = list(Path(self.resume_folder).glob('*.pdf'))
        
        print(f"Processing {len(resume_files)} resumes...")
        
        for file_path in resume_files:
            filename = file_path.name
            print(f"Processing: {filename}")
            
            try:
                text = self.extract_text_from_pdf(file_path)
                if not text.strip():
                    print(f"  -> Skipped (no text extracted)")
                    continue
                
                text = self.clean_text(text)
                
                # Extract all information
                name = self.extract_name(text, filename)
                email = self.extract_email(text)
                phone = self.extract_phone(text)
                location = self.extract_location(text)
                skills = self.extract_skills(text)
                education = self.extract_education(text)
                experience = self.estimate_experience(text)
                seniority = self.determine_seniority(experience)

                summary = self.generate_summary(name, experience, skills, education)
                
                candidate = {
                    'name': name,
                    'email': email,
                    'phone': phone,
                    'location': location,
                    'experience_years': experience,
                    'seniority_level': seniority,
                    'education_level': education,
                    'technical_skills': skills,

                    'summary': summary,
                    'availability': 'Immediate' if experience == 0 else '30 days notice',
                    'cv_url': f'/resumes/{filename}',
                    'status': 'applied',
                    'job_id': 1,
                    'processed_date': datetime.now().strftime('%Y-%m-%d')
                }
                
                candidates.append(candidate)
                print(f"  -> {name} ({seniority}, {experience} years)")
                
            except Exception as e:
                print(f"  -> Error processing {filename}: {e}")
                continue
        
        if candidates:
            df = pd.DataFrame(candidates)
            df.to_csv(self.output_file, index=False)
            print(f"\nSuccessfully saved {len(candidates)} candidates to {self.output_file}")
            
            # Summary statistics
            print(f"Skills extracted: {len(set([skill.strip() for candidate in candidates for skill in candidate['technical_skills'].split(',') if skill.strip() != 'Basic Computer Skills']))} unique skills")
            print(f"Locations found: {len(set([c['location'] for c in candidates]))} cities")
            print(f"Experience range: {min([c['experience_years'] for c in candidates])}-{max([c['experience_years'] for c in candidates])} years")
            
            return df
        else:
            print("No candidates processed successfully")
            return None

if __name__ == "__main__":
    processor = CleanResumeProcessor()
    processor.process_resumes()