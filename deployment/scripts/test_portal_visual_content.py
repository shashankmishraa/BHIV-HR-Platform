#!/usr/bin/env python3
"""
Portal Visual Content Testing
Tests unique content, BHIV values, and dynamic functionality of portal websites
"""

import requests
import re
import json
import logging
from bs4 import BeautifulSoup
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

PORTALS = {
    "HR Portal": "https://bhiv-hr-portal-cead.onrender.com",
    "Client Portal": "https://bhiv-hr-client-portal-5g33.onrender.com", 
    "Candidate Portal": "https://bhiv-hr-candidate-portal.onrender.com"
}

BHIV_VALUES = ["integrity", "honesty", "discipline", "hard work", "gratitude"]

def get_portal_content(portal_name, url):
    """Get portal content and parse HTML"""
    logger.info(f"=== ANALYZING {portal_name.upper()} CONTENT ===")
    
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            logger.info(f"✅ {portal_name} accessible (Status: {response.status_code})")
            
            # Parse HTML content
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text().lower()
            
            return {
                "status": "accessible",
                "html": response.text,
                "text": text_content,
                "soup": soup,
                "size": len(response.text)
            }
        else:
            logger.error(f"❌ {portal_name} HTTP {response.status_code}")
            return {"status": "error", "code": response.status_code}
            
    except Exception as e:
        logger.error(f"❌ {portal_name} error: {e}")
        return {"status": "error", "error": str(e)}

def test_bhiv_values_presence(portal_name, content):
    """Test presence of BHIV values in portal content"""
    logger.info(f"--- Testing BHIV Values in {portal_name} ---")
    
    if content["status"] != "accessible":
        return False
    
    text = content["text"]
    values_found = []
    
    for value in BHIV_VALUES:
        if value in text:
            values_found.append(value)
            logger.info(f"✅ Found '{value}' in {portal_name}")
        else:
            logger.warning(f"⚠️ '{value}' not found in {portal_name}")
    
    # Check for BHIV acronym or company name
    bhiv_mentions = text.count("bhiv")
    if bhiv_mentions > 0:
        logger.info(f"✅ 'BHIV' mentioned {bhiv_mentions} times in {portal_name}")
        
    logger.info(f"Values Summary: {len(values_found)}/5 BHIV values found in {portal_name}")
    return len(values_found) >= 3  # At least 3 values should be present

def test_unique_portal_content(portal_name, content):
    """Test unique content specific to each portal"""
    logger.info(f"--- Testing Unique Content in {portal_name} ---")
    
    if content["status"] != "accessible":
        return False
    
    text = content["text"]
    unique_content_found = []
    
    if "HR Portal" in portal_name:
        hr_keywords = [
            "candidate", "interview", "assessment", "recruitment", "hiring",
            "dashboard", "job posting", "values assessment", "shortlist"
        ]
        for keyword in hr_keywords:
            if keyword in text:
                unique_content_found.append(keyword)
                logger.info(f"✅ HR-specific content: '{keyword}' found")
                
    elif "Client Portal" in portal_name:
        client_keywords = [
            "client", "company", "job posting", "candidate review", 
            "interview scheduling", "hiring pipeline", "analytics"
        ]
        for keyword in client_keywords:
            if keyword in text:
                unique_content_found.append(keyword)
                logger.info(f"✅ Client-specific content: '{keyword}' found")
                
    elif "Candidate Portal" in portal_name:
        candidate_keywords = [
            "job search", "application", "profile", "career", "apply",
            "job seeker", "opportunities", "skills"
        ]
        for keyword in candidate_keywords:
            if keyword in text:
                unique_content_found.append(keyword)
                logger.info(f"✅ Candidate-specific content: '{keyword}' found")
    
    logger.info(f"Unique Content: {len(unique_content_found)} specific keywords found")
    return len(unique_content_found) >= 3

