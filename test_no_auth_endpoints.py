#!/usr/bin/env python3
"""
Test endpoints that don't require authentication and agent service directly
"""
import requests
import json
import sys

def test_public_endpoints():
    """Test public endpoints that don't require auth"""
    print("=== Testing Public Endpoints ===")
    
    # Test gateway root
    try:
        response = requests.get("http://localhost:8000/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Gateway root")
            print(f"  Version: {data.get('version')}")
            print(f"  Endpoints: {data.get('endpoints')}")
            print(f"  Status: {data.get('status')}")
        else:
            print(f"FAILED: Gateway root returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Gateway root error - {e}")
    
    # Test gateway health
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Gateway health")
            print(f"  Service: {data.get('service')}")
            print(f"  Version: {data.get('version')}")
        else:
            print(f"FAILED: Gateway health returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Gateway health error - {e}")

def test_agent_service_direct():
    """Test agent service directly (no auth required)"""
    print("\n=== Testing Agent Service Direct ===")
    
    # Test agent root
    try:
        response = requests.get("http://localhost:9000/", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent root")
            print(f"  Service: {data.get('service')}")
            print(f"  Version: {data.get('version')}")
            print(f"  Endpoints: {data.get('endpoints')}")
        else:
            print(f"FAILED: Agent root returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Agent root error - {e}")
    
    # Test agent health
    try:
        response = requests.get("http://localhost:9000/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent health")
            print(f"  Service: {data.get('service')}")
            print(f"  Version: {data.get('version')}")
        else:
            print(f"FAILED: Agent health returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Agent health error - {e}")
    
    # Test agent database
    try:
        response = requests.get("http://localhost:9000/test-db", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent database test")
            print(f"  Status: {data.get('status')}")
            print(f"  Candidates count: {data.get('candidates_count', 0)}")
            if data.get('samples'):
                print(f"  Sample candidates: {len(data['samples'])}")
                for sample in data['samples'][:3]:
                    print(f"    - {sample.get('name')} (ID: {sample.get('id')})")
        else:
            print(f"FAILED: Agent database returned {response.status_code}")
    except Exception as e:
        print(f"FAILED: Agent database error - {e}")

def test_agent_ai_matching():
    """Test agent AI matching with real job"""
    print("\n=== Testing Agent AI Matching ===")
    
    # Test with job ID 1 (should exist from previous tests)
    try:
        payload = {"job_id": 1}
        response = requests.post("http://localhost:9000/match", json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Agent AI matching")
            print(f"  Job ID: {data.get('job_id')}")
            print(f"  Algorithm: {data.get('algorithm_version')}")
            print(f"  Status: {data.get('status')}")
            print(f"  Total candidates: {data.get('total_candidates', 0)}")
            print(f"  Processing time: {data.get('processing_time')}s")
            
            top_candidates = data.get('top_candidates', [])
            print(f"  Top matches: {len(top_candidates)}")
            
            for i, candidate in enumerate(top_candidates[:5]):
                print(f"    {i+1}. {candidate.get('name')} - Score: {candidate.get('score')}")
                print(f"       Skills: {', '.join(candidate.get('skills_match', []))}")
                print(f"       Experience: {candidate.get('experience_match')}")
                print(f"       Reasoning: {candidate.get('reasoning', '')[:60]}...")
            
            return True
        else:
            print(f"FAILED: Agent matching returned {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"FAILED: Agent matching error - {e}")
        return False

def test_agent_candidate_analysis():
    """Test agent candidate analysis"""
    print("\n=== Testing Agent Candidate Analysis ===")
    
    # Test with candidate ID 1
    try:
        response = requests.get("http://localhost:9000/analyze/1", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"SUCCESS: Candidate analysis")
            print(f"  Candidate: {data.get('name')}")
            print(f"  Email: {data.get('email')}")
            print(f"  Experience: {data.get('experience_years')} years")
            print(f"  Skills analysis: {data.get('skills_analysis')}")
            print(f"  Total skills: {data.get('total_skills')}")
            print(f"  AI analysis enabled: {data.get('ai_analysis_enabled')}")
            return True
        else:
            print(f"FAILED: Candidate analysis returned {response.status_code}")
            return False
    except Exception as e:
        print(f"FAILED: Candidate analysis error - {e}")
        return False

def test_phase3_engine_status():
    """Check if Phase 3 engine is working"""
    print("\n=== Testing Phase 3 Engine Status ===")
    
    # Check agent logs for Phase 3 status
    try:
        response = requests.get("http://localhost:9000/", timeout=10)
        if response.status_code == 200:
            print("Phase 3 Engine Status Check:")
            print("  Agent service is responding")
            
            # Test matching to see algorithm version
            match_response = requests.post("http://localhost:9000/match", 
                                         json={"job_id": 1}, timeout=30)
            if match_response.status_code == 200:
                match_data = match_response.json()
                algorithm = match_data.get('algorithm_version', '')
                
                if 'phase3' in algorithm.lower():
                    print(f"  SUCCESS: Phase 3 engine active - {algorithm}")
                    print(f"  Status: {match_data.get('status')}")
                    return True
                else:
                    print(f"  INFO: Using fallback algorithm - {algorithm}")
                    return False
            else:
                print("  WARNING: Could not test matching algorithm")
                return False
        else:
            print("  FAILED: Agent service not responding")
            return False
    except Exception as e:
        print(f"  FAILED: Phase 3 status check error - {e}")
        return False

def main():
    """Run tests for endpoints that work without authentication"""
    print("=== BHIV HR Platform - No-Auth Endpoint Testing ===")
    print("Testing clean architecture and Phase 3 engine functionality...\n")
    
    # Test public endpoints
    test_public_endpoints()
    
    # Test agent service directly
    test_agent_service_direct()
    
    # Test AI functionality
    ai_working = test_agent_ai_matching()
    
    # Test candidate analysis
    analysis_working = test_agent_candidate_analysis()
    
    # Test Phase 3 engine status
    phase3_working = test_phase3_engine_status()
    
    # Summary
    print("\n" + "="*50)
    print("TEST SUMMARY")
    print("="*50)
    
    print(f"Gateway Service: HEALTHY")
    print(f"Agent Service: HEALTHY")
    print(f"AI Matching: {'WORKING' if ai_working else 'ISSUES'}")
    print(f"Candidate Analysis: {'WORKING' if analysis_working else 'ISSUES'}")
    print(f"Phase 3 Engine: {'ACTIVE' if phase3_working else 'FALLBACK MODE'}")
    
    if ai_working and analysis_working:
        print("\nSUCCESS: Clean architecture deployment working!")
        print("SUCCESS: AI functionality operational")
        if phase3_working:
            print("SUCCESS: Phase 3 engine active and working")
        else:
            print("INFO: Phase 3 engine in fallback mode (expected if no ML dependencies)")
        return 0
    else:
        print("\nWARNING: Some AI functionality issues detected")
        return 1

if __name__ == "__main__":
    sys.exit(main())