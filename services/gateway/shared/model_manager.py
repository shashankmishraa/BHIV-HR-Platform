"""
Centralized model management
"""
from typing import Dict, Any
import os

import pickle
class ModelManager:
    """Centralized model loading and management"""
    
    def __init__(self):
        self.models_path = os.path.join(os.path.dirname(__file__), '..', '..', 'models')
        self._skill_embeddings = None
    
    def get_skill_embeddings(self) -> Dict[str, Any]:
        """Load skill embeddings from centralized location"""
        if self._skill_embeddings is None:
            embeddings_path = os.path.join(self.models_path, 'skill_embeddings.pkl')
            try:
                with open(embeddings_path, 'rb') as f:
                    self._skill_embeddings = pickle.load(f)
            except FileNotFoundError:
                self._skill_embeddings = {}
        return self._skill_embeddings
    
    def get_model_path(self, model_name: str) -> str:
        """Get path to model file with security validation"""
        # Sanitize model name to prevent path traversal
        if not model_name or '..' in model_name or '/' in model_name or '\\' in model_name:
            raise ValueError("Invalid model name")
        
        model_path = os.path.join(self.models_path, model_name)
        
        # Ensure the resolved path is within models directory
        if not model_path.startswith(os.path.abspath(self.models_path)):
            raise ValueError("Path traversal attempt detected")
            
        return model_path