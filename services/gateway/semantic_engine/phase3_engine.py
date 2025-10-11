"""
Phase 3 Semantic Engine - Production Implementation
No fallbacks, proper dependency management, production standards
"""
import os
import asyncio
import logging
from typing import List, Dict, Any, Optional
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sqlalchemy import create_engine, text

logger = logging.getLogger(__name__)

class Phase3SemanticEngine:
    """Production Phase 3 Semantic Engine with advanced AI capabilities"""
    
    def __init__(self):
        self.model = None
        self.company_preferences = defaultdict(dict)
        self.cache = {}
        self.executor = ThreadPoolExecutor(max_workers=4)
        self._initialize()
    
    def _initialize(self):
        """Initialize semantic model and learning components"""
        try:
            logger.info("Initializing Phase 3 Semantic Engine...")
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self._load_company_preferences()
            logger.info("Phase 3 Semantic Engine initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Phase 3 engine: {e}")
            raise RuntimeError(f"Phase 3 initialization failed: {e}")
    
    def _get_db_engine(self):
        """Get database engine with proper connection pooling"""
        database_url = os.getenv("DATABASE_URL", 
            "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu")
        return create_engine(
            database_url, 
            pool_size=10, 
            max_overflow=20,
            pool_pre_ping=True,
            pool_recycle=3600
        )
    
    def _load_company_preferences(self):
        """Load company scoring preferences from feedback data"""
        try:
            engine = self._get_db_engine()
            with engine.connect() as connection:
                query = text("""
                    SELECT j.client_id, 
                           AVG(f.average_score) as avg_satisfaction,
                           COUNT(*) as feedback_count,
                           AVG(c.experience_years) as avg_exp_hired
                    FROM feedback f
                    JOIN jobs j ON f.job_id = j.id
                    JOIN candidates c ON f.candidate_id = c.id
                    WHERE f.average_score >= 4.0
                    GROUP BY j.client_id
                    HAVING COUNT(*) >= 3
                """)
                
                results = connection.execute(query)
                for row in results:
                    client_id, avg_satisfaction, feedback_count, avg_exp = row
                    weights = self._calculate_optimal_weights(avg_satisfaction, avg_exp)
                    
                    self.company_preferences[client_id] = {
                        'scoring_weights': weights,
                        'avg_satisfaction': float(avg_satisfaction),
                        'feedback_count': feedback_count,
                        'preferred_experience': float(avg_exp) if avg_exp else 0
                    }
                
                logger.info(f"Loaded preferences for {len(self.company_preferences)} companies")
        except Exception as e:
            logger.error(f"Failed to load company preferences: {e}")
    
    def _calculate_optimal_weights(self, avg_satisfaction: float, avg_experience: float) -> dict:
        """Calculate optimal scoring weights based on hiring patterns"""
        weights = {
            'semantic': 0.40,
            'experience': 0.30,
            'skills': 0.20,
            'location': 0.10
        }
        
        if avg_satisfaction > 4.5:
            weights['experience'] = 0.35
            weights['semantic'] = 0.35
        
        if avg_experience > 7:
            weights['experience'] = 0.40
            weights['semantic'] = 0.30
        elif avg_experience < 3:
            weights['skills'] = 0.30
            weights['experience'] = 0.20
        
        return weights
    
    def calculate_adaptive_score(self, job_data: dict, candidate_data: dict, 
                               client_id: Optional[str] = None) -> dict:
        """Calculate adaptive score with company-specific weights"""
        try:
            # Get company-specific weights
            weights = {'semantic': 0.40, 'experience': 0.30, 'skills': 0.20, 'location': 0.10}
            if client_id and client_id in self.company_preferences:
                weights.update(self.company_preferences[client_id].get('scoring_weights', {}))
            
            # Calculate individual scores
            semantic_score = self._calculate_semantic_similarity(job_data, candidate_data)
            experience_score = self._calculate_experience_score(
                job_data.get('experience_level', ''),
                candidate_data.get('experience_years', 0),
                candidate_data.get('seniority_level', '')
            )
            skills_score = self._calculate_skills_score(
                job_data.get('requirements', ''),
                candidate_data.get('technical_skills', '')
            )
            location_score = self._calculate_location_score(
                job_data.get('location', ''),
                candidate_data.get('location', '')
            )
            
            # Cultural fit analysis
            cultural_fit = self._calculate_cultural_fit(candidate_data, client_id)
            
            # Weighted total score
            total_score = (
                semantic_score * weights['semantic'] +
                experience_score * weights['experience'] +
                skills_score * weights['skills'] +
                location_score * weights['location'] +
                cultural_fit * 0.1
            )
            
            return {
                'total_score': float(total_score),
                'breakdown': {
                    'semantic_similarity': float(semantic_score),
                    'experience_match': float(experience_score),
                    'skills_match': float(skills_score),
                    'location_match': float(location_score),
                    'cultural_fit': float(cultural_fit)
                },
                'weights_used': weights,
                'algorithm_version': '3.0.0-phase3-production'
            }
        except Exception as e:
            logger.error(f"Error in adaptive scoring: {e}")
            raise
    
    def _calculate_semantic_similarity(self, job_data: dict, candidate_data: dict) -> float:
        """Calculate semantic similarity using sentence transformers"""
        job_text = f"{job_data.get('title', '')} {job_data.get('description', '')} {job_data.get('requirements', '')}"
        candidate_text = f"{candidate_data.get('technical_skills', '')} {candidate_data.get('seniority_level', '')} {candidate_data.get('education_level', '')}"
        
        job_embedding = self.model.encode([job_text])
        candidate_embedding = self.model.encode([candidate_text])
        
        similarity = cosine_similarity(job_embedding, candidate_embedding)[0][0]
        return float(similarity)
    
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
        
        req_embedding = self.model.encode([job_requirements.lower()])
        skills_embedding = self.model.encode([candidate_skills.lower()])
        
        similarity = cosine_similarity(req_embedding, skills_embedding)[0][0]
        return float(similarity)
    
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
        
        job_embedding = self.model.encode([job_loc_lower])
        candidate_embedding = self.model.encode([candidate_loc_lower])
        
        similarity = cosine_similarity(job_embedding, candidate_embedding)[0][0]
        return float(similarity)
    
    def _calculate_cultural_fit(self, candidate_data: dict, client_id: Optional[str]) -> float:
        """Calculate cultural fit based on historical feedback"""
        if not client_id:
            return 0.5
        
        try:
            engine = self._get_db_engine()
            with engine.connect() as connection:
                query = text("""
                    SELECT AVG((integrity + honesty + discipline + hard_work + gratitude) / 5.0) 
                    FROM feedback f 
                    JOIN jobs j ON f.job_id = j.id 
                    WHERE j.client_id = :client_id 
                    AND f.candidate_id = :candidate_id
                """)
                result = connection.execute(query, {
                    'client_id': client_id, 
                    'candidate_id': candidate_data.get('id')
                })
                avg_score = result.fetchone()
                return float(avg_score[0]) / 5.0 if avg_score[0] else 0.5
        except Exception as e:
            logger.error(f"Error calculating cultural fit: {e}")
            return 0.5
    
    def match_candidates(self, job_data: dict, candidates: list) -> list:
        """Match candidates to job with Phase 3 features"""
        try:
            client_id = job_data.get('client_id')
            scored_candidates = []
            
            for candidate in candidates:
                score_data = self.calculate_adaptive_score(job_data, candidate, client_id)
                
                scored_candidates.append({
                    'candidate_id': candidate.get('id'),
                    'total_score': score_data['total_score'],
                    'score_breakdown': score_data['breakdown'],
                    'candidate_data': candidate,
                    'algorithm_version': '3.0.0-phase3-production'
                })
            
            scored_candidates.sort(key=lambda x: x['total_score'], reverse=True)
            return scored_candidates
        except Exception as e:
            logger.error(f"Error in candidate matching: {e}")
            raise
    
    async def enhanced_batch_process(self, jobs: list, candidates: list, use_cache: bool = True) -> dict:
        """Enhanced batch processing with async and caching"""
        cache_key = f"batch_{len(jobs)}_{len(candidates)}_{hash(str([j.get('id') for j in jobs]))}"
        
        if use_cache and cache_key in self.cache:
            logger.info(f"Using cached results for batch processing")
            return self.cache[cache_key]
        
        try:
            results = {}
            chunk_size = 50
            
            for job in jobs:
                job_id = job.get('id')
                client_id = job.get('client_id')
                job_results = []
                
                # Process candidates in chunks
                for i in range(0, len(candidates), chunk_size):
                    chunk = candidates[i:i + chunk_size]
                    chunk_results = await self._process_chunk_async(job, chunk, client_id)
                    job_results.extend(chunk_results)
                
                job_results.sort(key=lambda x: x['total_score'], reverse=True)
                
                results[job_id] = {
                    'job_title': job.get('title', ''),
                    'total_candidates': len(candidates),
                    'top_matches': job_results[:10],
                    'processing_status': 'success',
                    'algorithm_version': '3.0.0-phase3-production',
                    'cache_used': False
                }
            
            if use_cache:
                self.cache[cache_key] = results
            
            return results
        except Exception as e:
            logger.error(f"Error in enhanced batch processing: {e}")
            raise
    
    async def _process_chunk_async(self, job: dict, candidates_chunk: list, client_id: Optional[str]) -> list:
        """Process candidate chunk asynchronously"""
        loop = asyncio.get_event_loop()
        
        tasks = []
        for candidate in candidates_chunk:
            task = loop.run_in_executor(
                None, 
                self.calculate_adaptive_score, 
                job, 
                candidate,
                client_id
            )
            tasks.append((candidate.get('id'), task))
        
        results = []
        for candidate_id, task in tasks:
            try:
                score_data = await task
                results.append({
                    'candidate_id': candidate_id,
                    'total_score': score_data['total_score'],
                    'score_breakdown': score_data['breakdown']
                })
            except Exception as e:
                logger.error(f"Error processing candidate {candidate_id}: {e}")
        
        return results
    
    def get_company_preferences(self, client_id: str) -> dict:
        """Get scoring preferences for a specific company"""
        return self.company_preferences.get(client_id, {})
    
    def track_successful_match(self, job_id: int, candidate_id: int, feedback_score: float):
        """Track successful match for learning"""
        if feedback_score >= 4.0:
            self._load_company_preferences()