def test_streamlit_components(portal_name, content):
    """Test Streamlit-specific components and functionality"""
    logger.info(f"--- Testing Streamlit Components in {portal_name} ---")
    
    if content["status"] != "accessible":
        return False
    
    html = content["html"]
    components_found = []
    
    # Check for Streamlit-specific elements
    streamlit_indicators = [
        "streamlit", "st-", "data-testid", "stApp", "stSidebar",
        "stSelectbox", "stButton", "stTextInput", "stDataFrame"
    ]
    
    for indicator in streamlit_indicators:
        if indicator in html:
            components_found.append(indicator)
            logger.info(f"✅ Streamlit component: '{indicator}' detected")
    
    # Check for interactive elements
    interactive_elements = ["button", "input", "select", "form", "sidebar"]
    interactive_found = []
    
    for element in interactive_elements:
        if element in html.lower():
            interactive_found.append(element)
    
    logger.info(f"Streamlit Components: {len(components_found)} detected")
    logger.info(f"Interactive Elements: {len(interactive_found)} found")
    
    return len(components_found) >= 2 and len(interactive_found) >= 2

def test_dynamic_content(portal_name, content):
    """Test dynamic content and data integration"""
    logger.info(f"--- Testing Dynamic Content in {portal_name} ---")
    
    if content["status"] != "accessible":
        return False
    
    text = content["text"]
    dynamic_indicators = []
    
    # Look for dynamic data indicators
    data_patterns = [
        r'\d+\s*(candidate|job|interview|application|client)',
        r'total.*\d+',
        r'\d+.*record',
        r'status.*active',
        r'last.*update'
    ]
    
    for pattern in data_patterns:
        matches = re.findall(pattern, text, re.IGNORECASE)
        if matches:
            dynamic_indicators.extend(matches)
            logger.info(f"✅ Dynamic data pattern found: {matches[0]}")
    
    # Check for real-time indicators
    realtime_keywords = [
        "real-time", "live", "current", "updated", "active", 
        "status", "dashboard", "metrics", "analytics"
    ]
    
    realtime_found = []
    for keyword in realtime_keywords:
        if keyword in text:
            realtime_found.append(keyword)
    
    logger.info(f"Dynamic Content: {len(dynamic_indicators)} data patterns found")
    logger.info(f"Real-time Indicators: {len(realtime_found)} keywords found")
    
    return len(dynamic_indicators) >= 1 or len(realtime_found) >= 3

def test_visual_branding(portal_name, content):
    """Test visual branding and design elements"""
    logger.info(f"--- Testing Visual Branding in {portal_name} ---")
    
    if content["status"] != "accessible":
        return False
    
    html = content["html"]
    text = content["text"]
    branding_elements = []
    
    # Check for branding elements
    branding_indicators = [
        "bhiv", "hr platform", "recruiting", "values-driven",
        "enterprise", "ai-powered", "semantic matching"
    ]
    
    for indicator in branding_indicators:
        if indicator in text:
            branding_elements.append(indicator)
            logger.info(f"✅ Branding element: '{indicator}' found")
    
    # Check for visual elements in HTML
    visual_elements = ["title", "header", "logo", "icon", "color", "style"]
    visual_found = []
    
    for element in visual_elements:
        if element in html.lower():
            visual_found.append(element)
    
    logger.info(f"Branding Elements: {len(branding_elements)} found")
    logger.info(f"Visual Elements: {len(visual_found)} detected")
    
    return len(branding_elements) >= 2

def test_functional_workflows(portal_name, content):
    """Test functional workflow elements"""
    logger.info(f"--- Testing Functional Workflows in {portal_name} ---")
    
    if content["status"] != "accessible":
        return False
    
    text = content["text"]
    workflow_elements = []
    
    if "HR Portal" in portal_name:
        hr_workflows = [
            "step 1", "step 2", "create job", "upload candidate", 
            "ai shortlist", "schedule interview", "assessment", "export"
        ]
        for workflow in hr_workflows:
            if workflow in text:
                workflow_elements.append(workflow)
                logger.info(f"✅ HR workflow: '{workflow}' found")
                
    elif "Client Portal" in portal_name:
        client_workflows = [
            "login", "dashboard", "post job", "review candidate",
            "schedule", "analytics", "manage"
        ]
        for workflow in client_workflows:
            if workflow in text:
                workflow_elements.append(workflow)
                logger.info(f"✅ Client workflow: '{workflow}' found")
                
    elif "Candidate Portal" in portal_name:
        candidate_workflows = [
            "register", "profile", "search job", "apply", 
            "track application", "interview", "notification"
        ]
        for workflow in candidate_workflows:
            if workflow in text:
                workflow_elements.append(workflow)
                logger.info(f"✅ Candidate workflow: '{workflow}' found")
    
    logger.info(f"Workflow Elements: {len(workflow_elements)} found")
    return len(workflow_elements) >= 3

