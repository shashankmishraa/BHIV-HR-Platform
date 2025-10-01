#!/usr/bin/env python3
"""
BHIV HR Platform - Integration & Reliability Test Suite
Tests service interconnections, data flow, and system reliability
"""

import requests
import json
import time
import asyncio
import concurrent.futures
from datetime import datetime, timedelta
from typing import Dict, List, Any
import psycopg2
import threading
import statistics

class IntegrationReliabilityTester:
    def __init__(self):
        self.base_urls = {
            'gateway': 'https://bhiv-hr-gateway-46pz.onrender.com',
            'agent': 'https://bhiv-hr-agent-m1me.onrender.com',
            'portal': 'https://bhiv-hr-portal-cead.onrender.com',
            'client_portal': 'https://bhiv-hr-client-portal-5g33.onrender.com'
        }
        
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        self.db_url = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
        
        self.test_results = {
            'timestamp': datetime.now().isoformat(),
            'reliability': {},
            'integration': {},
            'performance': {},
            'data_flow': {},
            'stress_test': {}
        }

    def test_service_reliability(self, service: str, duration_minutes: int = 5) -> Dict[str, Any]:
        """Test service reliability over time"""
        print(f"Testing {service} reliability for {duration_minutes} minutes...")
        
        results = {
            'service': service,
            'duration_minutes': duration_minutes,
            'total_requests': 0,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'error_types': {},
            'uptime_percentage': 0,
            'avg_response_time': 0,
            'max_response_time': 0,
            'min_response_time': float('inf')
        }
        
        base_url = self.base_urls[service]
        end_time = datetime.now() + timedelta(minutes=duration_minutes)
        
        while datetime.now() < end_time:
            start_time = time.time()
            
            try:
                response = requests.get(f"{base_url}/health", headers=self.headers, timeout=10)
                response_time = time.time() - start_time
                
                results['total_requests'] += 1
                results['response_times'].append(response_time)
                
                if response.status_code == 200:
                    results['successful_requests'] += 1
                else:
                    results['failed_requests'] += 1
                    error_type = f"HTTP_{response.status_code}"
                    results['error_types'][error_type] = results['error_types'].get(error_type, 0) + 1
                
                results['max_response_time'] = max(results['max_response_time'], response_time)
                results['min_response_time'] = min(results['min_response_time'], response_time)
                
            except Exception as e:
                results['total_requests'] += 1
                results['failed_requests'] += 1
                error_type = type(e).__name__
                results['error_types'][error_type] = results['error_types'].get(error_type, 0) + 1
            
            time.sleep(2)  # Test every 2 seconds
        
        # Calculate metrics
        if results['total_requests'] > 0:
            results['uptime_percentage'] = (results['successful_requests'] / results['total_requests']) * 100
        
        if results['response_times']:
            results['avg_response_time'] = statistics.mean(results['response_times'])
        
        return results

    def test_data_flow_integration(self) -> Dict[str, Any]:
        """Test complete data flow from job creation to candidate matching"""
        print("Testing complete data flow integration...")
        
        flow_results = {
            'steps': {},
            'total_time': 0,
            'success': False,
            'data_consistency': True,
            'errors': []
        }
        
        start_time = time.time()
        
        try:
            # Step 1: Create a job via Gateway
            job_data = {
                "title": "Integration Test Developer",
                "company": "Test Corp",
                "location": "Remote",
                "job_type": "Full-time",
                "experience_level": "Mid-level",
                "skills_required": "Python, FastAPI, Testing, Integration",
                "description": "Test job for integration testing workflow"
            }
            
            step_start = time.time()
            job_response = requests.post(
                f"{self.base_urls['gateway']}/v1/jobs",
                headers=self.headers,
                json=job_data,
                timeout=30
            )
            
            flow_results['steps']['job_creation'] = {
                'success': job_response.status_code == 201,
                'response_time': time.time() - step_start,
                'status_code': job_response.status_code
            }
            
            if job_response.status_code != 201:
                flow_results['errors'].append(f"Job creation failed: {job_response.status_code}")
                return flow_results
            
            job_id = job_response.json().get('id')
            
            # Step 2: Verify job exists in database
            step_start = time.time()
            db_job = self.verify_job_in_database(job_id)
            flow_results['steps']['database_verification'] = {
                'success': db_job is not None,
                'response_time': time.time() - step_start,
                'job_found': db_job is not None
            }
            
            # Step 3: Get candidates via Gateway
            step_start = time.time()
            candidates_response = requests.get(
                f"{self.base_urls['gateway']}/v1/candidates",
                headers=self.headers,
                timeout=30
            )
            
            flow_results['steps']['candidates_fetch'] = {
                'success': candidates_response.status_code == 200,
                'response_time': time.time() - step_start,
                'status_code': candidates_response.status_code,
                'candidate_count': len(candidates_response.json()) if candidates_response.status_code == 200 else 0
            }
            
            # Step 4: Test AI matching via Gateway
            step_start = time.time()
            match_response = requests.get(
                f"{self.base_urls['gateway']}/v1/match/{job_id}/top",
                headers=self.headers,
                timeout=30
            )
            
            flow_results['steps']['ai_matching'] = {
                'success': match_response.status_code == 200,
                'response_time': time.time() - step_start,
                'status_code': match_response.status_code
            }
            
            if match_response.status_code == 200:
                match_data = match_response.json()
                flow_results['steps']['ai_matching']['matches_found'] = len(match_data.get('candidates', []))
                flow_results['steps']['ai_matching']['processing_time'] = match_data.get('processing_time', 0)
            
            # Step 5: Test direct Agent service
            step_start = time.time()
            agent_response = requests.get(
                f"{self.base_urls['agent']}/health",
                headers=self.headers,
                timeout=30
            )
            
            flow_results['steps']['agent_direct'] = {
                'success': agent_response.status_code == 200,
                'response_time': time.time() - step_start,
                'status_code': agent_response.status_code
            }
            
            # Check overall success
            flow_results['success'] = all(
                step['success'] for step in flow_results['steps'].values()
            )
            
        except Exception as e:
            flow_results['errors'].append(f"Data flow test failed: {str(e)}")
        
        flow_results['total_time'] = time.time() - start_time
        return flow_results

    def verify_job_in_database(self, job_id: int) -> Dict[str, Any]:
        """Verify job exists in database"""
        try:
            conn = psycopg2.connect(self.db_url)
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM jobs WHERE id = %s", (job_id,))
            job = cursor.fetchone()
            
            conn.close()
            return job
            
        except Exception as e:
            print(f"Database verification failed: {e}")
            return None

    def test_concurrent_load(self, concurrent_users: int = 10, requests_per_user: int = 5) -> Dict[str, Any]:
        """Test system under concurrent load"""
        print(f"Testing concurrent load: {concurrent_users} users, {requests_per_user} requests each...")
        
        load_results = {
            'concurrent_users': concurrent_users,
            'requests_per_user': requests_per_user,
            'total_requests': concurrent_users * requests_per_user,
            'successful_requests': 0,
            'failed_requests': 0,
            'response_times': [],
            'errors': [],
            'throughput': 0,
            'avg_response_time': 0
        }
        
        def user_simulation(user_id: int) -> List[Dict[str, Any]]:
            """Simulate a user making multiple requests"""
            user_results = []
            
            for request_num in range(requests_per_user):
                start_time = time.time()
                
                try:
                    # Alternate between different endpoints
                    if request_num % 3 == 0:
                        response = requests.get(f"{self.base_urls['gateway']}/health", headers=self.headers, timeout=10)
                    elif request_num % 3 == 1:
                        response = requests.get(f"{self.base_urls['gateway']}/v1/jobs", headers=self.headers, timeout=10)
                    else:
                        response = requests.get(f"{self.base_urls['agent']}/health", headers=self.headers, timeout=10)
                    
                    response_time = time.time() - start_time
                    
                    user_results.append({
                        'user_id': user_id,
                        'request_num': request_num,
                        'success': 200 <= response.status_code < 300,
                        'response_time': response_time,
                        'status_code': response.status_code
                    })
                    
                except Exception as e:
                    user_results.append({
                        'user_id': user_id,
                        'request_num': request_num,
                        'success': False,
                        'response_time': time.time() - start_time,
                        'error': str(e)
                    })
            
            return user_results
        
        # Execute concurrent requests
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            futures = [executor.submit(user_simulation, user_id) for user_id in range(concurrent_users)]
            
            for future in concurrent.futures.as_completed(futures):
                try:
                    user_results = future.result()
                    
                    for result in user_results:
                        if result['success']:
                            load_results['successful_requests'] += 1
                        else:
                            load_results['failed_requests'] += 1
                            if 'error' in result:
                                load_results['errors'].append(result['error'])
                        
                        load_results['response_times'].append(result['response_time'])
                        
                except Exception as e:
                    load_results['errors'].append(f"User simulation failed: {str(e)}")
        
        total_time = time.time() - start_time
        
        # Calculate metrics
        if load_results['response_times']:
            load_results['avg_response_time'] = statistics.mean(load_results['response_times'])
        
        if total_time > 0:
            load_results['throughput'] = load_results['total_requests'] / total_time
        
        return load_results

    def test_service_interconnections(self) -> Dict[str, Any]:
        """Test interconnections between services"""
        print("Testing service interconnections...")
        
        interconnection_results = {
            'gateway_to_agent': False,
            'gateway_to_database': False,
            'agent_to_database': False,
            'portal_to_gateway': False,
            'client_portal_to_gateway': False,
            'response_times': {},
            'errors': []
        }
        
        # Test Gateway to Agent (via matching endpoint)
        try:
            # First create a job to test matching
            job_response = requests.post(
                f"{self.base_urls['gateway']}/v1/jobs",
                headers=self.headers,
                json={
                    "title": "Interconnection Test Job",
                    "company": "Test Company",
                    "location": "Remote",
                    "job_type": "Full-time",
                    "experience_level": "Mid-level",
                    "skills_required": "Python, Testing",
                    "description": "Test job for interconnection testing"
                },
                timeout=30
            )
            
            if job_response.status_code == 201:
                job_id = job_response.json().get('id')
                
                start_time = time.time()
                match_response = requests.get(
                    f"{self.base_urls['gateway']}/v1/match/{job_id}/top",
                    headers=self.headers,
                    timeout=30
                )
                
                interconnection_results['gateway_to_agent'] = match_response.status_code == 200
                interconnection_results['response_times']['gateway_to_agent'] = time.time() - start_time
                
        except Exception as e:
            interconnection_results['errors'].append(f"Gateway to Agent test failed: {str(e)}")
        
        # Test Gateway to Database (via candidates endpoint)
        try:
            start_time = time.time()
            candidates_response = requests.get(
                f"{self.base_urls['gateway']}/v1/candidates",
                headers=self.headers,
                timeout=30
            )
            
            interconnection_results['gateway_to_database'] = candidates_response.status_code == 200
            interconnection_results['response_times']['gateway_to_database'] = time.time() - start_time
            
        except Exception as e:
            interconnection_results['errors'].append(f"Gateway to Database test failed: {str(e)}")
        
        # Test Agent to Database (direct health check)
        try:
            start_time = time.time()
            agent_response = requests.get(
                f"{self.base_urls['agent']}/health",
                headers=self.headers,
                timeout=30
            )
            
            interconnection_results['agent_to_database'] = agent_response.status_code == 200
            interconnection_results['response_times']['agent_to_database'] = time.time() - start_time
            
        except Exception as e:
            interconnection_results['errors'].append(f"Agent to Database test failed: {str(e)}")
        
        # Test Portal accessibility
        try:
            start_time = time.time()
            portal_response = requests.get(self.base_urls['portal'], timeout=30)
            
            interconnection_results['portal_to_gateway'] = portal_response.status_code == 200
            interconnection_results['response_times']['portal_to_gateway'] = time.time() - start_time
            
        except Exception as e:
            interconnection_results['errors'].append(f"Portal accessibility test failed: {str(e)}")
        
        # Test Client Portal accessibility
        try:
            start_time = time.time()
            client_portal_response = requests.get(self.base_urls['client_portal'], timeout=30)
            
            interconnection_results['client_portal_to_gateway'] = client_portal_response.status_code == 200
            interconnection_results['response_times']['client_portal_to_gateway'] = time.time() - start_time
            
        except Exception as e:
            interconnection_results['errors'].append(f"Client Portal accessibility test failed: {str(e)}")
        
        return interconnection_results

    def run_integration_reliability_test(self) -> Dict[str, Any]:
        """Run complete integration and reliability test suite"""
        print("Starting Integration & Reliability Test Suite")
        print("=" * 60)
        
        # 1. Test service reliability (shorter duration for demo)
        print("\n1. Testing Service Reliability...")
        self.test_results['reliability']['gateway'] = self.test_service_reliability('gateway', 2)
        self.test_results['reliability']['agent'] = self.test_service_reliability('agent', 2)
        
        # 2. Test data flow integration
        print("\n2. Testing Data Flow Integration...")
        self.test_results['integration']['data_flow'] = self.test_data_flow_integration()
        
        # 3. Test service interconnections
        print("\n3. Testing Service Interconnections...")
        self.test_results['integration']['interconnections'] = self.test_service_interconnections()
        
        # 4. Test concurrent load
        print("\n4. Testing Concurrent Load...")
        self.test_results['performance']['concurrent_load'] = self.test_concurrent_load(5, 3)  # Reduced for demo
        
        return self.test_results

    def print_results(self):
        """Print formatted test results"""
        print("\n" + "=" * 60)
        print("INTEGRATION & RELIABILITY TEST RESULTS")
        print("=" * 60)
        
        # Reliability Results
        print(f"\nRELIABILITY:")
        for service, results in self.test_results['reliability'].items():
            uptime = results['uptime_percentage']
            avg_time = results['avg_response_time']
            status = "[OK]" if uptime >= 95 else "[WARN]" if uptime >= 80 else "[FAIL]"
            print(f"   {service}: {status} {uptime:.1f}% uptime, {avg_time:.3f}s avg response")
        
        # Integration Results
        print(f"\nINTEGRATION:")
        data_flow = self.test_results['integration']['data_flow']
        print(f"   Data Flow: {'[OK]' if data_flow['success'] else '[FAIL]'} ({data_flow['total_time']:.2f}s)")
        
        interconnections = self.test_results['integration']['interconnections']
        print(f"   Gateway ↔ Agent: {'✅' if interconnections['gateway_to_agent'] else '❌'}")
        print(f"   Gateway ↔ Database: {'✅' if interconnections['gateway_to_database'] else '❌'}")
        print(f"   Portal Access: {'✅' if interconnections['portal_to_gateway'] else '❌'}")
        
        # Performance Results
        print(f"\nPERFORMANCE:")
        load_test = self.test_results['performance']['concurrent_load']
        success_rate = (load_test['successful_requests'] / load_test['total_requests']) * 100
        print(f"   Concurrent Load: {success_rate:.1f}% success rate")
        print(f"   Throughput: {load_test['throughput']:.2f} req/sec")
        print(f"   Avg Response: {load_test['avg_response_time']:.3f}s")
        
        print("\n" + "=" * 60)

def main():
    """Run integration and reliability tests"""
    tester = IntegrationReliabilityTester()
    
    try:
        results = tester.run_integration_reliability_test()
        tester.print_results()
        
        # Save results
        with open('integration_reliability_results.json', 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: integration_reliability_results.json")
        
        return results
        
    except Exception as e:
        print(f"ERROR: Test execution failed: {str(e)}")
        return None

if __name__ == "__main__":
    main()