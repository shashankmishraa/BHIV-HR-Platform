import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import List, Dict, Any
import asyncio
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)

class AdvancedSemanticMatcher:
    """Advanced AI matcher with multi-factor scoring and batch processing"""
    def __init__(self):
        self.enabled = True
        self.model = None
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize sentence transformer model"""
        try:
            print("INFO: Loading advanced semantic model (Phase 2)...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("SUCCESS: Advanced semantic matcher loaded (Phase 2)")
        except Exception as e:
            logger.error(f"Failed to load advanced model: {e}")
            self.enabled = False
            print("WARNING: Advanced matcher disabled")
    
    def extract_skills_semantically(self, text: str) -> List[str]:
        """Extract skills using semantic similarity to known skill embeddings"""
        if not self.enabled or not self.model:
            return []
        
        # Common tech skills for semantic matching
        skill_categories = [
            "python programming", "java development", "javascript coding",
            "react frontend", "node backend", "database management",
            "machine learning", "data science", "cloud computing",
            "docker containers", "kubernetes orchestration", "aws services"
        ]
        
        try:
            text_embedding = self.model.encode([text.lower()])
            skill_embeddings = self.model.encode(skill_categories)
            
            similarities = cosine_similarity(text_embedding, skill_embeddings)[0]
            
            # Extract skills with similarity > 0.3
            extracted_skills = []
            for i, similarity in enumerate(similarities):
                if similarity > 0.3:
                    extracted_skills.append(skill_categories[i])
            
            return extracted_skills
        except Exception as e:
            logger.error(f"Error in semantic skill extraction: {e}")
            return []
    
    def calculate_multi_factor_score(self, job_data: dict, candidate_data: dict) -> dict:
        """Calculate comprehensive matching score with multiple factors"""
        if not self.enabled:
            return {"total_score": 0.0, "breakdown": {}}
        
        try:
            # Semantic similarity (40% weight)
            job_text = f"{job_data.get('title', '')} {job_data.get('description', '')} {job_data.get('requirements', '')}"
            candidate_text = f"{candidate_data.get('technical_skills', '')} {candidate_data.get('seniority_level', '')} {candidate_data.get('education_level', '')}"
            
            job_embedding = self.model.encode([job_text])
            candidate_embedding = self.model.encode([candidate_text])
            
            semantic_score = cosine_similarity(job_embedding, candidate_embedding)[0][0]
            
            # Experience matching (30% weight)
            experience_score = self._calculate_experience_score(
                job_data.get('experience_level', ''),
                candidate_data.get('experience_years', 0),
                candidate_data.get('seniority_level', '')
            )
            
            # Skills matching (20% weight)
            skills_score = self._calculate_skills_score(
                job_data.get('requirements', ''),
                candidate_data.get('technical_skills', '')
            )
            
            # Location matching (10% weight)
            location_score = self._calculate_location_score(
                job_data.get('location', ''),
                candidate_data.get('location', '')
            )
            
            # Weighted total score
            total_score = (
                semantic_score * 0.4 +
                experience_score * 0.3 +
                skills_score * 0.2 +
                location_score * 0.1
            )
            
            return {
                "total_score": float(total_score),
                "breakdown": {
                    "semantic_similarity": float(semantic_score),
                    "experience_match": float(experience_score),
                    "skills_match": float(skills_score),
                    "location_match": float(location_score)
                }
            }
            
        except Exception as e:
            logger.error(f"Error in multi-factor scoring: {e}")
            return {"total_score": 0.0, "breakdown": {}}
    
    def _calculate_experience_score(self, job_level: str, candidate_years: int, candidate_level: str) -> float:
        """Calculate experience matching score"""
        level_mapping = {
            'entry': (0, 2), 'junior': (1, 3), 'mid': (2, 5),
            'senior': (4, 8), 'lead': (6, 15), 'principal': (8, 20)
        }
        
        job_level_lower = job_level.lower()
        required_range = None
        
        for level, years_range in level_mapping.items():
            if level in job_level_lower:
                required_range = years_range
                break
        
        if not required_range:
            return 0.5
        
        min_years, max_years = required_range
        
        if min_years <= candidate_years <= max_years:
            return 1.0
        elif candidate_years < min_years:
            gap = min_years - candidate_years
            return max(0.3, 1.0 - (gap * 0.2))
        else:
            excess = candidate_years - max_years
            return max(0.7, 1.0 - (excess * 0.1))
    
    def _calculate_skills_score(self, job_requirements: str, candidate_skills: str) -> float:
        """Calculate skills matching score using semantic similarity"""
        if not job_requirements or not candidate_skills:
            return 0.0
        
        try:
            req_embedding = self.model.encode([job_requirements.lower()])
            skills_embedding = self.model.encode([candidate_skills.lower()])
            
            similarity = cosine_similarity(req_embedding, skills_embedding)[0][0]
            return float(similarity)
        except:
            return 0.0
    
    def _calculate_location_score(self, job_location: str, candidate_location: str) -> float:
        """Calculate location matching score"""
        if not job_location or not candidate_location:
            return 0.5
        
        job_loc_lower = job_location.lower()
        candidate_loc_lower = candidate_location.lower()
        
        if 'remote' in job_loc_lower:
            return 1.0
        
        if job_loc_lower == candidate_loc_lower:
            return 1.0
        
        # Use semantic similarity for location matching
        try:
            job_embedding = self.model.encode([job_loc_lower])
            candidate_embedding = self.model.encode([candidate_loc_lower])
            
            similarity = cosine_similarity(job_embedding, candidate_embedding)[0][0]
            return float(similarity)
        except:
            return 0.3
    
    def advanced_match(self, job_data: dict, candidates: list) -> list:
        """Advanced semantic matching with multi-factor scoring"""
        if not self.enabled:
            return []
        
        try:
            scored_candidates = []
            
            for candidate in candidates:
                score_data = self.calculate_multi_factor_score(job_data, candidate)
                
                scored_candidates.append({
                    'candidate_id': candidate.get('id'),
                    'total_score': score_data['total_score'],
                    'score_breakdown': score_data['breakdown'],
                    'candidate_data': candidate
                })
            
            # Sort by total score
            scored_candidates.sort(key=lambda x: x['total_score'], reverse=True)
            return scored_candidates
            
        except Exception as e:
            logger.error(f"Error in advanced matching: {e}")
            return []

class BatchMatcher:
    """Batch processing for multiple jobs and candidates"""
    def __init__(self):
        self.enabled = True
        self.advanced_matcher = AdvancedSemanticMatcher()
        print("INFO: Batch matcher initialized (Phase 2)")
    
    def batch_process(self, jobs: list, candidates: list) -> dict:
        """Process multiple jobs against candidates in batch"""
        if not self.enabled or not self.advanced_matcher.enabled:
            return {}
        
        try:
            results = {}
            
            for job in jobs:
                job_id = job.get('id')
                matches = self.advanced_matcher.advanced_match(job, candidates)
                
                results[job_id] = {
                    'job_title': job.get('title', ''),
                    'total_candidates': len(matches),
                    'top_matches': matches[:10],  # Top 10 matches
                    'processing_status': 'success'
                }
            
            return results
            
        except Exception as e:
            logger.error(f"Error in batch processing: {e}")
            return {}
    
    async def async_batch_process(self, jobs: list, candidates: list) -> dict:
        """Asynchronous batch processing for better performance"""
        if not self.enabled:
            return {}
        
        try:
            loop = asyncio.get_event_loop()
            
            # Process jobs concurrently
            tasks = []
            for job in jobs:
                task = loop.run_in_executor(
                    None, 
                    self.advanced_matcher.advanced_match, 
                    job, 
                    candidates
                )
                tasks.append((job.get('id'), job.get('title', ''), task))
            
            results = {}
            for job_id, job_title, task in tasks:
                matches = await task
                results[job_id] = {
                    'job_title': job_title,
                    'total_candidates': len(matches),
                    'top_matches': matches[:10],
                    'processing_status': 'success'
                }
            
            return results
            
        except Exception as e:
            logger.error(f"Error in async batch processing: {e}")
            return {}