#!/usr/bin/env python3
"""
BHIV HR Platform - Service Connection & Routing Audit
"""

import requests
import json
import time
from datetime import datetime

class ServiceAuditor:
    def __init__(self):
        self.services = {
            'gateway': {
                'production': 'https://bhiv-hr-gateway-46pz.onrender.com',
                'endpoints': [
                    '/', '/health', '/docs', '/metrics',
                    '/v1/jobs', '/v1/candidates', '/v1/candidates/search',
                    '/v1/match/1/top', '/v1/client/login'
                ]
            },
            'agent': {
                'production': 'https://bhiv-hr-agent-m1me.onrender.com',
                'endpoints': [
                    '/', '/health', '/docs', '/test-db'
                ]
            },
            'portal': {
                'production': 'https://bhiv-hr-portal-cead.onrender.com',
                'endpoints': ['/']
            },
            'client_portal': {
                'production': 'https://bhiv-hr-client-portal-5g33.onrender.com',
                'endpoints': ['/']
            }
        }
        
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.results = {'services': {}, 'issues': [], 'summary': {}}

    def test_endpoint(self, service, endpoint):
        """Test individual endpoint"""
        base_url = self.services[service]['production']
        full_url = f"{base_url}{endpoint}"
        
        try:
            headers = {}
            if endpoint.startswith('/v1/'):
                headers = {"Authorization": f"Bearer {self.api_key}"}
            
            start_time = time.time()
            response = requests.get(full_url, headers=headers, timeout=10)
            response_time = time.time() - start_time
            
            return {
                'url': full_url,
                'status': response.status_code,
                'time': round(response_time, 3),
                'success': response.status_code < 400
            }
        except Exception as e:
            return {
                'url': full_url,
                'status': None,
                'time': None,
                'success': False,
                'error': str(e)
            }

    def audit_service(self, service_name):
        """Audit all endpoints for a service"""
        print(f"Testing {service_name} service...")
        
        service_results = {
            'base_url': self.services[service_name]['production'],
            'endpoints': {},
            'summary': {'total': 0, 'success': 0, 'failed': 0}
        }
        
        for endpoint in self.services[service_name]['endpoints']:
            result = self.test_endpoint(service_name, endpoint)
            service_results['endpoints'][endpoint] = result
            service_results['summary']['total'] += 1
            
            if result['success']:
                service_results['summary']['success'] += 1
                print(f"  OK: {endpoint} - {result['status']} ({result['time']}s)")
            else:
                service_results['summary']['failed'] += 1
                error_msg = result.get('error', f"HTTP {result.get('status', 'Error')}")
                print(f"  FAIL: {endpoint} - {error_msg}")
                
                self.results['issues'].append({
                    'service': service_name,
                    'endpoint': endpoint,
                    'url': result['url'],
                    'error': error_msg
                })
        
        return service_results

    def test_integrations(self):
        """Test service integrations"""
        print("Testing service integrations...")
        
        integrations = {}
        
        # Test Gateway -> Agent integration
        try:
            gateway_url = self.services['gateway']['production']
            response = requests.get(
                f"{gateway_url}/v1/match/1/top",
                headers={"Authorization": f"Bearer {self.api_key}"},
                timeout=10
            )
            integrations['gateway_agent'] = {
                'success': response.status_code == 200,
                'status': response.status_code
            }
            print(f"  Gateway->Agent: {'OK' if response.status_code == 200 else 'FAIL'}")
        except Exception as e:
            integrations['gateway_agent'] = {'success': False, 'error': str(e)}
            print(f"  Gateway->Agent: FAIL - {str(e)}")
        
        # Test Client Portal authentication
        try:
            gateway_url = self.services['gateway']['production']
            login_data = {"client_id": "TECH001", "password": "demo123"}
            response = requests.post(f"{gateway_url}/v1/client/login", json=login_data, timeout=10)
            integrations['client_auth'] = {
                'success': response.status_code == 200,
                'status': response.status_code
            }
            print(f"  Client Auth: {'OK' if response.status_code == 200 else 'FAIL'}")
        except Exception as e:
            integrations['client_auth'] = {'success': False, 'error': str(e)}
            print(f"  Client Auth: FAIL - {str(e)}")
        
        return integrations

    def run_audit(self):
        """Run complete audit"""
        print("=" * 50)
        print("BHIV HR Platform Service Audit")
        print("=" * 50)
        
        # Test all services
        for service_name in self.services.keys():
            self.results['services'][service_name] = self.audit_service(service_name)
            print()
        
        # Test integrations
        self.results['integrations'] = self.test_integrations()
        
        # Generate summary
        self.generate_summary()
        
        return self.results

    def generate_summary(self):
        """Generate audit summary"""
        total_endpoints = sum(s['summary']['total'] for s in self.results['services'].values())
        total_success = sum(s['summary']['success'] for s in self.results['services'].values())
        total_failed = sum(s['summary']['failed'] for s in self.results['services'].values())
        
        self.results['summary'] = {
            'total_endpoints': total_endpoints,
            'successful': total_success,
            'failed': total_failed,
            'success_rate': round((total_success / total_endpoints) * 100, 1) if total_endpoints > 0 else 0,
            'total_issues': len(self.results['issues'])
        }

    def print_summary(self):
        """Print audit results"""
        print("=" * 50)
        print("AUDIT SUMMARY")
        print("=" * 50)
        
        summary = self.results['summary']
        print(f"Total Endpoints Tested: {summary['total_endpoints']}")
        print(f"Successful: {summary['successful']}")
        print(f"Failed: {summary['failed']}")
        print(f"Success Rate: {summary['success_rate']}%")
        print(f"Issues Found: {summary['total_issues']}")
        
        print("\nService Status:")
        for service, data in self.results['services'].items():
            s = data['summary']
            status = "HEALTHY" if s['failed'] == 0 else f"{s['failed']} ISSUES"
            print(f"  {service}: {s['success']}/{s['total']} - {status}")
        
        print("\nIntegration Status:")
        for integration, data in self.results['integrations'].items():
            status = "OK" if data['success'] else "FAIL"
            print(f"  {integration}: {status}")
        
        if self.results['issues']:
            print(f"\nIssues Found ({len(self.results['issues'])}):")
            for issue in self.results['issues']:
                print(f"  - {issue['service']}: {issue['endpoint']} - {issue['error']}")
        
        print("=" * 50)

if __name__ == "__main__":
    auditor = ServiceAuditor()
    results = auditor.run_audit()
    auditor.print_summary()
    
    # Save results
    with open('service_audit_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    print("Results saved to service_audit_results.json")