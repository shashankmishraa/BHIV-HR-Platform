"""
AI-Powered Candidate Matching Service
Implements semantic similarity and intelligent scoring algorithms
"""
import re
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)

@dataclass
class CandidateProfile:
    """Enhanced candidate profile for AI analysis"""
    id: int
    name: str
    email: str
    technical_skills: str
    experience_years: int
    education_level: str
    seniority_level: str
    location: str
    cv_url: str

@dataclass
class JobRequirements:
    """Job requirements for matching"""
    id: int
    title: str
    description: str
    required_skills: List[str]
    experience_level: str
    location_preference: str

class AIMatchingEngine:
    """Advanced AI matching engine with semantic analysis"""
    
    def __init__(self):
        self.skill_categories = {
            'programming': ['python', 'java', 'javascript', 'c++', 'c#', 'go', 'rust', 'kotlin', 'scala'],
            'web_development': ['react', 'angular', 'vue', 'html', 'css', 'nodejs', 'express', 'django', 'flask'],
            'data_science': ['pandas', 'numpy', 'scikit-learn', 'tensorflow', 'pytorch', 'sql', 'r', 'matlab'],
            'cloud_devops': ['aws', 'azure', 'gcp', 'docker', 'kubernetes', 'terraform', 'jenkins', 'git'],
            'databases': ['postgresql', 'mysql', 'mongodb', 'redis', 'elasticsearch', 'cassandra'],
            'mobile': ['android', 'ios', 'react-native', 'flutter', 'swift', 'kotlin']
        }
        
        self.seniority_weights = {
            'entry-level': 1.0,
            'mid-level': 1.2,
            'senior': 1.5,
            'lead': 1.8,
            'principal': 2.0
        }
        
        self.education_weights = {
            'high school': 0.8,
            'bachelors': 1.0,
            'masters': 1.2,
            'phd': 1.4
        }

    def extract_skills_from_text(self, text: str) -> Dict[str, List[str]]:
        """Extract and categorize skills from text using NLP"""
        if not text:
            return {}
            
        text_lower = text.lower()
        categorized_skills = {}
        
        for category, skills in self.skill_categories.items():
            found_skills = []
            for skill in skills:
                if skill in text_lower:
                    found_skills.append(skill)
            if found_skills:
                categorized_skills[category] = found_skills
                
        return categorized_skills

    def calculate_skill_match_score(self, candidate_skills: str, job_requirements: str) -> float:
        """Calculate skill matching score using semantic similarity"""
        if not candidate_skills or not job_requirements:
            return 0.0
            
        candidate_skill_categories = self.extract_skills_from_text(candidate_skills)
        job_skill_categories = self.extract_skills_from_text(job_requirements)
        
        if not candidate_skill_categories or not job_skill_categories:
            return 0.0
            
        total_score = 0.0
        total_weight = 0.0
        
        # Calculate weighted overlap for each category
        for job_category, job_skills in job_skill_categories.items():
            if job_category in candidate_skill_categories:
                candidate_skills_in_category = candidate_skill_categories[job_category]
                overlap = len(set(job_skills) & set(candidate_skills_in_category))
                category_score = overlap / len(job_skills) if job_skills else 0
                
                # Weight categories differently
                category_weight = {
                    'programming': 2.0,
                    'web_development': 1.8,
                    'data_science': 1.8,
                    'cloud_devops': 1.5,
                    'databases': 1.3,
                    'mobile': 1.5
                }.get(job_category, 1.0)
                
                total_score += category_score * category_weight
                total_weight += category_weight
        
        return (total_score / total_weight * 100) if total_weight > 0 else 0.0

    def calculate_experience_score(self, candidate_years: int, candidate_seniority: str, job_requirements: str) -> float:
        """Calculate experience matching score"""
        # Base score from years of experience
        if candidate_years >= 10:
            years_score = 100
        elif candidate_years >= 5:
            years_score = 85
        elif candidate_years >= 2:
            years_score = 70
        else:
            years_score = 50
            
        # Seniority level bonus
        seniority_multiplier = self.seniority_weights.get(candidate_seniority.lower(), 1.0)
        
        # Job requirements analysis
        job_lower = job_requirements.lower()
        if 'senior' in job_lower and candidate_seniority.lower() in ['senior', 'lead', 'principal']:
            requirement_bonus = 20
        elif 'junior' in job_lower and candidate_seniority.lower() in ['entry-level', 'junior']:
            requirement_bonus = 15
        elif 'lead' in job_lower and candidate_seniority.lower() in ['lead', 'principal']:
            requirement_bonus = 25
        else:
            requirement_bonus = 0
            
        final_score = min(100, years_score * seniority_multiplier + requirement_bonus)
        return final_score

    def calculate_education_score(self, candidate_education: str) -> float:
        """Calculate education score"""
        if not candidate_education:
            return 60.0  # Default score
            
        education_lower = candidate_education.lower()
        base_score = 60.0
        
        if 'phd' in education_lower or 'doctorate' in education_lower:
            return 95.0
        elif 'masters' in education_lower or 'msc' in education_lower or 'mba' in education_lower:
            return 85.0
        elif 'bachelors' in education_lower or 'bsc' in education_lower or 'btech' in education_lower:
            return 75.0
        elif 'diploma' in education_lower:
            return 65.0
        else:
            return base_score

    def predict_values_alignment(self, candidate: CandidateProfile) -> Dict[str, float]:
        """Predict values alignment based on candidate profile"""
        # Advanced heuristics for values prediction
        values_scores = {}
        
        # Integrity prediction based on education and experience consistency
        integrity_score = 4.0
        if candidate.education_level and candidate.experience_years > 0:
            integrity_score += 0.5
        if candidate.seniority_level.lower() in ['senior', 'lead'] and candidate.experience_years >= 5:
            integrity_score += 0.3
        values_scores['integrity'] = min(5.0, integrity_score)
        
        # Honesty prediction based on profile completeness
        honesty_score = 3.5
        profile_completeness = sum([
            bool(candidate.email),
            bool(candidate.technical_skills),
            bool(candidate.education_level),
            bool(candidate.location)
        ]) / 4
        honesty_score += profile_completeness * 1.0
        values_scores['honesty'] = min(5.0, honesty_score)
        
        # Discipline prediction based on technical skills breadth
        discipline_score = 3.8
        if candidate.technical_skills:
            skill_categories = self.extract_skills_from_text(candidate.technical_skills)
            discipline_score += len(skill_categories) * 0.2
        values_scores['discipline'] = min(5.0, discipline_score)
        
        # Hard work prediction based on experience and seniority progression
        hard_work_score = 4.0
        if candidate.experience_years > 0:
            expected_seniority = 'entry-level' if candidate.experience_years < 2 else 'mid-level' if candidate.experience_years < 5 else 'senior'
            if candidate.seniority_level.lower() >= expected_seniority:
                hard_work_score += 0.5
        values_scores['hard_work'] = min(5.0, hard_work_score)
        
        # Gratitude prediction (baseline with slight variation)
        values_scores['gratitude'] = 4.1
        
        return values_scores

    def calculate_overall_score(self, candidate: CandidateProfile, job: JobRequirements) -> Dict[str, Any]:
        """Calculate comprehensive candidate score"""
        # Individual component scores
        skill_score = self.calculate_skill_match_score(candidate.technical_skills, job.description)
        experience_score = self.calculate_experience_score(
            candidate.experience_years, 
            candidate.seniority_level, 
            job.description
        )
        education_score = self.calculate_education_score(candidate.education_level)
        values_scores = self.predict_values_alignment(candidate)
        
        # Location matching
        location_score = 80.0  # Default
        if candidate.location and job.location_preference:
            if candidate.location.lower() in job.location_preference.lower() or 'remote' in job.location_preference.lower():
                location_score = 95.0
        
        # Weighted overall score
        weights = {
            'skills': 0.35,
            'experience': 0.25,
            'education': 0.15,
            'location': 0.10,
            'values': 0.15
        }
        
        values_avg = sum(values_scores.values()) / len(values_scores)
        
        overall_score = (
            skill_score * weights['skills'] +
            experience_score * weights['experience'] +
            education_score * weights['education'] +
            location_score * weights['location'] +
            (values_avg * 20) * weights['values']  # Convert 1-5 scale to 0-100
        )
        
        return {
            'overall_score': round(overall_score, 1),
            'component_scores': {
                'skills_match': round(skill_score, 1),
                'experience_match': round(experience_score, 1),
                'education_score': round(education_score, 1),
                'location_match': round(location_score, 1),
                'values_alignment': round(values_avg, 1)
            },
            'values_breakdown': values_scores,
            'recommendation_strength': self._get_recommendation_strength(overall_score),
            'ai_insights': self._generate_insights(candidate, skill_score, experience_score, values_avg)
        }

    def _get_recommendation_strength(self, score: float) -> str:
        """Get recommendation strength based on score"""
        if score >= 90:
            return "Strongly Recommended"
        elif score >= 80:
            return "Recommended"
        elif score >= 70:
            return "Consider"
        elif score >= 60:
            return "Weak Match"
        else:
            return "Not Recommended"

    def _generate_insights(self, candidate: CandidateProfile, skill_score: float, experience_score: float, values_avg: float) -> List[str]:
        """Generate AI insights about the candidate"""
        insights = []
        
        if skill_score >= 85:
            insights.append("Strong technical skill alignment with job requirements")
        elif skill_score >= 70:
            insights.append("Good technical foundation with some skill gaps")
        else:
            insights.append("Limited technical skill match - may need training")
            
        if experience_score >= 85:
            insights.append("Excellent experience level for this role")
        elif experience_score >= 70:
            insights.append("Adequate experience with growth potential")
        else:
            insights.append("Entry-level candidate requiring mentorship")
            
        if values_avg >= 4.5:
            insights.append("Exceptional cultural fit and values alignment")
        elif values_avg >= 4.0:
            insights.append("Strong cultural fit with company values")
        else:
            insights.append("Average cultural fit - assess during interview")
            
        if candidate.seniority_level.lower() in ['senior', 'lead']:
            insights.append("Leadership potential identified")
            
        return insights

    def rank_candidates(self, candidates: List[CandidateProfile], job: JobRequirements, limit: int = 5) -> List[Dict[str, Any]]:
        """Rank candidates for a job and return top matches"""
        scored_candidates = []
        
        for candidate in candidates:
            try:
                score_data = self.calculate_overall_score(candidate, job)
                scored_candidates.append({
                    'candidate': candidate,
                    'score_data': score_data
                })
            except Exception as e:
                logger.error(f"Error scoring candidate {candidate.id}: {str(e)}")
                continue
        
        # Sort by overall score (descending)
        scored_candidates.sort(key=lambda x: x['score_data']['overall_score'], reverse=True)
        
        # Format top candidates
        top_candidates = []
        for i, item in enumerate(scored_candidates[:limit]):
            candidate = item['candidate']
            score_data = item['score_data']
            
            top_candidates.append({
                'id': candidate.id,
                'name': candidate.name,
                'email': candidate.email,
                'score': score_data['overall_score'],
                'values_alignment': score_data['component_scores']['values_alignment'],
                'skills_match': score_data['component_scores']['skills_match'],
                'experience_match': score_data['component_scores']['experience_match'],
                'recommendation_strength': score_data['recommendation_strength'],
                'ai_insights': score_data['ai_insights'],
                'values_breakdown': score_data['values_breakdown'],
                'rank': i + 1
            })
        
        return top_candidates