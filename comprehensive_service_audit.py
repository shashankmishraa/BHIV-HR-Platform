#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Service Connection & Routing Audit
Performs systematic verification of all service endpoints, routing, and integrations
"""

import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import concurrent.futures
import os

class ServiceAuditor:
    def __init__(self):
        self.results = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            'routing_tests': {},
            'integration_tests': {},
            'issues': [],
            'recommendations': []
        }
        
        # Service configurations
        self.services = {
            'gateway': {
                'local': 'http://localhost:8000',
                'production': 'https://bhiv-hr-gateway-46pz.onrender.com',
                'endpoints': [
                    '/', '/health', '/docs', '/metrics', '/health/detailed',
                    '/v1/jobs', '/v1/candidates', '/v1/candidates/search',
                    '/v1/match/1/top', '/v1/feedback', '/v1/interviews', '/v1/offers',
                    '/v1/client/login', '/v1/security/rate-limit-status'
                ]
            },
            'agent': {
                'local': 'http://localhost:9000',
                'production': 'https://bhiv-hr-agent-m1me.onrender.com',
                'endpoints': [
                    '/', '/health', '/docs', '/test-db', '/match', '/analyze/1'
                ]
            },
            'portal': {
                'local': 'http://localhost:8501',
                'production': 'https://bhiv-hr-portal-cead.onrender.com',
                'endpoints': [
                    '/', '/_stcore/health'
                ]
            },
            'client_portal': {
                'local': 'http://localhost:8502',
                'production': 'https://bhiv-hr-client-portal-5g33.onrender.com',
                'endpoints': [
                    '/', '/_stcore/health'
                ]
            }
        }
        
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def test_endpoint(self, service: str, env: str, endpoint: str) -> Dict:
        """Test individual endpoint connectivity and response"""
        base_url = self.services[service][env]
        full_url = f"{base_url}{endpoint}"
        
        try:
            # Use appropriate headers for authenticated endpoints
            headers = self.headers if endpoint.startswith('/v1/') else {}
            
            start_time = time.time()
            response = requests.get(full_url, headers=headers, timeout=10)
            response_time = time.time() - start_time
            
            return {
                'url': full_url,
                'status_code': response.status_code,
                'response_time': round(response_time, 3),
                'success': response.status_code < 400,
                'content_type': response.headers.get('content-type', ''),
                'error': None
            }
        except requests.exceptions.RequestException as e:
            return {
                'url': full_url,
                'status_code': None,
                'response_time': None,
                'success': False,
                'content_type': None,
                'error': str(e)
            }

    def audit_service_endpoints(self, service: str, env: str) -> Dict:
        """Audit all endpoints for a specific service"""
        print(f"🔍 Auditing {service} service ({env})...")
        
        service_results = {
            'service': service,
            'environment': env,
            'base_url': self.services[service][env],
            'endpoints': {},
            'summary': {'total': 0, 'success': 0, 'failed': 0}
        }
        
        for endpoint in self.services[service]['endpoints']:
            result = self.test_endpoint(service, env, endpoint)
            service_results['endpoints'][endpoint] = result
            service_results['summary']['total'] += 1
            
            if result['success']:
                service_results['summary']['success'] += 1
                print(f"  ✅ {endpoint}: {result['status_code']} ({result['response_time']}s)")
            else:
                service_results['summary']['failed'] += 1
                print(f"  ❌ {endpoint}: {result.get('error', 'HTTP ' + str(result.get('status_code', 'Error')))}")
                
                self.results['issues'].append({
                    'type': 'endpoint_failure',
                    'service': service,
                    'environment': env,
                    'endpoint': endpoint,
                    'url': result['url'],
                    'error': result.get('error', f"HTTP {result.get('status_code')}")
                })
        
        return service_results

    def test_service_integration(self) -> Dict:
        """Test integration between services"""
        print("🔗 Testing service integrations...")
        
        integration_results = {
            'gateway_to_agent': self.test_gateway_agent_integration(),
            'portal_to_gateway': self.test_portal_gateway_integration(),
            'client_portal_to_gateway': self.test_client_portal_gateway_integration()
        }
        
        return integration_results

    def test_gateway_agent_integration(self) -> Dict:
        """Test Gateway -> Agent communication"""
        try:
            # Test if Gateway can communicate with Agent for matching
            gateway_url = self.services['gateway']['production']
            response = requests.get(
                f"{gateway_url}/v1/match/1/top",
                headers=self.headers,
                timeout=10
            )
            
            return {
                'test': 'Gateway -> Agent matching',
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'response_time': response.elapsed.total_seconds(),
                'data_received': len(response.text) > 0
            }
        except Exception as e:
            return {
                'test': 'Gateway -> Agent matching',
                'success': False,
                'error': str(e)
            }

    def test_portal_gateway_integration(self) -> Dict:
        """Test Portal -> Gateway communication"""
        try:
            # Test if Portal can access Gateway endpoints
            gateway_url = self.services['gateway']['production']
            response = requests.get(f"{gateway_url}/health", timeout=10)
            
            return {
                'test': 'Portal -> Gateway health check',
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'gateway_accessible': True
            }
        except Exception as e:
            return {
                'test': 'Portal -> Gateway health check',
                'success': False,
                'error': str(e),
                'gateway_accessible': False
            }

    def test_client_portal_gateway_integration(self) -> Dict:
        """Test Client Portal -> Gateway communication"""
        try:
            # Test client login endpoint
            gateway_url = self.services['gateway']['production']
            login_data = {"client_id": "TECH001", "password": "demo123"}
            
            response = requests.post(
                f"{gateway_url}/v1/client/login",
                json=login_data,
                timeout=10
            )
            
            return {
                'test': 'Client Portal -> Gateway login',
                'success': response.status_code == 200,
                'status_code': response.status_code,
                'authentication_working': response.status_code == 200
            }
        except Exception as e:
            return {
                'test': 'Client Portal -> Gateway login',
                'success': False,
                'error': str(e),
                'authentication_working': False
            }

    def analyze_routing_configuration(self) -> Dict:
        """Analyze routing configurations in each service"""
        print("🛣️  Analyzing routing configurations...")
        
        routing_analysis = {
            'gateway_routes': self.analyze_gateway_routes(),
            'agent_routes': self.analyze_agent_routes(),
            'portal_routes': self.analyze_portal_routes(),
            'docker_networking': self.analyze_docker_networking()
        }
        
        return routing_analysis

    def analyze_gateway_routes(self) -> Dict:
        """Analyze Gateway service routing"""
        try:
            gateway_url = self.services['gateway']['production']
            response = requests.get(f"{gateway_url}/docs", timeout=10)
            
            # Check if OpenAPI docs are accessible
            docs_accessible = response.status_code == 200
            
            # Test key route patterns
            route_tests = {
                'core_routes': self.test_endpoint('gateway', 'production', '/'),
                'api_v1_routes': self.test_endpoint('gateway', 'production', '/v1/jobs'),
                'monitoring_routes': self.test_endpoint('gateway', 'production', '/metrics'),
                'security_routes': self.test_endpoint('gateway', 'production', '/v1/security/rate-limit-status')
            }
            
            return {
                'docs_accessible': docs_accessible,
                'route_patterns': route_tests,
                'total_endpoints': 48,
                'routing_health': all(test['success'] for test in route_tests.values())
            }
        except Exception as e:
            return {'error': str(e), 'routing_health': False}

    def analyze_agent_routes(self) -> Dict:
        """Analyze Agent service routing"""
        try:
            agent_url = self.services['agent']['production']
            response = requests.get(f"{agent_url}/docs", timeout=10)
            
            docs_accessible = response.status_code == 200
            
            route_tests = {
                'core_routes': self.test_endpoint('agent', 'production', '/'),
                'health_routes': self.test_endpoint('agent', 'production', '/health'),
                'ai_routes': self.test_endpoint('agent', 'production', '/analyze/1')
            }
            
            return {
                'docs_accessible': docs_accessible,
                'route_patterns': route_tests,
                'total_endpoints': 5,
                'routing_health': all(test['success'] for test in route_tests.values())
            }
        except Exception as e:
            return {'error': str(e), 'routing_health': False}

    def analyze_portal_routes(self) -> Dict:
        """Analyze Portal routing"""
        portal_tests = {
            'hr_portal': self.test_endpoint('portal', 'production', '/'),
            'client_portal': self.test_endpoint('client_portal', 'production', '/')
        }
        
        return {
            'streamlit_apps': portal_tests,
            'routing_health': all(test['success'] for test in portal_tests.values())
        }

    def analyze_docker_networking(self) -> Dict:
        """Analyze Docker networking configuration"""
        # Read docker-compose file to analyze networking
        try:
            with open('docker-compose.production.yml', 'r') as f:
                content = f.read()
                
            networking_config = {
                'services_defined': 'gateway:' in content and 'agent:' in content,
                'port_mappings': '8000:8000' in content and '9000:9000' in content,
                'health_checks': 'healthcheck:' in content,
                'dependencies': 'depends_on:' in content,
                'environment_vars': 'DATABASE_URL:' in content
            }
            
            return {
                'docker_compose_valid': all(networking_config.values()),
                'configuration': networking_config
            }
        except Exception as e:
            return {'error': str(e), 'docker_compose_valid': False}

    def generate_recommendations(self):
        """Generate recommendations based on audit findings"""
        print("💡 Generating recommendations...")
        
        # Analyze issues and generate recommendations
        if len(self.results['issues']) == 0:
            self.results['recommendations'].append({
                'priority': 'info',
                'category': 'overall',
                'recommendation': 'All services are functioning correctly with no critical issues found.'
            })
        
        # Check for common issues
        failed_endpoints = [issue for issue in self.results['issues'] if issue['type'] == 'endpoint_failure']
        
        if failed_endpoints:
            self.results['recommendations'].append({
                'priority': 'high',
                'category': 'connectivity',
                'recommendation': f'Fix {len(failed_endpoints)} failed endpoints. Check service health and network connectivity.',
                'affected_endpoints': [issue['url'] for issue in failed_endpoints]
            })
        
        # Performance recommendations
        slow_endpoints = []
        for service_name, service_data in self.results['services'].items():
            if isinstance(service_data, dict) and 'endpoints' in service_data:
                for endpoint, data in service_data['endpoints'].items():
                    if data.get('response_time', 0) > 2.0:
                        slow_endpoints.append(f"{service_name}{endpoint}")
        
        if slow_endpoints:
            self.results['recommendations'].append({
                'priority': 'medium',
                'category': 'performance',
                'recommendation': 'Optimize slow endpoints (>2s response time)',
                'affected_endpoints': slow_endpoints
            })

    def run_comprehensive_audit(self):
        """Run complete service audit"""
        print("🚀 Starting Comprehensive Service Audit...")
        print("=" * 60)
        
        # Test all services in both environments
        for env in ['production']:  # Focus on production for now
            for service in self.services.keys():
                service_results = self.audit_service_endpoints(service, env)
                self.results['services'][f"{service}_{env}"] = service_results
        
        # Test integrations
        self.results['integration_tests'] = self.test_service_integration()
        
        # Analyze routing
        self.results['routing_tests'] = self.analyze_routing_configuration()
        
        # Generate recommendations
        self.generate_recommendations()
        
        return self.results

    def save_audit_report(self):
        """Save audit results to file"""
        filename = f"service_audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n📄 Audit report saved to: {filename}")
        return filename

    def print_summary(self):
        """Print audit summary"""
        print("\n" + "=" * 60)
        print("📊 AUDIT SUMMARY")
        print("=" * 60)
        
        total_services = len([k for k in self.results['services'].keys()])
        total_issues = len(self.results['issues'])
        
        print(f"Services Audited: {total_services}")
        print(f"Issues Found: {total_issues}")
        print(f"Recommendations: {len(self.results['recommendations'])}")
        
        # Service status summary
        print("\n🔍 Service Status:")
        for service_key, service_data in self.results['services'].items():
            if isinstance(service_data, dict) and 'summary' in service_data:
                summary = service_data['summary']
                status = "✅ HEALTHY" if summary['failed'] == 0 else f"⚠️  {summary['failed']} ISSUES"
                print(f"  {service_key}: {summary['success']}/{summary['total']} endpoints - {status}")
        
        # Integration status
        print("\n🔗 Integration Status:")
        if 'integration_tests' in self.results:
            for test_name, test_result in self.results['integration_tests'].items():
                status = "✅ WORKING" if test_result.get('success', False) else "❌ FAILED"
                print(f"  {test_name}: {status}")
        
        # Critical issues
        if self.results['issues']:
            print(f"\n⚠️  Critical Issues ({len(self.results['issues'])}):")
            for issue in self.results['issues'][:5]:  # Show first 5
                print(f"  - {issue['service']} ({issue['environment']}): {issue['endpoint']} - {issue['error']}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    auditor = ServiceAuditor()
    results = auditor.run_comprehensive_audit()
    auditor.print_summary()
    report_file = auditor.save_audit_report()