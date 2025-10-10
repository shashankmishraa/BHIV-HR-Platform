import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import logging

logger = logging.getLogger(__name__)

class SemanticJobMatcher:
    """Real AI-powered semantic job matching using sentence transformers"""
    def __init__(self):
        self.enabled = True
        self.model = None
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize sentence transformer model"""
        try:
            print("INFO: Loading sentence transformer model (Phase 2)...")
            # Use lightweight, fast model optimized for semantic similarity
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            print("SUCCESS: Semantic matching model loaded (Phase 2)")
        except Exception as e:
            logger.error(f"Failed to load semantic model: {e}")
            self.enabled = False
            print("WARNING: Falling back to keyword matching")
    
    def get_job_embedding(self, job_text: str) -> np.ndarray:
        """Get semantic embedding for job description"""
        if not self.enabled or not self.model:
            return np.array([])
        
        try:
            # Combine job title, description, and requirements
            embedding = self.model.encode([job_text])
            return embedding[0]
        except Exception as e:
            logger.error(f"Error generating job embedding: {e}")
            return np.array([])
    
    def get_candidate_embedding(self, candidate_text: str) -> np.ndarray:
        """Get semantic embedding for candidate profile"""
        if not self.enabled or not self.model:
            return np.array([])
        
        try:
            embedding = self.model.encode([candidate_text])
            return embedding[0]
        except Exception as e:
            logger.error(f"Error generating candidate embedding: {e}")
            return np.array([])
    
    def calculate_semantic_similarity(self, job_embedding: np.ndarray, candidate_embedding: np.ndarray) -> float:
        """Calculate cosine similarity between job and candidate embeddings"""
        if job_embedding.size == 0 or candidate_embedding.size == 0:
            return 0.0
        
        try:
            # Reshape for sklearn cosine_similarity
            job_emb = job_embedding.reshape(1, -1)
            candidate_emb = candidate_embedding.reshape(1, -1)
            
            similarity = cosine_similarity(job_emb, candidate_emb)[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {e}")
            return 0.0
    
    def match_candidates(self, job_data: dict, candidates: list) -> list:
        """Semantic matching of candidates to job"""
        if not self.enabled:
            return []
        
        try:
            # Create comprehensive job text
            job_text = f"{job_data.get('title', '')} {job_data.get('description', '')} {job_data.get('requirements', '')}"
            job_embedding = self.get_job_embedding(job_text)
            
            if job_embedding.size == 0:
                return []
            
            scored_candidates = []
            
            for candidate in candidates:
                # Create comprehensive candidate text
                candidate_text = f"{candidate.get('technical_skills', '')} {candidate.get('seniority_level', '')} {candidate.get('education_level', '')}"
                candidate_embedding = self.get_candidate_embedding(candidate_text)
                
                if candidate_embedding.size == 0:
                    continue
                
                similarity_score = self.calculate_semantic_similarity(job_embedding, candidate_embedding)
                
                scored_candidates.append({
                    'candidate_id': candidate.get('id'),
                    'semantic_score': similarity_score,
                    'candidate_data': candidate
                })
            
            # Sort by semantic similarity
            scored_candidates.sort(key=lambda x: x['semantic_score'], reverse=True)
            return scored_candidates
            
        except Exception as e:
            logger.error(f"Error in semantic matching: {e}")
            return []