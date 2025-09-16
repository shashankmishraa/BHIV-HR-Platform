import numpy as np
import re
from typing import Dict, List, Tuple, Optional
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

class SemanticJobMatcher:
    """Advanced semantic job-candidate matching with NLP-based similarity"""
    
    def __init__(self):
        self.version = "2.1.0"
        self.skill_embeddings = self._initialize_skill_embeddings()
        self.experience_weights = self._initialize_experience_weights()
        self.domain_keywords = self._initialize_domain_keywords()
        logger.info(f"SemanticJobMatcher v{self.version} initialized successfully")
    
    def _initialize_skill_embeddings(self) -> Dict[str, np.ndarray]:
        """Initialize skill embeddings for semantic similarity"""
        # Simplified embeddings - in production, use pre-trained models
        skills = [
            'python', 'java', 'javascript', 'react', 'node', 'django', 'flask',
            'sql', 'mysql', 'postgresql', 'mongodb', 'aws', 'azure', 'docker',
            'kubernetes', 'machine learning', 'ai', 'data science', 'tensorflow',
            'pytorch', 'pandas', 'numpy', 'git', 'jenkins', 'linux', 'html', 'css'
        ]
        
        embeddings = {}
        for i, skill in enumerate(skills):
            # Generate pseudo-embeddings based on skill characteristics
            embedding = np.random.seed(hash(skill) % 1000)
            embeddings[skill] = np.random.rand(50)  # 50-dimensional vectors
        
        return embeddings
    
    def _initialize_experience_weights(self) -> Dict[str, float]:
        """Initialize experience level weights"""
        return {
            'entry': 1.0,
            'junior': 1.2,
            'mid': 1.5,
            'senior': 2.0,
            'lead': 2.5,
            'principal': 3.0
        }
    
    def _initialize_domain_keywords(self) -> Dict[str, List[str]]:
        """Initialize domain-specific keyword mappings"""
        return {
            'web_development': ['react', 'angular', 'vue', 'html', 'css', 'javascript', 'node', 'express'],
            'backend': ['python', 'java', 'django', 'flask', 'spring', 'api', 'microservices'],
            'data_science': ['python', 'r', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'machine learning'],
            'devops': ['docker', 'kubernetes', 'jenkins', 'aws', 'azure', 'terraform', 'ansible'],
            'mobile': ['android', 'ios', 'react native', 'flutter', 'swift', 'kotlin'],
            'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch']
        }
    
    def extract_skills(self, text: str) -> List[str]:
        """Extract skills from job requirements or candidate profile"""
        if not text:
            return []
        
        text_lower = text.lower()
        found_skills = []
        
        # Check all known skills
        for skill in self.skill_embeddings.keys():
            if skill in text_lower:
                found_skills.append(skill)
        
        # Check domain keywords
        for domain, keywords in self.domain_keywords.items():
            for keyword in keywords:
                if keyword in text_lower and keyword not in found_skills:
                    found_skills.append(keyword)
        
        return found_skills
    
    def calculate_skill_similarity(self, job_skills: List[str], candidate_skills: List[str]) -> float:
        """Calculate semantic similarity between skill sets"""
        if not job_skills or not candidate_skills:
            return 0.0
        
        # Direct matches
        direct_matches = set(job_skills) & set(candidate_skills)
        direct_score = len(direct_matches) / len(job_skills)
        
        # Semantic similarity using embeddings
        semantic_score = 0.0
        for job_skill in job_skills:
            if job_skill in self.skill_embeddings:
                best_match_score = 0.0
                for cand_skill in candidate_skills:
                    if cand_skill in self.skill_embeddings:
                        # Cosine similarity
                        job_vec = self.skill_embeddings[job_skill]
                        cand_vec = self.skill_embeddings[cand_skill]
                        similarity = np.dot(job_vec, cand_vec) / (np.linalg.norm(job_vec) * np.linalg.norm(cand_vec))
                        best_match_score = max(best_match_score, similarity)
                semantic_score += best_match_score
        
        semantic_score /= len(job_skills) if job_skills else 1
        
        # Combine direct and semantic scores
        return 0.7 * direct_score + 0.3 * semantic_score
    
    def match(self, job_requirements: str, candidate_skills: str, 
             job_level: str = None, candidate_experience: int = 0) -> Dict[str, float]:
        """Enhanced semantic matching with multiple factors"""
        
        # Extract skills
        job_skills = self.extract_skills(job_requirements)
        cand_skills = self.extract_skills(candidate_skills)
        
        # Calculate skill similarity
        skill_score = self.calculate_skill_similarity(job_skills, cand_skills)
        
        # Experience matching
        exp_score = self._calculate_experience_match(job_level, candidate_experience)
        
        # Domain alignment
        domain_score = self._calculate_domain_alignment(job_requirements, candidate_skills)
        
        # Weighted final score
        final_score = 0.5 * skill_score + 0.3 * exp_score + 0.2 * domain_score
        
        return {
            'overall_score': min(1.0, final_score),
            'skill_score': skill_score,
            'experience_score': exp_score,
            'domain_score': domain_score,
            'matched_skills': list(set(job_skills) & set(cand_skills)),
            'job_skills': job_skills,
            'candidate_skills': cand_skills
        }
    
    def _calculate_experience_match(self, job_level: str, candidate_experience: int) -> float:
        """Calculate experience level matching"""
        if not job_level:
            return 0.5
        
        job_level_lower = job_level.lower()
        
        # Map experience years to levels
        if candidate_experience >= 8:
            cand_level = 'senior'
        elif candidate_experience >= 5:
            cand_level = 'mid'
        elif candidate_experience >= 2:
            cand_level = 'junior'
        else:
            cand_level = 'entry'
        
        # Experience level matching
        level_mapping = {
            'entry': 0, 'junior': 1, 'mid': 2, 'senior': 3, 'lead': 4, 'principal': 5
        }
        
        job_level_num = 2  # Default to mid-level
        for level, num in level_mapping.items():
            if level in job_level_lower:
                job_level_num = num
                break
        
        cand_level_num = level_mapping.get(cand_level, 1)
        
        # Calculate match score
        diff = abs(job_level_num - cand_level_num)
        return max(0.0, 1.0 - (diff * 0.2))
    
    def _calculate_domain_alignment(self, job_requirements: str, candidate_skills: str) -> float:
        """Calculate domain-specific alignment"""
        if not job_requirements or not candidate_skills:
            return 0.0
        
        job_text = job_requirements.lower()
        cand_text = candidate_skills.lower()
        
        domain_scores = []
        
        for domain, keywords in self.domain_keywords.items():
            job_domain_match = sum(1 for kw in keywords if kw in job_text)
            cand_domain_match = sum(1 for kw in keywords if kw in cand_text)
            
            if job_domain_match > 0:
                domain_score = min(1.0, cand_domain_match / job_domain_match)
                domain_scores.append(domain_score)
        
        return np.mean(domain_scores) if domain_scores else 0.0