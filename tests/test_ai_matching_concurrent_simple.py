#!/usr/bin/env python3
"""
BHIV HR Platform - AI Matching Concurrent Load Testing (Simple Version)
Comprehensive concurrent request testing specifically for AI matching endpoints
"""

import requests
import time
import statistics
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Any
import json

class AIMatchingConcurrentTester:
    """Dedicated concurrent load tester for AI matching endpoints"""
    
    def __init__(self):
        self.api_base = "https://bhiv-hr-gateway.onrender.com"
        self.api_key = "myverysecureapikey123"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        # Performance thresholds for AI matching under load
        self.thresholds = {
            "max_response_time": 5.0,  # seconds
            "avg_response_time": 2.0,  # seconds
            "error_rate": 0.05,  # 5%
            "min_throughput": 5.0,  # requests per second
            "concurrent_users_target": 20  # target concurrent users
        }
        
        self.job_ids = [1, 2, 3]  # Test with multiple job IDs
    
    def make_ai_matching_request(self, user_id: int, request_id: int, job_id: int) -> Dict[str, Any]:
        """Make single AI matching request with detailed metrics"""
        start_time = time.time()
        
        try:
            response = requests.get(
                f"{self.api_base}/v1/match/{job_id}/top",
                headers=self.headers,
                timeout=30
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                data = response.json()
                candidates_count = len(data.get("matches", data.get("top_candidates", [])))
                
                return {
                    "user_id": user_id,
                    "request_id": request_id,
                    "job_id": job_id,
                    "response_time": response_time,
                    "success": True,
                    "status_code": response.status_code,
                    "candidates_returned": candidates_count,
                    "processing_time": data.get("processing_time", "unknown"),
                    "algorithm_version": data.get("algorithm_version", "unknown"),
                    "timestamp": start_time
                }
            else:
                return {
                    "user_id": user_id,
                    "request_id": request_id,
                    "job_id": job_id,
                    "response_time": response_time,
                    "success": False,
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": start_time
                }
                
        except requests.exceptions.Timeout:
            return {
                "user_id": user_id,
                "request_id": request_id,
                "job_id": job_id,
                "response_time": time.time() - start_time,
                "success": False,
                "status_code": 0,
                "error": "Request timeout",
                "timestamp": start_time
            }
        except Exception as e:
            return {
                "user_id": user_id,
                "request_id": request_id,
                "job_id": job_id,
                "response_time": time.time() - start_time,
                "success": False,
                "status_code": 0,
                "error": str(e),
                "timestamp": start_time
            }
    
    def test_concurrent_ai_matching(self, concurrent_users: int, requests_per_user: int) -> Dict[str, Any]:
        """Test AI matching with concurrent users"""
        print(f"Testing AI matching with {concurrent_users} concurrent users, {requests_per_user} requests each")
        
        # Create all request tasks
        tasks = []
        for user_id in range(concurrent_users):
            for request_id in range(requests_per_user):
                job_id = self.job_ids[request_id % len(self.job_ids)]  # Rotate job IDs
                tasks.append((user_id, request_id, job_id))
        
        # Execute concurrent requests
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            future_to_task = {
                executor.submit(self.make_ai_matching_request, user_id, request_id, job_id): (user_id, request_id, job_id)
                for user_id, request_id, job_id in tasks
            }
            
            results = []
            for future in concurrent.futures.as_completed(future_to_task):
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    user_id, request_id, job_id = future_to_task[future]
                    results.append({
                        "user_id": user_id,
                        "request_id": request_id,
                        "job_id": job_id,
                        "response_time": 0,
                        "success": False,
                        "error": f"Future exception: {str(e)}",
                        "timestamp": time.time()
                    })
        
        total_time = time.time() - start_time
        
        return {
            "results": results,
            "total_time": total_time,
            "concurrent_users": concurrent_users,
            "requests_per_user": requests_per_user,
            "total_requests": len(tasks)
        }
    
    def analyze_concurrent_results(self, test_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze concurrent test results"""
        results = test_data["results"]
        total_time = test_data["total_time"]
        concurrent_users = test_data["concurrent_users"]
        
        if not results:
            return {"status": "FAILED", "error": "No results received"}
        
        # Separate successful and failed requests
        successful = [r for r in results if r.get("success", False)]
        failed = [r for r in results if not r.get("success", False)]
        
        # Calculate metrics
        total_requests = len(results)
        success_rate = len(successful) / total_requests if total_requests > 0 else 0
        error_rate = len(failed) / total_requests if total_requests > 0 else 1
        
        if successful:
            response_times = [r["response_time"] for r in successful]
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            
            # Calculate percentiles
            sorted_times = sorted(response_times)
            p50 = sorted_times[len(sorted_times) // 2] if sorted_times else 0
            p95_idx = int(len(sorted_times) * 0.95)
            p95 = sorted_times[p95_idx] if p95_idx < len(sorted_times) else sorted_times[-1] if sorted_times else 0
            p99_idx = int(len(sorted_times) * 0.99)
            p99 = sorted_times[p99_idx] if p99_idx < len(sorted_times) else sorted_times[-1] if sorted_times else 0
            
            # Calculate candidates metrics
            candidates_returned = [r.get("candidates_returned", 0) for r in successful if "candidates_returned" in r]
            avg_candidates = statistics.mean(candidates_returned) if candidates_returned else 0
        else:
            avg_response_time = min_response_time = max_response_time = 0
            p50 = p95 = p99 = 0
            avg_candidates = 0
        
        # Calculate throughput
        throughput = len(successful) / total_time if total_time > 0 else 0
        
        # Performance evaluation
        performance_checks = {
            "avg_response_time": avg_response_time <= self.thresholds["avg_response_time"],
            "max_response_time": max_response_time <= self.thresholds["max_response_time"],
            "error_rate": error_rate <= self.thresholds["error_rate"],
            "throughput": throughput >= self.thresholds["min_throughput"]
        }
        
        passed_checks = sum(performance_checks.values())
        
        # Determine status
        if passed_checks == 4:
            status = "EXCELLENT"
        elif passed_checks == 3:
            status = "GOOD"
        elif passed_checks >= 2:
            status = "ACCEPTABLE"
        else:
            status = "POOR"
        
        return {
            "status": status,
            "concurrent_users": concurrent_users,
            "total_requests": total_requests,
            "successful_requests": len(successful),
            "failed_requests": len(failed),
            "success_rate": success_rate,
            "error_rate": error_rate,
            "avg_response_time": avg_response_time,
            "min_response_time": min_response_time,
            "max_response_time": max_response_time,
            "p50_response_time": p50,
            "p95_response_time": p95,
            "p99_response_time": p99,
            "throughput_rps": throughput,
            "avg_candidates_returned": avg_candidates,
            "total_time": total_time,
            "performance_checks": performance_checks,
            "thresholds": self.thresholds
        }
    
    def run_stress_test_suite(self) -> Dict[str, Any]:
        """Run comprehensive stress test suite for AI matching"""
        print("STARTING AI MATCHING CONCURRENT LOAD TESTS")
        print("=" * 60)
        
        # Test different concurrent user levels
        user_levels = [1, 3, 5, 10, 15, 20, 25, 30]
        requests_per_user = 3
        
        stress_results = {}
        max_successful_users = 0
        breaking_point = None
        
        for users in user_levels:
            print(f"\nTesting {users} concurrent users...")
            
            try:
                # Run concurrent test
                test_data = self.test_concurrent_ai_matching(users, requests_per_user)
                
                # Analyze results
                analysis = self.analyze_concurrent_results(test_data)
                stress_results[users] = analysis
                
                # Print results
                print(f"   Status: {analysis['status']}")
                print(f"   Success Rate: {analysis['success_rate']:.1%}")
                print(f"   Avg Response: {analysis['avg_response_time']:.3f}s")
                print(f"   Max Response: {analysis['max_response_time']:.3f}s")
                print(f"   Throughput: {analysis['throughput_rps']:.1f} req/s")
                print(f"   Avg Candidates: {analysis['avg_candidates_returned']:.1f}")
                
                # Track performance
                if analysis['status'] in ['EXCELLENT', 'GOOD']:
                    max_successful_users = users
                elif breaking_point is None:
                    breaking_point = users
                
                # Stop if performance degrades significantly
                if analysis['error_rate'] > 0.5:  # 50% error rate
                    print(f"   WARNING: High error rate detected - stopping stress test")
                    break
                    
            except Exception as e:
                print(f"   ERROR: Test failed: {e}")
                stress_results[users] = {"status": "ERROR", "error": str(e)}
                if breaking_point is None:
                    breaking_point = users
                break
            
            # Brief pause between tests
            time.sleep(2)
        
        return {
            "stress_results": stress_results,
            "max_successful_users": max_successful_users,
            "breaking_point": breaking_point,
            "test_timestamp": datetime.now().isoformat()
        }
    
    def generate_performance_report(self, suite_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        stress_results = suite_results["stress_results"]
        max_users = suite_results["max_successful_users"]
        breaking_point = suite_results["breaking_point"]
        
        # Overall assessment
        if max_users >= 20:
            overall_status = "EXCELLENT"
            message = "AI matching handles high concurrent load excellently"
        elif max_users >= 15:
            overall_status = "GOOD"
            message = "AI matching performs well under moderate concurrent load"
        elif max_users >= 10:
            overall_status = "ACCEPTABLE"
            message = "AI matching needs optimization for higher concurrent loads"
        else:
            overall_status = "POOR"
            message = "AI matching requires significant performance improvements"
        
        # Generate recommendations
        recommendations = [message]
        
        if max_users > 0:
            recommendations.append(f"Maximum concurrent users handled successfully: {max_users}")
        
        if breaking_point:
            recommendations.append(f"Performance degrades at {breaking_point} concurrent users")
            recommendations.append("Consider implementing caching or load balancing")
        
        # Check specific performance issues
        if stress_results:
            last_good_result = None
            for users in sorted(stress_results.keys()):
                result = stress_results[users]
                if isinstance(result, dict) and result.get("status") in ["EXCELLENT", "GOOD"]:
                    last_good_result = result
            
            if last_good_result:
                if last_good_result["avg_response_time"] > 1.0:
                    recommendations.append("Response times are high - consider database optimization")
                if last_good_result["error_rate"] > 0.02:
                    recommendations.append("Some errors detected - check error handling")
        
        return {
            "overall_status": overall_status,
            "message": message,
            "max_concurrent_users": max_users,
            "breaking_point": breaking_point,
            "recommendations": recommendations,
            "detailed_results": stress_results,
            "test_summary": {
                "total_test_levels": len(stress_results),
                "successful_levels": len([r for r in stress_results.values() if isinstance(r, dict) and r.get("status") in ["EXCELLENT", "GOOD"]]),
                "test_timestamp": suite_results["test_timestamp"]
            }
        }

def main():
    """Main test execution"""
    print("AI MATCHING CONCURRENT LOAD TESTING")
    print("=" * 60)
    
    tester = AIMatchingConcurrentTester()
    
    try:
        # Verify AI matching endpoint is available
        print("Verifying AI matching endpoint availability...")
        response = requests.get(f"{tester.api_base}/v1/match/1/top", headers=tester.headers, timeout=10)
        
        if response.status_code != 200:
            print(f"ERROR: AI matching endpoint not available (status: {response.status_code})")
            return False
        
        print("SUCCESS: AI matching endpoint is available")
        
        # Run stress test suite
        suite_results = tester.run_stress_test_suite()
        
        # Generate report
        report = tester.generate_performance_report(suite_results)
        
        # Print summary
        print("\n" + "=" * 60)
        print("AI MATCHING CONCURRENT LOAD TEST SUMMARY")
        print("=" * 60)
        
        print(f"Overall Status: {report['overall_status']}")
        print(f"Max Concurrent Users: {report['max_concurrent_users']}")
        
        if report.get('breaking_point'):
            print(f"Breaking Point: {report['breaking_point']} users")
        
        print("\nRecommendations:")
        for rec in report['recommendations']:
            print(f"• {rec}")
        
        # Determine success
        success = report['overall_status'] in ['EXCELLENT', 'GOOD']
        
        if success:
            print("\nSUCCESS: AI MATCHING CONCURRENT LOAD TESTS PASSED")
            print("System ready for production concurrent load")
        else:
            print("\nFAILED: AI MATCHING CONCURRENT LOAD TESTS FAILED")
            print("System requires performance optimization for concurrent requests")
        
        # Save detailed results
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'ai_matching_concurrent_test_results_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\nDetailed results saved to: {filename}")
        
        return success
        
    except Exception as e:
        print(f"\nERROR: Test execution failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\nWARNING: Tests interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nERROR: Unexpected error: {e}")
        sys.exit(1)