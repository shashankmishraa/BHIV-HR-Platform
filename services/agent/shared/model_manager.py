"""
Centralized model management
"""
import os
import pickle
from typing import Dict, Any

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
        """Get path to model file"""
        return os.path.join(self.models_path, model_name)