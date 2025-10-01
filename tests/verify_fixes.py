#!/usr/bin/env python3
"""
BHIV HR Platform - Fix Verification Script
Tests the 6 previously failing endpoints to confirm fixes
"""

import requests
import json
import time
from datetime import datetime

class FixVerifier:
    def __init__(self):
        self.base_urls = {
            'gateway': 'https://bhiv-hr-gateway-46pz.onrender.com',
            'agent': 'https://bhiv-hr-agent-m1me.onrender.com'
        }
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        self.failed_endpoints = [
            ('gateway', 'GET', '/test-candidates'),
            ('gateway', 'GET', '/v1/jobs'),
            ('gateway', 'POST', '/v1/jobs'),
            ('gateway', 'POST', '/v1/candidates/bulk'),
            ('agent', 'GET', '/analyze/1'),
            ('agent', 'POST', '/match')
        ]

    def test_endpoint(self, service: str, method: str, path: str) -> dict:
        """Test a specific endpoint"""
        url = f"{self.base_urls[service]}{path}"
        
        result = {
            'service': service,
            'method': method,
            'path': path,
            'url': url,
            'success': False,
            'status_code': None,
            'response_time': None,
            'error': None,
            'response_data': None
        }
        
        try:
            start_time = time.time()
            
            if method == 'GET':
                response = requests.get(url, headers=self.headers, timeout=30)
            elif method == 'POST':
                test_data = self.get_test_data(path)
                response = requests.post(url, headers=self.headers, json=test_data, timeout=30)
            
            result['status_code'] = response.status_code
            result['response_time'] = time.time() - start_time
            result['success'] = 200 <= response.status_code < 300
            
            try:
                result['response_data'] = response.json()
            except:
                result['response_data'] = response.text[:200]
                
        except Exception as e:
            result['error'] = str(e)
        
        return result

    def get_test_data(self, path: str) -> dict:
        """Get test data for POST endpoints"""
        if '/v1/jobs' in path:
            return {
                "title": "Fix Verification Test Job",
                "department": "Engineering",
                "location": "Remote",
                "experience_level": "Mid-level",
                "requirements": "Python, FastAPI, Testing",
                "description": "Test job for verifying database fixes"
            }
        elif '/v1/candidates/bulk' in path:
            return {
                "candidates": [{
                    "name": "Test Candidate Fix",
                    "email": f"test_fix_{int(time.time())}@example.com",
                    "technical_skills": "Python, Testing",
                    "experience_years": 3
                }]
            }
        elif '/match' in path:
            return {"job_id": 1}
        
        return {}

    def run_verification(self) -> dict:
        """Run verification of all previously failing endpoints"""
        print("BHIV HR Platform - Fix Verification")
        print("=" * 50)
        print(f"Testing {len(self.failed_endpoints)} previously failing endpoints...")
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'total_tested': len(self.failed_endpoints),
            'passed': 0,
            'failed': 0,
            'endpoint_results': [],
            'summary': {}
        }
        
        for service, method, path in self.failed_endpoints:
            print(f"\nTesting: {method} {service}{path}")
            
            result = self.test_endpoint(service, method, path)
            results['endpoint_results'].append(result)
            
            if result['success']:
                results['passed'] += 1
                status = "[FIXED]"
                print(f"  Status: {status} ({result['status_code']}) - {result['response_time']:.2f}s")
            else:
                results['failed'] += 1
                status = "[STILL FAILING]"
                error_info = result['error'] or f"HTTP {result['status_code']}"
                print(f"  Status: {status} - {error_info}")
        
        # Calculate success rate
        success_rate = (results['passed'] / results['total_tested']) * 100
        
        results['summary'] = {
            'success_rate': success_rate,
            'endpoints_fixed': results['passed'],
            'endpoints_still_failing': results['failed'],
            'overall_status': 'EXCELLENT' if success_rate >= 95 else 'GOOD' if success_rate >= 80 else 'NEEDS_WORK'
        }
        
        self.print_summary(results)
        return results

    def print_summary(self, results: dict):
        """Print verification summary"""
        summary = results['summary']
        
        print("\n" + "=" * 50)
        print("FIX VERIFICATION SUMMARY")
        print("=" * 50)
        
        print(f"Total Endpoints Tested: {results['total_tested']}")
        print(f"Endpoints Fixed: {results['passed']}")
        print(f"Still Failing: {results['failed']}")
        print(f"Success Rate: {summary['success_rate']:.1f}%")
        print(f"Overall Status: {summary['overall_status']}")
        
        if results['failed'] > 0:
            print(f"\nSTILL FAILING ({results['failed']} endpoints):")
            for result in results['endpoint_results']:
                if not result['success']:
                    error_info = result['error'] or f"HTTP {result['status_code']}"
                    print(f"  {result['method']} {result['service']}{result['path']} - {error_info}")
        
        if results['passed'] > 0:
            print(f"\nSUCCESSFULLY FIXED ({results['passed']} endpoints):")
            for result in results['endpoint_results']:
                if result['success']:
                    print(f"  {result['method']} {result['service']}{result['path']} - {result['status_code']} ({result['response_time']:.2f}s)")
        
        print("\n" + "=" * 50)

def main():
    """Run fix verification"""
    verifier = FixVerifier()
    
    try:
        results = verifier.run_verification()
        
        # Save results
        with open('fix_verification_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nResults saved to: fix_verification_results.json")
        
        # Return appropriate exit code
        return 0 if results['summary']['success_rate'] >= 80 else 1
        
    except Exception as e:
        print(f"ERROR: Verification failed: {str(e)}")
        return 1

if __name__ == "__main__":
    exit(main())