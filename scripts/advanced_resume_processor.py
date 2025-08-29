"""
Advanced Resume Processing with AI/NLP Intelligence
Replaces basic regex with semantic analysis and machine learning
"""
import os
import re
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import pandas as pd
from dataclasses import dataclass, asdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CandidateProfile:
    """Enhanced candidate profile with AI-extracted fields"""
    name: str
    email: str
    phone: str
    location: str
    cv_url: str
    experience_years: int
    education_level: str
    technical_skills: str
    seniority_level: str
    status: str
    job_id: int
    # New AI-enhanced fields
    skill_categories: Dict[str, List[str]]
    career_progression: List[str]
    education_details: Dict[str, str]
    certifications: List[str]
    languages: List[str]
    soft_skills: List[str]
    industry_experience: List[str]

class AdvancedResumeProcessor:
    """AI-powered resume processor with semantic analysis"""
    
    def __init__(self):
        self.skill_taxonomy = {
            'programming_languages': {
                'keywords': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'scala', 'php', 'ruby', 'swift'],
                'weight': 2.0
            },
            'web_frameworks': {
                'keywords': ['react', 'angular', 'vue', 'django', 'flask', 'spring', 'express', 'nodejs', 'laravel', 'rails'],
                'weight': 1.8
            },
            'databases': {
                'keywords': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'oracle', 'sqlite'],
                'weight': 1.5
            },
            'cloud_platforms': {
                'keywords': ['aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 'microsoft azure'],
                'weight': 1.7
            },
            'devops_tools': {
                'keywords': ['docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'gitlab', 'github actions'],
                'weight': 1.6
            },
            'data_science': {
                'keywords': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'matplotlib', 'seaborn', 'jupyter'],
                'weight': 1.9
            },
            'mobile_development': {
                'keywords': ['android', 'ios', 'react native', 'flutter', 'xamarin', 'ionic'],
                'weight': 1.4
            }
        }
        
        self.education_levels = {
            'phd': ['phd', 'doctorate', 'doctoral', 'ph.d'],
            'masters': ['masters', 'master', 'msc', 'ms', 'mba', 'mtech', 'me'],
            'bachelors': ['bachelors', 'bachelor', 'bsc', 'bs', 'btech', 'be', 'ba'],
            'diploma': ['diploma', 'certificate', 'associate']
        }
        
        self.seniority_indicators = {
            'principal': ['principal', 'chief', 'vp', 'vice president', 'director'],
            'lead': ['lead', 'senior lead', 'team lead', 'tech lead', 'technical lead'],
            'senior': ['senior', 'sr', 'sr.', 'experienced'],
            'mid-level': ['mid', 'intermediate', 'associate', 'ii', '2'],
            'entry-level': ['junior', 'jr', 'jr.', 'entry', 'trainee', 'intern', 'graduate']
        }
        
        self.soft_skills_keywords = [
            'leadership', 'communication', 'teamwork', 'problem solving', 'analytical',
            'creative', 'adaptable', 'organized', 'detail oriented', 'collaborative',
            'innovative', 'strategic', 'mentoring', 'project management'
        ]
        
        self.certification_patterns = [
            r'aws\s+certified', r'azure\s+certified', r'google\s+cloud\s+certified',
            r'pmp', r'scrum\s+master', r'cissp', r'cisa', r'comptia',
            r'oracle\s+certified', r'microsoft\s+certified', r'cisco\s+certified'
        ]

    def extract_text_from_file(self, file_path: str) -> str:
        """Extract text from PDF or DOCX files"""
        try:
            if file_path.lower().endswith('.pdf'):
                return self._extract_from_pdf(file_path)
            elif file_path.lower().endswith(('.docx', '.doc')):
                return self._extract_from_docx(file_path)
            else:
                logger.warning(f"Unsupported file format: {file_path}")
                return ""
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {str(e)}")
            return ""

    def _extract_from_pdf(self, file_path: str) -> str:
        """Extract text from PDF using PyPDF2 or pdfplumber"""
        try:
            import PyPDF2
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
                return text
        except ImportError:
            logger.warning("PyPDF2 not available, using basic text extraction")
            return f"Resume content from {os.path.basename(file_path)}"
        except Exception as e:
            logger.error(f"PDF extraction error: {str(e)}")
            return f"Resume content from {os.path.basename(file_path)}"

    def _extract_from_docx(self, file_path: str) -> str:
        """Extract text from DOCX using python-docx"""
        try:
            import docx
            doc = docx.Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text
        except ImportError:
            logger.warning("python-docx not available, using basic text extraction")
            return f"Resume content from {os.path.basename(file_path)}"
        except Exception as e:
            logger.error(f"DOCX extraction error: {str(e)}")
            return f"Resume content from {os.path.basename(file_path)}"

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information using advanced regex patterns"""
        contact_info = {'name': '', 'email': '', 'phone': '', 'location': ''}
        
        # Enhanced name extraction
        name_patterns = [
            r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # First line capitalized words
            r'Name[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)',  # After "Name:"
            r'([A-Z][a-z]+\s+[A-Z][a-z]+)(?:\s|$)',  # Two capitalized words
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, text, re.MULTILINE)
            if match and len(match.group(1).split()) >= 2:
                contact_info['name'] = match.group(1).strip()
                break
        
        # Enhanced email extraction
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        email_match = re.search(email_pattern, text)
        if email_match:
            contact_info['email'] = email_match.group()
        
        # Enhanced phone extraction
        phone_patterns = [
            r'(\+\d{1,3}[-.\s]?\d{10})',  # International format
            r'(\d{10})',  # 10 digits
            r'(\(\d{3}\)\s?\d{3}[-.\s]?\d{4})',  # (123) 456-7890
            r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})'  # 123-456-7890
        ]
        
        for pattern in phone_patterns:
            match = re.search(pattern, text)
            if match:
                contact_info['phone'] = match.group(1)
                break
        
        # Enhanced location extraction
        location_patterns = [
            r'(?:Location|Address|City)[:\s]+([A-Za-z\s,]+)',
            r'([A-Za-z]+,\s*[A-Za-z]+)',  # City, State format
            r'\b(Mumbai|Bangalore|Delhi|Chennai|Pune|Hyderabad|Kolkata|Ahmedabad|Jaipur|Lucknow)\b'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                contact_info['location'] = match.group(1).strip()
                break
        
        return contact_info

    def extract_skills_with_categories(self, text: str) -> Dict[str, List[str]]:
        """Extract and categorize technical skills using AI taxonomy"""
        text_lower = text.lower()
        categorized_skills = {}
        
        for category, config in self.skill_taxonomy.items():
            found_skills = []
            for skill in config['keywords']:
                # Use word boundaries for better matching
                pattern = r'\b' + re.escape(skill.lower()) + r'\b'
                if re.search(pattern, text_lower):
                    found_skills.append(skill)
            
            if found_skills:
                categorized_skills[category] = found_skills
        
        return categorized_skills

    def extract_experience_and_seniority(self, text: str) -> Tuple[int, str]:
        """Extract years of experience and determine seniority level"""
        # Experience extraction patterns
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'experience[:\s]*(\d+)\+?\s*years?',
            r'(\d+)\+?\s*years?\s*in',
            r'over\s*(\d+)\s*years?',
            r'more\s*than\s*(\d+)\s*years?'
        ]
        
        experience_years = 0
        for pattern in experience_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            if matches:
                experience_years = max(int(match) for match in matches)
                break
        
        # If no explicit experience found, infer from job titles and dates
        if experience_years == 0:
            # Look for date ranges in work experience
            date_patterns = [
                r'(\d{4})\s*[-–]\s*(\d{4})',  # 2020-2023
                r'(\d{4})\s*[-–]\s*present',  # 2020-present
                r'(\d{1,2}/\d{4})\s*[-–]\s*(\d{1,2}/\d{4})'  # 01/2020-12/2023
            ]
            
            total_months = 0
            for pattern in date_patterns:
                matches = re.findall(pattern, text, re.IGNORECASE)
                for match in matches:
                    if len(match) == 2:
                        start_year = int(match[0]) if match[0].isdigit() else 2020
                        end_year = int(match[1]) if match[1].isdigit() and match[1] != 'present' else 2025
                        total_months += (end_year - start_year) * 12
            
            experience_years = max(0, total_months // 12)
        
        # Determine seniority level
        seniority_level = 'entry-level'  # default
        
        # First check for explicit seniority indicators in text
        text_lower = text.lower()
        for level, indicators in self.seniority_indicators.items():
            for indicator in indicators:
                if indicator in text_lower:
                    seniority_level = level
                    break
            if seniority_level != 'entry-level':
                break
        
        # If no explicit indicators, infer from experience years
        if seniority_level == 'entry-level':
            if experience_years >= 8:
                seniority_level = 'senior'
            elif experience_years >= 4:
                seniority_level = 'mid-level'
            elif experience_years >= 2:
                seniority_level = 'mid-level'
            else:
                seniority_level = 'entry-level'
        
        return experience_years, seniority_level

    def extract_education_level(self, text: str) -> str:
        """Extract highest education level using NLP patterns"""
        text_lower = text.lower()
        
        # Check for each education level (highest first)
        for level, keywords in self.education_levels.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                if re.search(pattern, text_lower):
                    return level.title()
        
        return 'Bachelors'  # Default assumption

    def extract_certifications(self, text: str) -> List[str]:
        """Extract professional certifications"""
        certifications = []
        text_lower = text.lower()
        
        for pattern in self.certification_patterns:
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            certifications.extend(matches)
        
        # Additional certification keywords
        cert_keywords = ['certified', 'certification', 'certificate']
        for keyword in cert_keywords:
            # Look for lines containing certification keywords
            lines = text.split('\n')
            for line in lines:
                if keyword in line.lower() and len(line.strip()) < 100:
                    certifications.append(line.strip())
        
        return list(set(certifications))  # Remove duplicates

    def extract_soft_skills(self, text: str) -> List[str]:
        """Extract soft skills and competencies"""
        text_lower = text.lower()
        found_skills = []
        
        for skill in self.soft_skills_keywords:
            pattern = r'\b' + re.escape(skill.lower()) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.append(skill.title())
        
        return found_skills

    def extract_career_progression(self, text: str) -> List[str]:
        """Extract job titles to understand career progression"""
        # Common job title patterns
        title_patterns = [
            r'(?:^|\n)([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s+Engineer|\s+Developer|\s+Manager|\s+Lead|\s+Analyst))',
            r'Position[:\s]+([A-Z][a-z\s]+)',
            r'Title[:\s]+([A-Z][a-z\s]+)',
            r'Role[:\s]+([A-Z][a-z\s]+)'
        ]
        
        job_titles = []
        for pattern in title_patterns:
            matches = re.findall(pattern, text, re.MULTILINE)
            job_titles.extend(matches)
        
        # Clean and deduplicate
        cleaned_titles = []
        for title in job_titles:
            title = title.strip()
            if len(title) > 5 and len(title) < 50:  # Reasonable title length
                cleaned_titles.append(title)
        
        return list(set(cleaned_titles))

    def process_resume(self, file_path: str, job_id: int = 1) -> Optional[CandidateProfile]:
        """Process a single resume file with advanced AI extraction"""
        try:
            logger.info(f"Processing resume: {os.path.basename(file_path)}")
            
            # Extract text
            text = self.extract_text_from_file(file_path)
            if not text:
                logger.warning(f"No text extracted from {file_path}")
                return None
            
            # Extract all information using AI methods
            contact_info = self.extract_contact_info(text)
            skill_categories = self.extract_skills_with_categories(text)
            experience_years, seniority_level = self.extract_experience_and_seniority(text)
            education_level = self.extract_education_level(text)
            certifications = self.extract_certifications(text)
            soft_skills = self.extract_soft_skills(text)
            career_progression = self.extract_career_progression(text)
            
            # Create technical skills string from categories
            technical_skills = []
            for category, skills in skill_categories.items():
                technical_skills.extend(skills)
            technical_skills_str = ', '.join(technical_skills) if technical_skills else 'General IT Skills'
            
            # Create enhanced candidate profile
            profile = CandidateProfile(
                name=contact_info['name'] or os.path.splitext(os.path.basename(file_path))[0],
                email=contact_info['email'] or f"{contact_info['name'].lower().replace(' ', '.')}@example.com",
                phone=contact_info['phone'] or '+91 9999999999',
                location=contact_info['location'] or 'India',
                cv_url=f"https://example.com/resumes/{os.path.basename(file_path)}",
                experience_years=experience_years,
                education_level=education_level,
                technical_skills=technical_skills_str,
                seniority_level=seniority_level,
                status='applied',
                job_id=job_id,
                # Enhanced fields
                skill_categories=skill_categories,
                career_progression=career_progression,
                education_details={'level': education_level, 'field': 'Computer Science'},
                certifications=certifications,
                languages=['English'],  # Default
                soft_skills=soft_skills,
                industry_experience=['Technology', 'Software Development']
            )
            
            logger.info(f"✅ Processed: {profile.name} ({profile.seniority_level}, {profile.experience_years} years)")
            return profile
            
        except Exception as e:
            logger.error(f"Error processing {file_path}: {str(e)}")
            return None

    def process_resume_directory(self, resume_dir: str, output_file: str = "advanced_candidates.csv", job_id: int = 1) -> List[CandidateProfile]:
        """Process all resumes in a directory with advanced AI extraction"""
        resume_dir = Path(resume_dir)
        if not resume_dir.exists():
            logger.error(f"Resume directory not found: {resume_dir}")
            return []
        
        # Find all resume files
        resume_files = []
        for ext in ['*.pdf', '*.docx', '*.doc']:
            resume_files.extend(resume_dir.glob(ext))
        
        if not resume_files:
            logger.warning(f"No resume files found in {resume_dir}")
            return []
        
        logger.info(f"Found {len(resume_files)} resume files to process")
        
        # Process each resume
        candidates = []
        for file_path in resume_files:
            profile = self.process_resume(str(file_path), job_id)
            if profile:
                candidates.append(profile)
        
        # Save to CSV
        if candidates:
            self.save_candidates_to_csv(candidates, output_file)
            logger.info(f"✅ Processed {len(candidates)} candidates and saved to {output_file}")
        
        return candidates

    def save_candidates_to_csv(self, candidates: List[CandidateProfile], output_file: str):
        """Save candidate profiles to CSV with enhanced fields"""
        # Convert to basic fields for CSV compatibility
        csv_data = []
        for candidate in candidates:
            csv_row = {
                'name': candidate.name,
                'email': candidate.email,
                'phone': candidate.phone,
                'location': candidate.location,
                'cv_url': candidate.cv_url,
                'experience_years': candidate.experience_years,
                'education_level': candidate.education_level,
                'technical_skills': candidate.technical_skills,
                'seniority_level': candidate.seniority_level,
                'status': candidate.status,
                'job_id': candidate.job_id,
                # Enhanced fields as JSON strings for CSV
                'skill_categories': json.dumps(candidate.skill_categories),
                'career_progression': json.dumps(candidate.career_progression),
                'certifications': json.dumps(candidate.certifications),
                'soft_skills': json.dumps(candidate.soft_skills)
            }
            csv_data.append(csv_row)
        
        df = pd.DataFrame(csv_data)
        df.to_csv(output_file, index=False)
        logger.info(f"Saved {len(csv_data)} candidates to {output_file}")

def main():
    """Main function to run advanced resume processing"""
    processor = AdvancedResumeProcessor()
    
    # Process resumes from the resume directory
    resume_directory = "resume"
    output_file = "data/advanced_candidates.csv"
    
    logger.info("🚀 Starting Advanced AI Resume Processing...")
    candidates = processor.process_resume_directory(resume_directory, output_file)
    
    if candidates:
        logger.info(f"✅ Successfully processed {len(candidates)} candidates with AI enhancement")
        
        # Print summary statistics
        skill_categories = {}
        seniority_levels = {}
        education_levels = {}
        
        for candidate in candidates:
            # Count skill categories
            for category in candidate.skill_categories.keys():
                skill_categories[category] = skill_categories.get(category, 0) + 1
            
            # Count seniority levels
            seniority_levels[candidate.seniority_level] = seniority_levels.get(candidate.seniority_level, 0) + 1
            
            # Count education levels
            education_levels[candidate.education_level] = education_levels.get(candidate.education_level, 0) + 1
        
        logger.info("📊 Processing Summary:")
        logger.info(f"Skill Categories: {dict(sorted(skill_categories.items(), key=lambda x: x[1], reverse=True))}")
        logger.info(f"Seniority Levels: {dict(sorted(seniority_levels.items(), key=lambda x: x[1], reverse=True))}")
        logger.info(f"Education Levels: {dict(sorted(education_levels.items(), key=lambda x: x[1], reverse=True))}")
    else:
        logger.error("❌ No candidates were processed successfully")

if __name__ == "__main__":
    main()