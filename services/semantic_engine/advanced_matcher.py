"""
Advanced Semantic Matching Engine - Day 2
Enhanced candidate-job matching with detailed scoring breakdown
"""

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from typing import Dict, List, Tuple, Optional
import json
import logging

class AdvancedSemanticMatcher:
    """Enhanced semantic matching with detailed scoring breakdown"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def calculate_detailed_match(self, candidate: Dict, job: Dict) -> Dict:
        """Calculate detailed match scores with explanations"""
        try:
            # Skills matching (40% weight)
            skills_score, skills_details = self._match_skills(candidate, job)
            
            # Experience matching (30% weight)
            exp_score, exp_details = self._match_experience(candidate, job)
            
            # Role/Title matching (20% weight)
            role_score, role_details = self._match_role(candidate, job)
            
            # Location matching (10% weight)
            location_score, location_details = self._match_location(candidate, job)
            
            # Calculate weighted total
            total_score = (
                skills_score * 0.4 +
                exp_score * 0.3 +
                role_score * 0.2 +
                location_score * 0.1
            )
            
            return {
                'total_score': round(total_score, 2),
                'breakdown': {
                    'skills': {'score': skills_score, 'details': skills_details},
                    'experience': {'score': exp_score, 'details': exp_details},
                    'role': {'score': role_score, 'details': role_details},
                    'location': {'score': location_score, 'details': location_details}
                },
                'recommendation': self._get_recommendation(total_score),
                'strengths': self._identify_strengths(skills_score, exp_score, role_score, location_score),
                'gaps': self._identify_gaps(skills_score, exp_score, role_score, location_score)
            }
            
        except Exception as e:
            self.logger.error(f"Error in detailed matching: {e}")
            return self._fallback_match(candidate, job)
    
    def _match_skills(self, candidate: Dict, job: Dict) -> Tuple[float, Dict]:
        """Match skills with detailed breakdown"""
        try:
            candidate_skills = set(str(candidate.get('skills', '')).lower().split(','))
            job_skills = set(str(job.get('required_skills', '')).lower().split(','))
            
            # Clean empty strings
            candidate_skills = {s.strip() for s in candidate_skills if s.strip()}
            job_skills = {s.strip() for s in job_skills if s.strip()}
            
            if not job_skills:
                return 0.5, {'matched': [], 'missing': [], 'extra': list(candidate_skills)}
            
            matched = candidate_skills.intersection(job_skills)
            missing = job_skills - candidate_skills
            extra = candidate_skills - job_skills
            
            score = len(matched) / len(job_skills) if job_skills else 0
            
            return min(score, 1.0), {
                'matched': list(matched),
                'missing': list(missing),
                'extra': list(extra),
                'match_percentage': round(score * 100, 1)
            }
            
        except Exception as e:
            return 0.3, {'error': str(e)}
    
    def _match_experience(self, candidate: Dict, job: Dict) -> Tuple[float, Dict]:
        """Match experience levels"""
        try:
            candidate_exp = self._parse_experience(candidate.get('experience', ''))
            job_exp = self._parse_experience(job.get('experience_required', ''))
            
            if candidate_exp is None or job_exp is None:
                return 0.5, {'candidate_exp': candidate_exp, 'required_exp': job_exp}
            
            if candidate_exp >= job_exp:
                score = 1.0
                status = 'Meets requirement'
            elif candidate_exp >= job_exp * 0.8:
                score = 0.8
                status = 'Close match'
            elif candidate_exp >= job_exp * 0.6:
                score = 0.6
                status = 'Partial match'
            else:
                score = 0.3
                status = 'Below requirement'
            
            return score, {
                'candidate_years': candidate_exp,
                'required_years': job_exp,
                'status': status,
                'gap': max(0, job_exp - candidate_exp)
            }
            
        except Exception as e:
            return 0.4, {'error': str(e)}
    
    def _match_role(self, candidate: Dict, job: Dict) -> Tuple[float, Dict]:
        """Match job roles/titles"""
        try:
            candidate_role = str(candidate.get('designation', '')).lower()
            job_title = str(job.get('title', '')).lower()
            
            if not candidate_role or not job_title:
                return 0.4, {'candidate_role': candidate_role, 'job_title': job_title}
            
            # Simple keyword matching
            candidate_words = set(candidate_role.split())
            job_words = set(job_title.split())
            
            common_words = candidate_words.intersection(job_words)
            score = len(common_words) / max(len(job_words), 1)
            
            return min(score, 1.0), {
                'candidate_role': candidate_role,
                'job_title': job_title,
                'common_keywords': list(common_words),
                'match_percentage': round(score * 100, 1)
            }
            
        except Exception as e:
            return 0.3, {'error': str(e)}
    
    def _match_location(self, candidate: Dict, job: Dict) -> Tuple[float, Dict]:
        """Match location preferences"""
        try:
            candidate_location = str(candidate.get('location', '')).lower()
            job_location = str(job.get('location', '')).lower()
            
            if not candidate_location or not job_location:
                return 0.5, {'candidate_location': candidate_location, 'job_location': job_location}
            
            if candidate_location == job_location:
                score = 1.0
                status = 'Exact match'
            elif any(word in job_location for word in candidate_location.split()):
                score = 0.8
                status = 'Partial match'
            else:
                score = 0.3
                status = 'Different location'
            
            return score, {
                'candidate_location': candidate_location,
                'job_location': job_location,
                'status': status
            }
            
        except Exception as e:
            return 0.4, {'error': str(e)}
    
    def _parse_experience(self, exp_str: str) -> Optional[float]:
        """Parse experience string to years"""
        try:
            exp_str = str(exp_str).lower()
            if 'fresher' in exp_str or 'fresh' in exp_str:
                return 0.0
            
            # Extract numbers
            import re
            numbers = re.findall(r'\d+', exp_str)
            if numbers:
                return float(numbers[0])
            
            return None
        except:
            return None
    
    def _get_recommendation(self, score: float) -> str:
        """Get hiring recommendation based on score"""
        if score >= 0.8:
            return "Strong Match - Highly Recommended"
        elif score >= 0.6:
            return "Good Match - Recommended"
        elif score >= 0.4:
            return "Moderate Match - Consider with reservations"
        else:
            return "Weak Match - Not recommended"
    
    def _identify_strengths(self, skills: float, exp: float, role: float, location: float) -> List[str]:
        """Identify candidate strengths"""
        strengths = []
        if skills >= 0.7:
            strengths.append("Strong skill match")
        if exp >= 0.8:
            strengths.append("Excellent experience level")
        if role >= 0.6:
            strengths.append("Relevant role background")
        if location >= 0.8:
            strengths.append("Good location fit")
        
        return strengths or ["Basic qualifications present"]
    
    def _identify_gaps(self, skills: float, exp: float, role: float, location: float) -> List[str]:
        """Identify potential gaps"""
        gaps = []
        if skills < 0.5:
            gaps.append("Missing key skills")
        if exp < 0.6:
            gaps.append("Limited experience")
        if role < 0.4:
            gaps.append("Different role background")
        if location < 0.5:
            gaps.append("Location mismatch")
        
        return gaps
    
    def _fallback_match(self, candidate: Dict, job: Dict) -> Dict:
        """Fallback matching when advanced matching fails"""
        return {
            'total_score': 0.5,
            'breakdown': {
                'skills': {'score': 0.5, 'details': {'error': 'Fallback mode'}},
                'experience': {'score': 0.5, 'details': {'error': 'Fallback mode'}},
                'role': {'score': 0.5, 'details': {'error': 'Fallback mode'}},
                'location': {'score': 0.5, 'details': {'error': 'Fallback mode'}}
            },
            'recommendation': "Moderate Match - Manual review needed",
            'strengths': ["Requires manual evaluation"],
            'gaps': ["System evaluation incomplete"]
        }

# Batch processing for multiple candidates
class BatchMatcher:
    """Process multiple candidates efficiently"""
    
    def __init__(self):
        self.matcher = AdvancedSemanticMatcher()
    
    def rank_candidates(self, candidates: List[Dict], job: Dict) -> List[Dict]:
        """Rank candidates by match score"""
        results = []
        
        for candidate in candidates:
            match_result = self.matcher.calculate_detailed_match(candidate, job)
            results.append({
                'candidate': candidate,
                'match_score': match_result['total_score'],
                'match_details': match_result
            })
        
        # Sort by match score (descending)
        results.sort(key=lambda x: x['match_score'], reverse=True)
        
        return results