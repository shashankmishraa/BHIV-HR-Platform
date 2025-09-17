#!/usr/bin/env python3
"""
BHIV HR Platform - Workflow Performance Testing
Performance benchmarks for end-to-end workflows and multi-service operations
"""

import requests
import time
import statistics
import concurrent.futures
from datetime import datetime
from typing import Dict, List, Tuple, Any
import json

class WorkflowPerformanceTester:
    """Performance testing for multi-service workflows"""
    
    def __init__(self):
        self.api_base = "http://localhost:8000"
        self.ai_base = "http://localhost:9000"
        self.api_key = "myverysecureapikey123"
        self.headers = {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}
        
        self.performance_results = {}
        self.benchmarks = {
            "job_creation": 2.0,  # seconds
            "candidate_upload": 5.0,  # seconds for 10 candidates
            "ai_matching": 10.0,  # seconds
            "interview_scheduling": 1.0,  # seconds
            "feedback_submission": 1.0,  # seconds
            "offer_creation": 1.0,  # seconds
            "concurrent_requests": 0.5,  # seconds per request
            "end_to_end_workflow": 30.0  # seconds for complete workflow
        }
    
    def measure_operation(self, operation_name: str, operation_func, *args, **kwargs) -> Dict[str, Any]:
        """Measure performance of a single operation"""
        start_time = time.time()
        
        try:
            result = operation_func(*args, **kwargs)
            end_time = time.time()
            
            execution_time = end_time - start_time
            success = True
            
        except Exception as e:
            end_time = time.time()
            execution_time = end_time - start_time
            result = None
            success = False
        
        return {
            "operation": operation_name,
            "execution_time": execution_time,
            "success": success,
            "result": result,
            "timestamp": datetime.now().isoformat()
        }
    
    def test_job_creation_performance(self, iterations: int = 5) -> Dict[str, Any]:
        """Test job creation performance"""
        print(f"\n📋 Testing job creation performance ({iterations} iterations)...")
        
        times = []
        successes = 0
        
        for i in range(iterations):
            job_data = {
                "title": f"Performance Test Job {i+1}",
                "description": f"Performance testing job creation {i+1}",
                "client_id": 1,
                "department": "Engineering",
                "location": "Remote",
                "experience_level": "Mid",
                "employment_type": "Full-time",
                "requirements": "Python, FastAPI",
                "status": "active"
            }
            
            start_time = time.time()
            
            try:
                response = requests.post(
                    f"{self.api_base}/v1/jobs",
                    headers=self.headers,
                    json=job_data,
                    timeout=10
                )
                
                end_time = time.time()
                execution_time = end_time - start_time
                times.append(execution_time)
                
                if response.status_code == 200:
                    successes += 1
                
            except Exception as e:
                end_time = time.time()
                times.append(end_time - start_time)
        
        avg_time = statistics.mean(times)
        min_time = min(times)
        max_time = max(times)
        
        result = {
            "operation": "job_creation",
            "iterations": iterations,
            "avg_time": avg_time,
            "min_time": min_time,
            "max_time": max_time,
            "success_rate": successes / iterations,
            "benchmark_met": avg_time <= self.benchmarks["job_creation"]
        }
        
        print(f"   Average: {avg_time:.3f}s | Min: {min_time:.3f}s | Max: {max_time:.3f}s")
        print(f"   Success Rate: {result['success_rate']:.1%}")
        print(f"   Benchmark: {'✅ PASSED' if result['benchmark_met'] else '❌ FAILED'} ({self.benchmarks['job_creation']}s)")
        
        return result
    
    def test_candidate_upload_performance(self, batch_sizes: List[int] = [1, 5, 10, 20]) -> Dict[str, Any]:
        """Test candidate upload performance with different batch sizes"""
        print(f"\n👥 Testing candidate upload performance...")
        
        results = {}
        
        for batch_size in batch_sizes:
            print(f"\n   Testing batch size: {batch_size} candidates")
            
            # Create test candidates
            candidates = []
            for i in range(batch_size):
                candidates.append({
                    "name": f"Perf Test Candidate {i+1}",
                    "email": f"perf.test{i+1}@testdomain.com",
                    "phone": f"+1-555-{1000+i:04d}",
                    "location": "Remote",
                    "experience_years": 3,
                    "technical_skills": "Python, FastAPI, SQL",
                    "seniority_level": "Mid-level",
                    "education_level": "Bachelors",
                    "job_id": 1,
                    "status": "applied"
                })
            
            start_time = time.time()
            
            try:
                response = requests.post(
                    f"{self.api_base}/v1/candidates/bulk",
                    headers=self.headers,
                    json={"candidates": candidates},
                    timeout=30
                )
                
                end_time = time.time()
                execution_time = end_time - start_time
                
                success = response.status_code == 200
                throughput = batch_size / execution_time if execution_time > 0 else 0
                
                results[batch_size] = {
                    "batch_size": batch_size,
                    "execution_time": execution_time,
                    "success": success,
                    "throughput": throughput,
                    "time_per_candidate": execution_time / batch_size if batch_size > 0 else 0
                }
                
                print(f"      Time: {execution_time:.3f}s | Throughput: {throughput:.1f} candidates/s")
                
            except Exception as e:
                results[batch_size] = {
                    "batch_size": batch_size,
                    "execution_time": None,
                    "success": False,
                    "error": str(e)
                }
                print(f"      Failed: {str(e)}")
        
        # Find optimal batch size
        successful_results = {k: v for k, v in results.items() if v.get("success", False)}
        if successful_results:
            optimal_batch = max(successful_results.keys(), key=lambda k: successful_results[k]["throughput"])
            print(f"\n   Optimal batch size: {optimal_batch} candidates ({successful_results[optimal_batch]['throughput']:.1f} candidates/s)")
        
        return {
            "operation": "candidate_upload",
            "batch_results": results,
            "optimal_batch_size": optimal_batch if successful_results else None
        }
    
    def test_ai_matching_performance(self, job_id: int = 1, iterations: int = 3) -> Dict[str, Any]:
        """Test AI matching performance"""
        print(f"\n🤖 Testing AI matching performance ({iterations} iterations)...")
        
        times = []
        successes = 0
        candidate_counts = []
        
        for i in range(iterations):
            start_time = time.time()
            
            try:
                response = requests.get(
                    f"{self.api_base}/v1/match/{job_id}/top",
                    headers=self.headers,
                    timeout=30
                )
                
                end_time = time.time()
                execution_time = end_time - start_time
                times.append(execution_time)
                
                if response.status_code == 200:
                    successes += 1
                    result = response.json()
                    candidate_counts.append(len(result.get("top_candidates", [])))
                
            except Exception as e:
                end_time = time.time()
                times.append(end_time - start_time)
        
        avg_time = statistics.mean(times) if times else 0
        avg_candidates = statistics.mean(candidate_counts) if candidate_counts else 0
        
        result = {
            "operation": "ai_matching",
            "iterations": iterations,
            "avg_time": avg_time,
            "min_time": min(times) if times else 0,
            "max_time": max(times) if times else 0,
            "success_rate": successes / iterations,
            "avg_candidates_processed": avg_candidates,
            "benchmark_met": avg_time <= self.benchmarks["ai_matching"]
        }
        
        print(f"   Average: {avg_time:.3f}s | Candidates: {avg_candidates:.1f}")
        print(f"   Success Rate: {result['success_rate']:.1%}")
        print(f"   Benchmark: {'✅ PASSED' if result['benchmark_met'] else '❌ FAILED'} ({self.benchmarks['ai_matching']}s)")
        
        return result
    
    def test_concurrent_request_performance(self, concurrent_users: int = 5, requests_per_user: int = 3) -> Dict[str, Any]:
        """Test concurrent request handling performance"""
        print(f"\n⚡ Testing concurrent request performance ({concurrent_users} users, {requests_per_user} requests each)...")
        
        def make_request(user_id: int, request_id: int) -> Dict[str, Any]:
            """Make a single request"""
            start_time = time.time()
            
            try:
                response = requests.get(
                    f"{self.api_base}/health",
                    headers=self.headers,
                    timeout=10
                )
                
                end_time = time.time()
                
                return {
                    "user_id": user_id,
                    "request_id": request_id,
                    "execution_time": end_time - start_time,
                    "success": response.status_code == 200,
                    "status_code": response.status_code
                }
                
            except Exception as e:
                return {
                    "user_id": user_id,
                    "request_id": request_id,
                    "execution_time": time.time() - start_time,
                    "success": False,
                    "error": str(e)
                }
        
        # Create all request tasks
        tasks = []
        for user_id in range(concurrent_users):
            for request_id in range(requests_per_user):
                tasks.append((user_id, request_id))
        
        # Execute concurrent requests
        start_time = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=concurrent_users) as executor:
            future_to_task = {
                executor.submit(make_request, user_id, request_id): (user_id, request_id)
                for user_id, request_id in tasks
            }
            
            results = []
            for future in concurrent.futures.as_completed(future_to_task):
                result = future.result()
                results.append(result)
        
        total_time = time.time() - start_time
        
        # Analyze results
        successful_requests = [r for r in results if r["success"]]
        failed_requests = [r for r in results if not r["success"]]
        
        if successful_requests:
            avg_response_time = statistics.mean([r["execution_time"] for r in successful_requests])
            min_response_time = min([r["execution_time"] for r in successful_requests])
            max_response_time = max([r["execution_time"] for r in successful_requests])
        else:
            avg_response_time = min_response_time = max_response_time = 0
        
        throughput = len(successful_requests) / total_time if total_time > 0 else 0
        
        result = {
            "operation": "concurrent_requests",
            "concurrent_users": concurrent_users,
            "requests_per_user": requests_per_user,
            "total_requests": len(tasks),
            "successful_requests": len(successful_requests),
            "failed_requests": len(failed_requests),
            "success_rate": len(successful_requests) / len(tasks),
            "total_time": total_time,
            "avg_response_time": avg_response_time,
            "min_response_time": min_response_time,
            "max_response_time": max_response_time,
            "throughput": throughput,
            "benchmark_met": avg_response_time <= self.benchmarks["concurrent_requests"]
        }
        
        print(f"   Total Time: {total_time:.3f}s | Throughput: {throughput:.1f} req/s")
        print(f"   Avg Response: {avg_response_time:.3f}s | Success Rate: {result['success_rate']:.1%}")
        print(f"   Benchmark: {'✅ PASSED' if result['benchmark_met'] else '❌ FAILED'} ({self.benchmarks['concurrent_requests']}s)")
        
        return result
    
    def test_end_to_end_workflow_performance(self) -> Dict[str, Any]:
        """Test complete end-to-end workflow performance"""
        print(f"\n🎯 Testing end-to-end workflow performance...")
        
        workflow_start = time.time()
        
        try:
            # Step 1: Create job
            step1_start = time.time()
            job_data = {
                "title": "E2E Performance Test Job",
                "description": "End-to-end performance testing",
                "client_id": 1,
                "department": "Engineering",
                "location": "Remote",
                "experience_level": "Mid",
                "employment_type": "Full-time",
                "requirements": "Python, FastAPI",
                "status": "active"
            }
            
            response = requests.post(f"{self.api_base}/v1/jobs", headers=self.headers, json=job_data, timeout=10)
            job_creation_time = time.time() - step1_start
            
            if response.status_code != 200:
                raise Exception(f"Job creation failed: {response.status_code}")
            
            job_id = response.json().get("job_id")
            
            # Step 2: Upload candidates
            step2_start = time.time()
            candidates = [
                {
                    "name": f"E2E Perf Candidate {i+1}",
                    "email": f"e2e.perf{i+1}@testdomain.com",
                    "phone": f"+1-555-{2000+i:04d}",
                    "location": "Remote",
                    "experience_years": 3,
                    "technical_skills": "Python, FastAPI, SQL",
                    "seniority_level": "Mid-level",
                    "education_level": "Bachelors",
                    "job_id": job_id,
                    "status": "applied"
                }
                for i in range(5)
            ]
            
            response = requests.post(f"{self.api_base}/v1/candidates/bulk", headers=self.headers, json={"candidates": candidates}, timeout=15)
            candidate_upload_time = time.time() - step2_start
            
            if response.status_code != 200:
                raise Exception(f"Candidate upload failed: {response.status_code}")
            
            # Step 3: AI matching
            step3_start = time.time()
            response = requests.get(f"{self.api_base}/v1/match/{job_id}/top", headers=self.headers, timeout=20)
            ai_matching_time = time.time() - step3_start
            
            if response.status_code != 200:
                raise Exception(f"AI matching failed: {response.status_code}")
            
            top_candidates = response.json().get("top_candidates", [])
            if not top_candidates:
                raise Exception("No candidates returned from AI matching")
            
            best_candidate_id = top_candidates[0].get("candidate_id")
            
            # Step 4: Schedule interview
            step4_start = time.time()
            interview_data = {
                "candidate_id": best_candidate_id,
                "job_id": job_id,
                "interview_date": "2025-02-15T10:00:00Z",
                "interviewer": "E2E Performance Tester"
            }
            
            response = requests.post(f"{self.api_base}/v1/interviews", headers=self.headers, json=interview_data, timeout=10)
            interview_scheduling_time = time.time() - step4_start
            
            if response.status_code != 200:
                raise Exception(f"Interview scheduling failed: {response.status_code}")
            
            # Step 5: Submit feedback
            step5_start = time.time()
            feedback_data = {
                "candidate_id": best_candidate_id,
                "reviewer": "E2E Performance Tester",
                "feedback_text": "Performance test feedback",
                "values_scores": {"integrity": 5, "honesty": 5, "discipline": 4, "hard_work": 5, "gratitude": 4}
            }
            
            response = requests.post(f"{self.api_base}/v1/feedback", headers=self.headers, json=feedback_data, timeout=10)
            feedback_submission_time = time.time() - step5_start
            
            if response.status_code != 200:
                raise Exception(f"Feedback submission failed: {response.status_code}")
            
            total_workflow_time = time.time() - workflow_start
            
            result = {
                "operation": "end_to_end_workflow",
                "total_time": total_workflow_time,
                "job_creation_time": job_creation_time,
                "candidate_upload_time": candidate_upload_time,
                "ai_matching_time": ai_matching_time,
                "interview_scheduling_time": interview_scheduling_time,
                "feedback_submission_time": feedback_submission_time,
                "success": True,
                "benchmark_met": total_workflow_time <= self.benchmarks["end_to_end_workflow"]
            }
            
            print(f"   Total Workflow: {total_workflow_time:.3f}s")
            print(f"   Job Creation: {job_creation_time:.3f}s")
            print(f"   Candidate Upload: {candidate_upload_time:.3f}s")
            print(f"   AI Matching: {ai_matching_time:.3f}s")
            print(f"   Interview Scheduling: {interview_scheduling_time:.3f}s")
            print(f"   Feedback Submission: {feedback_submission_time:.3f}s")
            print(f"   Benchmark: {'✅ PASSED' if result['benchmark_met'] else '❌ FAILED'} ({self.benchmarks['end_to_end_workflow']}s)")
            
            return result
            
        except Exception as e:
            total_workflow_time = time.time() - workflow_start
            
            result = {
                "operation": "end_to_end_workflow",
                "total_time": total_workflow_time,
                "success": False,
                "error": str(e),
                "benchmark_met": False
            }
            
            print(f"   Failed after {total_workflow_time:.3f}s: {str(e)}")
            return result
    
    def run_performance_suite(self) -> Dict[str, Any]:
        """Run complete performance test suite"""
        print("🚀 STARTING WORKFLOW PERFORMANCE TESTING")
        print("="*60)
        
        # Verify service health
        try:
            response = requests.get(f"{self.api_base}/health", timeout=5)
            if response.status_code != 200:
                print("❌ API Gateway not healthy - aborting performance tests")
                return {}
        except:
            print("❌ Cannot connect to API Gateway - aborting performance tests")
            return {}
        
        # Run all performance tests
        results = {}
        
        results["job_creation"] = self.test_job_creation_performance()
        results["candidate_upload"] = self.test_candidate_upload_performance()
        results["ai_matching"] = self.test_ai_matching_performance()
        results["concurrent_requests"] = self.test_concurrent_request_performance()
        results["end_to_end_workflow"] = self.test_end_to_end_workflow_performance()
        
        # Print comprehensive summary
        self.print_performance_summary(results)
        
        return results
    
    def print_performance_summary(self, results: Dict[str, Any]):
        """Print comprehensive performance summary"""
        print("\n" + "="*60)
        print("📊 WORKFLOW PERFORMANCE SUMMARY")
        print("="*60)
        
        benchmarks_met = 0
        total_benchmarks = 0
        
        for test_name, result in results.items():
            if isinstance(result, dict) and "benchmark_met" in result:
                benchmark_status = "✅ PASSED" if result["benchmark_met"] else "❌ FAILED"
                
                if test_name == "job_creation":
                    print(f"   Job Creation: {result['avg_time']:.3f}s avg - {benchmark_status}")
                elif test_name == "ai_matching":
                    print(f"   AI Matching: {result['avg_time']:.3f}s avg - {benchmark_status}")
                elif test_name == "concurrent_requests":
                    print(f"   Concurrent Requests: {result['avg_response_time']:.3f}s avg - {benchmark_status}")
                elif test_name == "end_to_end_workflow":
                    print(f"   End-to-End Workflow: {result['total_time']:.3f}s - {benchmark_status}")
                
                if result["benchmark_met"]:
                    benchmarks_met += 1
                total_benchmarks += 1
        
        print(f"\n📈 Performance Benchmarks: {benchmarks_met}/{total_benchmarks} passed")
        
        if benchmarks_met == total_benchmarks:
            print("🎉 ALL PERFORMANCE BENCHMARKS PASSED!")
            print("✅ System performance meets enterprise standards")
        elif benchmarks_met >= total_benchmarks * 0.75:
            print("⚠️ MOST BENCHMARKS PASSED - Minor optimizations needed")
        else:
            print("❌ PERFORMANCE ISSUES DETECTED")
            print("🚨 System requires performance optimization")
        
        print(f"\n🏁 Performance Testing Complete: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main entry point for performance testing"""
    tester = WorkflowPerformanceTester()
    results = tester.run_performance_suite()
    
    # Determine if all benchmarks passed
    benchmarks_passed = all(
        result.get("benchmark_met", False) 
        for result in results.values() 
        if isinstance(result, dict) and "benchmark_met" in result
    )
    
    return 0 if benchmarks_passed else 1

if __name__ == "__main__":
    import sys
    sys.exit(main())