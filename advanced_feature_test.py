#!/usr/bin/env python3
"""
Advanced Feature Testing: Test complex endpoints and edge cases
"""

import requests
import json
import time

GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_advanced_endpoint(url, method="GET", data=None, expected_status=200):
    """Test endpoint with detailed response analysis"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=20)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=20)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=20)
        
        # Analyze response content
        content_analysis = {
            "has_json": False,
            "has_data": False,
            "error_message": None,
            "response_keys": []
        }
        
        try:
            json_data = response.json()
            content_analysis["has_json"] = True
            content_analysis["has_data"] = len(json_data) > 0
            content_analysis["response_keys"] = list(json_data.keys()) if isinstance(json_data, dict) else []
            if "error" in json_data:
                content_analysis["error_message"] = json_data.get("error", "Unknown error")
        except:
            pass
        
        return {
            "url": url,
            "method": method,
            "status": response.status_code,
            "success": response.status_code == expected_status,
            "response_size": len(response.text),
            "content_analysis": content_analysis
        }
    except Exception as e:
        return {
            "url": url,
            "method": method,
            "status": "ERROR",
            "success": False,
            "error": str(e)[:150],
            "content_analysis": {"has_json": False, "has_data": False}
        }

def test_complex_workflows():
    """Test complex multi-step workflows"""
    print("Testing Complex Workflows...")
    
    results = []
    
    # Test 1: Complete Job Creation and Matching Workflow
    print("  Testing: Job Creation -> AI Matching Workflow")
    
    # Create a job
    job_data = {
        "title": "Senior Python Developer",
        "department": "Engineering",
        "location": "Remote",
        "experience_level": "Senior",
        "requirements": "Python, Django, React, AWS, 5+ years experience",
        "description": "Senior developer role with Python and cloud experience"
    }
    
    job_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/jobs", "POST", job_data, 200)
    results.append({"feature": "Job Creation Workflow", "result": job_result})
    
    # Test AI matching for the job (assuming job_id 1 exists)
    match_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/match/1/top?limit=5", "GET", None, 200)
    results.append({"feature": "AI Matching Workflow", "result": match_result})
    
    # Test 2: Bulk Candidate Upload
    print("  Testing: Bulk Candidate Upload")
    bulk_data = {
        "candidates": [
            {
                "name": "Test Candidate 1",
                "email": f"test1_{int(time.time())}@example.com",
                "technical_skills": "Python, Django, PostgreSQL",
                "experience_years": 3,
                "location": "Mumbai"
            },
            {
                "name": "Test Candidate 2", 
                "email": f"test2_{int(time.time())}@example.com",
                "technical_skills": "React, Node.js, MongoDB",
                "experience_years": 2,
                "location": "Bangalore"
            }
        ]
    }
    
    bulk_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/candidates/bulk", "POST", bulk_data, 200)
    results.append({"feature": "Bulk Candidate Upload", "result": bulk_result})
    
    # Test 3: Assessment Workflow
    print("  Testing: Assessment Workflow")
    feedback_data = {
        "candidate_id": 1,
        "job_id": 1,
        "integrity": 4,
        "honesty": 5,
        "discipline": 4,
        "hard_work": 5,
        "gratitude": 4,
        "comments": "Strong candidate with good technical skills"
    }
    
    feedback_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/feedback", "POST", feedback_data, 200)
    results.append({"feature": "Values Assessment Workflow", "result": feedback_result})
    
    # Test 4: Interview Scheduling
    print("  Testing: Interview Scheduling")
    interview_data = {
        "candidate_id": 1,
        "job_id": 1,
        "interview_date": "2025-01-15T10:00:00Z",
        "interviewer": "Technical Team Lead",
        "notes": "Technical interview for Python developer role"
    }
    
    interview_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/interviews", "POST", interview_data, 200)
    results.append({"feature": "Interview Scheduling Workflow", "result": interview_result})
    
    return results

def test_advanced_ai_features():
    """Test advanced AI and semantic features"""
    print("Testing Advanced AI Features...")
    
    results = []
    
    # Test 1: Batch AI Matching
    print("  Testing: Batch AI Matching")
    batch_data = {"job_ids": [1, 2, 3]}
    batch_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/match/batch", "POST", batch_data, 200)
    results.append({"feature": "Batch AI Matching", "result": batch_result})
    
    # Test 2: Agent Service Batch Matching
    print("  Testing: Agent Batch Matching")
    agent_batch_result = test_advanced_endpoint(f"{AGENT_URL}/batch-match", "POST", batch_data, 200)
    results.append({"feature": "Agent Batch Matching", "result": agent_batch_result})
    
    # Test 3: Detailed Candidate Analysis
    print("  Testing: Detailed Candidate Analysis")
    analysis_result = test_advanced_endpoint(f"{AGENT_URL}/analyze/1", "GET", None, 200)
    results.append({"feature": "Detailed Candidate Analysis", "result": analysis_result})
    
    # Test 4: Advanced Search with Filters
    print("  Testing: Advanced Candidate Search")
    search_params = "?skills=Python&location=Mumbai&experience_min=2"
    search_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/candidates/search{search_params}", "GET", None, 200)
    results.append({"feature": "Advanced Candidate Search", "result": search_result})
    
    return results

def test_security_features():
    """Test advanced security features"""
    print("Testing Advanced Security Features...")
    
    results = []
    
    # Test 1: Input Validation with XSS
    print("  Testing: XSS Input Validation")
    xss_data = {"input_data": "<script>alert('XSS')</script>"}
    xss_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/security/test-input-validation", "POST", xss_data, 200)
    results.append({"feature": "XSS Input Validation", "result": xss_result})
    
    # Test 2: SQL Injection Test
    print("  Testing: SQL Injection Validation")
    sql_data = {"input_data": "'; DROP TABLE users; --"}
    sql_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/security/test-input-validation", "POST", sql_data, 200)
    results.append({"feature": "SQL Injection Validation", "result": sql_result})
    
    # Test 3: Email Validation
    print("  Testing: Email Validation")
    email_data = {"email": "test@example.com"}
    email_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/security/test-email-validation", "POST", email_data, 200)
    results.append({"feature": "Email Validation", "result": email_result})
    
    # Test 4: Phone Validation
    print("  Testing: Phone Validation")
    phone_data = {"phone": "+1-555-123-4567"}
    phone_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/security/test-phone-validation", "POST", phone_data, 200)
    results.append({"feature": "Phone Validation", "result": phone_result})
    
    # Test 5: CSP Policy Testing
    print("  Testing: CSP Policy Testing")
    csp_data = {"policy": "default-src 'self'; script-src 'self' 'unsafe-inline'"}
    csp_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/security/test-csp-policy", "POST", csp_data, 200)
    results.append({"feature": "CSP Policy Testing", "result": csp_result})
    
    # Test 6: 2FA Token Testing
    print("  Testing: 2FA Token Validation")
    token_result = test_advanced_endpoint(f"{GATEWAY_URL}/v1/2fa/test-token/test_user/123456", "GET", None, 200)
    results.append({"feature": "2FA Token Validation", "result": token_result})
    
    return results

def test_monitoring_features():
    """Test monitoring and metrics features"""
    print("Testing Monitoring Features...")
    
    results = []
    
    # Test 1: Prometheus Metrics
    print("  Testing: Prometheus Metrics Export")
    metrics_result = test_advanced_endpoint(f"{GATEWAY_URL}/metrics", "GET", None, 200)
    results.append({"feature": "Prometheus Metrics Export", "result": metrics_result})
    
    # Test 2: Detailed Health Check
    print("  Testing: Detailed Health Check")
    health_result = test_advanced_endpoint(f"{GATEWAY_URL}/health/detailed", "GET", None, 200)
    results.append({"feature": "Detailed Health Check", "result": health_result})
    
    # Test 3: Metrics Dashboard
    print("  Testing: Metrics Dashboard")
    dashboard_result = test_advanced_endpoint(f"{GATEWAY_URL}/metrics/dashboard", "GET", None, 200)
    results.append({"feature": "Metrics Dashboard", "result": dashboard_result})
    
    # Test 4: Candidate Statistics
    print("  Testing: Candidate Statistics")
    stats_result = test_advanced_endpoint(f"{GATEWAY_URL}/candidates/stats", "GET", None, 200)
    results.append({"feature": "Candidate Statistics", "result": stats_result})
    
    return results

def generate_advanced_report(all_results):
    """Generate detailed analysis report"""
    print("\n" + "=" * 60)
    print("ADVANCED FEATURE ANALYSIS REPORT")
    print("=" * 60)
    
    total_tests = len(all_results)
    successful_tests = [r for r in all_results if r['result']['success']]
    failed_tests = [r for r in all_results if not r['result']['success']]
    
    print(f"\nOVERALL RESULTS:")
    print(f"Total Advanced Features Tested: {total_tests}")
    print(f"Successful: {len(successful_tests)} ({len(successful_tests)/total_tests*100:.1f}%)")
    print(f"Failed: {len(failed_tests)} ({len(failed_tests)/total_tests*100:.1f}%)")
    
    if failed_tests:
        print(f"\nFAILED FEATURES:")
        for test in failed_tests:
            result = test['result']
            print(f"  - {test['feature']}: {result['method']} -> Status: {result['status']}")
            if 'error' in result:
                print(f"    Error: {result['error']}")
            elif result['content_analysis'].get('error_message'):
                print(f"    API Error: {result['content_analysis']['error_message']}")
    
    # Analyze successful features by complexity
    print(f"\nSUCCESSFUL ADVANCED FEATURES:")
    for test in successful_tests:
        result = test['result']
        content = result['content_analysis']
        data_indicator = "✓ Has Data" if content['has_data'] else "✗ No Data"
        json_indicator = "✓ JSON" if content['has_json'] else "✗ No JSON"
        print(f"  ✓ {test['feature']}: {json_indicator}, {data_indicator}")
        if content['response_keys']:
            key_preview = ', '.join(content['response_keys'][:5])
            if len(content['response_keys']) > 5:
                key_preview += "..."
            print(f"    Keys: {key_preview}")
    
    # Feature complexity analysis
    print(f"\nFEATURE COMPLEXITY ANALYSIS:")
    
    workflow_features = [r for r in all_results if 'workflow' in r['feature'].lower()]
    ai_features = [r for r in all_results if any(x in r['feature'].lower() for x in ['ai', 'matching', 'analysis', 'batch'])]
    security_features = [r for r in all_results if any(x in r['feature'].lower() for x in ['security', 'validation', '2fa', 'csp'])]
    monitoring_features = [r for r in all_results if any(x in r['feature'].lower() for x in ['metrics', 'health', 'monitoring', 'stats'])]
    
    categories = {
        'Workflow Features': workflow_features,
        'AI & Matching Features': ai_features,
        'Security Features': security_features,
        'Monitoring Features': monitoring_features
    }
    
    for category, features in categories.items():
        if features:
            successful = [f for f in features if f['result']['success']]
            print(f"  {category}: {len(successful)}/{len(features)} ({len(successful)/len(features)*100:.1f}%)")
    
    return {
        'total_tests': total_tests,
        'successful': len(successful_tests),
        'failed': len(failed_tests),
        'success_rate': len(successful_tests) / total_tests,
        'results': all_results
    }

def main():
    print("BHIV HR Platform - Advanced Feature Analysis")
    print("Testing complex workflows and edge cases")
    print("=" * 60)
    
    all_results = []
    
    # Test complex workflows
    workflow_results = test_complex_workflows()
    all_results.extend(workflow_results)
    
    # Test advanced AI features
    ai_results = test_advanced_ai_features()
    all_results.extend(ai_results)
    
    # Test security features
    security_results = test_security_features()
    all_results.extend(security_results)
    
    # Test monitoring features
    monitoring_results = test_monitoring_features()
    all_results.extend(monitoring_results)
    
    # Generate comprehensive report
    report = generate_advanced_report(all_results)
    
    # Save detailed results
    with open('advanced_feature_analysis.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\nDetailed results saved to: advanced_feature_analysis.json")
    print("=" * 60)

if __name__ == "__main__":
    main()