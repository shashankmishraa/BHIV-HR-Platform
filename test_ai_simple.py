#!/usr/bin/env python3
"""
Simple Test for Advanced AI Matching System
"""

import requests
import json

def test_ai_matching():
    """Test the AI matching system"""
    
    api_base = "https://bhiv-hr-gateway.onrender.com"
    headers = {"Authorization": "Bearer myverysecureapikey123"}
    
    print("TESTING ADVANCED AI MATCHING SYSTEM")
    print("=" * 50)
    
    response = requests.get(f"{api_base}/v1/match/1/top?limit=5", headers=headers, timeout=15)
    
    if response.status_code == 200:
        data = response.json()
        
        print(f"Algorithm Version: {data.get('algorithm_version', 'Unknown')}")
        print(f"Processing Time: {data.get('processing_time', 'N/A')}")
        print(f"AI Analysis: {data.get('ai_analysis', 'N/A')}")
        
        matches = data.get('matches', [])
        print(f"Candidates Returned: {len(matches)}")
        
        if matches:
            print("\nCANDIDATE SCORES:")
            scores = []
            for i, candidate in enumerate(matches, 1):
                score = candidate.get('score', 0)
                scores.append(score)
                print(f"  {i}. {candidate.get('name', 'Unknown')}: {score}")
            
            # Check score differentiation
            unique_scores = len(set(scores))
            score_range = max(scores) - min(scores) if scores else 0
            
            print(f"\nSCORE ANALYSIS:")
            print(f"  Unique Scores: {unique_scores}")
            print(f"  Score Range: {score_range:.1f}")
            print(f"  All Scores: {scores}")
            
            if unique_scores > 1 and score_range > 3:
                print("  SUCCESS: Scores are differentiated!")
                return True
            else:
                print("  ISSUE: Scores are still too similar")
                return False
        
        # Check for advanced features
        advanced_features = 0
        if 'job_context' in data:
            advanced_features += 1
            print("FOUND: Job Context")
        if 'matching_statistics' in data:
            advanced_features += 1
            print("FOUND: Matching Statistics")
        if 'recruiter_insights' in data:
            advanced_features += 1
            print("FOUND: Recruiter Insights")
        if 'advanced_analytics' in data:
            advanced_features += 1
            print("FOUND: Advanced Analytics")
        if 'portal_integration' in data:
            advanced_features += 1
            print("FOUND: Portal Integration")
        
        print(f"Advanced Features Found: {advanced_features}/5")
        
        return advanced_features >= 3
    else:
        print(f"ERROR: HTTP {response.status_code}")
        print(f"Response: {response.text}")
        return False

if __name__ == "__main__":
    success = test_ai_matching()
    
    print("\n" + "=" * 50)
    if success:
        print("TEST RESULT: SUCCESS - Advanced AI matching is working!")
    else:
        print("TEST RESULT: NEEDS ATTENTION - Waiting for deployment...")
    
    print("\nExpected Features:")
    print("- Job-specific matching")
    print("- Differentiated scoring")
    print("- Recruiter preferences")
    print("- Reviewer feedback integration")
    print("- Advanced analytics")
    print("- Portal integration")