from typing import Dict, List, Tuple, Optional, Any
import logging
import re

from .advanced_matcher import AdvancedSemanticMatcher
from .job_matcher import SemanticJobMatcher
from .model_manager import ModelManager
logger = logging.getLogger(__name__)

class SemanticProcessor:
    """Main semantic processing engine for candidate-job matching"""
    
    def __init__(self):
        self.version = "2.1.0"
        self.model_manager = ModelManager()
        self.job_matcher = SemanticJobMatcher()
        self.advanced_matcher = AdvancedSemanticMatcher()
        
        self.text_processors = {
            'skill_extractor': self._extract_skills,
            'experience_parser': self._parse_experience,
            'education_parser': self._parse_education,
            'location_normalizer': self._normalize_location
        }
        
        logger.info(f"SemanticProcessor v{self.version} initialized successfully")
    
    def process_candidate_profile(self, candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and enhance candidate profile data"""
        processed = candidate_data.copy()
        
        # Extract and normalize skills
        skills_text = candidate_data.get('technical_skills', '')
        processed['extracted_skills'] = self._extract_skills(skills_text)
        processed['skill_categories'] = self._categorize_skills(processed['extracted_skills'])
        
        # Parse experience
        experience_info = self._parse_experience(
            candidate_data.get('experience_years', 0),
            candidate_data.get('seniority_level', '')
        )
        processed['experience_info'] = experience_info
        
        # Normalize education
        processed['education_normalized'] = self._parse_education(
            candidate_data.get('education_level', '')
        )
        
        # Normalize location
        processed['location_normalized'] = self._normalize_location(
            candidate_data.get('location', '')
        )
        
        # Calculate profile completeness
        processed['profile_completeness'] = self._calculate_completeness(candidate_data)
        
        return processed
    
    def process_job_requirements(self, job_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process and enhance job requirements"""
        processed = job_data.copy()
        
        # Extract requirements from description and requirements fields
        full_text = f"{job_data.get('description', '')} {job_data.get('requirements', '')}"
        
        processed['required_skills'] = self._extract_skills(full_text)
        processed['skill_categories'] = self._categorize_skills(processed['required_skills'])
        
        # Determine job level and experience requirements
        processed['experience_requirements'] = self._extract_experience_requirements(full_text)
        
        # Extract location preferences
        processed['location_requirements'] = self._extract_location_requirements(
            job_data.get('location', ''), full_text
        )
        
        # Identify job template
        template = self.model_manager.get_job_template(job_data.get('title', ''))
        processed['job_template'] = template
        
        return processed
    
    def semantic_match(self, job_data: Dict[str, Any], candidate_data: Dict[str, Any]) -> Dict[str, Any]:
        """Perform comprehensive semantic matching"""
        
        # Process inputs
        processed_job = self.process_job_requirements(job_data)
        processed_candidate = self.process_candidate_profile(candidate_data)
        
        # Use advanced matcher for comprehensive scoring
        match_result = self.advanced_matcher.advanced_match(processed_job, processed_candidate)
        
        # Add semantic-specific enhancements
        semantic_enhancements = self._calculate_semantic_enhancements(
            processed_job, processed_candidate
        )
        
        match_result.update(semantic_enhancements)
        match_result['processor_version'] = self.version
        
        return match_result
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from text"""
        if not text:
            return []
        
        text_lower = text.lower()
        
        # Known skills from model manager
        known_skills = list(self.model_manager.skill_embeddings.keys())
        
        extracted = []
        for skill in known_skills:
            if skill in text_lower:
                extracted.append(skill)
        
        # Additional pattern-based extraction
        patterns = [
            r'\b(react\.js|reactjs)\b',
            r'\b(node\.js|nodejs)\b',
            r'\b(machine learning|ml)\b',
            r'\b(artificial intelligence|ai)\b',
            r'\b(deep learning|dl)\b'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            for match in matches:
                if isinstance(match, tuple):
                    match = match[0]
                if match not in extracted:
                    extracted.append(match)
        
        return extracted
    
    def _categorize_skills(self, skills: List[str]) -> Dict[str, List[str]]:
        """Categorize skills into domains"""
        categories = {
            'programming': [],
            'web_frontend': [],
            'web_backend': [],
            'database': [],
            'cloud_devops': [],
            'data_science': [],
            'mobile': [],
            'tools': []
        }
        
        category_mapping = {
            'programming': ['python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust'],
            'web_frontend': ['react', 'angular', 'vue', 'html', 'css', 'bootstrap', 'jquery'],
            'web_backend': ['node', 'express', 'django', 'flask', 'spring', 'laravel'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch'],
            'cloud_devops': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'jenkins', 'terraform'],
            'data_science': ['machine learning', 'ai', 'pandas', 'numpy', 'tensorflow', 'pytorch'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'swift', 'kotlin'],
            'tools': ['git', 'jira', 'linux', 'bash', 'vim']
        }
        
        for skill in skills:
            categorized = False
            for category, category_skills in category_mapping.items():
                if skill in category_skills:
                    categories[category].append(skill)
                    categorized = True
                    break
            
            if not categorized:
                categories['tools'].append(skill)
        
        # Remove empty categories
        return {k: v for k, v in categories.items() if v}
    
    def _parse_experience(self, years: int, level: str) -> Dict[str, Any]:
        """Parse and normalize experience information"""
        return {
            'years': years or 0,
            'level': level.lower() if level else 'unknown',
            'category': self._categorize_experience_level(years or 0),
            'weight': self._calculate_experience_weight(years or 0)
        }
    
    def _categorize_experience_level(self, years: int) -> str:
        """Categorize experience into levels"""
        if years == 0:
            return 'entry'
        elif years <= 2:
            return 'junior'
        elif years <= 5:
            return 'mid'
        elif years <= 8:
            return 'senior'
        else:
            return 'expert'
    
    def _calculate_experience_weight(self, years: int) -> float:
        """Calculate experience weight for scoring"""
        if years == 0:
            return 0.5
        elif years <= 2:
            return 0.7
        elif years <= 5:
            return 1.0
        elif years <= 8:
            return 1.2
        else:
            return 1.3
    
    def _parse_education(self, education: str) -> Dict[str, Any]:
        """Parse and normalize education information"""
        if not education:
            return {'level': 'unknown', 'weight': 0.5}
        
        education_lower = education.lower()
        
        if any(term in education_lower for term in ['phd', 'doctorate', 'ph.d']):
            return {'level': 'doctorate', 'weight': 1.3}
        elif any(term in education_lower for term in ['master', 'mba', 'm.tech', 'ms']):
            return {'level': 'masters', 'weight': 1.1}
        elif any(term in education_lower for term in ['bachelor', 'b.tech', 'be', 'bs']):
            return {'level': 'bachelors', 'weight': 1.0}
        elif any(term in education_lower for term in ['diploma', 'associate']):
            return {'level': 'diploma', 'weight': 0.8}
        else:
            return {'level': 'other', 'weight': 0.7}
    
    def _normalize_location(self, location: str) -> Dict[str, Any]:
        """Normalize location information"""
        if not location:
            return {'city': 'unknown', 'remote_friendly': False}
        
        location_lower = location.lower()
        
        # Check for remote work
        remote_friendly = any(term in location_lower for term in ['remote', 'anywhere', 'wfh'])
        
        # Major cities mapping
        city_mapping = {
            'mumbai': ['mumbai', 'bombay'],
            'bangalore': ['bangalore', 'bengaluru'],
            'delhi': ['delhi', 'new delhi'],
            'pune': ['pune'],
            'hyderabad': ['hyderabad'],
            'chennai': ['chennai', 'madras'],
            'kolkata': ['kolkata', 'calcutta']
        }
        
        normalized_city = 'other'
        for city, variants in city_mapping.items():
            if any(variant in location_lower for variant in variants):
                normalized_city = city
                break
        
        return {
            'city': normalized_city,
            'original': location,
            'remote_friendly': remote_friendly
        }
    
    def _calculate_completeness(self, candidate_data: Dict[str, Any]) -> float:
        """Calculate profile completeness score"""
        required_fields = ['name', 'email', 'technical_skills']
        optional_fields = ['phone', 'location', 'experience_years', 'education_level']
        
        required_score = sum(1 for field in required_fields if candidate_data.get(field))
        optional_score = sum(1 for field in optional_fields if candidate_data.get(field))
        
        total_score = (required_score / len(required_fields)) * 0.7 + (optional_score / len(optional_fields)) * 0.3
        return round(total_score, 2)
    
    def _extract_experience_requirements(self, job_text: str) -> Dict[str, Any]:
        """Extract experience requirements from job description"""
        text_lower = job_text.lower()
        
        # Extract years of experience
        year_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*yrs?\s*(?:of\s*)?experience',
            r'minimum\s*(\d+)\s*years?',
            r'at least\s*(\d+)\s*years?'
        ]
        
        min_years = 0
        for pattern in year_patterns:
            matches = re.findall(pattern, text_lower)
            if matches:
                min_years = max(min_years, int(matches[0]))
        
        # Extract level requirements
        level_keywords = {
            'entry': ['entry', 'junior', 'fresher', 'graduate'],
            'mid': ['mid', 'intermediate', 'experienced'],
            'senior': ['senior', 'lead', 'principal', 'expert']
        }
        
        required_level = 'any'
        for level, keywords in level_keywords.items():
            if any(keyword in text_lower for keyword in keywords):
                required_level = level
                break
        
        return {
            'min_years': min_years,
            'required_level': required_level,
            'flexible': 'flexible' in text_lower or 'negotiable' in text_lower
        }
    
    def _extract_location_requirements(self, job_location: str, job_text: str) -> Dict[str, Any]:
        """Extract location requirements"""
        location_info = self._normalize_location(job_location)
        
        text_lower = job_text.lower()
        
        # Check for remote work options
        remote_options = {
            'fully_remote': any(term in text_lower for term in ['fully remote', '100% remote', 'remote only']),
            'hybrid': any(term in text_lower for term in ['hybrid', 'flexible', 'part remote']),
            'on_site': any(term in text_lower for term in ['on-site', 'onsite', 'office based'])
        }
        
        location_info.update(remote_options)
        return location_info
    
    def _calculate_semantic_enhancements(self, processed_job: Dict, processed_candidate: Dict) -> Dict[str, Any]:
        """Calculate additional semantic enhancements"""
        
        # Skill diversity score
        job_categories = set(processed_job.get('skill_categories', {}).keys())
        candidate_categories = set(processed_candidate.get('skill_categories', {}).keys())
        
        category_overlap = len(job_categories & candidate_categories)
        category_diversity = category_overlap / max(len(job_categories), 1)
        
        # Profile quality score
        profile_quality = processed_candidate.get('profile_completeness', 0.5)
        
        # Experience alignment
        job_exp_req = processed_job.get('experience_requirements', {})
        candidate_exp = processed_candidate.get('experience_info', {})
        
        exp_alignment = self._calculate_experience_alignment(job_exp_req, candidate_exp)
        
        return {
            'semantic_category_diversity': round(category_diversity, 3),
            'semantic_profile_quality': round(profile_quality, 3),
            'semantic_experience_alignment': round(exp_alignment, 3),
            'semantic_overall_enhancement': round((category_diversity + profile_quality + exp_alignment) / 3, 3)
        }
    
    def _calculate_experience_alignment(self, job_req: Dict, candidate_exp: Dict) -> float:
        """Calculate experience alignment score"""
        if not job_req or not candidate_exp:
            return 0.5
        
        min_years = job_req.get('min_years', 0)
        candidate_years = candidate_exp.get('years', 0)
        
        if min_years == 0:
            return 0.8  # No specific requirement
        
        if candidate_years >= min_years:
            # Bonus for exceeding requirements, but diminishing returns
            excess = candidate_years - min_years
            return min(1.0, 0.8 + (excess * 0.05))
        else:
            # Penalty for not meeting requirements
            gap = min_years - candidate_years
            return max(0.2, 0.8 - (gap * 0.15))