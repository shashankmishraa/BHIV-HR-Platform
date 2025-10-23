#!/usr/bin/env python3
"""
Live Portal Functionality Testing
Tests actual portal functionality and content through direct interaction
"""

import requests
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

PORTALS = {
    "HR Portal": "https://bhiv-hr-portal-cead.onrender.com",
    "Client Portal": "https://bhiv-hr-client-portal-5g33.onrender.com", 
    "Candidate Portal": "https://bhiv-hr-candidate-portal.onrender.com"
}

def test_portal_accessibility_and_content(portal_name, url):
    """Test portal accessibility and extract meaningful content"""
    logger.info(f"=== TESTING {portal_name.upper()} LIVE FUNCTIONALITY ===")
    
    try:
        # Test basic accessibility
        response = requests.get(url, timeout=45)
        if response.status_code == 200:
            logger.info(f"✅ {portal_name} is accessible (Status: {response.status_code})")
            
            # Check response size and content type
            content_size = len(response.content)
            content_type = response.headers.get('content-type', 'unknown')
            
            logger.info(f"📊 Content size: {content_size} bytes")
            logger.info(f"📊 Content type: {content_type}")
            
            # Check for Streamlit indicators
            content_text = response.text.lower()
            
            streamlit_indicators = [
                "streamlit", "st-", "stApp", "tornado", "bokeh", "altair"
            ]
            
            found_indicators = []
            for indicator in streamlit_indicators:
                if indicator in content_text:
                    found_indicators.append(indicator)
            
            if found_indicators:
                logger.info(f"✅ Streamlit framework detected: {found_indicators}")
            else:
                logger.warning(f"⚠️ No clear Streamlit indicators found")
            
            # Check for portal-specific content
            if "hr" in portal_name.lower():
                hr_content = ["candidate", "job", "interview", "assessment", "dashboard"]
                found_content = [c for c in hr_content if c in content_text]
                if found_content:
                    logger.info(f"✅ HR-specific content found: {found_content}")
                    
            elif "client" in portal_name.lower():
                client_content = ["login", "client", "company", "hiring", "analytics"]
                found_content = [c for c in client_content if c in content_text]
                if found_content:
                    logger.info(f"✅ Client-specific content found: {found_content}")
                    
            elif "candidate" in portal_name.lower():
                candidate_content = ["job", "application", "profile", "search", "career"]
                found_content = [c for c in candidate_content if c in content_text]
                if found_content:
                    logger.info(f"✅ Candidate-specific content found: {found_content}")
            
            return True
            
        else:
            logger.error(f"❌ {portal_name} returned HTTP {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        logger.error(f"❌ {portal_name} timed out (45 seconds)")
        return False
    except Exception as e:
        logger.error(f"❌ {portal_name} error: {e}")
        return False

def test_backend_data_integration():
    """Test backend data that portals display"""
    logger.info("=== TESTING BACKEND DATA INTEGRATION ===")
    
    data_tests = [
        ("Candidates Data", "/v1/candidates", "candidates available for HR Portal"),
        ("Jobs Data", "/v1/jobs", "jobs available for Client Portal"),
        ("Interview Data", "/v1/interviews", "interviews for scheduling"),
        ("Client Data", "/v1/database/schema", "database schema for analytics"),
        ("Statistics", "/candidates/stats", "statistics for dashboards")
    ]
    
    backend_data = {}
    
    for test_name, endpoint, description in data_tests:
        try:
            response = requests.get(f"{GATEWAY_URL}{endpoint}", headers=HEADERS, timeout=15)
            if response.status_code == 200:
                data = response.json()
                
                if endpoint == "/v1/candidates":
                    count = len(data) if isinstance(data, list) else data.get('count', 0)
                    backend_data['candidates'] = count
                    logger.info(f"✅ {test_name}: {count} {description}")
                    
                elif endpoint == "/v1/jobs":
                    jobs = data.get('jobs', []) if isinstance(data, dict) else data
                    count = len(jobs)
                    backend_data['jobs'] = count
                    logger.info(f"✅ {test_name}: {count} {description}")
                    
                elif endpoint == "/v1/interviews":
                    interviews = data.get('interviews', [])
                    count = len(interviews)
                    backend_data['interviews'] = count
                    logger.info(f"✅ {test_name}: {count} {description}")
                    
                elif endpoint == "/v1/database/schema":
                    tables = data.get('total_tables', 0)
                    schema_version = data.get('schema_version', 'unknown')
                    backend_data['schema'] = f"v{schema_version} ({tables} tables)"
                    logger.info(f"✅ {test_name}: Schema {schema_version} with {tables} tables")
                    
                elif endpoint == "/candidates/stats":
                    backend_data['stats'] = "available"
                    logger.info(f"✅ {test_name}: Statistics data available")
                    
            else:
                logger.warning(f"⚠️ {test_name}: HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"❌ {test_name}: {e}")
    
    return backend_data

def test_portal_specific_functionality():
    """Test portal-specific functionality through API"""
    logger.info("=== TESTING PORTAL-SPECIFIC FUNCTIONALITY ===")
    
    functionality_results = {}
    
    # HR Portal functionality
    logger.info("--- HR Portal Functionality ---")
    hr_functions = []
    
    # Test job creation (HR Portal feature)
    try:
        job_data = {
            "title": "Visual Test Job",
            "department": "Testing",
            "location": "Remote",
            "experience_level": "Mid",
            "requirements": "Visual testing requirements",
            "description": "Job created for visual portal testing",
            "client_id": 1,
            "employment_type": "Full-time"
        }
        
        response = requests.post(f"{GATEWAY_URL}/v1/jobs", json=job_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            hr_functions.append("Job Creation")
            logger.info("✅ HR Portal: Job creation functionality working")
        else:
            logger.warning(f"⚠️ HR Portal: Job creation returned {response.status_code}")
            
    except Exception as e:
        logger.error(f"❌ HR Portal job creation: {e}")
    
    # Test candidate search (HR Portal feature)
    try:
        response = requests.get(f"{GATEWAY_URL}/v1/candidates/search", 
                              params={"job_id": 1}, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            hr_functions.append("Candidate Search")
            logger.info("✅ HR Portal: Candidate search functionality working")
    except Exception as e:
        logger.error(f"❌ HR Portal candidate search: {e}")
    
    functionality_results['HR Portal'] = hr_functions
    
    # Client Portal functionality
    logger.info("--- Client Portal Functionality ---")
    client_functions = []
    
    # Test client authentication
    try:
        login_data = {"client_id": "TECH001", "password": "demo123"}
        response = requests.post(f"{GATEWAY_URL}/v1/client/login", 
                               json=login_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            client_functions.append("Client Authentication")
            logger.info("✅ Client Portal: Authentication functionality working")
    except Exception as e:
        logger.error(f"❌ Client Portal authentication: {e}")
    
    # Test offer management
    try:
        offer_data = {
            "candidate_id": 1,
            "job_id": 1,
            "salary": 80000.00,
            "start_date": "2025-11-15",
            "terms": "Visual test offer terms"
        }
        response = requests.post(f"{GATEWAY_URL}/v1/offers", 
                               json=offer_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            client_functions.append("Offer Management")
            logger.info("✅ Client Portal: Offer management functionality working")
    except Exception as e:
        logger.error(f"❌ Client Portal offer management: {e}")
    
    functionality_results['Client Portal'] = client_functions
    
    # Candidate Portal functionality
    logger.info("--- Candidate Portal Functionality ---")
    candidate_functions = []
    
    # Test candidate registration
    try:
        reg_data = {
            "name": "Visual Test Candidate",
            "email": "visual.test@example.com",
            "phone": "+1-555-0177",
            "location": "Remote",
            "experience_years": 3,
            "technical_skills": "Visual Testing, QA",
            "education_level": "Bachelors"
        }
        response = requests.post(f"{GATEWAY_URL}/v1/candidate/register", 
                               json=reg_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            candidate_functions.append("Candidate Registration")
            logger.info("✅ Candidate Portal: Registration functionality working")
    except Exception as e:
        logger.error(f"❌ Candidate Portal registration: {e}")
    
    # Test job application
    try:
        app_data = {
            "candidate_id": 1,
            "job_id": 1,
            "cover_letter": "Visual test application",
            "status": "applied"
        }
        response = requests.post(f"{GATEWAY_URL}/v1/candidate/apply", 
                               json=app_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            candidate_functions.append("Job Application")
            logger.info("✅ Candidate Portal: Job application functionality working")
    except Exception as e:
        logger.error(f"❌ Candidate Portal job application: {e}")
    
    functionality_results['Candidate Portal'] = candidate_functions
    
    return functionality_results

def test_bhiv_values_integration():
    """Test BHIV values integration in the system"""
    logger.info("=== TESTING BHIV VALUES INTEGRATION ===")
    
    # Test values assessment functionality
    values_data = {
        "candidate_id": 1,
        "job_id": 1,
        "integrity": 5,
        "honesty": 4,
        "discipline": 5,
        "hard_work": 4,
        "gratitude": 5,
        "comments": "Visual test - BHIV values assessment with Integrity, Honesty, Discipline, Hard Work, and Gratitude",
        "reviewer_name": "Visual Test Reviewer"
    }
    
    try:
        response = requests.post(f"{GATEWAY_URL}/v1/feedback", 
                               json=values_data, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            logger.info("✅ BHIV Values: Assessment system working")
            logger.info("✅ Values tested: Integrity, Honesty, Discipline, Hard Work, Gratitude")
            
            # Test retrieving feedback
            response = requests.get(f"{GATEWAY_URL}/v1/feedback", headers=HEADERS, timeout=15)
            if response.status_code == 200:
                feedback_data = response.json()
                feedback_list = feedback_data.get('feedback', [])
                logger.info(f"✅ BHIV Values: {len(feedback_list)} assessments in system")
                return True
        else:
            logger.error(f"❌ BHIV Values assessment: HTTP {response.status_code}")
            return False
            
    except Exception as e:
        logger.error(f"❌ BHIV Values integration: {e}")
        return False

def generate_live_functionality_report(portal_results, backend_data, functionality_results, values_result):
    """Generate comprehensive live functionality report"""
    logger.info("=== GENERATING LIVE FUNCTIONALITY REPORT ===")
    
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "portal_accessibility": portal_results,
        "backend_data": backend_data,
        "portal_functionality": functionality_results,
        "bhiv_values_integration": values_result,
        "summary": {}
    }
    
    # Calculate scores
    accessible_portals = sum(1 for result in portal_results.values() if result)
    total_functions = sum(len(functions) for functions in functionality_results.values())
    
    report["summary"] = {
        "accessible_portals": f"{accessible_portals}/{len(PORTALS)}",
        "backend_data_sources": len(backend_data),
        "total_functions_tested": total_functions,
        "bhiv_values_working": values_result,
        "overall_status": "OPERATIONAL" if accessible_portals == len(PORTALS) and values_result else "PARTIAL"
    }
    
    # Save report
    with open('live_functionality_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    logger.info(f"Live Functionality Report saved")
    return report

def main():
    """Main live functionality testing"""
    logger.info("🔴 Starting Live Portal Functionality Testing...")
    
    # Test portal accessibility
    portal_results = {}
    for portal_name, url in PORTALS.items():
        portal_results[portal_name] = test_portal_accessibility_and_content(portal_name, url)
        time.sleep(3)  # Avoid overwhelming servers
    
    # Test backend data integration
    backend_data = test_backend_data_integration()
    
    # Test portal-specific functionality
    functionality_results = test_portal_specific_functionality()
    
    # Test BHIV values integration
    values_result = test_bhiv_values_integration()
    
    # Generate report
    report = generate_live_functionality_report(portal_results, backend_data, functionality_results, values_result)
    
    # Final summary
    logger.info(f"\n🎯 LIVE FUNCTIONALITY TESTING COMPLETE")
    logger.info(f"Portal Accessibility: {report['summary']['accessible_portals']}")
    logger.info(f"Backend Data Sources: {report['summary']['backend_data_sources']}")
    logger.info(f"Functions Tested: {report['summary']['total_functions_tested']}")
    logger.info(f"BHIV Values: {'✅ Working' if values_result else '❌ Issues'}")
    logger.info(f"Overall Status: {report['summary']['overall_status']}")
    
    # Portal-specific summary
    for portal_name, accessible in portal_results.items():
        functions = functionality_results.get(portal_name, [])
        status = "✅" if accessible else "❌"
        logger.info(f"{status} {portal_name}: {'Accessible' if accessible else 'Issues'} - {len(functions)} functions working")

if __name__ == "__main__":
    main()