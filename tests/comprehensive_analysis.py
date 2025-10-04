#!/usr/bin/env python3
"""
Comprehensive BHIV HR Platform Analysis
Tests all features, endpoints, and functions across four services
"""

import requests
import json
import os
import re
from datetime import datetime

# Configuration
GATEWAY_URL = "https://bhiv-hr-gateway-46pz.onrender.com"
AGENT_URL = "https://bhiv-hr-agent-m1me.onrender.com"
PORTAL_URL = "https://bhiv-hr-portal-cead.onrender.com"
CLIENT_PORTAL_URL = "https://bhiv-hr-client-portal-5g33.onrender.com"

API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
HEADERS = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

class ComprehensiveAnalyzer:
    def __init__(self):
        self.results = {
            'implemented_working': [],
            'implemented_not_working': [],
            'missing_endpoints': [],
            'code_not_exposed': [],
            'unused_code': [],
            'portal_features': []
        }
        
    def scan_code_endpoints(self, file_path, service_name):
        """Scan code files for endpoint definitions"""
        if not os.path.exists(file_path):
            return []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        patterns = [
            (r'@app\.get\("([^"]+)"', 'GET'),
            (r'@app\.post\("([^"]+)"', 'POST'),
            (r'@app\.put\("([^"]+)"', 'PUT'),
            (r'@app\.delete\("([^"]+)"', 'DELETE')
        ]
        
        endpoints = []
        for pattern, method in patterns:
            matches = re.findall(pattern, content)
            for match in matches:
                endpoints.append({
                    'method': method,
                    'path': match,
                    'service': service_name,
                    'full_endpoint': f"{method} {match}"
                })
        
        return endpoints
    
    def test_endpoint(self, method, url, data=None, timeout=15):
        """Test individual endpoint"""
        try:
            if method == "GET":
                response = requests.get(url, headers=HEADERS, timeout=timeout)
            elif method == "POST":
                response = requests.post(url, headers=HEADERS, json=data, timeout=timeout)
            elif method == "PUT":
                response = requests.put(url, headers=HEADERS, json=data, timeout=timeout)
            elif method == "DELETE":
                response = requests.delete(url, headers=HEADERS, timeout=timeout)
            
            return {
                'status_code': response.status_code,
                'success': response.status_code in [200, 201, 202],
                'response': response.json() if response.content else {},
                'error': None
            }
        except Exception as e:
            return {
                'status_code': None,
                'success': False,
                'response': None,
                'error': str(e)
            }
    
    def analyze_gateway_service(self):
        """Comprehensive Gateway service analysis"""
        print("Analyzing Gateway Service...")
        
        # Scan code for endpoints
        gateway_file = "c:\\BHIV-HR-Platform\\services\\gateway\\app\\main.py"
        code_endpoints = self.scan_code_endpoints(gateway_file, "gateway")
        
        # Test each endpoint
        for endpoint in code_endpoints:
            url = f"{GATEWAY_URL}{endpoint['path']}"
            
            # Prepare test data for POST endpoints
            test_data = None
            if endpoint['method'] == 'POST':
                test_data = self.get_test_data(endpoint['path'])
            
            result = self.test_endpoint(endpoint['method'], url, test_data)
            
            endpoint_info = {
                'endpoint': endpoint['full_endpoint'],
                'url': url,
                'status_code': result['status_code'],
                'working': result['success'],
                'error': result['error'],
                'response_sample': str(result['response'])[:100] if result['response'] else None
            }
            
            if result['success']:
                self.results['implemented_working'].append(endpoint_info)
            else:
                self.results['implemented_not_working'].append(endpoint_info)
        
        return len(code_endpoints)
    
    def analyze_agent_service(self):
        """Comprehensive Agent service analysis"""
        print("Analyzing Agent Service...")
        
        # Scan code for endpoints
        agent_file = "c:\\BHIV-HR-Platform\\services\\agent\\app.py"
        code_endpoints = self.scan_code_endpoints(agent_file, "agent")
        
        # Test each endpoint
        for endpoint in code_endpoints:
            url = f"{AGENT_URL}{endpoint['path']}"
            
            # Prepare test data for POST endpoints
            test_data = None
            if endpoint['method'] == 'POST' and 'match' in endpoint['path']:
                test_data = {"job_id": 1}
            
            result = self.test_endpoint(endpoint['method'], url, test_data)
            
            endpoint_info = {
                'endpoint': endpoint['full_endpoint'],
                'url': url,
                'status_code': result['status_code'],
                'working': result['success'],
                'error': result['error'],
                'response_sample': str(result['response'])[:100] if result['response'] else None
            }
            
            if result['success']:
                self.results['implemented_working'].append(endpoint_info)
            else:
                self.results['implemented_not_working'].append(endpoint_info)
        
        return len(code_endpoints)
    
    def analyze_portal_services(self):
        """Analyze Portal services accessibility and features"""
        print("Analyzing Portal Services...")
        
        portals = [
            ("HR Portal", PORTAL_URL),
            ("Client Portal", CLIENT_PORTAL_URL)
        ]
        
        for name, url in portals:
            try:
                response = requests.get(url, timeout=10)
                portal_info = {
                    'name': name,
                    'url': url,
                    'accessible': response.status_code == 200,
                    'status_code': response.status_code
                }
                self.results['portal_features'].append(portal_info)
            except Exception as e:
                portal_info = {
                    'name': name,
                    'url': url,
                    'accessible': False,
                    'error': str(e)
                }
                self.results['portal_features'].append(portal_info)
    
    def scan_unused_code(self):
        """Scan for potentially unused code"""
        print("Scanning for unused code...")
        
        # Check for unused imports and functions
        files_to_check = [
            "c:\\BHIV-HR-Platform\\services\\gateway\\app\\main.py",
            "c:\\BHIV-HR-Platform\\services\\agent\\app.py",
            "c:\\BHIV-HR-Platform\\services\\portal\\app.py",
            "c:\\BHIV-HR-Platform\\services\\client_portal\\app.py"
        ]
        
        for file_path in files_to_check:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for unused imports
                imports = re.findall(r'^import\s+(\w+)', content, re.MULTILINE)
                from_imports = re.findall(r'^from\s+[\w.]+\s+import\s+(.+)', content, re.MULTILINE)
                
                # Check for defined but unused functions
                functions = re.findall(r'^def\s+(\w+)', content, re.MULTILINE)
                
                # Simple usage check (not perfect but gives indication)
                for func in functions:
                    if content.count(func) == 1:  # Only defined, never called
                        self.results['unused_code'].append({
                            'file': file_path,
                            'type': 'function',
                            'name': func,
                            'reason': 'Defined but never called'
                        })
    
    def check_missing_features(self):
        """Check for missing expected features"""
        print("Checking for missing features...")
        
        # Expected endpoints that should exist
        expected_endpoints = [
            "PUT /v1/jobs/{job_id}",
            "DELETE /v1/jobs/{job_id}",
            "PUT /v1/candidates/{candidate_id}",
            "DELETE /v1/candidates/{candidate_id}",
            "GET /v1/analytics/dashboard",
            "GET /v1/reports/candidates",
            "POST /v1/notifications/email",
            "GET /v1/calendar/integration"
        ]
        
        # Check which are missing
        implemented = [ep['endpoint'] for ep in self.results['implemented_working']]
        implemented.extend([ep['endpoint'] for ep in self.results['implemented_not_working']])
        
        for expected in expected_endpoints:
            if expected not in implemented:
                self.results['missing_endpoints'].append({
                    'endpoint': expected,
                    'reason': 'Expected but not implemented'
                })
    
    def get_test_data(self, endpoint_path):
        """Get appropriate test data for POST endpoints"""
        if 'jobs' in endpoint_path:
            return {
                "title": "Test Job",
                "department": "Engineering",
                "location": "Remote",
                "experience_level": "Senior",
                "requirements": "Python, FastAPI",
                "description": "Test job posting"
            }
        elif 'candidates/bulk' in endpoint_path:
            return {
                "candidates": [{
                    "name": "Test Candidate",
                    "email": "test@example.com",
                    "phone": "+1-555-0123",
                    "location": "Test City",
                    "experience_years": 5,
                    "technical_skills": "Python, FastAPI",
                    "seniority_level": "Senior",
                    "education_level": "Masters"
                }]
            }
        elif 'feedback' in endpoint_path:
            return {
                "candidate_id": 1,
                "job_id": 1,
                "integrity": 5,
                "honesty": 4,
                "discipline": 5,
                "hard_work": 5,
                "gratitude": 4
            }
        elif 'interviews' in endpoint_path:
            return {
                "candidate_id": 1,
                "job_id": 1,
                "interview_date": "2025-02-01T10:00:00Z",
                "interviewer": "Test Interviewer"
            }
        elif 'offers' in endpoint_path:
            return {
                "candidate_id": 1,
                "job_id": 1,
                "salary": 120000,
                "start_date": "2025-03-01",
                "terms": "Standard terms"
            }
        elif 'client/login' in endpoint_path:
            return {
                "client_id": "TECH001",
                "password": "demo123"
            }
        elif '2fa/setup' in endpoint_path:
            return {"user_id": "test_user"}
        elif 'password/validate' in endpoint_path:
            return {"password": "TestPassword123!"}
        elif 'security/test-input-validation' in endpoint_path:
            return {"input_data": "test input"}
        elif 'security/test-email-validation' in endpoint_path:
            return {"email": "test@example.com"}
        elif 'security/csp-report' in endpoint_path:
            return {
                "violated_directive": "script-src",
                "blocked_uri": "https://example.com/script.js",
                "document_uri": "https://example.com/page"
            }
        
        return {}
    
    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\nGenerating comprehensive analysis report...")
        
        total_working = len(self.results['implemented_working'])
        total_not_working = len(self.results['implemented_not_working'])
        total_implemented = total_working + total_not_working
        
        report = {
            'analysis_date': datetime.now().isoformat(),
            'summary': {
                'total_endpoints_implemented': total_implemented,
                'working_endpoints': total_working,
                'non_working_endpoints': total_not_working,
                'success_rate': (total_working / total_implemented * 100) if total_implemented > 0 else 0,
                'missing_endpoints': len(self.results['missing_endpoints']),
                'unused_code_items': len(self.results['unused_code']),
                'portal_services': len(self.results['portal_features'])
            },
            'detailed_results': self.results
        }
        
        return report
    
    def run_analysis(self):
        """Run complete analysis"""
        print("Starting Comprehensive BHIV HR Platform Analysis")
        print("=" * 60)
        
        # Analyze all services
        gateway_count = self.analyze_gateway_service()
        agent_count = self.analyze_agent_service()
        self.analyze_portal_services()
        
        # Additional analysis
        self.scan_unused_code()
        self.check_missing_features()
        
        # Generate report
        report = self.generate_report()
        
        # Save report
        with open('comprehensive_analysis_report.json', 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nAnalysis Complete!")
        print(f"Gateway endpoints analyzed: {gateway_count}")
        print(f"Agent endpoints analyzed: {agent_count}")
        print(f"Total working endpoints: {report['summary']['working_endpoints']}")
        print(f"Total non-working endpoints: {report['summary']['non_working_endpoints']}")
        print(f"Success rate: {report['summary']['success_rate']:.1f}%")
        
        return report

def main():
    analyzer = ComprehensiveAnalyzer()
    report = analyzer.run_analysis()
    
    print("\n" + "=" * 60)
    print("COMPREHENSIVE ANALYSIS SUMMARY")
    print("=" * 60)
    
    summary = report['summary']
    print(f"Total Endpoints Implemented: {summary['total_endpoints_implemented']}")
    print(f"Working Endpoints: {summary['working_endpoints']}")
    print(f"Non-Working Endpoints: {summary['non_working_endpoints']}")
    print(f"Success Rate: {summary['success_rate']:.1f}%")
    print(f"Missing Expected Endpoints: {summary['missing_endpoints']}")
    print(f"Unused Code Items: {summary['unused_code_items']}")
    print(f"Portal Services: {summary['portal_services']}")
    
    print(f"\nDetailed report saved to: comprehensive_analysis_report.json")

if __name__ == "__main__":
    main()