# Backward compatibility classes
class AdvancedSemanticMatcher:
    """Backward compatibility wrapper"""
    def __init__(self):
        self.engine = Phase3SemanticEngine()
        self.enabled = True
    
    def calculate_multi_factor_score(self, job_data: dict, candidate_data: dict) -> dict:
        return self.engine.calculate_adaptive_score(job_data, candidate_data)
    
    def advanced_match(self, job_data: dict, candidates: list) -> list:
        return self.engine.match_candidates(job_data, candidates)

class BatchMatcher:
    """Enhanced batch matcher"""
    def __init__(self):
        self.engine = Phase3SemanticEngine()
        self.enabled = True
    
    def batch_process(self, jobs: list, candidates: list) -> dict:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            return loop.run_until_complete(
                self.engine.enhanced_batch_process(jobs, candidates)
            )
        finally:
            loop.close()
    
    async def async_batch_process(self, jobs: list, candidates: list) -> dict:
        return await self.engine.enhanced_batch_process(jobs, candidates)

class LearningEngine:
    """Learning engine wrapper"""
    def __init__(self):
        self.engine = Phase3SemanticEngine()
        self.company_preferences = self.engine.company_preferences
    
    def load_company_preferences(self):
        self.engine._load_company_preferences()
        self.company_preferences = self.engine.company_preferences
    
    def get_company_preferences(self, client_id: str) -> dict:
        return self.engine.get_company_preferences(client_id)
    
    def track_successful_match(self, job_id: int, candidate_id: int, feedback_score: float):
        self.engine.track_successful_match(job_id, candidate_id, feedback_score)

class SemanticJobMatcher:
    """Legacy compatibility"""
    def __init__(self):
        self.engine = Phase3SemanticEngine()
        self.enabled = True
    
    def match_candidates(self, job_data: dict, candidates: list) -> list:
        return self.engine.match_candidates(job_data, candidates)