"""
Client Portal Scoring Explanations
Detailed explanations of AI matching scores for clients
"""

def get_score_explanation(score: float) -> dict:
    """Get detailed explanation for match score"""
    if score >= 90:
        return {
            "level": "Excellent Match",
            "color": "green",
            "explanation": "This candidate is an exceptional fit with strong alignment across all criteria.",
            "recommendation": "Highly recommend proceeding with interview immediately."
        }
    elif score >= 80:
        return {
            "level": "Very Good Match", 
            "color": "lightgreen",
            "explanation": "Strong candidate with good alignment on most key requirements.",
            "recommendation": "Recommend scheduling interview soon."
        }
    elif score >= 70:
        return {
            "level": "Good Match",
            "color": "yellow", 
            "explanation": "Solid candidate with reasonable fit for the role.",
            "recommendation": "Consider for interview with some reservations."
        }
    elif score >= 60:
        return {
            "level": "Fair Match",
            "color": "orange",
            "explanation": "Candidate meets basic requirements but has some gaps.",
            "recommendation": "Review carefully before proceeding."
        }
    else:
        return {
            "level": "Poor Match",
            "color": "red",
            "explanation": "Candidate has significant gaps in key requirements.",
            "recommendation": "Not recommended for this position."
        }

def explain_skills_match(matched_skills: list, missing_skills: list) -> str:
    """Explain skills matching results"""
    if not matched_skills and not missing_skills:
        return "Skills assessment unavailable"
    
    explanation = ""
    if matched_skills:
        explanation += f"✅ Has: {', '.join(matched_skills[:3])}"
        if len(matched_skills) > 3:
            explanation += f" (+{len(matched_skills)-3} more)"
    
    if missing_skills:
        if explanation:
            explanation += " | "
        explanation += f"❌ Missing: {', '.join(missing_skills[:2])}"
        if len(missing_skills) > 2:
            explanation += f" (+{len(missing_skills)-2} more)"
    
    return explanation

def get_experience_explanation(candidate_years: int, required_years: str) -> str:
    """Explain experience matching"""
    if not required_years or required_years == "Any":
        return f"{candidate_years} years experience"
    
    if "entry" in required_years.lower() or "0-2" in required_years:
        target = 1
    elif "mid" in required_years.lower() or "2-5" in required_years:
        target = 3
    elif "senior" in required_years.lower() or "5+" in required_years:
        target = 5
    else:
        return f"{candidate_years} years experience"
    
    if candidate_years >= target:
        return f"✅ {candidate_years} years (meets {required_years})"
    else:
        gap = target - candidate_years
        return f"⚠️ {candidate_years} years ({gap} years below {required_years})"