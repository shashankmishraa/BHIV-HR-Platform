import os
import pandas as pd
import PyPDF2
import docx
import re
from pathlib import Path

class PreciseResumeExtractor:
    def __init__(self, resume_folder="resume", output_csv="data/candidates.csv"):
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
        """Extract correct name from PDF"""
        # Try filename first - clean it properly
        name_from_file = Path(filename).stem
        name_from_file = re.sub(r'[_-]', ' ', name_from_file)
        name_from_file = re.sub(r'(?i)(resume|cv|curriculum|vitae)', '', name_from_file)
        name_from_file = re.sub(r'\(\d+\)', '', name_from_file)
        name_from_file = re.sub(r'[^\w\s]', '', name_from_file).strip()
        
        # If filename gives good name, use it
        if len(name_from_file) > 2 and not name_from_file.isdigit() and len(name_from_file.split()) <= 4:
            return ' '.join(word.capitalize() for word in name_from_file.split())
        
        # Extract from text - look at first few lines
        lines = [line.strip() for line in text.split('\n')[:5] if line.strip()]
        for line in lines:
            # Skip lines with common resume headers
            if any(word in line.lower() for word in ['resume', 'curriculum', 'contact', 'email', 'phone']):
                continue
            
            # Look for name pattern: 2-4 words, all alphabetic
            words = line.split()
            if 2 <= len(words) <= 4 and all(word.replace('.', '').isalpha() for word in words):
                if len(line) < 50:  # Not too long
                    return ' '.join(word.capitalize() for word in words)
        
        # Fallback to cleaned filename
        return ' '.join(word.capitalize() for word in name_from_file.split()) if name_from_file else "Unknown"
    
    def extract_email(self, text):
        """Extract email if present"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)
        # Return first valid email
        for email in emails:
            if '.' in email.split('@')[1]:  # Valid domain
                return email.lower()
        return ""
    
    def extract_phone(self, text):
        """Extract correct phone number"""
        # Indian phone patterns
        patterns = [
            r'\+91[-\s]?\d{10}',  # +91 format
            r'\+91[-\s]?\d{5}[-\s]?\d{5}',  # +91 with space/dash
            r'91[-\s]?\d{10}',  # 91 prefix
            r'\d{10}',  # 10 digit number
            r'\+\d{1,3}[-\s]?\d{10,14}'  # International format
        ]
        
        for pattern in patterns:
            phones = re.findall(pattern, text)
            for phone in phones:
                # Clean and validate
                clean_phone = re.sub(r'[-\s]', '', phone)
                if len(clean_phone) >= 10:
                    return phone
        return ""
    
    def extract_location(self, text):
        """Extract location"""
        # Indian cities
        indian_cities = [
            'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 
            'Pune', 'Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur',
            'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Patna'
        ]
        
        # International cities
        intl_cities = [
            'New York', 'San Francisco', 'Los Angeles', 'Chicago', 'Boston',
            'Seattle', 'Austin', 'Denver', 'London', 'Toronto', 'Sydney'
        ]
        
        all_cities = indian_cities + intl_cities
        
        # Check for cities in text
        for city in all_cities:
            if city.lower() in text.lower():
                return city
        
        # Look for address patterns
        address_patterns = [
            r'([A-Z][a-z]+,\s*[A-Z]{2,3})',  # City, State
            r'([A-Z][a-z]+\s+[A-Z][a-z]+,\s*[A-Z]{2})'  # City Name, State
        ]
        
        for pattern in address_patterns:
            matches = re.findall(pattern, text)
            if matches:
                return matches[0]
        
        return ""
    
    def extract_designation(self, text):
        """Extract designation if any"""
        # Common job titles
        designations = [
            'Software Engineer', 'Senior Software Engineer', 'Lead Software Engineer',
            'Software Developer', 'Senior Developer', 'Full Stack Developer',
            'Frontend Developer', 'Backend Developer', 'Web Developer',
            'Data Scientist', 'Senior Data Scientist', 'Data Analyst',
            'Machine Learning Engineer', 'AI Engineer', 'DevOps Engineer',
            'Product Manager', 'Project Manager', 'Technical Lead',
            'System Administrator', 'Database Administrator', 'Cloud Engineer'
        ]
        
        text_lower = text.lower()
        
        # Look for exact matches first
        for designation in designations:
            if designation.lower() in text_lower:
                return designation
        
        # Look for partial matches
        if 'software engineer' in text_lower or 'swe' in text_lower:
            return 'Software Engineer'
        elif 'developer' in text_lower:
            return 'Software Developer'
        elif 'data scientist' in text_lower:
            return 'Data Scientist'
        elif 'data analyst' in text_lower:
            return 'Data Analyst'
        elif 'product manager' in text_lower:
            return 'Product Manager'
        elif 'project manager' in text_lower:
            return 'Project Manager'
        
        return ""
    
    def extract_skills(self, text):
        """Extract skills they have"""
        # Technical skills list
        skills_list = [
            # Programming Languages
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin',
            # Web Technologies
            'React', 'Angular', 'Vue', 'Node.js', 'Express', 'Django', 'Flask', 'Spring Boot',
            'HTML', 'CSS', 'Bootstrap', 'jQuery', 'TypeScript',
            # Databases
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Oracle', 'Redis', 'Cassandra',
            # Cloud & DevOps
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins', 'Git', 'GitHub',
            # Data & AI
            'Machine Learning', 'Deep Learning', 'AI', 'Data Science', 'Pandas', 'NumPy',
            'TensorFlow', 'PyTorch', 'Scikit-learn', 'Tableau', 'Power BI',
            # Others
            'Linux', 'Windows', 'REST API', 'GraphQL', 'Microservices'
        ]
        
        found_skills = []
        text_lower = text.lower()
        
        for skill in skills_list:
            if skill.lower() in text_lower:
                found_skills.append(skill)
        
        return ', '.join(found_skills[:10])  # Limit to 10 skills
    
    def extract_experience(self, text):
        """Extract experience or fresher"""
        # Look for experience patterns
        exp_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?(?:experience|exp)',
            r'experience\s*:?\s*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?(?:experience|exp)'
        ]
        
        for pattern in exp_patterns:
            matches = re.findall(pattern, text.lower())
            if matches:
                years = int(matches[0])
                return f"{years} years" if years > 0 else "Fresher"
        
        # Check for fresher keywords
        fresher_keywords = ['fresher', 'fresh graduate', 'recent graduate', 'entry level']
        text_lower = text.lower()
        
        for keyword in fresher_keywords:
            if keyword in text_lower:
                return "Fresher"
        
        # Try to estimate from graduation year
        current_year = 2024
        years = re.findall(r'\b(20\d{2})\b', text)
        if years:
            years = [int(y) for y in years if 2015 <= int(y) <= current_year]
            if years:
                grad_year = max(years)  # Assume latest year is graduation
                exp_years = current_year - grad_year
                if exp_years <= 1:
                    return "Fresher"
                elif exp_years <= 25:
                    return f"{exp_years} years"
        
        return "Not Specified"
    
    def extract_education(self, text):
        """Extract education with proper if-else logic"""
        text_lower = text.lower()
        
        # Check for PhD/Doctorate first (highest priority)
        if 'phd' in text_lower or 'ph.d' in text_lower or 'doctorate' in text_lower:
            return 'PhD'
        
        # Check for Masters (second priority)
        elif ('master' in text_lower or 'mba' in text_lower or 'm.tech' in text_lower or 
              'mtech' in text_lower or 'm.s' in text_lower or 'ms' in text_lower):
            return 'Masters'
        
        # Check for Bachelors (third priority)
        elif ('bachelor' in text_lower or 'b.tech' in text_lower or 'btech' in text_lower or 
              'be' in text_lower or 'b.e' in text_lower or 'b.s' in text_lower or 
              'bs' in text_lower or 'b.a' in text_lower or 'ba' in text_lower):
            return 'Bachelors'
        
        # Check for Diploma
        elif 'diploma' in text_lower or 'polytechnic' in text_lower:
            return 'Diploma'
        
        # Check for 12th
        elif '12th' in text_lower or 'higher secondary' in text_lower or 'intermediate' in text_lower:
            return '12th'
        
        # Default for professional resumes without clear education info
        else:
            return 'Bachelors'
    
    def process_resumes(self):
        """Process all resumes individually"""
        if not os.path.exists(self.resume_folder):
            print(f"Resume folder not found: {self.resume_folder}")
            return
        
        candidates = []
        resume_files = []
        
        # Get all resume files
        for ext in ['*.pdf', '*.docx', '*.doc']:
            resume_files.extend(Path(self.resume_folder).glob(ext))
        
        print(f"Processing {len(resume_files)} resume files individually...")
        print("=" * 60)
        
        for i, file_path in enumerate(resume_files, 1):
            filename = file_path.name
            print(f"\n[{i}/{len(resume_files)}] Processing: {filename}")
            
            # Extract text
            text = self.extract_text(file_path)
            if not text.strip():
                print("  - Could not extract text")
                continue
            
            # Extract each field individually
            name = self.extract_name(text, filename)
            email = self.extract_email(text)
            phone = self.extract_phone(text)
            location = self.extract_location(text)
            designation = self.extract_designation(text)
            skills = self.extract_skills(text)
            experience = self.extract_experience(text)
            education = self.extract_education(text)
            
            # Create candidate record
            candidate = {
                'name': name,
                'email': email,
                'phone': phone,
                'location': location,
                'designation': designation,
                'skills': skills,
                'experience': experience,
                'education': education,
                'resume_name': filename
            }
            
            candidates.append(candidate)
            
            # Show extracted info
            print(f"  + Name: {name}")
            print(f"  + Email: {email if email else 'Not found'}")
            print(f"  + Phone: {phone if phone else 'Not found'}")
            print(f"  + Location: {location if location else 'Not found'}")
            print(f"  + Designation: {designation if designation else 'Not found'}")
            print(f"  + Experience: {experience}")
            print(f"  + Education: {education} (detected from text)")
            print(f"  + Skills: {skills[:50]}{'...' if len(skills) > 50 else ''}")
        
        if candidates:
            # Create output directory
            os.makedirs(os.path.dirname(self.output_csv), exist_ok=True)
            
            # Save to CSV
            df = pd.DataFrame(candidates)
            df.to_csv(self.output_csv, index=False)
            
            print(f"\n" + "=" * 60)
            print(f"SUCCESS: Processed {len(candidates)} candidates")
            print(f"Output saved to: {self.output_csv}")
            
            # Show summary statistics
            print(f"\nSummary:")
            print(f"- Names extracted: {len(df)}")
            print(f"- Emails found: {df['email'].astype(bool).sum()}")
            print(f"- Phones found: {df['phone'].astype(bool).sum()}")
            print(f"- Locations found: {df['location'].astype(bool).sum()}")
            print(f"- Designations found: {df['designation'].astype(bool).sum()}")
            
            return df
        
        print("No resumes processed successfully")
        return None

def main():
    extractor = PreciseResumeExtractor()
    extractor.process_resumes()

if __name__ == "__main__":
    main()