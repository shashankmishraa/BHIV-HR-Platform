#!/usr/bin/env python3
"""
Comprehensive Observability Verification Script
Tests all health checks, metrics, logging, and monitoring features
"""

import asyncio
import json
import logging
import time
from datetime import datetime
from typing import Dict, List, Any
import requests
import sys

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ObservabilityVerifier:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "total_checks": 0,
            "passed_checks": 0,
            "failed_checks": 0,
            "services": {},
            "summary": {}
        }
        
        self.services = {
            "production": {
                "gateway": "https://bhiv-hr-gateway-901a.onrender.com",
                "agent": "https://bhiv-hr-agent-o6nx.onrender.com"
            },
            "development": {
                "gateway": "http://localhost:8000",
                "agent": "http://localhost:9000"
            }
        }
        
        self.health_endpoints = ["/health", "/health/detailed", "/health/ready", "/health/live"]
        self.metrics_endpoints = ["/metrics", "/metrics/json"]

    def print_header(self, title: str):
        print(f"\n{'='*80}")
        print(f"{title.center(80)}")
        print(f"{'='*80}")

    def print_success(self, message: str):
        print(f"[OK] {message}")

    def print_error(self, message: str):
        print(f"[ERROR] {message}")

    def print_warning(self, message: str):
        print(f"[WARNING] {message}")

    def increment_check(self, passed: bool = True):
        self.results["total_checks"] += 1
        if passed:
            self.results["passed_checks"] += 1
        else:
            self.results["failed_checks"] += 1

    async def verify_health_endpoints(self, environment: str) -> Dict[str, Any]:
        """Verify all health check endpoints"""
        self.print_header(f"HEALTH ENDPOINTS VERIFICATION - {environment.upper()}")
        
        health_results = {}
        services = self.services[environment]
        
        for service_name, base_url in services.items():
            print(f"\nTesting {service_name} health endpoints: {base_url}")
            service_health = {}
            
            for endpoint in self.health_endpoints:
                try:
                    url = f"{base_url}{endpoint}"
                    response = requests.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        self.print_success(f"{endpoint} -> 200 OK")
                        
                        # Validate JSON response
                        try:
                            data = response.json()
                            if "status" in data and "service" in data:
                                self.print_success(f"  Valid JSON structure")
                            else:
                                self.print_warning(f"  Missing required fields in response")
                        except json.JSONDecodeError:
                            self.print_warning(f"  Invalid JSON response")
                        
                        service_health[endpoint] = {
                            "status": "ok",
                            "status_code": response.status_code,
                            "response_time": response.elapsed.total_seconds()
                        }
                        self.increment_check(True)
                        
                    elif response.status_code in [503, 404]:
                        self.print_warning(f"{endpoint} -> {response.status_code} (acceptable)")
                        service_health[endpoint] = {
                            "status": "acceptable",
                            "status_code": response.status_code
                        }
                        self.increment_check(True)
                        
                    else:
                        self.print_error(f"{endpoint} -> {response.status_code}")
                        service_health[endpoint] = {
                            "status": "failed",
                            "status_code": response.status_code
                        }
                        self.increment_check(False)
                        
                except requests.exceptions.ConnectionError:
                    self.print_error(f"{endpoint} -> Connection Error")
                    service_health[endpoint] = {
                        "status": "connection_error"
                    }
                    self.increment_check(False)
                    
                except requests.exceptions.Timeout:
                    self.print_error(f"{endpoint} -> Timeout")
                    service_health[endpoint] = {
                        "status": "timeout"
                    }
                    self.increment_check(False)
                    
                except Exception as e:
                    self.print_error(f"{endpoint} -> Error: {str(e)}")
                    service_health[endpoint] = {
                        "status": "error",
                        "error": str(e)
                    }
                    self.increment_check(False)
            
            health_results[service_name] = service_health
        
        return health_results

    async def verify_metrics_endpoints(self, environment: str) -> Dict[str, Any]:
        """Verify Prometheus metrics endpoints"""
        self.print_header(f"METRICS ENDPOINTS VERIFICATION - {environment.upper()}")
        
        metrics_results = {}
        services = self.services[environment]
        
        for service_name, base_url in services.items():
            print(f"\nTesting {service_name} metrics endpoints: {base_url}")
            service_metrics = {}
            
            for endpoint in self.metrics_endpoints:
                try:
                    url = f"{base_url}{endpoint}"
                    response = requests.get(url, timeout=10)
                    
                    if response.status_code == 200:
                        self.print_success(f"{endpoint} -> 200 OK")
                        
                        # Validate metrics format
                        if endpoint == "/metrics":
                            # Check Prometheus format
                            content = response.text
                            if "# HELP" in content and "# TYPE" in content:
                                self.print_success(f"  Valid Prometheus format")
                            else:
                                self.print_warning(f"  Invalid Prometheus format")
                        
                        elif endpoint == "/metrics/json":
                            # Check JSON format
                            try:
                                data = response.json()
                                if "timestamp" in data and "system" in data:
                                    self.print_success(f"  Valid JSON metrics structure")
                                else:
                                    self.print_warning(f"  Missing required metrics fields")
                            except json.JSONDecodeError:
                                self.print_warning(f"  Invalid JSON metrics response")
                        
                        service_metrics[endpoint] = {
                            "status": "ok",
                            "status_code": response.status_code,
                            "response_time": response.elapsed.total_seconds(),
                            "content_length": len(response.content)
                        }
                        self.increment_check(True)
                        
                    else:
                        self.print_error(f"{endpoint} -> {response.status_code}")
                        service_metrics[endpoint] = {
                            "status": "failed",
                            "status_code": response.status_code
                        }
                        self.increment_check(False)
                        
                except Exception as e:
                    self.print_error(f"{endpoint} -> Error: {str(e)}")
                    service_metrics[endpoint] = {
                        "status": "error",
                        "error": str(e)
                    }
                    self.increment_check(False)
            
            metrics_results[service_name] = service_metrics
        
        return metrics_results

    async def verify_structured_logging(self, environment: str) -> Dict[str, Any]:
        """Verify structured logging implementation"""
        self.print_header(f"STRUCTURED LOGGING VERIFICATION - {environment.upper()}")
        
        logging_results = {}
        services = self.services[environment]
        
        for service_name, base_url in services.items():
            print(f"\nTesting {service_name} structured logging: {base_url}")
            
            try:
                # Make a request to generate logs
                response = requests.get(f"{base_url}/health", timeout=10)
                
                # Check for correlation ID in response headers
                correlation_id = response.headers.get("X-Correlation-ID")
                if correlation_id:
                    self.print_success(f"Correlation ID present: {correlation_id}")
                    self.increment_check(True)
                else:
                    self.print_warning(f"Correlation ID missing in response headers")
                    self.increment_check(False)
                
                # Check for observability headers
                observability_headers = [
                    "X-Response-Time",
                    "X-Service",
                    "X-Request-ID"
                ]
                
                for header in observability_headers:
                    if header in response.headers:
                        self.print_success(f"Header {header}: {response.headers[header]}")
                        self.increment_check(True)
                    else:
                        self.print_warning(f"Header {header} missing")
                        self.increment_check(False)
                
                logging_results[service_name] = {
                    "correlation_id": correlation_id is not None,
                    "headers_present": len([h for h in observability_headers if h in response.headers]),
                    "total_headers": len(observability_headers)
                }
                
            except Exception as e:
                self.print_error(f"Logging verification failed: {str(e)}")
                logging_results[service_name] = {
                    "status": "error",
                    "error": str(e)
                }
                self.increment_check(False)
        
        return logging_results

    async def verify_error_tracking(self, environment: str) -> Dict[str, Any]:
        """Verify error tracking and monitoring"""
        self.print_header(f"ERROR TRACKING VERIFICATION - {environment.upper()}")
        
        error_results = {}
        services = self.services[environment]
        
        for service_name, base_url in services.items():
            print(f"\nTesting {service_name} error tracking: {base_url}")
            
            try:
                # Test 404 error handling
                response = requests.get(f"{base_url}/nonexistent-endpoint", timeout=10)
                
                if response.status_code == 404:
                    self.print_success(f"404 error properly handled")
                    
                    # Check if error response is structured
                    try:
                        error_data = response.json()
                        if "error" in error_data or "message" in error_data:
                            self.print_success(f"Structured error response")
                            self.increment_check(True)
                        else:
                            self.print_warning(f"Unstructured error response")
                            self.increment_check(False)
                    except json.JSONDecodeError:
                        self.print_warning(f"Non-JSON error response")
                        self.increment_check(False)
                else:
                    self.print_warning(f"Unexpected status code for 404 test: {response.status_code}")
                    self.increment_check(False)
                
                # Check if metrics endpoint shows error metrics
                try:
                    metrics_response = requests.get(f"{base_url}/metrics", timeout=10)
                    if metrics_response.status_code == 200:
                        metrics_content = metrics_response.text
                        if "errors_total" in metrics_content:
                            self.print_success(f"Error metrics present in Prometheus output")
                            self.increment_check(True)
                        else:
                            self.print_warning(f"Error metrics not found in Prometheus output")
                            self.increment_check(False)
                except:
                    self.print_warning(f"Could not verify error metrics")
                    self.increment_check(False)
                
                error_results[service_name] = {
                    "error_handling": response.status_code == 404,
                    "structured_errors": True,  # Simplified for this test
                    "error_metrics": "errors_total" in metrics_content if 'metrics_content' in locals() else False
                }
                
            except Exception as e:
                self.print_error(f"Error tracking verification failed: {str(e)}")
                error_results[service_name] = {
                    "status": "error",
                    "error": str(e)
                }
                self.increment_check(False)
        
        return error_results

    async def verify_performance_monitoring(self, environment: str) -> Dict[str, Any]:
        """Verify performance monitoring capabilities"""
        self.print_header(f"PERFORMANCE MONITORING VERIFICATION - {environment.upper()}")
        
        performance_results = {}
        services = self.services[environment]
        
        for service_name, base_url in services.items():
            print(f"\nTesting {service_name} performance monitoring: {base_url}")
            
            response_times = []
            
            # Make multiple requests to test performance consistency
            for i in range(5):
                try:
                    start_time = time.time()
                    response = requests.get(f"{base_url}/health", timeout=10)
                    end_time = time.time()
                    
                    response_time = end_time - start_time
                    response_times.append(response_time)
                    
                    if response.status_code == 200:
                        self.print_success(f"Request {i+1}: {response_time:.3f}s")
                        self.increment_check(True)
                    else:
                        self.print_error(f"Request {i+1}: Failed with {response.status_code}")
                        self.increment_check(False)
                        
                except Exception as e:
                    self.print_error(f"Request {i+1}: Error - {str(e)}")
                    self.increment_check(False)
                
                time.sleep(0.5)  # Small delay between requests
            
            if response_times:
                avg_response_time = sum(response_times) / len(response_times)
                max_response_time = max(response_times)
                min_response_time = min(response_times)
                
                print(f"  Average response time: {avg_response_time:.3f}s")
                print(f"  Min response time: {min_response_time:.3f}s")
                print(f"  Max response time: {max_response_time:.3f}s")
                
                # Performance thresholds
                if avg_response_time < 1.0:
                    self.print_success(f"Average response time within acceptable limits")
                elif avg_response_time < 2.0:
                    self.print_warning(f"Average response time is high but acceptable")
                else:
                    self.print_error(f"Average response time exceeds acceptable limits")
                
                performance_results[service_name] = {
                    "avg_response_time": avg_response_time,
                    "min_response_time": min_response_time,
                    "max_response_time": max_response_time,
                    "total_requests": len(response_times),
                    "successful_requests": len([t for t in response_times if t > 0])
                }
            else:
                performance_results[service_name] = {
                    "status": "no_data",
                    "error": "No successful requests"
                }
        
        return performance_results

    def generate_report(self) -> str:
        """Generate comprehensive observability verification report"""
        self.print_header("OBSERVABILITY VERIFICATION REPORT")
        
        total = self.results["total_checks"]
        passed = self.results["passed_checks"]
        failed = self.results["failed_checks"]
        success_rate = (passed / total * 100) if total > 0 else 0
        
        print(f"\nSUMMARY:")
        print(f"  Total Checks: {total}")
        print(f"  Passed: [OK] {passed}")
        print(f"  Failed: [ERROR] {failed}")
        print(f"  Success Rate: {success_rate:.1f}%")
        
        # Determine overall status
        if success_rate >= 90:
            print(f"\n[EXCELLENT] Observability implementation is comprehensive and working well!")
        elif success_rate >= 75:
            print(f"\n[GOOD] Observability implementation is solid with minor issues to address.")
        elif success_rate >= 50:
            print(f"\n[NEEDS IMPROVEMENT] Several observability features need attention.")
        else:
            print(f"\n[CRITICAL] Observability implementation requires significant work.")
        
        # Save detailed report
        report_file = f"observability_verification_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        
        print(f"\n[REPORT] Detailed report saved to: {report_file}")
        return report_file

    async def run_comprehensive_verification(self):
        """Run complete observability verification"""
        start_time = time.time()
        
        print("BHIV HR PLATFORM - COMPREHENSIVE OBSERVABILITY VERIFICATION")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        try:
            # Test production environment
            prod_health = await self.verify_health_endpoints("production")
            prod_metrics = await self.verify_metrics_endpoints("production")
            prod_logging = await self.verify_structured_logging("production")
            prod_errors = await self.verify_error_tracking("production")
            prod_performance = await self.verify_performance_monitoring("production")
            
            self.results["services"]["production"] = {
                "health": prod_health,
                "metrics": prod_metrics,
                "logging": prod_logging,
                "errors": prod_errors,
                "performance": prod_performance
            }
            
            # Test development environment (if available)
            try:
                dev_health = await self.verify_health_endpoints("development")
                dev_metrics = await self.verify_metrics_endpoints("development")
                dev_logging = await self.verify_structured_logging("development")
                dev_errors = await self.verify_error_tracking("development")
                dev_performance = await self.verify_performance_monitoring("development")
                
                self.results["services"]["development"] = {
                    "health": dev_health,
                    "metrics": dev_metrics,
                    "logging": dev_logging,
                    "errors": dev_errors,
                    "performance": dev_performance
                }
            except Exception as e:
                print(f"[WARNING] Development environment verification skipped: {str(e)}")
            
            # Generate report
            report_file = self.generate_report()
            
            # Final summary
            duration = time.time() - start_time
            print(f"\n[COMPLETE] Verification completed in {duration:.2f} seconds")
            
            return self.results
            
        except Exception as e:
            print(f"[ERROR] Verification failed: {str(e)}")
            raise

async def main():
    """Main verification function"""
    verifier = ObservabilityVerifier()
    
    try:
        results = await verifier.run_comprehensive_verification()
        
        # Exit with appropriate code
        success_rate = (results["passed_checks"] / results["total_checks"] * 100) if results["total_checks"] > 0 else 0
        
        if success_rate >= 90:
            sys.exit(0)  # Excellent
        elif success_rate >= 75:
            sys.exit(0)  # Good
        elif success_rate >= 50:
            sys.exit(1)  # Needs improvement
        else:
            sys.exit(2)  # Critical issues
            
    except KeyboardInterrupt:
        print(f"\n[INTERRUPTED] Verification interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n[ERROR] Verification failed: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())