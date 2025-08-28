import os
import pandas as pd
import PyPDF2
import docx
import re
from pathlib import Path
import time
from datetime import datetime
import json

class EnhancedResumeProcessor:
    def __init__(self, resume_folder="resume", output_file="enhanced_candidates.csv"):
        self.resume_folder = resume_folder
        self.output_file = output_file
        
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
    
    def extract_enhanced_info(self, text, filename):
        """Extract comprehensive information from resume text"""
        text = text.replace('\n', ' ').replace('\r', ' ')
        text = ' '.join(text.split())
        
        # Basic info
        name = self.extract_name(text, filename)
        email = self.extract_email(text, name)
        phone = self.extract_phone(text)
        
        # Enhanced fields
        location = self.extract_location(text)
        education = self.extract_education(text)
        skills = self.extract_skills(text)
        experience_years = self.estimate_experience(text)
        job_titles = self.extract_job_titles(text)
        companies = self.extract_companies(text)
        certifications = self.extract_certifications(text)
        languages = self.extract_languages(text)
        linkedin = self.extract_linkedin(text)
        github = self.extract_github(text)
        
        # AI-ready fields for better matching
        technical_skills = self.categorize_technical_skills(skills)
        seniority_level = self.determine_seniority(experience_years, job_titles, text)
        industry_experience = self.extract_industry_keywords(text)
        
        return {
            # Basic Info
            'name': name,
            'email': email,
            'phone': phone,
            'location': location,
            'linkedin_url': linkedin,
            'github_url': github,
            
            # Experience & Education
            'experience_years': experience_years,
            'seniority_level': seniority_level,
            'education_level': education,
            'certifications': certifications,
            'languages': languages,
            
            # Skills & Expertise
            'technical_skills': technical_skills,
            'all_skills': skills,
            'job_titles': job_titles,
            'companies': companies,
            'industry_keywords': industry_experience,
            
            # System Fields
            'cv_url': f"https://example.com/resumes/{filename}",
            'status': 'applied',
            'resume_filename': filename,
            'processed_date': datetime.now().isoformat()
        }
    
    def extract_name(self, text, filename):
        """Extract candidate name"""
        name_from_file = Path(filename).stem
        name_from_file = re.sub(r'[_-]', ' ', name_from_file)
        name_from_file = re.sub(r'(?i)(resume|cv|curriculum|vitae)', '', name_from_file)
        name_from_file = name_from_file.strip()
        
        if len(name_from_file) > 3 and not name_from_file.isdigit():
            return name_from_file.title()
        
        # Try to extract from text
        lines = text.split('\n')[:5]
        for line in lines:
            line = line.strip()
            if len(line) > 5 and len(line) < 50:
                words = line.split()
                if 2 <= len(words) <= 4 and all(word.replace('.', '').isalpha() for word in words):
                    return line.title()
        
        return name_from_file.title() if name_from_file else "Unknown Candidate"
    
    def extract_email(self, text, name):
        """Extract email address"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else f"{name.lower().replace(' ', '.')}@email.com"
    
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
        return "+1-555-0000"
    
    def extract_location(self, text):
        """Extract location/address"""
        location_patterns = [
            r'(?i)(address|location|based in|residing in|lives in)[\s:]+([^,\n]+(?:,\s*[^,\n]+)*)',
            r'(?i)([A-Z][a-z]+,\s*[A-Z]{2}(?:\s+\d{5})?)',
            r'(?i)([A-Z][a-z]+\s+[A-Z][a-z]+,\s*[A-Z]{2})',
        ]
        
        for pattern in location_patterns:
            matches = re.findall(pattern, text)
            if matches:
                if isinstance(matches[0], tuple):
                    return matches[0][-1].strip()
                return matches[0].strip()
        
        # Look for common city names
        cities = ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia', 
                 'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
                 'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata', 'Pune']
        
        for city in cities:
            if city.lower() in text.lower():
                return city
        
        return "Not specified"
    
    def extract_education(self, text):
        """Extract education level"""
        education_keywords = {
            'PhD': ['phd', 'ph.d', 'doctorate', 'doctoral'],
            'Masters': ['masters', 'master', 'm.s', 'ms', 'm.a', 'ma', 'mba', 'm.tech', 'mtech'],
            'Bachelors': ['bachelor', 'bachelors', 'b.s', 'bs', 'b.a', 'ba', 'b.tech', 'btech', 'be', 'b.e'],
            'Associates': ['associate', 'associates', 'diploma'],
            'High School': ['high school', 'secondary', '12th', 'intermediate']
        }
        
        text_lower = text.lower()
        for level, keywords in education_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    return level
        
        return "Not specified"
    
    def extract_skills(self, text):
        """Extract skills from resume"""
        # Common technical skills
        skill_patterns = [
            r'(?i)skills?[\s:]+([^.]+?)(?:\.|experience|education|work)',
            r'(?i)technical skills?[\s:]+([^.]+?)(?:\.|experience|education|work)',
            r'(?i)technologies?[\s:]+([^.]+?)(?:\.|experience|education|work)',
        ]
        
        skills = set()
        
        # Extract from skill sections
        for pattern in skill_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                skill_items = re.split(r'[,;|•\n]', match)
                for item in skill_items:
                    clean_skill = item.strip()
                    if len(clean_skill) > 2 and len(clean_skill) < 30:
                        skills.add(clean_skill)
        
        # Common technical skills to look for
        common_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
            'SQL', 'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'Oracle',
            'AWS', 'Azure', 'GCP', 'Docker', 'Kubernetes', 'Jenkins',
            'Git', 'Linux', 'Windows', 'MacOS', 'Agile', 'Scrum',
            'Machine Learning', 'AI', 'Data Science', 'Analytics', 'Tableau', 'Power BI'
        ]
        
        text_lower = text.lower()
        for skill in common_skills:
            if skill.lower() in text_lower:
                skills.add(skill)
        
        return ', '.join(sorted(list(skills)[:15]))  # Limit to top 15 skills
    
    def categorize_technical_skills(self, skills_str):
        """Categorize skills into technical domains"""
        if not skills_str:
            return "General"
        
        skills_lower = skills_str.lower()
        categories = []
        
        if any(lang in skills_lower for lang in ['python', 'java', 'javascript', 'c++', 'c#', 'php', 'ruby']):
            categories.append('Programming')
        
        if any(web in skills_lower for web in ['react', 'angular', 'vue', 'html', 'css', 'node.js']):
            categories.append('Web Development')
        
        if any(db in skills_lower for db in ['sql', 'mysql', 'postgresql', 'mongodb', 'oracle']):
            categories.append('Database')
        
        if any(cloud in skills_lower for cloud in ['aws', 'azure', 'gcp', 'docker', 'kubernetes']):
            categories.append('Cloud/DevOps')
        
        if any(ml in skills_lower for ml in ['machine learning', 'ai', 'data science', 'analytics']):
            categories.append('Data Science/AI')
        
        return ', '.join(categories) if categories else 'General'
    
    def extract_job_titles(self, text):
        """Extract job titles from experience"""
        title_patterns = [
            r'(?i)(software engineer|developer|programmer|analyst|manager|director|lead|senior|junior|intern)',
            r'(?i)(data scientist|data analyst|machine learning|ai engineer)',
            r'(?i)(product manager|project manager|scrum master|team lead)',
            r'(?i)(designer|architect|consultant|specialist|coordinator)'
        ]
        
        titles = set()
        for pattern in title_patterns:
            matches = re.findall(pattern, text)
            titles.update(matches)
        
        return ', '.join(sorted(list(titles)[:5]))  # Limit to 5 titles
    
    def extract_companies(self, text):
        """Extract company names"""
        # Look for common company patterns
        company_patterns = [
            r'(?i)(?:worked at|employed at|company|organization)[\s:]+([A-Z][a-zA-Z\s&.]+?)(?:\s|,|\.|$)',
            r'(?i)([A-Z][a-zA-Z\s&.]{2,30})\s+(?:Inc|LLC|Corp|Ltd|Company|Technologies|Solutions)',
        ]
        
        companies = set()
        for pattern in company_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                clean_company = match.strip()
                if len(clean_company) > 2 and len(clean_company) < 50:
                    companies.add(clean_company)
        
        return ', '.join(sorted(list(companies)[:5]))  # Limit to 5 companies
    
    def extract_certifications(self, text):
        """Extract certifications"""
        cert_keywords = [
            'AWS Certified', 'Microsoft Certified', 'Google Cloud', 'Cisco', 'Oracle Certified',
            'PMP', 'Scrum Master', 'Agile', 'ITIL', 'Six Sigma', 'CompTIA'
        ]
        
        certifications = []
        text_lower = text.lower()
        for cert in cert_keywords:
            if cert.lower() in text_lower:
                certifications.append(cert)
        
        return ', '.join(certifications[:5])  # Limit to 5 certifications
    
    def extract_languages(self, text):
        """Extract programming and spoken languages"""
        languages = set()
        
        # Programming languages
        prog_langs = ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'PHP', 'Ruby', 'Go', 'Rust', 'Swift', 'Kotlin']
        
        # Spoken languages
        spoken_langs = ['English', 'Spanish', 'French', 'German', 'Chinese', 'Japanese', 'Korean', 'Hindi', 'Arabic']
        
        text_lower = text.lower()
        for lang in prog_langs + spoken_langs:
            if lang.lower() in text_lower:
                languages.add(lang)
        
        return ', '.join(sorted(list(languages)[:8]))  # Limit to 8 languages
    
    def extract_linkedin(self, text):
        """Extract LinkedIn URL"""
        linkedin_pattern = r'(?i)(?:linkedin\.com/in/|linkedin\.com/profile/)([a-zA-Z0-9-]+)'
        matches = re.findall(linkedin_pattern, text)
        if matches:
            return f"https://linkedin.com/in/{matches[0]}"
        
        # Look for LinkedIn mentions
        if 'linkedin' in text.lower():
            return "Available on request"
        
        return "Not provided"
    
    def extract_github(self, text):
        """Extract GitHub URL"""
        github_pattern = r'(?i)(?:github\.com/)([a-zA-Z0-9-]+)'
        matches = re.findall(github_pattern, text)
        if matches:
            return f"https://github.com/{matches[0]}"
        
        if 'github' in text.lower():
            return "Available on request"
        
        return "Not provided"
    
    def estimate_experience(self, text):
        """Estimate years of experience"""
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
            grad_years = [year for year in years if 1990 <= year <= current_year]
            if grad_years:
                estimated_grad_year = max(grad_years)
                experience = max(0, current_year - estimated_grad_year - 1)
                return min(experience, 25)  # Cap at 25 years
        
        return 2  # Default to 2 years
    
    def determine_seniority(self, experience_years, job_titles, text):
        """Determine seniority level"""
        text_lower = text.lower()
        titles_lower = job_titles.lower()
        
        if experience_years >= 8 or any(word in titles_lower for word in ['senior', 'lead', 'principal', 'architect']):
            return 'Senior'
        elif experience_years >= 4 or any(word in titles_lower for word in ['mid', 'intermediate']):
            return 'Mid-level'
        elif any(word in titles_lower for word in ['junior', 'intern', 'entry']):
            return 'Junior'
        elif experience_years <= 2:
            return 'Entry-level'
        else:
            return 'Mid-level'
    
    def extract_industry_keywords(self, text):
        """Extract industry-specific keywords"""
        industries = {
            'Finance': ['finance', 'banking', 'investment', 'trading', 'fintech'],
            'Healthcare': ['healthcare', 'medical', 'hospital', 'pharma', 'biotech'],
            'Technology': ['software', 'tech', 'startup', 'saas', 'platform'],
            'E-commerce': ['ecommerce', 'retail', 'marketplace', 'shopping'],
            'Education': ['education', 'university', 'school', 'learning', 'training'],
            'Gaming': ['gaming', 'game', 'entertainment', 'mobile games'],
            'Consulting': ['consulting', 'advisory', 'strategy', 'management']
        }
        
        text_lower = text.lower()
        found_industries = []
        
        for industry, keywords in industries.items():
            if any(keyword in text_lower for keyword in keywords):
                found_industries.append(industry)
        
        return ', '.join(found_industries[:3])  # Limit to 3 industries
    
    def process_all_resumes(self):
        """Process all resume files and create enhanced CSV"""
        if not os.path.exists(self.resume_folder):
            print(f"Resume folder '{self.resume_folder}' not found!")
            return
        
        candidates = []
        resume_files = []
        
        # Get all resume files
        for ext in ['*.pdf', '*.docx', '*.doc']:
            resume_files.extend(Path(self.resume_folder).glob(ext))
        
        print(f"Found {len(resume_files)} resume files")
        print("Processing resumes with enhanced extraction...")
        
        for file_path in resume_files:
            filename = file_path.name
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
            
            # Extract enhanced candidate information
            candidate_info = self.extract_enhanced_info(text, filename)
            candidates.append(candidate_info)
            
            print(f"Processed: {candidate_info['name']} - {candidate_info['seniority_level']} - {candidate_info['technical_skills']}")
        
        if candidates:
            # Create enhanced CSV
            df = pd.DataFrame(candidates)
            df.to_csv(self.output_file, index=False)
            
            print(f"\n🎉 Successfully processed {len(candidates)} resumes!")
            print(f"📄 Enhanced CSV saved as: {self.output_file}")
            print(f"📊 Total candidates: {len(df)}")
            
            # Show preview
            print("\n📋 Preview of enhanced data:")
            print(df[['name', 'seniority_level', 'technical_skills', 'experience_years', 'education_level']].head())
            
            return df
        else:
            print("No resumes processed successfully.")
            return None

def main():
    processor = EnhancedResumeProcessor()
    
    print("🎯 BHIV Enhanced Resume Processor")
    print("=" * 50)
    print("Extracting comprehensive candidate data for better AI analysis...")
    
    df = processor.process_all_resumes()
    
    if df is not None:
        print(f"\n✅ Processing complete!")
        print(f"📊 Enhanced fields extracted:")
        print("   - Basic Info: name, email, phone, location")
        print("   - Professional: experience_years, seniority_level, job_titles")
        print("   - Skills: technical_skills, certifications, languages")
        print("   - Education: education_level")
        print("   - Social: linkedin_url, github_url")
        print("   - Industry: industry_keywords, companies")

if __name__ == "__main__":
    main()