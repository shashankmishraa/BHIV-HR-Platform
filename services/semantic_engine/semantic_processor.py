from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

class SemanticProcessor:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        
    def calculate_similarity(self, resume_text, job_description):
        """Calculate semantic similarity between resume and job"""
        resume_embedding = self.model.encode([resume_text])
        job_embedding = self.model.encode([job_description])
        
        similarity = cosine_similarity(resume_embedding, job_embedding)[0][0]
        return float(similarity)
    
    def enhanced_matching(self, candidate_data, job_requirements):
        """Enhanced matching with semantic scoring"""
        resume_text = f"{candidate_data.get('technical_skills', '')} {candidate_data.get('name', '')}"
        
        # Semantic similarity
        semantic_score = self.calculate_similarity(resume_text, job_requirements)
        
        # Rule-based scoring
        skills_match = self._calculate_skills_match(candidate_data.get('technical_skills', ''), job_requirements)
        experience_match = self._calculate_experience_match(candidate_data.get('experience_years', 0))
        
        # Weighted final score
        final_score = (semantic_score * 0.5) + (skills_match * 0.3) + (experience_match * 0.2)
        
        return {
            'total_score': min(100, int(final_score * 100)),
            'semantic_similarity': int(semantic_score * 100),
            'skills_match': int(skills_match * 100),
            'experience_match': int(experience_match * 100),
            'explanation': self._generate_explanation(semantic_score, skills_match, experience_match)
        }
    
    def _calculate_skills_match(self, candidate_skills, job_requirements):
        """Calculate skills match percentage"""
        if not candidate_skills:
            return 0.0
        
        job_skills = re.findall(r'\b(?:Python|Java|JavaScript|React|Node\.js|SQL|AWS|Docker)\b', 
                               job_requirements, re.IGNORECASE)
        candidate_skill_list = re.findall(r'\b(?:Python|Java|JavaScript|React|Node\.js|SQL|AWS|Docker)\b', 
                                        candidate_skills, re.IGNORECASE)
        
        if not job_skills:
            return 0.5
        
        matches = len(set(skill.lower() for skill in candidate_skill_list) & 
                     set(skill.lower() for skill in job_skills))
        return matches / len(job_skills)
    
    def _calculate_experience_match(self, experience_years):
        """Calculate experience match score"""
        if experience_years >= 5:
            return 1.0
        elif experience_years >= 3:
            return 0.8
        elif experience_years >= 1:
            return 0.6
        else:
            return 0.3
    
    def _generate_explanation(self, semantic_score, skills_match, experience_match):
        """Generate human-readable match explanation"""
        explanations = []
        
        if semantic_score > 0.7:
            explanations.append("Strong semantic match with job requirements")
        elif semantic_score > 0.5:
            explanations.append("Good semantic alignment with role")
        else:
            explanations.append("Limited semantic match with requirements")
        
        if skills_match > 0.7:
            explanations.append("Excellent technical skills alignment")
        elif skills_match > 0.4:
            explanations.append("Good technical skills match")
        else:
            explanations.append("Some technical skills gaps identified")
        
        if experience_match > 0.8:
            explanations.append("Strong experience level for role")
        elif experience_match > 0.5:
            explanations.append("Adequate experience level")
        else:
            explanations.append("Entry-level experience")
        
        return "; ".join(explanations)