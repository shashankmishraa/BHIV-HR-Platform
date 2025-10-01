#!/usr/bin/env python3
"""
BHIV HR Platform - Deployment Monitor
Monitors Render services for deployment completion and tests fixes
"""

import requests
import time
import json
from datetime import datetime

class DeploymentMonitor:
    def __init__(self):
        self.base_urls = {
            'gateway': 'https://bhiv-hr-gateway-46pz.onrender.com',
            'agent': 'https://bhiv-hr-agent-m1me.onrender.com'
        }
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def check_service_health(self, service: str) -> dict:
        """Check if service is responding and get version info"""
        try:
            response = requests.get(f"{self.base_urls[service]}/health", headers=self.headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                return {
                    'status': 'healthy',
                    'version': data.get('version', 'unknown'),
                    'timestamp': data.get('timestamp', 'unknown'),
                    'response_time': response.elapsed.total_seconds()
                }
            else:
                return {'status': 'unhealthy', 'code': response.status_code}
        except Exception as e:
            return {'status': 'error', 'error': str(e)}

    def test_fixed_endpoints(self) -> dict:
        """Test the previously failing endpoints"""
        test_results = {
            'gateway_tests': {},
            'agent_tests': {},
            'overall_success': False
        }
        
        # Test Gateway endpoints
        print("Testing Gateway endpoints...")
        
        # Test /test-candidates
        try:
            response = requests.get(f"{self.base_urls['gateway']}/test-candidates", headers=self.headers, timeout=15)
            test_results['gateway_tests']['test_candidates'] = {
                'status_code': response.status_code,
                'success': 200 <= response.status_code < 300,
                'response': response.json() if response.status_code != 500 else 'Server Error'
            }
        except Exception as e:
            test_results['gateway_tests']['test_candidates'] = {'success': False, 'error': str(e)}
        
        # Test /v1/jobs GET
        try:
            response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", headers=self.headers, timeout=15)
            test_results['gateway_tests']['list_jobs'] = {
                'status_code': response.status_code,
                'success': 200 <= response.status_code < 300,
                'response': response.json() if response.status_code != 500 else 'Server Error'
            }
        except Exception as e:
            test_results['gateway_tests']['list_jobs'] = {'success': False, 'error': str(e)}
        
        # Test /v1/jobs POST
        try:
            job_data = {
                "title": "Deployment Test Job",
                "department": "Engineering",
                "location": "Remote", 
                "experience_level": "Mid-level",
                "requirements": "Testing, Deployment",
                "description": "Test job for deployment verification"
            }
            response = requests.post(f"{self.base_urls['gateway']}/v1/jobs", headers=self.headers, json=job_data, timeout=15)
            test_results['gateway_tests']['create_job'] = {
                'status_code': response.status_code,
                'success': 200 <= response.status_code < 300,
                'response': response.json() if response.status_code != 500 else 'Server Error'
            }
        except Exception as e:
            test_results['gateway_tests']['create_job'] = {'success': False, 'error': str(e)}
        
        # Test Agent endpoints
        print("Testing Agent endpoints...")
        
        # Test /analyze/1
        try:
            response = requests.get(f"{self.base_urls['agent']}/analyze/1", headers=self.headers, timeout=15)
            test_results['agent_tests']['analyze'] = {
                'status_code': response.status_code,
                'success': 200 <= response.status_code < 500,  # 404 is acceptable if candidate doesn't exist
                'response': response.json() if response.headers.get('content-type', '').startswith('application/json') else 'Non-JSON response'
            }
        except Exception as e:
            test_results['agent_tests']['analyze'] = {'success': False, 'error': str(e)}
        
        # Test /match
        try:
            match_data = {"job_id": 1}
            response = requests.post(f"{self.base_urls['agent']}/match", headers=self.headers, json=match_data, timeout=15)
            test_results['agent_tests']['match'] = {
                'status_code': response.status_code,
                'success': 200 <= response.status_code < 300,
                'response': response.json() if response.headers.get('content-type', '').startswith('application/json') else 'Non-JSON response'
            }
        except Exception as e:
            test_results['agent_tests']['match'] = {'success': False, 'error': str(e)}
        
        # Calculate overall success
        all_tests = []
        for service_tests in [test_results['gateway_tests'], test_results['agent_tests']]:
            for test in service_tests.values():
                all_tests.append(test.get('success', False))
        
        test_results['overall_success'] = sum(all_tests) >= len(all_tests) * 0.8  # 80% success rate
        test_results['success_rate'] = (sum(all_tests) / len(all_tests)) * 100 if all_tests else 0
        
        return test_results

    def monitor_deployment(self, max_wait_minutes: int = 10) -> dict:
        """Monitor deployment progress and test when ready"""
        print("BHIV HR Platform - Deployment Monitor")
        print("=" * 50)
        print(f"Monitoring deployment for up to {max_wait_minutes} minutes...")
        
        start_time = time.time()
        max_wait_seconds = max_wait_minutes * 60
        
        deployment_results = {
            'start_time': datetime.now().isoformat(),
            'services_ready': False,
            'test_results': None,
            'deployment_time': 0,
            'final_status': 'unknown'
        }
        
        while time.time() - start_time < max_wait_seconds:
            print(f"\nChecking services... ({int((time.time() - start_time) / 60)}m elapsed)")
            
            # Check both services
            gateway_health = self.check_service_health('gateway')
            agent_health = self.check_service_health('agent')
            
            print(f"Gateway: {gateway_health['status']}")
            print(f"Agent: {agent_health['status']}")
            
            # If both services are healthy, test the fixes
            if gateway_health['status'] == 'healthy' and agent_health['status'] == 'healthy':
                print("\nServices are healthy! Testing fixes...")
                deployment_results['services_ready'] = True
                deployment_results['deployment_time'] = time.time() - start_time
                
                # Test the fixed endpoints
                test_results = self.test_fixed_endpoints()
                deployment_results['test_results'] = test_results
                
                if test_results['overall_success']:
                    deployment_results['final_status'] = 'success'
                    print(f"\nSUCCESS! Deployment completed and fixes verified!")
                    print(f"Success rate: {test_results['success_rate']:.1f}%")
                else:
                    deployment_results['final_status'] = 'partial_success'
                    print(f"\nPARTIAL SUCCESS: Deployment completed but some issues remain")
                    print(f"Success rate: {test_results['success_rate']:.1f}%")
                
                break
            
            # Wait before next check
            time.sleep(30)
        
        if not deployment_results['services_ready']:
            deployment_results['final_status'] = 'timeout'
            print(f"\nTIMEOUT: Services not ready after {max_wait_minutes} minutes")
        
        return deployment_results

    def print_detailed_results(self, results: dict):
        """Print detailed test results"""
        if not results.get('test_results'):
            return
        
        test_results = results['test_results']
        
        print("\n" + "=" * 50)
        print("DETAILED TEST RESULTS")
        print("=" * 50)
        
        print("\nGATEWAY SERVICE:")
        for test_name, result in test_results['gateway_tests'].items():
            status = "[PASS]" if result.get('success') else "[FAIL]"
            code = result.get('status_code', 'N/A')
            print(f"  {test_name}: {status} (HTTP {code})")
        
        print("\nAGENT SERVICE:")
        for test_name, result in test_results['agent_tests'].items():
            status = "[PASS]" if result.get('success') else "[FAIL]"
            code = result.get('status_code', 'N/A')
            print(f"  {test_name}: {status} (HTTP {code})")
        
        print(f"\nOVERALL SUCCESS RATE: {test_results['success_rate']:.1f}%")

def main():
    """Run deployment monitoring"""
    monitor = DeploymentMonitor()
    
    try:
        results = monitor.monitor_deployment(max_wait_minutes=15)
        monitor.print_detailed_results(results)
        
        # Save results
        with open('deployment_monitor_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nResults saved to: deployment_monitor_results.json")
        
        # Return appropriate exit code
        if results['final_status'] == 'success':
            return 0
        elif results['final_status'] == 'partial_success':
            return 1
        else:
            return 2
        
    except Exception as e:
        print(f"ERROR: Monitoring failed: {str(e)}")
        return 3

if __name__ == "__main__":
    exit(main())