#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Dynamic System Test
Scans codebase and tests all live services with real data and integration testing
"""

import requests
import json
import time
import psycopg2
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Tuple
import re
import ast
import inspect
from pathlib import Path

class ComprehensiveSystemTester:
    def __init__(self):
        self.base_urls = {
            'gateway': 'https://bhiv-hr-gateway-46pz.onrender.com',
            'agent': 'https://bhiv-hr-agent-m1me.onrender.com',
            'portal': 'https://bhiv-hr-portal-cead.onrender.com',
            'client_portal': 'https://bhiv-hr-client-portal-5g33.onrender.com'
        }
        
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Database connection
        self.db_url = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
        
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'services': {},
            'database': {},
            'integration': {},
            'endpoints': {},
            'summary': {}
        }

    def scan_codebase_endpoints(self) -> Dict[str, List[str]]:
        """Dynamically scan codebase for all API endpoints"""
        print("Scanning codebase for endpoints...")
        
        endpoints = {
            'gateway': [],
            'agent': [],
            'portal': [],
            'client_portal': []
        }
        
        # Scan gateway endpoints
        gateway_file = Path("services/gateway/app/main.py")
        if gateway_file.exists():
            with open(gateway_file, 'r') as f:
                content = f.read()
                # Find FastAPI route decorators
                routes = re.findall(r'@app\.(get|post|put|delete|patch)\("([^"]+)"', content)
                endpoints['gateway'] = [f"{method.upper()} {path}" for method, path in routes]
        
        # Scan agent endpoints
        agent_file = Path("services/agent/app.py")
        if agent_file.exists():
            with open(agent_file, 'r') as f:
                content = f.read()
                routes = re.findall(r'@app\.(get|post|put|delete|patch)\("([^"]+)"', content)
                endpoints['agent'] = [f"{method.upper()} {path}" for method, path in routes]
        
        print(f"Found {sum(len(eps) for eps in endpoints.values())} endpoints")
        return endpoints

    def test_database_connectivity(self) -> Dict[str, Any]:
        """Test database connectivity and data integrity"""
        print("Testing database connectivity and data...")
        
        db_results = {
            'connection': False,
            'tables': {},
            'data_counts': {},
            'sample_data': {},
            'errors': []
        }
        
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            db_results['connection'] = True
            
            # Test table existence and counts
            tables = ['candidates', 'jobs', 'job_applications', 'users', 'clients']
            
            for table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    db_results['data_counts'][table] = count
                    
                    # Get sample data
                    cursor.execute(f"SELECT * FROM {table} LIMIT 3")
                    columns = [desc[0] for desc in cursor.description]
                    rows = cursor.fetchall()
                    db_results['sample_data'][table] = {
                        'columns': columns,
                        'sample_rows': len(rows),
                        'has_data': len(rows) > 0
                    }
                    
                except Exception as e:
                    db_results['errors'].append(f"Table {table}: {str(e)}")
            
            # Test data relationships
            try:
                cursor.execute("""
                    SELECT j.id, j.title, COUNT(c.id) as candidate_count
                    FROM jobs j 
                    LEFT JOIN candidates c ON true 
                    GROUP BY j.id, j.title 
                    LIMIT 5
                """)
                relationships = cursor.fetchall()
                db_results['relationships'] = len(relationships)
            except Exception as e:
                db_results['errors'].append(f"Relationships test: {str(e)}")
            
            conn.close()
            
        except Exception as e:
            db_results['errors'].append(f"Connection failed: {str(e)}")
        
        return db_results

    def test_service_endpoints(self, service: str, endpoints: List[str]) -> Dict[str, Any]:
        """Test all endpoints for a service with dynamic data"""
        print(f"Testing {service} service endpoints...")
        
        service_results = {
            'service': service,
            'base_url': self.base_urls[service],
            'endpoints_tested': 0,
            'endpoints_passed': 0,
            'endpoints_failed': 0,
            'response_times': [],
            'detailed_results': {}
        }
        
        base_url = self.base_urls[service]
        
        # Test basic health endpoints
        health_endpoints = [
            ('GET', '/health', {}),
            ('GET', '/', {}),
        ]
        
        # Test gateway-specific endpoints with real data
        if service == 'gateway':
            gateway_endpoints = [
                ('GET', '/v1/jobs', {}),
                ('GET', '/v1/candidates', {}),
                ('GET', '/v1/candidates/stats', {}),
                ('POST', '/v1/jobs', {
                    "title": "Test Software Engineer",
                    "company": "Test Company",
                    "location": "Remote",
                    "job_type": "Full-time",
                    "experience_level": "Mid-level",
                    "skills_required": "Python, FastAPI, PostgreSQL",
                    "description": "Test job for system testing"
                }),
                ('GET', '/metrics', {}),
                ('GET', '/health/detailed', {}),
            ]
            health_endpoints.extend(gateway_endpoints)
        
        # Test agent-specific endpoints
        elif service == 'agent':
            agent_endpoints = [
                ('GET', '/candidates', {}),
                ('GET', '/jobs', {}),
            ]
            health_endpoints.extend(agent_endpoints)
        
        for method, endpoint, payload in health_endpoints:
            start_time = time.time()
            
            try:
                url = f"{base_url}{endpoint}"
                
                if method == 'GET':
                    response = requests.get(url, headers=self.headers, timeout=30)
                elif method == 'POST':
                    response = requests.post(url, headers=self.headers, json=payload, timeout=30)
                else:
                    continue
                
                response_time = time.time() - start_time
                service_results['response_times'].append(response_time)
                
                result = {
                    'method': method,
                    'endpoint': endpoint,
                    'status_code': response.status_code,
                    'response_time': response_time,
                    'success': 200 <= response.status_code < 300,
                    'response_size': len(response.content),
                    'content_type': response.headers.get('content-type', 'unknown')
                }
                
                # Parse response content
                try:
                    if 'application/json' in result['content_type']:
                        json_data = response.json()
                        result['response_data'] = {
                            'type': 'json',
                            'keys': list(json_data.keys()) if isinstance(json_data, dict) else 'array',
                            'data_count': len(json_data) if isinstance(json_data, (list, dict)) else 1
                        }
                    else:
                        result['response_data'] = {
                            'type': 'text',
                            'length': len(response.text)
                        }
                except:
                    result['response_data'] = {'type': 'unknown'}
                
                service_results['detailed_results'][f"{method} {endpoint}"] = result
                
                if result['success']:
                    service_results['endpoints_passed'] += 1
                else:
                    service_results['endpoints_failed'] += 1
                
                service_results['endpoints_tested'] += 1
                
            except Exception as e:
                service_results['detailed_results'][f"{method} {endpoint}"] = {
                    'method': method,
                    'endpoint': endpoint,
                    'error': str(e),
                    'success': False
                }
                service_results['endpoints_failed'] += 1
                service_results['endpoints_tested'] += 1
        
        return service_results

    def test_ai_matching_integration(self) -> Dict[str, Any]:
        """Test AI matching integration with real data"""
        print("Testing AI matching integration...")
        
        integration_results = {
            'job_creation': False,
            'candidate_matching': False,
            'match_quality': {},
            'performance': {},
            'errors': []
        }
        
        try:
            # Create a test job
            job_data = {
                "title": "Senior Python Developer",
                "company": "Tech Innovations Inc",
                "location": "San Francisco, CA",
                "job_type": "Full-time",
                "experience_level": "Senior",
                "skills_required": "Python, Django, PostgreSQL, AWS, Docker",
                "description": "Looking for an experienced Python developer with strong backend skills"
            }
            
            response = requests.post(
                f"{self.base_urls['gateway']}/v1/jobs",
                headers=self.headers,
                json=job_data,
                timeout=30
            )
            
            if response.status_code == 201:
                integration_results['job_creation'] = True
                job_id = response.json().get('id')
                
                # Test AI matching
                if job_id:
                    match_response = requests.get(
                        f"{self.base_urls['gateway']}/v1/match/{job_id}/top",
                        headers=self.headers,
                        timeout=30
                    )
                    
                    if match_response.status_code == 200:
                        integration_results['candidate_matching'] = True
                        match_data = match_response.json()
                        
                        integration_results['match_quality'] = {
                            'candidates_found': len(match_data.get('candidates', [])),
                            'avg_score': sum(c.get('score', 0) for c in match_data.get('candidates', [])) / max(1, len(match_data.get('candidates', []))),
                            'processing_time': match_data.get('processing_time', 0)
                        }
            
        except Exception as e:
            integration_results['errors'].append(f"AI matching test failed: {str(e)}")
        
        return integration_results

    def test_portal_integration(self) -> Dict[str, Any]:
        """Test portal accessibility and basic functionality"""
        print("Testing portal integration...")
        
        portal_results = {
            'hr_portal': {'accessible': False, 'response_time': 0},
            'client_portal': {'accessible': False, 'response_time': 0},
            'errors': []
        }
        
        # Test HR Portal
        try:
            start_time = time.time()
            response = requests.get(self.base_urls['portal'], timeout=30)
            portal_results['hr_portal'] = {
                'accessible': response.status_code == 200,
                'response_time': time.time() - start_time,
                'status_code': response.status_code
            }
        except Exception as e:
            portal_results['errors'].append(f"HR Portal: {str(e)}")
        
        # Test Client Portal
        try:
            start_time = time.time()
            response = requests.get(self.base_urls['client_portal'], timeout=30)
            portal_results['client_portal'] = {
                'accessible': response.status_code == 200,
                'response_time': time.time() - start_time,
                'status_code': response.status_code
            }
        except Exception as e:
            portal_results['errors'].append(f"Client Portal: {str(e)}")
        
        return portal_results

    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run complete system test"""
        print("Starting Comprehensive System Test")
        print("=" * 60)
        
        # 1. Scan codebase for endpoints
        endpoints = self.scan_codebase_endpoints()
        
        # 2. Test database
        self.test_results['database'] = self.test_database_connectivity()
        
        # 3. Test each service
        for service in ['gateway', 'agent']:
            self.test_results['services'][service] = self.test_service_endpoints(
                service, endpoints.get(service, [])
            )
        
        # 4. Test AI integration
        self.test_results['integration']['ai_matching'] = self.test_ai_matching_integration()
        
        # 5. Test portals
        self.test_results['integration']['portals'] = self.test_portal_integration()
        
        # 6. Generate summary
        self.generate_summary()
        
        return self.test_results

    def generate_summary(self):
        """Generate test summary"""
        summary = {
            'total_services_tested': len(self.test_results['services']),
            'services_healthy': 0,
            'database_healthy': self.test_results['database']['connection'],
            'total_endpoints_tested': 0,
            'total_endpoints_passed': 0,
            'avg_response_time': 0,
            'critical_issues': [],
            'recommendations': []
        }
        
        # Analyze service results
        total_response_times = []
        for service, results in self.test_results['services'].items():
            if results['endpoints_passed'] > results['endpoints_failed']:
                summary['services_healthy'] += 1
            
            summary['total_endpoints_tested'] += results['endpoints_tested']
            summary['total_endpoints_passed'] += results['endpoints_passed']
            total_response_times.extend(results['response_times'])
        
        if total_response_times:
            summary['avg_response_time'] = sum(total_response_times) / len(total_response_times)
        
        # Check for critical issues
        if not summary['database_healthy']:
            summary['critical_issues'].append("Database connectivity failed")
        
        if summary['services_healthy'] < summary['total_services_tested']:
            summary['critical_issues'].append("Some services are unhealthy")
        
        # Generate recommendations
        if summary['avg_response_time'] > 2.0:
            summary['recommendations'].append("Consider optimizing response times")
        
        if summary['total_endpoints_passed'] < summary['total_endpoints_tested']:
            summary['recommendations'].append("Fix failing endpoints")
        
        self.test_results['summary'] = summary

    def print_results(self):
        """Print formatted test results"""
        print("\n" + "=" * 60)
        print("COMPREHENSIVE SYSTEM TEST RESULTS")
        print("=" * 60)
        
        # Summary
        summary = self.test_results['summary']
        print(f"\nSUMMARY:")
        print(f"   Services Tested: {summary['total_services_tested']}")
        print(f"   Services Healthy: {summary['services_healthy']}")
        print(f"   Database Healthy: {'[OK]' if summary['database_healthy'] else '[FAIL]'}")
        print(f"   Endpoints Tested: {summary['total_endpoints_tested']}")
        print(f"   Endpoints Passed: {summary['total_endpoints_passed']}")
        print(f"   Average Response Time: {summary['avg_response_time']:.3f}s")
        
        # Database Results
        print(f"\nDATABASE:")
        db = self.test_results['database']
        print(f"   Connection: {'[OK]' if db['connection'] else '[FAIL]'}")
        for table, count in db.get('data_counts', {}).items():
            print(f"   {table}: {count} records")
        
        # Service Results
        print(f"\nSERVICES:")
        for service, results in self.test_results['services'].items():
            status = "[OK]" if results['endpoints_passed'] > results['endpoints_failed'] else "[FAIL]"
            print(f"   {service}: {status} ({results['endpoints_passed']}/{results['endpoints_tested']} passed)")
        
        # Integration Results
        print(f"\nINTEGRATION:")
        ai = self.test_results['integration'].get('ai_matching', {})
        print(f"   AI Matching: {'[OK]' if ai.get('candidate_matching') else '[FAIL]'}")
        
        portals = self.test_results['integration'].get('portals', {})
        hr_status = "[OK]" if portals.get('hr_portal', {}).get('accessible') else "[FAIL]"
        client_status = "[OK]" if portals.get('client_portal', {}).get('accessible') else "[FAIL]"
        print(f"   HR Portal: {hr_status}")
        print(f"   Client Portal: {client_status}")
        
        # Issues and Recommendations
        if summary['critical_issues']:
            print(f"\nCRITICAL ISSUES:")
            for issue in summary['critical_issues']:
                print(f"   • {issue}")
        
        if summary['recommendations']:
            print(f"\nRECOMMENDATIONS:")
            for rec in summary['recommendations']:
                print(f"   • {rec}")
        
        print("\n" + "=" * 60)

def main():
    """Run comprehensive system test"""
    tester = ComprehensiveSystemTester()
    
    try:
        results = tester.run_comprehensive_test()
        tester.print_results()
        
        # Save results to file
        with open('comprehensive_test_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: comprehensive_test_results.json")
        
        return results
        
    except Exception as e:
        print(f"ERROR: Test execution failed: {str(e)}")
        return None

if __name__ == "__main__":
    main()