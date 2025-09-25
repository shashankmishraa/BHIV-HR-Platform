from typing import Dict, List, Tuple, Any, Optional
import logging
import time

from concurrent.futures import ThreadPoolExecutor

from .job_matcher import SemanticJobMatcher

logger = logging.getLogger(__name__)


class AdvancedSemanticMatcher:
    """Advanced semantic matcher with ML-based scoring and bias mitigation"""

    def __init__(self):
        self.version = "2.1.0"
        self.base_matcher = SemanticJobMatcher()
        self.bias_weights = self._initialize_bias_weights()
        self.performance_cache = {}
        logger.info(f"AdvancedSemanticMatcher v{self.version} initialized")

    def _initialize_bias_weights(self) -> Dict[str, float]:
        """Initialize bias mitigation weights"""
        return {
            "gender_neutral": 1.0,
            "experience_fair": 0.9,
            "education_balanced": 0.95,
            "location_diverse": 0.85,
            "skill_focused": 1.1,
        }

    def advanced_match(
        self, job_data: Dict[str, Any], candidate_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Perform advanced semantic matching with bias mitigation"""
        start_time = time.time()

        # Extract relevant fields
        job_requirements = (
            job_data.get("requirements", "") + " " + job_data.get("description", "")
        )
        job_title = job_data.get("title", "")
        job_level = job_data.get("experience_level", "")
        job_location = job_data.get("location", "")

        candidate_skills = candidate_data.get("technical_skills", "")
        candidate_experience = candidate_data.get("experience_years", 0)
        candidate_location = candidate_data.get("location", "")
        candidate_education = candidate_data.get("education_level", "")

        # Base semantic matching
        base_match = self.base_matcher.match(
            job_requirements, candidate_skills, job_level, candidate_experience
        )

        # Advanced scoring factors
        advanced_scores = self._calculate_advanced_scores(
            job_data, candidate_data, base_match
        )

        # Bias mitigation
        bias_adjusted_score = self._apply_bias_mitigation(
            base_match["overall_score"], candidate_data, advanced_scores
        )

        # Generate detailed reasoning
        reasoning = self._generate_reasoning(
            base_match, advanced_scores, job_title, candidate_data
        )

        processing_time = time.time() - start_time

        result = {
            "score": round(bias_adjusted_score * 100, 1),  # Convert to 0-100 scale
            "base_score": round(base_match["overall_score"] * 100, 1),
            "skill_match": base_match["skill_score"],
            "experience_match": base_match["experience_score"],
            "domain_alignment": base_match["domain_score"],
            "advanced_factors": advanced_scores,
            "matched_skills": base_match["matched_skills"],
            "reasoning": reasoning,
            "bias_adjusted": True,
            "processing_time": round(processing_time, 4),
            "algorithm_version": self.version,
        }

        # Cache for performance optimization
        cache_key = f"{job_data.get('id', 0)}_{candidate_data.get('id', 0)}"
        self.performance_cache[cache_key] = result

        return result

    def _calculate_advanced_scores(
        self, job_data: Dict, candidate_data: Dict, base_match: Dict
    ) -> Dict[str, float]:
        """Calculate advanced scoring factors"""
        scores = {}

        # Cultural fit based on values alignment
        scores["cultural_fit"] = self._calculate_cultural_fit(job_data, candidate_data)

        # Growth potential
        scores["growth_potential"] = self._calculate_growth_potential(candidate_data)

        # Communication skills (inferred from profile completeness)
        scores["communication"] = self._calculate_communication_score(candidate_data)

        # Technical depth
        scores["technical_depth"] = self._calculate_technical_depth(
            candidate_data.get("technical_skills", ""), base_match["matched_skills"]
        )

        # Industry relevance
        scores["industry_relevance"] = self._calculate_industry_relevance(
            job_data, candidate_data
        )

        return scores

    def _calculate_cultural_fit(self, job_data: Dict, candidate_data: Dict) -> float:
        """Calculate cultural fit score"""
        # Simplified cultural fit based on job type and candidate profile
        job_title = job_data.get("title", "").lower()
        candidate_skills = candidate_data.get("technical_skills", "").lower()

        fit_score = 0.5  # Base score

        # Team-oriented roles
        if any(word in job_title for word in ["lead", "senior", "manager"]):
            if candidate_data.get("experience_years", 0) >= 3:
                fit_score += 0.3

        # Innovation-focused roles
        if any(word in job_title for word in ["ai", "ml", "data", "research"]):
            if any(
                skill in candidate_skills
                for skill in ["python", "tensorflow", "pytorch"]
            ):
                fit_score += 0.2

        return min(1.0, fit_score)

    def _calculate_growth_potential(self, candidate_data: Dict) -> float:
        """Calculate growth potential score"""
        experience = candidate_data.get("experience_years", 0)
        education = candidate_data.get("education_level", "").lower()
        skills_count = len(candidate_data.get("technical_skills", "").split(","))

        # Growth potential factors
        potential = 0.5

        # Education factor
        if "master" in education or "mba" in education:
            potential += 0.2
        elif "bachelor" in education:
            potential += 0.1

        # Experience sweet spot (2-7 years for high growth)
        if 2 <= experience <= 7:
            potential += 0.2
        elif experience < 2:
            potential += 0.1  # High potential for fresh talent

        # Skill diversity
        if skills_count >= 5:
            potential += 0.1

        return min(1.0, potential)

    def _calculate_communication_score(self, candidate_data: Dict) -> float:
        """Infer communication skills from profile completeness"""
        fields = ["name", "email", "technical_skills", "education_level", "location"]
        completed_fields = sum(1 for field in fields if candidate_data.get(field))

        base_score = completed_fields / len(fields)

        # Bonus for detailed skills description
        skills_text = candidate_data.get("technical_skills", "")
        if len(skills_text) > 50:  # Detailed skills description
            base_score += 0.1

        return min(1.0, base_score)

    def _calculate_technical_depth(
        self, candidate_skills: str, matched_skills: List[str]
    ) -> float:
        """Calculate technical depth score"""
        if not candidate_skills:
            return 0.0

        skills_list = [s.strip().lower() for s in candidate_skills.split(",")]
        total_skills = len(skills_list)
        matched_count = len(matched_skills)

        # Base depth from skill count
        depth_score = min(1.0, total_skills / 10)  # Normalize to 10 skills

        # Bonus for high match ratio
        if total_skills > 0:
            match_ratio = matched_count / total_skills
            depth_score += match_ratio * 0.3

        return min(1.0, depth_score)

    def _calculate_industry_relevance(
        self, job_data: Dict, candidate_data: Dict
    ) -> float:
        """Calculate industry relevance score"""
        job_dept = job_data.get("department", "").lower()
        job_title = job_data.get("title", "").lower()
        candidate_skills = candidate_data.get("technical_skills", "").lower()

        relevance = 0.5  # Base score

        # Department-specific relevance
        if "engineering" in job_dept or "tech" in job_dept:
            tech_skills = ["python", "java", "javascript", "react", "node", "sql"]
            if any(skill in candidate_skills for skill in tech_skills):
                relevance += 0.3

        if "data" in job_title or "analytics" in job_title:
            data_skills = ["python", "sql", "pandas", "numpy", "machine learning"]
            if any(skill in candidate_skills for skill in data_skills):
                relevance += 0.3

        return min(1.0, relevance)

    def _apply_bias_mitigation(
        self, base_score: float, candidate_data: Dict, advanced_scores: Dict
    ) -> float:
        """Apply bias mitigation techniques"""
        adjusted_score = base_score

        # Promote diversity in experience levels
        experience = candidate_data.get("experience_years", 0)
        if experience < 2:  # Support entry-level candidates
            adjusted_score += 0.05

        # Education bias mitigation
        education = candidate_data.get("education_level", "").lower()
        if "bachelor" in education:  # Don't penalize bachelor's degree
            adjusted_score += 0.02

        # Skill-focused adjustment
        if advanced_scores.get("technical_depth", 0) > 0.7:
            adjusted_score += 0.03

        return min(1.0, adjusted_score)

    def _generate_reasoning(
        self,
        base_match: Dict,
        advanced_scores: Dict,
        job_title: str,
        candidate_data: Dict,
    ) -> str:
        """Generate detailed reasoning for the match"""
        reasons = []

        # Skill matching
        if base_match["matched_skills"]:
            skills_str = ", ".join(base_match["matched_skills"][:3])
            reasons.append(f"Strong skill match: {skills_str}")

        # Experience relevance
        exp_score = base_match["experience_score"]
        if exp_score > 0.8:
            reasons.append("Excellent experience alignment")
        elif exp_score > 0.6:
            reasons.append("Good experience match")

        # Advanced factors
        if advanced_scores.get("cultural_fit", 0) > 0.7:
            reasons.append("Strong cultural fit")

        if advanced_scores.get("growth_potential", 0) > 0.7:
            reasons.append("High growth potential")

        if advanced_scores.get("technical_depth", 0) > 0.7:
            reasons.append("Deep technical expertise")

        return "; ".join(reasons) if reasons else "Basic qualification match"


class BatchMatcher:
    """Efficient batch processing for multiple job-candidate matches"""

    def __init__(self, max_workers: int = 4):
        self.version = "2.1.0"
        self.max_workers = max_workers
        self.advanced_matcher = AdvancedSemanticMatcher()
        logger.info(
            f"BatchMatcher v{self.version} initialized with {max_workers} workers"
        )

    def batch_match(
        self, jobs: List[Dict], candidates: List[Dict], top_k: int = 10
    ) -> Dict[int, List[Dict]]:
        """Perform batch matching for multiple jobs and candidates"""
        start_time = time.time()
        results = {}

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            # Submit all job-candidate combinations
            futures = {}

            for job in jobs:
                job_id = job.get("id")
                if job_id is None:
                    continue

                job_futures = []
                for candidate in candidates:
                    future = executor.submit(
                        self.advanced_matcher.advanced_match, job, candidate
                    )
                    job_futures.append((future, candidate))

                futures[job_id] = job_futures

            # Collect results
            for job_id, job_futures in futures.items():
                job_results = []

                for future, candidate in job_futures:
                    try:
                        match_result = future.result(timeout=30)
                        match_result["candidate_id"] = candidate.get("id")
                        match_result["candidate_name"] = candidate.get("name")
                        match_result["candidate_email"] = candidate.get("email")
                        job_results.append(match_result)
                    except Exception as e:
                        logger.error(
                            f"Batch match error for candidate {candidate.get('id')}: {e}"
                        )
                        continue

                # Sort by score and take top_k
                job_results.sort(key=lambda x: x["score"], reverse=True)
                results[job_id] = job_results[:top_k]

        processing_time = time.time() - start_time
        logger.info(
            f"Batch matching completed in {processing_time:.2f}s for {len(jobs)} jobs and {len(candidates)} candidates"
        )

        return results

    def batch_match_single_job(
        self, job: Dict, candidates: List[Dict], top_k: int = 10
    ) -> List[Dict]:
        """Optimized batch matching for a single job against multiple candidates"""
        results = []

        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            futures = [
                executor.submit(self.advanced_matcher.advanced_match, job, candidate)
                for candidate in candidates
            ]

            for i, future in enumerate(futures):
                try:
                    match_result = future.result(timeout=30)
                    match_result["candidate_id"] = candidates[i].get("id")
                    match_result["candidate_name"] = candidates[i].get("name")
                    match_result["candidate_email"] = candidates[i].get("email")
                    results.append(match_result)
                except Exception as e:
                    logger.error(f"Single job batch match error: {e}")
                    continue

        # Sort by score and return top_k
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
