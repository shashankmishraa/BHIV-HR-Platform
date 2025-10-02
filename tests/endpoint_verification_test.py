#!/usr/bin/env python3
"""
BHIV HR Platform - Complete Endpoint Verification Test
Compares codebase endpoints vs live service endpoints
"""

import requests
import json
import re
from typing import Dict, List, Set, Tuple
from pathlib import Path

class EndpointVerificationTester:
    def __init__(self):
        self.base_urls = {
            'gateway': 'https://bhiv-hr-gateway-46pz.onrender.com',
            'agent': 'https://bhiv-hr-agent-m1me.onrender.com'
        }
        self.api_key = "<REDACTED>"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        self.results = {
            'codebase_endpoints': {},
            'live_endpoints': {},
            'verification_results': {},
            'discrepancies': {},
            'endpoint_tests': {}
        }

    def extract_endpoints_from_code(self) -> Dict[str, List[Tuple[str, str]]]:
        """Extract all endpoints from codebase files"""
        print("Extracting endpoints from codebase...")
        
        endpoints = {
            'gateway': [],
            'agent': []
        }
        
        # Gateway endpoints
        gateway_file = Path("c:/BHIV-HR-Platform/services/gateway/app/main.py")
        if gateway_file.exists():
            with open(gateway_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Simple but effective regex pattern
                pattern = r'@app\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
                matches = re.findall(pattern, content, re.IGNORECASE)
                for method, path in matches:
                    endpoints['gateway'].append((method.upper(), path.strip()))
        
        # Agent endpoints
        agent_file = Path("c:/BHIV-HR-Platform/services/agent/app.py")
        if agent_file.exists():
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
                pattern = r'@app\.(get|post|put|delete|patch)\s*\(\s*["\']([^"\']+)["\']'
                matches = re.findall(pattern, content, re.IGNORECASE)
                for method, path in matches:
                    endpoints['agent'].append((method.upper(), path.strip()))
        
        # Remove duplicates and sort
        for service in endpoints:
            endpoints[service] = sorted(list(set(endpoints[service])))
            print(f"Found {len(endpoints[service])} endpoints in {service} codebase")
        
        return endpoints

    def get_live_endpoints_from_openapi(self, service: str) -> List[Tuple[str, str]]:
        """Get endpoints from live service OpenAPI docs"""
        print(f"Fetching live endpoints from {service} service...")
        
        try:
            response = requests.get(f"{self.base_urls[service]}/openapi.json", timeout=30)
            if response.status_code != 200:
                print(f"Failed to get OpenAPI spec for {service}: {response.status_code}")
                return []
            
            openapi_spec = response.json()
            endpoints = []
            
            if 'paths' in openapi_spec:
                for path, methods in openapi_spec['paths'].items():
                    for method in methods.keys():
                        if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']:
                            endpoints.append((method.upper(), path))
            
            return sorted(endpoints)
            
        except Exception as e:
            print(f"Error fetching OpenAPI spec for {service}: {e}")
            return []

    def test_endpoint_accessibility(self, service: str, method: str, path: str) -> Dict:
        """Test if endpoint is accessible and returns expected response"""
        url = f"{self.base_urls[service]}{path}"
        
        test_result = {
            'method': method,
            'path': path,
            'url': url,
            'accessible': False,
            'status_code': None,
            'response_time': None,
            'error': None,
            'response_data': None
        }
        
        try:
            import time
            start_time = time.time()
            
            # Handle path parameters for testing
            test_path = path
            if '{' in path and '}' in path:
                test_path = re.sub(r'\{job_id\}', '1', test_path)
                test_path = re.sub(r'\{candidate_id\}', '1', test_path)
                test_path = re.sub(r'\{client_id\}', 'TECH001', test_path)
                test_path = re.sub(r'\{token\}', '123456', test_path)
                url = f"{self.base_urls[service]}{test_path}"
            
            if method == 'GET':
                response = requests.get(url, headers=self.headers, timeout=15)
            elif method == 'POST':
                test_data = self.get_test_data_for_endpoint(path)
                response = requests.post(url, headers=self.headers, json=test_data, timeout=15)
            else:
                response = requests.get(url, headers=self.headers, timeout=15)
            
            test_result['status_code'] = response.status_code
            test_result['response_time'] = time.time() - start_time
            test_result['accessible'] = True
            
            try:
                if response.headers.get('content-type', '').startswith('application/json'):
                    test_result['response_data'] = {
                        'type': 'json',
                        'size': len(response.content),
                        'keys': list(response.json().keys()) if isinstance(response.json(), dict) else 'array'
                    }
                else:
                    test_result['response_data'] = {
                        'type': 'text',
                        'size': len(response.content)
                    }
            except:
                test_result['response_data'] = {'type': 'unknown'}
                
        except Exception as e:
            test_result['error'] = str(e)
        
        return test_result

    def get_test_data_for_endpoint(self, path: str) -> Dict:
        """Get appropriate test data for POST endpoints"""
        test_data_map = {
            '/v1/jobs': {
                "title": "Test Job",
                "department": "Engineering", 
                "location": "Remote",
                "experience_level": "Mid-level",
                "requirements": "Python, FastAPI",
                "description": "Test job posting"
            },
            '/v1/candidates/bulk': {
                "candidates": [{
                    "name": "Test Candidate",
                    "email": "test@example.com",
                    "technical_skills": "Python, JavaScript"
                }]
            },
            '/match': {
                "job_id": 1
            }
        }
        
        for endpoint_path, data in test_data_map.items():
            if endpoint_path in path:
                return data
        
        return {}

    def compare_endpoints(self) -> Dict:
        """Compare codebase vs live endpoints"""
        print("Comparing codebase vs live endpoints...")
        
        codebase_endpoints = self.extract_endpoints_from_code()
        live_endpoints = {}
        
        for service in ['gateway', 'agent']:
            live_endpoints[service] = self.get_live_endpoints_from_openapi(service)
        
        self.results['codebase_endpoints'] = codebase_endpoints
        self.results['live_endpoints'] = live_endpoints
        
        discrepancies = {}
        
        for service in ['gateway', 'agent']:
            codebase_set = set(codebase_endpoints[service])
            live_set = set(live_endpoints[service])
            
            discrepancies[service] = {
                'in_code_not_live': list(codebase_set - live_set),
                'in_live_not_code': list(live_set - codebase_set),
                'matching': list(codebase_set & live_set),
                'total_codebase': len(codebase_set),
                'total_live': len(live_set),
                'match_percentage': (len(codebase_set & live_set) / max(1, len(codebase_set))) * 100
            }
        
        self.results['discrepancies'] = discrepancies
        return discrepancies

    def test_all_endpoints(self) -> Dict:
        """Test accessibility of all endpoints"""
        print("Testing accessibility of all endpoints...")
        
        endpoint_tests = {}
        
        for service in ['gateway', 'agent']:
            endpoint_tests[service] = {
                'tested_endpoints': [],
                'accessible_count': 0,
                'total_count': 0,
                'success_rate': 0
            }
            
            codebase_endpoints = self.results['codebase_endpoints'][service]
            
            for method, path in codebase_endpoints:
                test_result = self.test_endpoint_accessibility(service, method, path)
                endpoint_tests[service]['tested_endpoints'].append(test_result)
                endpoint_tests[service]['total_count'] += 1
                
                if test_result['accessible'] and test_result['status_code'] in [200, 201, 422]:
                    endpoint_tests[service]['accessible_count'] += 1
            
            if endpoint_tests[service]['total_count'] > 0:
                endpoint_tests[service]['success_rate'] = (
                    endpoint_tests[service]['accessible_count'] / 
                    endpoint_tests[service]['total_count']
                ) * 100
        
        self.results['endpoint_tests'] = endpoint_tests
        return endpoint_tests

    def run_complete_verification(self) -> Dict:
        """Run complete endpoint verification"""
        print("Starting Complete Endpoint Verification")
        print("=" * 60)
        
        self.compare_endpoints()
        self.test_all_endpoints()
        
        print(f"\nDEBUG - Codebase endpoints found:")
        for service, eps in self.results['codebase_endpoints'].items():
            print(f"{service}: {len(eps)} endpoints")
            for method, path in eps[:5]:
                print(f"  {method} {path}")
        
        print(f"\nDEBUG - Live endpoints found:")
        for service, eps in self.results['live_endpoints'].items():
            print(f"{service}: {len(eps)} endpoints")
            for method, path in eps[:5]:
                print(f"  {method} {path}")
        
        self.generate_verification_summary()
        return self.results

    def generate_verification_summary(self):
        """Generate comprehensive verification summary"""
        summary = {
            'overall_status': 'Unknown',
            'services_analyzed': 2,
            'total_endpoints_found': 0,
            'total_endpoints_accessible': 0,
            'critical_issues': [],
            'missing_endpoints': [],
            'extra_endpoints': [],
            'recommendations': []
        }
        
        for service in ['gateway', 'agent']:
            discrepancy = self.results['discrepancies'][service]
            test_results = self.results['endpoint_tests'][service]
            
            summary['total_endpoints_found'] += discrepancy['total_codebase']
            summary['total_endpoints_accessible'] += test_results['accessible_count']
            
            if discrepancy['in_code_not_live']:
                summary['missing_endpoints'].extend([
                    f"{service}: {method} {path}" 
                    for method, path in discrepancy['in_code_not_live']
                ])
            
            if discrepancy['in_live_not_code']:
                summary['extra_endpoints'].extend([
                    f"{service}: {method} {path}" 
                    for method, path in discrepancy['in_live_not_code']
                ])
            
            if discrepancy['match_percentage'] < 90:
                summary['critical_issues'].append(
                    f"{service} service: Only {discrepancy['match_percentage']:.1f}% endpoint match"
                )
        
        if summary['total_endpoints_found'] > 0:
            if summary['total_endpoints_accessible'] >= summary['total_endpoints_found'] * 0.9:
                summary['overall_status'] = 'Excellent'
            elif summary['total_endpoints_accessible'] >= summary['total_endpoints_found'] * 0.75:
                summary['overall_status'] = 'Good'
            elif summary['total_endpoints_accessible'] >= summary['total_endpoints_found'] * 0.5:
                summary['overall_status'] = 'Fair'
            else:
                summary['overall_status'] = 'Poor'
        
        if summary['missing_endpoints']:
            summary['recommendations'].append("Deploy missing endpoints to live services")
        
        if summary['extra_endpoints']:
            summary['recommendations'].append("Update documentation for extra endpoints")
        
        if summary['critical_issues']:
            summary['recommendations'].append("Address critical endpoint discrepancies")
        
        self.results['verification_results'] = summary

    def print_detailed_results(self):
        """Print comprehensive verification results"""
        print("\n" + "=" * 80)
        print("COMPLETE ENDPOINT VERIFICATION RESULTS")
        print("=" * 80)
        
        summary = self.results['verification_results']
        print(f"\nOVERALL STATUS: {summary['overall_status']}")
        print(f"Total Endpoints Found: {summary['total_endpoints_found']}")
        print(f"Total Endpoints Accessible: {summary['total_endpoints_accessible']}")
        
        if summary['total_endpoints_found'] > 0:
            success_rate = (summary['total_endpoints_accessible']/summary['total_endpoints_found'])*100
            print(f"Success Rate: {success_rate:.1f}%")
        
        for service in ['gateway', 'agent']:
            print(f"\n{service.upper()} SERVICE ANALYSIS:")
            print("-" * 40)
            
            discrepancy = self.results['discrepancies'][service]
            test_results = self.results['endpoint_tests'][service]
            
            print(f"Codebase Endpoints: {discrepancy['total_codebase']}")
            print(f"Live Endpoints: {discrepancy['total_live']}")
            print(f"Matching Endpoints: {len(discrepancy['matching'])}")
            print(f"Match Percentage: {discrepancy['match_percentage']:.1f}%")
            print(f"Accessible Endpoints: {test_results['accessible_count']}/{test_results['total_count']}")
            print(f"Accessibility Rate: {test_results['success_rate']:.1f}%")
            
            if discrepancy['in_code_not_live']:
                print(f"\nMISSING FROM LIVE ({len(discrepancy['in_code_not_live'])}):")
                for method, path in discrepancy['in_code_not_live'][:10]:
                    print(f"  {method} {path}")
            
            if discrepancy['in_live_not_code']:
                print(f"\nEXTRA IN LIVE ({len(discrepancy['in_live_not_code'])}):")
                for method, path in discrepancy['in_live_not_code'][:10]:
                    print(f"  {method} {path}")
        
        if summary['critical_issues']:
            print(f"\nCRITICAL ISSUES:")
            for issue in summary['critical_issues']:
                print(f"  • {issue}")
        
        if summary['recommendations']:
            print(f"\nRECOMMENDATIONS:")
            for rec in summary['recommendations']:
                print(f"  • {rec}")
        
        print("\n" + "=" * 80)

def main():
    """Run complete endpoint verification"""
    tester = EndpointVerificationTester()
    
    try:
        results = tester.run_complete_verification()
        tester.print_detailed_results()
        
        with open('endpoint_verification_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: endpoint_verification_results.json")
        
        return results
        
    except Exception as e:
        print(f"ERROR: Verification failed: {str(e)}")
        return None

if __name__ == "__main__":
    main()