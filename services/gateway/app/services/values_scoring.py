"""
Values scoring and integration service
"""
import json
from typing import Dict, Optional, List
from datetime import datetime, timezone

class ValuesScoring:
    """Service for handling values assessment and scoring"""
    
    CORE_VALUES = {
        "integrity": "Moral uprightness and ethical behavior",
        "honesty": "Truthfulness and transparency",
        "discipline": "Self-control and consistency", 
        "hard_work": "Dedication and perseverance",
        "gratitude": "Appreciation and humility"
    }
    
    @staticmethod
    def validate_values_scores(scores: Dict[str, float]) -> Dict[str, float]:
        """Validate and normalize values scores"""
        validated_scores = {}
        
        for value in ValuesScoring.CORE_VALUES.keys():
            score = scores.get(value, 3.0)
            # Ensure score is between 1 and 5
            validated_scores[value] = max(1.0, min(5.0, float(score)))
        
        return validated_scores
    
    @staticmethod
    def calculate_values_average(scores: Dict[str, float]) -> float:
        """Calculate average values score"""
        if not scores:
            return 0.0
        
        valid_scores = [score for score in scores.values() if isinstance(score, (int, float))]
        if not valid_scores:
            return 0.0
        
        return round(sum(valid_scores) / len(valid_scores), 2)
    
    @staticmethod
    def get_recommendation(avg_score: float) -> str:
        """Get hiring recommendation based on values average"""
        if avg_score >= 4.5:
            return "Strongly Recommend"
        elif avg_score >= 4.0:
            return "Recommend"
        elif avg_score >= 3.0:
            return "Neutral"
        elif avg_score >= 2.0:
            return "Do Not Recommend"
        else:
            return "Strongly Do Not Recommend"
    
    @staticmethod
    def get_values_insights(scores: Dict[str, float]) -> List[str]:
        """Generate insights based on values scores"""
        insights = []
        avg_score = ValuesScoring.calculate_values_average(scores)
        
        # Overall assessment
        if avg_score >= 4.0:
            insights.append("Strong cultural fit with excellent values alignment")
        elif avg_score >= 3.5:
            insights.append("Good cultural fit with solid values foundation")
        elif avg_score >= 3.0:
            insights.append("Moderate cultural fit, may need values development")
        else:
            insights.append("Cultural fit concerns, significant values gap identified")
        
        # Individual value insights
        high_values = [k for k, v in scores.items() if v >= 4.5]
        low_values = [k for k, v in scores.items() if v <= 2.5]
        
        if high_values:
            insights.append(f"Exceptional strength in: {', '.join(high_values).title()}")
        
        if low_values:
            insights.append(f"Development needed in: {', '.join(low_values).title()}")
        
        return insights
    
    @staticmethod
    def create_values_profile(scores: Dict[str, float], feedback_text: str = "") -> Dict:
        """Create comprehensive values profile"""
        validated_scores = ValuesScoring.validate_values_scores(scores)
        avg_score = ValuesScoring.calculate_values_average(validated_scores)
        recommendation = ValuesScoring.get_recommendation(avg_score)
        insights = ValuesScoring.get_values_insights(validated_scores)
        
        return {
            "values_scores": validated_scores,
            "values_average": avg_score,
            "recommendation": recommendation,
            "insights": insights,
            "feedback_text": feedback_text[:1000] if feedback_text else "",
            "assessment_date": datetime.now(timezone.utc).isoformat(),
            "cultural_fit_level": ValuesScoring._get_fit_level(avg_score)
        }
    
    @staticmethod
    def _get_fit_level(avg_score: float) -> str:
        """Get cultural fit level description"""
        if avg_score >= 4.5:
            return "Excellent"
        elif avg_score >= 4.0:
            return "Very Good"
        elif avg_score >= 3.5:
            return "Good"
        elif avg_score >= 3.0:
            return "Fair"
        elif avg_score >= 2.5:
            return "Poor"
        else:
            return "Very Poor"
    
    @staticmethod
    def integrate_values_in_matching(candidate_data: Dict, values_weight: float = 0.3) -> Dict:
        """Integrate values scores into AI matching algorithm"""
        if not candidate_data.get("values_prediction"):
            return candidate_data
        
        try:
            values_scores = json.loads(candidate_data["values_prediction"])
            values_avg = ValuesScoring.calculate_values_average(values_scores)
            
            # Adjust AI score based on values
            current_ai_score = candidate_data.get("ai_score", 0.0)
            values_bonus = (values_avg - 3.0) * 10 * values_weight  # Scale values impact
            
            candidate_data["ai_score"] = max(0, min(100, current_ai_score + values_bonus))
            candidate_data["values_average"] = values_avg
            candidate_data["cultural_fit"] = ValuesScoring._get_fit_level(values_avg)
            
        except (json.JSONDecodeError, KeyError, TypeError):
            pass
        
        return candidate_data