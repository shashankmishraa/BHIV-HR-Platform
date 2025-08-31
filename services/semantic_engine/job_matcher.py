import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import json

class SemanticJobMatcher:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize job matcher with semantic model"""
        try:
            self.model = SentenceTransformer(model_name)
            print(f"✅ Job matcher loaded with model: {model_name}")
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            self.model = None
    
    def calculate_fit_score(self, candidate_profile, job_description):
        """Calculate comprehensive fit score between candidate and job"""
        if not self.model:
            return self._fallback_scoring(candidate_profile, job_description)
        
        try:
            # Extract candidate text for embedding
            candidate_text = self._build_candidate_text(candidate_profile)
            
            # Calculate semantic similarity
            semantic_score = self._calculate_semantic_similarity(candidate_text, job_description)
            
            # Calculate skill match score
            skill_score = self._calculate_skill_match(candidate_profile, job_description)
            
            # Calculate role match score
            role_score = self._calculate_role_match(candidate_profile, job_description)
            
            # Weighted final score
            final_score = (
                semantic_score * 0.4 +
                skill_score * 0.4 +
                role_score * 0.2
            )
            
            return {
                "overall_score": float(final_score),
                "semantic_similarity": float(semantic_score),
                "skill_match": float(skill_score),
                "role_match": float(role_score),
                "explanation": self._generate_explanation(semantic_score, skill_score, role_score)
            }
        
        except Exception as e:
            print(f"Error calculating fit score: {e}")
            return self._fallback_scoring(candidate_profile, job_description)
    
    def _build_candidate_text(self, candidate_profile):
        """Build text representation of candidate"""
        text_parts = []
        
        # Add skills
        if 'semantic_skills' in candidate_profile:
            skills = [skill['skill'] for skill in candidate_profile['semantic_skills']]
            text_parts.append(f"Skills: {', '.join(skills)}")
        
        # Add roles
        if 'semantic_roles' in candidate_profile:
            roles = [role['role'] for role in candidate_profile['semantic_roles']]
            text_parts.append(f"Roles: {', '.join(roles)}")
        
        # Add experience
        if 'experience_years' in candidate_profile:
            text_parts.append(f"Experience: {candidate_profile['experience_years']} years")
        
        return ". ".join(text_parts)
    
    def _calculate_semantic_similarity(self, candidate_text, job_description):
        """Calculate semantic similarity using embeddings"""
        try:
            candidate_embedding = self.model.encode([candidate_text])
            job_embedding = self.model.encode([job_description])
            similarity = cosine_similarity(candidate_embedding, job_embedding)[0][0]
            return max(0.0, min(1.0, similarity))
        except:
            return 0.5
    
    def _calculate_skill_match(self, candidate_profile, job_description):
        """Calculate skill match score"""
        if 'semantic_skills' not in candidate_profile:
            return 0.5
        
        candidate_skills = [skill['skill'].lower() for skill in candidate_profile['semantic_skills']]
        job_desc_lower = job_description.lower()
        
        matches = 0
        total_skills = len(candidate_skills)
        
        for skill in candidate_skills:
            if any(word in job_desc_lower for word in skill.split()):
                matches += 1
        
        return matches / max(total_skills, 1)
    
    def _calculate_role_match(self, candidate_profile, job_description):
        """Calculate role match score"""
        if 'semantic_roles' not in candidate_profile:
            return 0.5
        
        candidate_roles = [role['role'].lower() for role in candidate_profile['semantic_roles']]
        job_desc_lower = job_description.lower()
        
        for role in candidate_roles:
            if any(word in job_desc_lower for word in role.split()):
                return 0.9
        
        return 0.3
    
    def _generate_explanation(self, semantic_score, skill_score, role_score):
        """Generate human-readable explanation"""
        explanations = []
        
        if semantic_score > 0.7:
            explanations.append("Strong semantic match with job requirements")
        elif semantic_score > 0.5:
            explanations.append("Good semantic alignment")
        else:
            explanations.append("Limited semantic match")
        
        if skill_score > 0.7:
            explanations.append("Excellent skill match")
        elif skill_score > 0.4:
            explanations.append("Good skill alignment")
        else:
            explanations.append("Some skill gaps identified")
        
        if role_score > 0.7:
            explanations.append("Role experience aligns well")
        else:
            explanations.append("Role transition may be needed")
        
        return ". ".join(explanations)
    
    def _fallback_scoring(self, candidate_profile, job_description):
        """Fallback scoring without semantic model"""
        return {
            "overall_score": 0.6,
            "semantic_similarity": 0.6,
            "skill_match": 0.6,
            "role_match": 0.6,
            "explanation": "Basic matching (semantic model unavailable)"
        }
    
    def rank_candidates(self, candidates, job_description, top_k=5):
        """Rank candidates for a job and return top matches"""
        scored_candidates = []
        
        for candidate in candidates:
            score_data = self.calculate_fit_score(candidate, job_description)
            candidate_with_score = {
                **candidate,
                **score_data
            }
            scored_candidates.append(candidate_with_score)
        
        # Sort by overall score
        scored_candidates.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return scored_candidates[:top_k]

def test_job_matcher():
    """Test the job matcher"""
    matcher = SemanticJobMatcher()
    
    # Sample candidate
    candidate = {
        "name": "John Doe",
        "semantic_skills": [
            {"skill": "Python programming", "confidence": 0.9},
            {"skill": "Machine Learning", "confidence": 0.8}
        ],
        "semantic_roles": [
            {"role": "Data Scientist", "confidence": 0.8}
        ],
        "experience_years": 3
    }
    
    # Sample job description
    job_desc = "We are looking for a Data Scientist with Python and Machine Learning experience."
    
    # Calculate fit score
    score = matcher.calculate_fit_score(candidate, job_desc)
    print(f"Fit Score: {score}")

if __name__ == "__main__":
    test_job_matcher()