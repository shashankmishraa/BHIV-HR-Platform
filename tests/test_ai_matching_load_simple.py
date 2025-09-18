#!/usr/bin/env python3
"""
BHIV HR Platform - Simplified AI Matching Load Test
Basic load testing for AI matching endpoints with concurrent requests
"""

import asyncio
import aiohttp
import time
import statistics
from datetime import datetime
from typing import List, Dict, Any

class SimpleAIMatchingLoadTester:
    """Simplified load tester for AI matching endpoints"""
    
    def __init__(self):
        self.base_url = "https://bhiv-hr-gateway.onrender.com"
        self.api_key = "myverysecureapikey123"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Performance thresholds
        self.thresholds = {
            'avg_response_time': 3.0,  # seconds
            'error_rate': 0.1,  # 10%
            'min_throughput': 5.0,  # requests per second
        }
    
    async def make_ai_matching_request(self, session: aiohttp.ClientSession, job_id: int, user_id: int) -> Dict[str, Any]:
        """Make single AI matching request"""
        url = f"{self.base_url}/v1/match/{job_id}/top"
        start_time = time.time()
        
        try:
            async with session.get(url, headers=self.headers, timeout=30) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    candidates_count = len(data.get('matches', data.get('top_candidates', [])))
                    
                    return {
                        'success': True,
                        'response_time': response_time,
                        'status_code': response.status,
                        'candidates_returned': candidates_count,
                        'job_id': job_id,
                        'user_id': user_id
                    }
                else:
                    return {
                        'success': False,
                        'response_time': response_time,
                        'status_code': response.status,
                        'error': f"HTTP {response.status}",
                        'job_id': job_id,
                        'user_id': user_id
                    }
                    
        except asyncio.TimeoutError:
            return {
                'success': False,
                'response_time': time.time() - start_time,
                'status_code': 0,
                'error': "Timeout",
                'job_id': job_id,
                'user_id': user_id
            }
        except Exception as e:
            return {
                'success': False,
                'response_time': time.time() - start_time,
                'status_code': 0,
                'error': str(e),
                'job_id': job_id,
                'user_id': user_id
            }
    
    async def run_concurrent_load_test(self, concurrent_users: int, requests_per_user: int) -> Dict[str, Any]:
        """Run concurrent load test"""
        print(f"🔥 Starting load test: {concurrent_users} users, {requests_per_user} requests each")
        
        timeout = aiohttp.ClientTimeout(total=60)
        connector = aiohttp.TCPConnector(limit=100, limit_per_host=50)
        
        async with aiohttp.ClientSession(timeout=timeout, connector=connector) as session:
            # Create all tasks
            tasks = []
            for user_id in range(concurrent_users):
                for request_id in range(requests_per_user):
                    job_id = (request_id % 3) + 1  # Rotate between job IDs 1, 2, 3
                    task = self.make_ai_matching_request(session, job_id, user_id)
                    tasks.append(task)
            
            # Execute all tasks concurrently
            start_time = time.time()
            results = await asyncio.gather(*tasks, return_exceptions=True)
            total_time = time.time() - start_time
            
            # Filter out exceptions
            valid_results = [r for r in results if isinstance(r, dict)]
            
            return {
                'results': valid_results,
                'total_time': total_time,
                'total_requests': len(tasks),
                'valid_responses': len(valid_results)
            }
    
    def analyze_results(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze test results"""
        results = test_data['results']
        total_time = test_data['total_time']
        
        if not results:
            return {
                'status': 'FAILED',
                'error': 'No valid responses received'
            }
        
        # Separate successful and failed requests
        successful = [r for r in results if r.get('success', False)]
        failed = [r for r in results if not r.get('success', False)]
        
        # Calculate metrics
        total_requests = len(results)
        success_rate = len(successful) / total_requests if total_requests > 0 else 0
        error_rate = len(failed) / total_requests if total_requests > 0 else 1
        
        if successful:
            response_times = [r['response_time'] for r in successful]
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p95_response_time = sorted(response_times)[int(len(response_times) * 0.95)] if len(response_times) > 1 else response_times[0]
        else:
            avg_response_time = min_response_time = max_response_time = p95_response_time = 0
        
        throughput = len(successful) / total_time if total_time > 0 else 0
        
        # Performance evaluation
        performance_checks = {
            'avg_response_time': avg_response_time <= self.thresholds['avg_response_time'],
            'error_rate': error_rate <= self.thresholds['error_rate'],
            'throughput': throughput >= self.thresholds['min_throughput']
        }
        
        passed_checks = sum(performance_checks.values())
        overall_status = 'EXCELLENT' if passed_checks == 3 else 'GOOD' if passed_checks == 2 else 'ACCEPTABLE' if passed_checks == 1 else 'POOR'
        
        return {
            'status': overall_status,
            'total_requests': total_requests,
            'successful_requests': len(successful),
            'failed_requests': len(failed),
            'success_rate': success_rate,
            'error_rate': error_rate,
            'avg_response_time': avg_response_time,
            'min_response_time': min_response_time,
            'max_response_time': max_response_time,
            'p95_response_time': p95_response_time,
            'throughput_rps': throughput,
            'total_time': total_time,
            'performance_checks': performance_checks,
            'thresholds': self.thresholds
        }
    
    async def run_stress_test_suite(self) -> Dict[str, Any]:
        """Run comprehensive stress test suite"""
        print("🚀 STARTING AI MATCHING LOAD & STRESS TESTS")
        print("=" * 60)
        
        stress_results = {}
        user_levels = [1, 3, 5, 10, 15, 20]  # Gradual increase
        
        for users in user_levels:
            print(f"\n📊 Testing with {users} concurrent users...")
            
            try:
                # Run load test
                test_data = await self.run_concurrent_load_test(users, 3)  # 3 requests per user
                
                # Analyze results
                analysis = self.analyze_results(test_data)
                stress_results[users] = analysis
                
                print(f"   Status: {analysis['status']}")
                print(f"   Avg Response: {analysis['avg_response_time']:.3f}s")
                print(f"   Success Rate: {analysis['success_rate']:.1%}")
                print(f"   Throughput: {analysis['throughput_rps']:.1f} req/s")
                
                # Stop if performance degrades significantly
                if analysis['error_rate'] > 0.5:  # 50% error rate
                    print(f"   ⚠️ High error rate detected - stopping stress test")
                    break
                    
            except Exception as e:
                print(f"   ❌ Test failed: {e}")
                stress_results[users] = {'status': 'ERROR', 'error': str(e)}
                break
            
            # Brief pause between tests
            await asyncio.sleep(1)
        
        return stress_results
    
    def generate_report(self, stress_results: Dict[int, Dict[str, Any]]) -> Dict[str, Any]:
        """Generate performance report"""
        if not stress_results:
            return {'status': 'NO_RESULTS', 'message': 'No test results available'}
        
        # Find maximum successful concurrent users
        max_users = 0
        breaking_point = None
        
        for users, result in stress_results.items():
            if result.get('status') in ['EXCELLENT', 'GOOD', 'ACCEPTABLE']:
                max_users = users
            elif breaking_point is None:
                breaking_point = users
        
        # Overall assessment
        if max_users >= 15:
            overall_status = 'EXCELLENT'
            message = "System handles high concurrent load excellently"
        elif max_users >= 10:
            overall_status = 'GOOD'
            message = "System performs well under moderate load"
        elif max_users >= 5:
            overall_status = 'ACCEPTABLE'
            message = "System needs optimization for higher loads"
        else:
            overall_status = 'POOR'
            message = "System requires significant performance improvements"
        
        return {
            'overall_status': overall_status,
            'message': message,
            'max_concurrent_users': max_users,
            'breaking_point': breaking_point,
            'detailed_results': stress_results,
            'test_timestamp': datetime.now().isoformat(),
            'recommendations': [
                message,
                f"Maximum concurrent users handled: {max_users}",
                f"Breaking point: {breaking_point} users" if breaking_point else "No breaking point found"
            ]
        }

async def main():
    """Main test execution"""
    tester = SimpleAIMatchingLoadTester()
    
    try:
        # Run stress test suite
        stress_results = await tester.run_stress_test_suite()
        
        # Generate report
        report = tester.generate_report(stress_results)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📈 AI MATCHING LOAD TEST SUMMARY")
        print("=" * 60)
        
        print(f"Overall Status: {report['overall_status']}")
        print(f"Max Concurrent Users: {report['max_concurrent_users']}")
        
        if report.get('breaking_point'):
            print(f"Breaking Point: {report['breaking_point']} users")
        
        for recommendation in report['recommendations']:
            print(f"• {recommendation}")
        
        # Determine success
        success = report['overall_status'] in ['EXCELLENT', 'GOOD']
        
        if success:
            print("\n✅ AI MATCHING LOAD TESTS PASSED")
            print("🎉 System ready for production load")
        else:
            print("\n❌ AI MATCHING LOAD TESTS FAILED")
            print("🚨 System requires performance optimization")
        
        return success
        
    except Exception as e:
        print(f"\n❌ Test execution failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    try:
        success = asyncio.run(main())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)