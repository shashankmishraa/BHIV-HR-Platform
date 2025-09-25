from pathlib import Path
from typing import Dict, List, Optional, Any
import json
import logging
import os

import numpy as np
import pickle
logger = logging.getLogger(__name__)

class ModelManager:
    """Manages AI model artifacts and embeddings for semantic matching"""
    
    def __init__(self, model_dir: Optional[str] = None):
        self.version = "2.1.0"
        # Use centralized models directory with security validation
        if model_dir is None:
            model_dir = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
        
        # Validate and sanitize model directory path
        model_dir = os.path.abspath(model_dir)
        if '..' in model_dir:
            raise ValueError("Invalid model directory path")
            
        self.model_dir = Path(model_dir)
        self.model_dir.mkdir(exist_ok=True)
        
        self.skill_embeddings = {}
        self.job_templates = {}
        self.similarity_cache = {}
        
        self._initialize_models()
        logger.info(f"ModelManager v{self.version} initialized")
    
    def _initialize_models(self):
        """Initialize or load pre-trained models"""
        try:
            self._load_skill_embeddings()
            self._load_job_templates()
            logger.info("Model artifacts loaded successfully")
        except Exception as e:
            logger.warning(f"Failed to load models, creating new ones: {e}")
            self._create_skill_embeddings()
            self._create_job_templates()
    
    def _load_skill_embeddings(self):
        """Load skill embeddings from file"""
        embeddings_path = self.model_dir / "skill_embeddings.pkl"
        if embeddings_path.exists():
            with open(embeddings_path, 'rb') as f:
                self.skill_embeddings = pickle.load(f)
        else:
            self._create_skill_embeddings()
    
    def _create_skill_embeddings(self):
        """Create skill embeddings using word2vec-like approach"""
        skills = [
            'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue',
            'node', 'express', 'django', 'flask', 'spring', 'sql', 'mysql', 
            'postgresql', 'mongodb', 'redis', 'aws', 'azure', 'gcp', 'docker',
            'kubernetes', 'jenkins', 'git', 'linux', 'html', 'css', 'bootstrap',
            'machine learning', 'ai', 'data science', 'tensorflow', 'pytorch',
            'pandas', 'numpy', 'scikit-learn', 'tableau', 'power bi'
        ]
        
        # Create embeddings based on skill relationships
        embedding_dim = 100
        
        for skill in skills:
            # Generate deterministic embeddings based on skill characteristics
            np.random.seed(hash(skill) % 10000)
            embedding = np.random.randn(embedding_dim)
            
            # Add domain-specific patterns
            if skill in ['python', 'java', 'javascript']:
                embedding[0:10] += 2.0  # Programming languages cluster
            elif skill in ['react', 'angular', 'vue', 'html', 'css']:
                embedding[10:20] += 2.0  # Frontend technologies
            elif skill in ['sql', 'mysql', 'postgresql', 'mongodb']:
                embedding[20:30] += 2.0  # Database technologies
            elif skill in ['aws', 'azure', 'docker', 'kubernetes']:
                embedding[30:40] += 2.0  # Cloud/DevOps
            
            # Normalize
            embedding = embedding / np.linalg.norm(embedding)
            self.skill_embeddings[skill] = embedding
        
        self._save_skill_embeddings()
    
    def _save_skill_embeddings(self):
        """Save skill embeddings to file"""
        embeddings_path = self.model_dir / "skill_embeddings.pkl"
        with open(embeddings_path, 'wb') as f:
            pickle.dump(self.skill_embeddings, f)
    
    def _load_job_templates(self):
        """Load job templates from file"""
        templates_path = self.model_dir / "job_templates.json"
        if templates_path.exists():
            with open(templates_path, 'r') as f:
                self.job_templates = json.load(f)
        else:
            self._create_job_templates()
    
    def _create_job_templates(self):
        """Create job role templates"""
        self.job_templates = {
            'software_engineer': {
                'required_skills': ['python', 'java', 'javascript', 'sql', 'git'],
                'preferred_skills': ['react', 'docker', 'aws'],
                'experience_range': (2, 8),
                'weight_factors': {'skills': 0.6, 'experience': 0.3, 'education': 0.1}
            },
            'data_scientist': {
                'required_skills': ['python', 'sql', 'machine learning', 'pandas', 'numpy'],
                'preferred_skills': ['tensorflow', 'pytorch', 'aws', 'tableau'],
                'experience_range': (1, 6),
                'weight_factors': {'skills': 0.7, 'experience': 0.2, 'education': 0.1}
            },
            'frontend_developer': {
                'required_skills': ['javascript', 'html', 'css', 'react'],
                'preferred_skills': ['typescript', 'vue', 'angular', 'bootstrap'],
                'experience_range': (1, 5),
                'weight_factors': {'skills': 0.8, 'experience': 0.15, 'education': 0.05}
            },
            'devops_engineer': {
                'required_skills': ['docker', 'kubernetes', 'aws', 'linux', 'git'],
                'preferred_skills': ['jenkins', 'terraform', 'ansible'],
                'experience_range': (2, 10),
                'weight_factors': {'skills': 0.5, 'experience': 0.4, 'education': 0.1}
            }
        }
        self._save_job_templates()
    
    def _save_job_templates(self):
        """Save job templates to file"""
        templates_path = self.model_dir / "job_templates.json"
        with open(templates_path, 'w') as f:
            json.dump(self.job_templates, f, indent=2)
    
    def get_skill_embedding(self, skill: str) -> Optional[np.ndarray]:
        """Get embedding for a specific skill"""
        return self.skill_embeddings.get(skill.lower())
    
    def calculate_skill_similarity(self, skill1: str, skill2: str) -> float:
        """Calculate similarity between two skills"""
        cache_key = f"{skill1.lower()}_{skill2.lower()}"
        if cache_key in self.similarity_cache:
            return self.similarity_cache[cache_key]
        
        emb1 = self.get_skill_embedding(skill1)
        emb2 = self.get_skill_embedding(skill2)
        
        if emb1 is None or emb2 is None:
            similarity = 1.0 if skill1.lower() == skill2.lower() else 0.0
        else:
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
            similarity = max(0.0, similarity)  # Ensure non-negative
        
        self.similarity_cache[cache_key] = similarity
        return similarity
    
    def get_job_template(self, job_title: str) -> Optional[Dict]:
        """Get job template based on title"""
        title_lower = job_title.lower()
        
        # Direct match
        if title_lower in self.job_templates:
            return self.job_templates[title_lower]
        
        # Fuzzy matching
        for template_name, template in self.job_templates.items():
            if any(word in title_lower for word in template_name.split('_')):
                return template
        
        return None
    
    def update_model_artifacts(self, new_skills: Optional[List[str]] = None, 
                             new_templates: Optional[Dict] = None):
        """Update model artifacts with new data"""
        if new_skills:
            for skill in new_skills:
                if skill.lower() not in self.skill_embeddings:
                    # Create embedding for new skill
                    np.random.seed(hash(skill) % 10000)
                    embedding = np.random.randn(100)
                    embedding = embedding / np.linalg.norm(embedding)
                    self.skill_embeddings[skill.lower()] = embedding
            
            self._save_skill_embeddings()
        
        if new_templates:
            self.job_templates.update(new_templates)
            self._save_job_templates()
        
        logger.info("Model artifacts updated successfully")
    
    def get_model_stats(self) -> Dict[str, Any]:
        """Get statistics about loaded models"""
        return {
            'skill_embeddings_count': len(self.skill_embeddings),
            'job_templates_count': len(self.job_templates),
            'cache_size': len(self.similarity_cache),
            'embedding_dimension': len(next(iter(self.skill_embeddings.values()))) if self.skill_embeddings else 0,
            'model_version': self.version
        }