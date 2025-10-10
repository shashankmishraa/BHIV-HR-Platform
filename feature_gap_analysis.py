#!/usr/bin/env python3
"""
Feature Gap Analysis: Identify features present in code but missing from live services
"""

import requests
import json
import time
from typing import Dict, List, Any

# Service URLs
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def test_endpoint(url: str, method: str = "GET", data: Dict = None, expected_status: int = 200) -> Dict[str, Any]:
    """Test a single endpoint and return results"""
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data, timeout=30)
        elif method == "PUT":
            response = requests.put(url, headers=headers, json=data, timeout=30)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=30)
        
        return {
            "url": url,
            "method": method,
            "status_code": response.status_code,
            "success": response.status_code == expected_status,
            "response_size": len(response.text),
            "has_json": response.headers.get('content-type', '').startswith('application/json'),
            "error": None
        }
    except Exception as e:
        return {
            "url": url,
            "method": method,
            "status_code": None,
            "success": False,
            "response_size": 0,
            "has_json": False,
            "error": str(e)
        }

def analyze_gateway_features():
    """Analyze Gateway service features"""
    print("🔍 ANALYZING GATEWAY SERVICE FEATURES...")
    
    # Core endpoints from code analysis
    gateway_endpoints = [
        # Core API (7 endpoints)
        {"url": f"{GATEWAY_URL}/", "method": "GET", "feature": "API Root Information"},
        {"url": f"{GATEWAY_URL}/health", "method": "GET", "feature": "Health Check"},
        {"url": f"{GATEWAY_URL}/test-candidates", "method": "GET", "feature": "Database Connectivity Test"},
        {"url": f"{GATEWAY_URL}/metrics", "method": "GET", "feature": "Prometheus Metrics Export"},
        {"url": f"{GATEWAY_URL}/health/detailed", "method": "GET", "feature": "Detailed Health Check"},
        {"url": f"{GATEWAY_URL}/metrics/dashboard", "method": "GET", "feature": "Metrics Dashboard"},
        {"url": f"{GATEWAY_URL}/candidates/stats", "method": "GET", "feature": "Candidate Statistics"},
        
        # Job Management (2 endpoints)
        {"url": f"{GATEWAY_URL}/v1/jobs", "method": "GET", "feature": "List Jobs"},
        {"url": f"{GATEWAY_URL}/v1/jobs", "method": "POST", "feature": "Create Job", "data": {
            "title": "Test Job", "department": "Engineering", "location": "Remote",
            "experience_level": "Mid", "requirements": "Python, React", "description": "Test job"
        }},
        
        # Candidate Management (5 endpoints)
        {"url": f"{GATEWAY_URL}/v1/candidates", "method": "GET", "feature": "Get All Candidates"},
        {"url": f"{GATEWAY_URL}/v1/candidates/search", "method": "GET", "feature": "Search Candidates"},
        {"url": f"{GATEWAY_URL}/v1/candidates/1", "method": "GET", "feature": "Get Candidate by ID"},
        {"url": f"{GATEWAY_URL}/v1/candidates/job/1", "method": "GET", "feature": "Get Candidates by Job"},
        {"url": f"{GATEWAY_URL}/v1/candidates/bulk", "method": "POST", "feature": "Bulk Upload Candidates", "data": {
            "candidates": [{"name": "Test User", "email": "test@example.com", "technical_skills": "Python"}]
        }},
        
        # AI Matching (2 endpoints)
        {"url": f"{GATEWAY_URL}/v1/match/1/top", "method": "GET", "feature": "AI Top Matches"},
        {"url": f"{GATEWAY_URL}/v1/match/batch", "method": "POST", "feature": "Batch AI Matching", "data": {"job_ids": [1, 2]}},
        
        # Assessment & Workflow (6 endpoints)
        {"url": f"{GATEWAY_URL}/v1/feedback", "method": "GET", "feature": "Get All Feedback"},
        {"url": f"{GATEWAY_URL}/v1/feedback", "method": "POST", "feature": "Submit Feedback", "data": {
            "candidate_id": 1, "job_id": 1, "integrity": 4, "honesty": 4, "discipline": 4, "hard_work": 4, "gratitude": 4
        }},
        {"url": f"{GATEWAY_URL}/v1/interviews", "method": "GET", "feature": "Get Interviews"},
        {"url": f"{GATEWAY_URL}/v1/interviews", "method": "POST", "feature": "Schedule Interview", "data": {
            "candidate_id": 1, "job_id": 1, "interview_date": "2025-01-15T10:00:00Z"
        }},
        {"url": f"{GATEWAY_URL}/v1/offers", "method": "GET", "feature": "Get Job Offers"},
        {"url": f"{GATEWAY_URL}/v1/offers", "method": "POST", "feature": "Create Job Offer", "data": {
            "candidate_id": 1, "job_id": 1, "salary": 75000, "start_date": "2025-02-01", "terms": "Standard terms"
        }},
        
        # Reports (1 endpoint)
        {"url": f"{GATEWAY_URL}/v1/reports/job/1/export.csv", "method": "GET", "feature": "Export Job Report"},
        
        # Client Portal (1 endpoint)
        {"url": f"{GATEWAY_URL}/v1/client/login", "method": "POST", "feature": "Client Authentication", "data": {
            "client_id": "TECH001", "password": "demo123"
        }},
        
        # Security Testing (7 endpoints)
        {"url": f"{GATEWAY_URL}/v1/security/rate-limit-status", "method": "GET", "feature": "Rate Limit Status"},
        {"url": f"{GATEWAY_URL}/v1/security/blocked-ips", "method": "GET", "feature": "View Blocked IPs"},
        {"url": f"{GATEWAY_URL}/v1/security/test-input-validation", "method": "POST", "feature": "Input Validation Test", "data": {
            "input_data": "<script>alert('test')</script>"
        }},
        {"url": f"{GATEWAY_URL}/v1/security/test-email-validation", "method": "POST", "feature": "Email Validation Test", "data": {
            "email": "test@example.com"
        }},
        {"url": f"{GATEWAY_URL}/v1/security/test-phone-validation", "method": "POST", "feature": "Phone Validation Test", "data": {
            "phone": "+1-555-123-4567"
        }},
        {"url": f"{GATEWAY_URL}/v1/security/security-headers-test", "method": "GET", "feature": "Security Headers Test"},
        {"url": f"{GATEWAY_URL}/v1/security/penetration-test-endpoints", "method": "GET", "feature": "Penetration Test Endpoints"},
        
        # CSP Management (4 endpoints)
        {"url": f"{GATEWAY_URL}/v1/security/csp-report", "method": "POST", "feature": "CSP Violation Reporting", "data": {
            "violated_directive": "script-src", "blocked_uri": "https://malicious.com", "document_uri": "https://app.com"
        }},
        {"url": f"{GATEWAY_URL}/v1/security/csp-violations", "method": "GET", "feature": "View CSP Violations"},
        {"url": f"{GATEWAY_URL}/v1/security/csp-policies", "method": "GET", "feature": "Current CSP Policies"},
        {"url": f"{GATEWAY_URL}/v1/security/test-csp-policy", "method": "POST", "feature": "Test CSP Policy", "data": {
            "policy": "default-src 'self'"
        }},
        
        # Two-Factor Authentication (8 endpoints)
        {"url": f"{GATEWAY_URL}/v1/2fa/setup", "method": "POST", "feature": "Setup 2FA", "data": {"user_id": "test_user"}},
        {"url": f"{GATEWAY_URL}/v1/2fa/verify-setup", "method": "POST", "feature": "Verify 2FA Setup", "data": {"user_id": "test_user", "totp_code": "123456"}},
        {"url": f"{GATEWAY_URL}/v1/2fa/login-with-2fa", "method": "POST", "feature": "Login with 2FA", "data": {"user_id": "test_user", "totp_code": "123456"}},
        {"url": f"{GATEWAY_URL}/v1/2fa/status/test_user", "method": "GET", "feature": "Get 2FA Status"},
        {"url": f"{GATEWAY_URL}/v1/2fa/disable", "method": "POST", "feature": "Disable 2FA", "data": {"user_id": "test_user"}},
        {"url": f"{GATEWAY_URL}/v1/2fa/regenerate-backup-codes", "method": "POST", "feature": "Regenerate Backup Codes", "data": {"user_id": "test_user"}},
        {"url": f"{GATEWAY_URL}/v1/2fa/test-token/test_user/123456", "method": "GET", "feature": "Test 2FA Token"},
        {"url": f"{GATEWAY_URL}/v1/2fa/demo-setup", "method": "GET", "feature": "Demo 2FA Setup"},
        
        # Password Management (6 endpoints)
        {"url": f"{GATEWAY_URL}/v1/password/validate", "method": "POST", "feature": "Validate Password Strength", "data": {"password": "TestPass123!"}},
        {"url": f"{GATEWAY_URL}/v1/password/generate", "method": "POST", "feature": "Generate Secure Password"},
        {"url": f"{GATEWAY_URL}/v1/password/policy", "method": "GET", "feature": "Get Password Policy"},
        {"url": f"{GATEWAY_URL}/v1/password/change", "method": "POST", "feature": "Change Password", "data": {"old_password": "old", "new_password": "new"}},
        {"url": f"{GATEWAY_URL}/v1/password/strength-test", "method": "GET", "feature": "Password Strength Testing Tool"},
        {"url": f"{GATEWAY_URL}/v1/password/security-tips", "method": "GET", "feature": "Password Security Best Practices"},
    ]
    
    results = []
    for endpoint in gateway_endpoints:
        print(f"Testing: {endpoint['feature']}")
        result = test_endpoint(
            endpoint["url"], 
            endpoint["method"], 
            endpoint.get("data"),
            200
        )
        result["feature"] = endpoint["feature"]
        results.append(result)
        time.sleep(0.1)  # Rate limiting
    
    return results

