#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Load & Stress Testing for AI Matching
Enterprise-grade performance testing with concurrent request simulation
"""

import asyncio
import aiohttp
import time
import statistics
import concurrent.futures
import threading
import psutil
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('load_stress_test.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class LoadTestConfig:
    """Load test configuration parameters"""
    base_url: str = "https://bhiv-hr-gateway.onrender.com"
    api_key: str = "myverysecureapikey123"
    max_concurrent_users: int = 50
    test_duration_seconds: int = 300  # 5 minutes
    ramp_up_seconds: int = 60
    ai_matching_endpoint: str = "/v1/match/{job_id}/top"
    job_ids: List[int] = None
    request_timeout: int = 30
    
    def __post_init__(self):
        if self.job_ids is None:
            self.job_ids = [1, 2, 3]  # Default job IDs

@dataclass
class RequestResult:
    """Individual request result"""
    timestamp: float
    response_time: float
    status_code: int
    success: bool
    error: Optional[str] = None
    user_id: int = 0
    request_id: int = 0
    endpoint: str = ""
    candidates_returned: int = 0

@dataclass
class LoadTestMetrics:
    """Comprehensive load test metrics"""
    total_requests: int = 0
    successful_requests: int = 0
    failed_requests: int = 0
    avg_response_time: float = 0.0
    min_response_time: float = 0.0
    max_response_time: float = 0.0
    p50_response_time: float = 0.0
    p95_response_time: float = 0.0
    p99_response_time: float = 0.0
    throughput_rps: float = 0.0
    error_rate: float = 0.0
    concurrent_users: int = 0
    test_duration: float = 0.0
    cpu_usage_avg: float = 0.0
    memory_usage_avg: float = 0.0
    
class SystemMonitor:
    """Monitor system resources during load testing"""
    
    def __init__(self):
        self.monitoring = False
        self.metrics = []
        self.monitor_thread = None
    
    def start_monitoring(self):
        """Start system monitoring"""
        self.monitoring = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop)
        self.monitor_thread.start()
        logger.info("System monitoring started")
    
    def stop_monitoring(self):
        """Stop system monitoring"""
        self.monitoring = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("System monitoring stopped")
    
    def _monitor_loop(self):
        """Monitor system resources"""
        while self.monitoring:
            try:
                cpu_percent = psutil.cpu_percent(interval=1)
                memory = psutil.virtual_memory()
                
                self.metrics.append({
                    'timestamp': time.time(),
                    'cpu_percent': cpu_percent,
                    'memory_percent': memory.percent,
                    'memory_used_gb': memory.used / (1024**3)
                })
            except Exception as e:
                logger.error(f"System monitoring error: {e}")
            
            time.sleep(1)
    
    def get_average_metrics(self) -> Dict[str, float]:
        """Get average system metrics"""
        if not self.metrics:
            return {'cpu_avg': 0.0, 'memory_avg': 0.0}
        
        cpu_values = [m['cpu_percent'] for m in self.metrics]
        memory_values = [m['memory_percent'] for m in self.metrics]
        
        return {
            'cpu_avg': statistics.mean(cpu_values),
            'memory_avg': statistics.mean(memory_values),
            'cpu_max': max(cpu_values),
            'memory_max': max(memory_values)
        }

class AIMatchingLoadTester:
    """Comprehensive load and stress tester for AI matching endpoints"""
    
    def __init__(self, config: LoadTestConfig):
        self.config = config
        self.results: List[RequestResult] = []
        self.system_monitor = SystemMonitor()
        self.session = None
        
        # Performance thresholds
        self.thresholds = {
            'avg_response_time': 2.0,  # seconds
            'p95_response_time': 5.0,  # seconds
            'error_rate': 0.05,  # 5%
            'min_throughput': 10.0,  # requests per second
            'cpu_usage': 80.0,  # percentage
            'memory_usage': 80.0  # percentage
        }
    
    async def create_session(self):
        """Create aiohttp session with proper configuration"""
        timeout = aiohttp.ClientTimeout(total=self.config.request_timeout)
        connector = aiohttp.TCPConnector(
            limit=100,  # Total connection pool size
            limit_per_host=50,  # Per-host connection limit
            ttl_dns_cache=300,  # DNS cache TTL
            use_dns_cache=True
        )
        
        self.session = aiohttp.ClientSession(
            timeout=timeout,
            connector=connector,
            headers={'Authorization': f'Bearer {self.config.api_key}'}
        )
    
    async def close_session(self):
        """Close aiohttp session"""
        if self.session:
            await self.session.close()
    
    async def make_ai_matching_request(self, user_id: int, request_id: int, job_id: int) -> RequestResult:
        """Make single AI matching request"""
        endpoint = self.config.ai_matching_endpoint.format(job_id=job_id)
        url = f"{self.config.base_url}{endpoint}"
        
        start_time = time.time()
        
        try:
            async with self.session.get(url) as response:
                response_time = time.time() - start_time
                
                if response.status == 200:
                    data = await response.json()
                    candidates_count = len(data.get('matches', data.get('top_candidates', [])))
                    
                    return RequestResult(
                        timestamp=start_time,
                        response_time=response_time,
                        status_code=response.status,
                        success=True,
                        user_id=user_id,
                        request_id=request_id,
                        endpoint=endpoint,
                        candidates_returned=candidates_count
                    )
                else:
                    return RequestResult(
                        timestamp=start_time,
                        response_time=response_time,
                        status_code=response.status,
                        success=False,
                        error=f"HTTP {response.status}",
                        user_id=user_id,
                        request_id=request_id,
                        endpoint=endpoint
                    )
                    
        except asyncio.TimeoutError:
            return RequestResult(
                timestamp=start_time,
                response_time=time.time() - start_time,
                status_code=0,
                success=False,
                error="Timeout",
                user_id=user_id,
                request_id=request_id,
                endpoint=endpoint
            )
        except Exception as e:
            return RequestResult(
                timestamp=start_time,
                response_time=time.time() - start_time,
                status_code=0,
                success=False,
                error=str(e),
                user_id=user_id,
                request_id=request_id,
                endpoint=endpoint
            )
    
    async def simulate_user_load(self, user_id: int, requests_per_user: int, delay_between_requests: float):
        """Simulate load from a single user"""
        user_results = []
        
        for request_id in range(requests_per_user):
            # Select random job ID
            job_id = np.random.choice(self.config.job_ids)
            
            # Make request
            result = await self.make_ai_matching_request(user_id, request_id, job_id)
            user_results.append(result)
            
            # Add delay between requests
            if delay_between_requests > 0 and request_id < requests_per_user - 1:
                await asyncio.sleep(delay_between_requests)
        
        return user_results
    
    async def run_load_test(self, concurrent_users: int, requests_per_user: int, 
                           delay_between_requests: float = 1.0) -> List[RequestResult]:
        """Run load test with specified parameters"""
        logger.info(f"Starting load test: {concurrent_users} users, {requests_per_user} requests each")
        
        await self.create_session()
        
        try:
            # Create tasks for all users
            tasks = []
            for user_id in range(concurrent_users):
                task = self.simulate_user_load(user_id, requests_per_user, delay_between_requests)
                tasks.append(task)
            
            # Execute all tasks concurrently
            start_time = time.time()
            user_results_list = await asyncio.gather(*tasks, return_exceptions=True)
            end_time = time.time()
            
            # Flatten results
            all_results = []
            for user_results in user_results_list:
                if isinstance(user_results, list):
                    all_results.extend(user_results)
                else:
                    logger.error(f"User task failed: {user_results}")
            
            logger.info(f"Load test completed in {end_time - start_time:.2f} seconds")
            return all_results
            
        finally:
            await self.close_session()
    
    async def run_stress_test(self) -> Dict[str, Any]:
        """Run comprehensive stress test with increasing load"""
        logger.info("Starting comprehensive stress test")
        
        stress_results = {}
        user_levels = [1, 5, 10, 20, 30, 40, 50]  # Gradual increase
        
        self.system_monitor.start_monitoring()
        
        try:
            for users in user_levels:
                logger.info(f"Testing with {users} concurrent users")
                
                # Run load test for this user level
                results = await self.run_load_test(
                    concurrent_users=users,
                    requests_per_user=5,  # 5 requests per user
                    delay_between_requests=0.5  # 500ms between requests
                )
                
                # Calculate metrics
                metrics = self.calculate_metrics(results, users)
                stress_results[users] = metrics
                
                logger.info(f"Users: {users}, Avg Response: {metrics.avg_response_time:.3f}s, "
                           f"Success Rate: {(1-metrics.error_rate)*100:.1f}%")
                
                # Check if system is failing
                if metrics.error_rate > 0.5:  # 50% error rate
                    logger.warning(f"High error rate detected at {users} users - stopping stress test")
                    break
                
                # Brief pause between stress levels
                await asyncio.sleep(2)
        
        finally:
            self.system_monitor.stop_monitoring()
        
        return stress_results
    
    async def run_endurance_test(self, duration_minutes: int = 10) -> Dict[str, Any]:
        """Run endurance test with sustained load"""
        logger.info(f"Starting {duration_minutes}-minute endurance test")
        
        duration_seconds = duration_minutes * 60
        concurrent_users = 10
        requests_per_minute = 6  # 1 request every 10 seconds per user
        
        self.system_monitor.start_monitoring()
        
        try:
            start_time = time.time()
            all_results = []
            
            while time.time() - start_time < duration_seconds:
                # Run batch of requests
                batch_results = await self.run_load_test(
                    concurrent_users=concurrent_users,
                    requests_per_user=1,
                    delay_between_requests=0
                )
                
                all_results.extend(batch_results)
                
                # Wait before next batch (10 seconds)
                await asyncio.sleep(10)
                
                elapsed = time.time() - start_time
                logger.info(f"Endurance test progress: {elapsed/60:.1f}/{duration_minutes} minutes")
            
            metrics = self.calculate_metrics(all_results, concurrent_users)
            
            return {
                'duration_minutes': duration_minutes,
                'metrics': metrics,
                'system_metrics': self.system_monitor.get_average_metrics()
            }
            
        finally:
            self.system_monitor.stop_monitoring()
    
    def calculate_metrics(self, results: List[RequestResult], concurrent_users: int) -> LoadTestMetrics:
        """Calculate comprehensive metrics from test results"""
        if not results:
            return LoadTestMetrics()
        
        successful_results = [r for r in results if r.success]
        failed_results = [r for r in results if not r.success]
        
        response_times = [r.response_time for r in successful_results]
        
        if response_times:
            avg_response_time = statistics.mean(response_times)
            min_response_time = min(response_times)
            max_response_time = max(response_times)
            p50_response_time = np.percentile(response_times, 50)
            p95_response_time = np.percentile(response_times, 95)
            p99_response_time = np.percentile(response_times, 99)
        else:
            avg_response_time = min_response_time = max_response_time = 0.0
            p50_response_time = p95_response_time = p99_response_time = 0.0
        
        # Calculate test duration
        if results:
            timestamps = [r.timestamp for r in results]
            test_duration = max(timestamps) - min(timestamps)
            throughput_rps = len(successful_results) / test_duration if test_duration > 0 else 0
        else:
            test_duration = 0
            throughput_rps = 0
        
        # Get system metrics
        system_metrics = self.system_monitor.get_average_metrics()
        
        return LoadTestMetrics(
            total_requests=len(results),
            successful_requests=len(successful_results),
            failed_requests=len(failed_results),
            avg_response_time=avg_response_time,
            min_response_time=min_response_time,
            max_response_time=max_response_time,
            p50_response_time=p50_response_time,
            p95_response_time=p95_response_time,
            p99_response_time=p99_response_time,
            throughput_rps=throughput_rps,
            error_rate=len(failed_results) / len(results) if results else 0,
            concurrent_users=concurrent_users,
            test_duration=test_duration,
            cpu_usage_avg=system_metrics.get('cpu_avg', 0),
            memory_usage_avg=system_metrics.get('memory_avg', 0)
        )
    
    def evaluate_performance(self, metrics: LoadTestMetrics) -> Dict[str, bool]:
        """Evaluate performance against thresholds"""
        return {
            'avg_response_time': metrics.avg_response_time <= self.thresholds['avg_response_time'],
            'p95_response_time': metrics.p95_response_time <= self.thresholds['p95_response_time'],
            'error_rate': metrics.error_rate <= self.thresholds['error_rate'],
            'throughput': metrics.throughput_rps >= self.thresholds['min_throughput'],
            'cpu_usage': metrics.cpu_usage_avg <= self.thresholds['cpu_usage'],
            'memory_usage': metrics.memory_usage_avg <= self.thresholds['memory_usage']
        }
    
    def generate_performance_report(self, stress_results: Dict[int, LoadTestMetrics], 
                                  endurance_results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive performance report"""
        report = {
            'test_timestamp': datetime.now().isoformat(),
            'test_configuration': asdict(self.config),
            'performance_thresholds': self.thresholds,
            'stress_test_results': {},
            'endurance_test_results': endurance_results,
            'recommendations': [],
            'overall_assessment': 'UNKNOWN'
        }
        
        # Process stress test results
        max_successful_users = 0
        breaking_point = None
        
        for users, metrics in stress_results.items():
            evaluation = self.evaluate_performance(metrics)
            
            report['stress_test_results'][users] = {
                'metrics': asdict(metrics),
                'performance_evaluation': evaluation,
                'passed_all_thresholds': all(evaluation.values())
            }
            
            if all(evaluation.values()):
                max_successful_users = users
            elif breaking_point is None:
                breaking_point = users
        
        # Determine overall assessment
        if max_successful_users >= 30:
            report['overall_assessment'] = 'EXCELLENT'
            report['recommendations'].append("System handles high concurrent load excellently")
        elif max_successful_users >= 20:
            report['overall_assessment'] = 'GOOD'
            report['recommendations'].append("System performs well under moderate load")
        elif max_successful_users >= 10:
            report['overall_assessment'] = 'ACCEPTABLE'
            report['recommendations'].append("System needs optimization for higher loads")
        else:
            report['overall_assessment'] = 'POOR'
            report['recommendations'].append("System requires significant performance improvements")
        
        # Add specific recommendations
        if breaking_point:
            report['recommendations'].append(f"Performance degrades at {breaking_point} concurrent users")
        
        if endurance_results:
            endurance_metrics = endurance_results.get('metrics')
            if endurance_metrics and endurance_metrics.error_rate > 0.1:
                report['recommendations'].append("High error rate during endurance test - check for memory leaks")
        
        return report
    
    def save_results_to_file(self, report: Dict[str, Any], filename: str = None):
        """Save test results to JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'ai_matching_load_test_results_{timestamp}.json'
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        logger.info(f"Test results saved to {filename}")

async def run_comprehensive_ai_matching_tests():
    """Run complete AI matching load and stress test suite"""
    print("🚀 STARTING COMPREHENSIVE AI MATCHING LOAD & STRESS TESTS")
    print("=" * 70)
    
    # Configuration
    config = LoadTestConfig(
        max_concurrent_users=50,
        test_duration_seconds=300,
        job_ids=[1, 2, 3]
    )
    
    tester = AIMatchingLoadTester(config)
    
    try:
        # 1. Basic Load Test
        print("\n📊 Phase 1: Basic Load Test (10 concurrent users)")
        basic_results = await tester.run_load_test(
            concurrent_users=10,
            requests_per_user=5,
            delay_between_requests=1.0
        )
        basic_metrics = tester.calculate_metrics(basic_results, 10)
        
        print(f"   Avg Response Time: {basic_metrics.avg_response_time:.3f}s")
        print(f"   Throughput: {basic_metrics.throughput_rps:.1f} req/s")
        print(f"   Error Rate: {basic_metrics.error_rate:.1%}")
        
        # 2. Stress Test
        print("\n🔥 Phase 2: Stress Test (Increasing Load)")
        stress_results = await tester.run_stress_test()
        
        # 3. Endurance Test
        print("\n⏱️ Phase 3: Endurance Test (10 minutes)")
        endurance_results = await tester.run_endurance_test(duration_minutes=10)
        
        # 4. Generate Report
        print("\n📋 Phase 4: Generating Performance Report")
        report = tester.generate_performance_report(stress_results, endurance_results)
        
        # 5. Save Results
        tester.save_results_to_file(report)
        
        # 6. Print Summary
        print("\n" + "=" * 70)
        print("📈 AI MATCHING PERFORMANCE TEST SUMMARY")
        print("=" * 70)
        
        print(f"Overall Assessment: {report['overall_assessment']}")
        print(f"Max Concurrent Users Handled: {max(stress_results.keys()) if stress_results else 0}")
        
        for recommendation in report['recommendations']:
            print(f"• {recommendation}")
        
        # Determine success
        success = report['overall_assessment'] in ['EXCELLENT', 'GOOD']
        
        if success:
            print("\n✅ AI MATCHING PERFORMANCE TESTS PASSED")
            print("🎉 System ready for production load")
        else:
            print("\n❌ AI MATCHING PERFORMANCE TESTS FAILED")
            print("🚨 System requires performance optimization")
        
        return success
        
    except Exception as e:
        logger.error(f"Test execution failed: {e}")
        print(f"\n❌ Test execution failed: {e}")
        return False

def main():
    """Main entry point"""
    try:
        success = asyncio.run(run_comprehensive_ai_matching_tests())
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 1
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    import sys
    sys.exit(main())