def analyze_content_uniqueness(all_content):
    """Analyze content uniqueness across portals"""
    logger.info("=== ANALYZING CONTENT UNIQUENESS ===")
    
    portal_texts = {}
    for portal_name, content in all_content.items():
        if content["status"] == "accessible":
            portal_texts[portal_name] = set(content["text"].split())
    
    # Calculate uniqueness
    for portal1 in portal_texts:
        for portal2 in portal_texts:
            if portal1 != portal2:
                common_words = portal_texts[portal1] & portal_texts[portal2]
                unique_words = portal_texts[portal1] - portal_texts[portal2]
                
                uniqueness_ratio = len(unique_words) / len(portal_texts[portal1]) * 100
                logger.info(f"{portal1} vs {portal2}: {uniqueness_ratio:.1f}% unique content")
    
    return True

def generate_visual_content_report(all_results):
    """Generate comprehensive visual content report"""
    logger.info("=== GENERATING VISUAL CONTENT REPORT ===")
    
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "portals_tested": len(PORTALS),
        "total_tests": 0,
        "passed_tests": 0,
        "portal_results": {},
        "summary": {}
    }
    
    for portal_name, results in all_results.items():
        portal_score = sum(1 for result in results.values() if result)
        total_portal_tests = len(results)
        
        report["portal_results"][portal_name] = {
            "score": f"{portal_score}/{total_portal_tests}",
            "percentage": f"{(portal_score/total_portal_tests)*100:.1f}%",
            "tests": results
        }
        
        report["total_tests"] += total_portal_tests
        report["passed_tests"] += portal_score
    
    # Overall summary
    overall_percentage = (report["passed_tests"] / report["total_tests"]) * 100
    report["summary"] = {
        "overall_score": f"{report['passed_tests']}/{report['total_tests']}",
        "overall_percentage": f"{overall_percentage:.1f}%",
        "status": "EXCELLENT" if overall_percentage >= 90 else "GOOD" if overall_percentage >= 80 else "NEEDS_IMPROVEMENT"
    }
    
    # Save report
    with open('visual_content_report.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"Visual Content Report: {report['summary']['overall_score']} ({report['summary']['overall_percentage']})")
    return report

def main():
    """Main visual content testing function"""
    logger.info("🎨 Starting Portal Visual Content Testing...")
    
    # Get content from all portals
    all_content = {}
    for portal_name, url in PORTALS.items():
        all_content[portal_name] = get_portal_content(portal_name, url)
        time.sleep(2)  # Avoid overwhelming servers
    
    # Run tests for each portal
    all_results = {}
    
    for portal_name, content in all_content.items():
        logger.info(f"\n🔍 TESTING {portal_name.upper()} VISUAL CONTENT")
        
        results = {
            "bhiv_values": test_bhiv_values_presence(portal_name, content),
            "unique_content": test_unique_portal_content(portal_name, content),
            "streamlit_components": test_streamlit_components(portal_name, content),
            "dynamic_content": test_dynamic_content(portal_name, content),
            "visual_branding": test_visual_branding(portal_name, content),
            "functional_workflows": test_functional_workflows(portal_name, content)
        }
        
        all_results[portal_name] = results
        
        # Portal summary
        passed = sum(1 for result in results.values() if result)
        total = len(results)
        logger.info(f"📊 {portal_name} Summary: {passed}/{total} tests passed ({(passed/total)*100:.1f}%)")
    
    # Analyze content uniqueness
    analyze_content_uniqueness(all_content)
    
    # Generate final report
    report = generate_visual_content_report(all_results)
    
    # Final summary
    logger.info(f"\n🎉 VISUAL CONTENT TESTING COMPLETE")
    logger.info(f"Overall Score: {report['summary']['overall_score']}")
    logger.info(f"Success Rate: {report['summary']['overall_percentage']}")
    logger.info(f"Status: {report['summary']['status']}")
    
    for portal_name, results in report["portal_results"].items():
        status = "✅" if float(results["percentage"].rstrip('%')) >= 80 else "⚠️"
        logger.info(f"{status} {portal_name}: {results['score']} ({results['percentage']})")

if __name__ == "__main__":
    main()