def analyze_agent_features():
    """Analyze Agent service features"""
    print("\n🤖 ANALYZING AGENT SERVICE FEATURES...")
    
    agent_endpoints = [
        # Core API (2 endpoints)
        {"url": f"{AGENT_URL}/", "method": "GET", "feature": "AI Service Information"},
        {"url": f"{AGENT_URL}/health", "method": "GET", "feature": "Health Check"},
        
        # System Diagnostics (1 endpoint)
        {"url": f"{AGENT_URL}/test-db", "method": "GET", "feature": "Database Connectivity Test"},
        
        # AI Processing (3 endpoints)
        {"url": f"{AGENT_URL}/match", "method": "POST", "feature": "AI-Powered Candidate Matching", "data": {"job_id": 1}},
        {"url": f"{AGENT_URL}/batch-match", "method": "POST", "feature": "Batch AI Matching", "data": {"job_ids": [1, 2]}},
        {"url": f"{AGENT_URL}/analyze/1", "method": "GET", "feature": "Detailed Candidate Analysis"},
    ]
    
    results = []
    for endpoint in agent_endpoints:
        print(f"Testing: {endpoint['feature']}")
        result = test_endpoint(
            endpoint["url"], 
            endpoint["method"], 
            endpoint.get("data"),
            200
        )
        result["feature"] = endpoint["feature"]
        results.append(result)
        time.sleep(0.1)
    
    return results

def generate_report(gateway_results: List[Dict], agent_results: List[Dict]):
    """Generate comprehensive feature gap analysis report"""
    
    print("\n" + "="*80)
    print("📊 FEATURE GAP ANALYSIS REPORT")
    print("="*80)
    
    # Gateway Analysis
    print(f"\n🔧 GATEWAY SERVICE ANALYSIS ({len(gateway_results)} features tested)")
    print("-" * 60)
    
    working_features = [r for r in gateway_results if r['success']]
    failing_features = [r for r in gateway_results if not r['success']]
    
    print(f"✅ Working Features: {len(working_features)}/{len(gateway_results)} ({len(working_features)/len(gateway_results)*100:.1f}%)")
    print(f"❌ Missing/Failing Features: {len(failing_features)}/{len(gateway_results)} ({len(failing_features)/len(gateway_results)*100:.1f}%)")
    
    if failing_features:
        print(f"\n❌ MISSING/FAILING GATEWAY FEATURES:")
        for feature in failing_features:
            status = feature['status_code'] if feature['status_code'] else 'CONNECTION_ERROR'
            print(f"   • {feature['feature']} - {feature['method']} - Status: {status}")
            if feature['error']:
                print(f"     Error: {feature['error'][:100]}...")
    
    # Agent Analysis
    print(f"\n🤖 AGENT SERVICE ANALYSIS ({len(agent_results)} features tested)")
    print("-" * 60)
    
    agent_working = [r for r in agent_results if r['success']]
    agent_failing = [r for r in agent_results if not r['success']]
    
    print(f"✅ Working Features: {len(agent_working)}/{len(agent_results)} ({len(agent_working)/len(agent_results)*100:.1f}%)")
    print(f"❌ Missing/Failing Features: {len(agent_failing)}/{len(agent_results)} ({len(agent_failing)/len(agent_results)*100:.1f}%)")
    
    if agent_failing:
        print(f"\n❌ MISSING/FAILING AGENT FEATURES:")
        for feature in agent_failing:
            status = feature['status_code'] if feature['status_code'] else 'CONNECTION_ERROR'
            print(f"   • {feature['feature']} - {feature['method']} - Status: {status}")
            if feature['error']:
                print(f"     Error: {feature['error'][:100]}...")
    
    # Overall Summary
    total_features = len(gateway_results) + len(agent_results)
    total_working = len(working_features) + len(agent_working)
    total_failing = len(failing_features) + len(agent_failing)
    
    print(f"\n📈 OVERALL SYSTEM ANALYSIS")
    print("-" * 60)
    print(f"Total Features Tested: {total_features}")
    print(f"✅ Working Features: {total_working} ({total_working/total_features*100:.1f}%)")
    print(f"❌ Missing/Failing Features: {total_failing} ({total_failing/total_features*100:.1f}%)")
    
    # Feature Categories Analysis
    print(f"\n📋 FEATURE CATEGORIES BREAKDOWN")
    print("-" * 60)
    
    categories = {}
    for result in gateway_results + agent_results:
        # Categorize by feature type
        feature = result['feature']
        if any(x in feature.lower() for x in ['2fa', 'password', 'security', 'csp']):
            category = 'Security & Authentication'
        elif any(x in feature.lower() for x in ['ai', 'match', 'semantic', 'analyze']):
            category = 'AI & Matching'
        elif any(x in feature.lower() for x in ['candidate', 'job', 'feedback', 'interview', 'offer']):
            category = 'Core HR Functions'
        elif any(x in feature.lower() for x in ['health', 'metrics', 'test', 'diagnostic']):
            category = 'Monitoring & Diagnostics'
        else:
            category = 'Other'
        
        if category not in categories:
            categories[category] = {'total': 0, 'working': 0}
        
        categories[category]['total'] += 1
        if result['success']:
            categories[category]['working'] += 1
    
    for category, stats in categories.items():
        percentage = (stats['working'] / stats['total']) * 100
        print(f"{category}: {stats['working']}/{stats['total']} ({percentage:.1f}%)")
    
    # Key Findings
    print(f"\n🔍 KEY FINDINGS")
    print("-" * 60)
    
    if total_working / total_features > 0.9:
        print("✅ EXCELLENT: Most features are working as expected")
    elif total_working / total_features > 0.8:
        print("✅ GOOD: Majority of features are functional")
    elif total_working / total_features > 0.7:
        print("⚠️  MODERATE: Some features need attention")
    else:
        print("❌ CRITICAL: Many features are not working")
    
    # Recommendations
    print(f"\n💡 RECOMMENDATIONS")
    print("-" * 60)
    
    if failing_features or agent_failing:
        print("1. Investigate failing endpoints for implementation gaps")
        print("2. Check service configurations and dependencies")
        print("3. Verify database connectivity and schema")
        print("4. Review authentication and authorization setup")
    else:
        print("1. All tested features appear to be working correctly")
        print("2. Consider adding more comprehensive integration tests")
        print("3. Monitor performance and error rates in production")
    
    return {
        'gateway_results': gateway_results,
        'agent_results': agent_results,
        'total_features': total_features,
        'total_working': total_working,
        'total_failing': total_failing,
        'success_rate': total_working / total_features
    }

def main():
    """Main analysis function"""
    print("🚀 BHIV HR Platform - Feature Gap Analysis")
    print("Comparing code features vs live service functionality")
    print("=" * 80)
    
    # Test Gateway features
    gateway_results = analyze_gateway_features()
    
    # Test Agent features  
    agent_results = analyze_agent_features()
    
    # Generate comprehensive report
    report = generate_report(gateway_results, agent_results)
    
    # Save detailed results
    with open('feature_gap_analysis_results.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    print(f"\n💾 Detailed results saved to: feature_gap_analysis_results.json")
    print("=" * 80)

if __name__ == "__main__":
    main()