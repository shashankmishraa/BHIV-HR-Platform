#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive E2E Test Runner
Orchestrates all end-to-end testing including workflows, performance, and regression tests
"""

import sys
import os
import json
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import test modules
from test_e2e_workflows import E2EWorkflowTester
from test_workflow_performance import WorkflowPerformanceTester

class E2ETestRunner:
    """Comprehensive end-to-end test runner"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
        
        # Test configuration
        self.config = {
            "run_workflow_tests": True,
            "run_performance_tests": True,
            "run_regression_tests": True,
            "generate_report": True,
            "cleanup_after_tests": True,
            "fail_fast": False
        }
        
        # Test categories
        self.test_categories = {
            "workflow": "End-to-End Workflow Tests",
            "performance": "Performance Benchmark Tests", 
            "regression": "Regression Validation Tests"
        }
    
    def setup_test_environment(self) -> bool:
        """Setup test environment and verify prerequisites"""
        print("🔧 Setting up test environment...")
        
        # Check if services are running
        import requests
        
        services = [
            ("API Gateway", "http://localhost:8000/health"),
            ("AI Agent", "http://localhost:9000/health")
        ]
        
        all_services_ready = True
        
        for service_name, health_url in services:
            try:
                response = requests.get(health_url, timeout=5)
                if response.status_code == 200:
                    print(f"   ✅ {service_name}: Ready")
                else:
                    print(f"   ❌ {service_name}: Not ready ({response.status_code})")
                    all_services_ready = False
            except Exception as e:
                print(f"   ❌ {service_name}: Failed - {str(e)}")
                all_services_ready = False
        
        if not all_services_ready:
            print("❌ Not all services are ready. Please start all services before running E2E tests.")
            return False
        
        print("✅ Test environment ready")
        return True
    
    def run_workflow_tests(self) -> Dict[str, Any]:
        """Run end-to-end workflow tests"""
        print("\n" + "="*60)
        print("🎯 RUNNING WORKFLOW TESTS")
        print("="*60)
        
        try:
            workflow_tester = E2EWorkflowTester()
            results = workflow_tester.run_all_workflows()
            
            # Calculate summary statistics
            total_workflows = len(results)
            passed_workflows = sum(1 for result in results.values() if result)
            success_rate = passed_workflows / total_workflows if total_workflows > 0 else 0
            
            return {
                "category": "workflow",
                "total_tests": total_workflows,
                "passed_tests": passed_workflows,
                "failed_tests": total_workflows - passed_workflows,
                "success_rate": success_rate,
                "results": results,
                "status": "passed" if success_rate == 1.0 else "failed"
            }
            
        except Exception as e:
            print(f"❌ Workflow tests failed: {str(e)}")
            return {
                "category": "workflow",
                "status": "error",
                "error": str(e)
            }
    
    def run_performance_tests(self) -> Dict[str, Any]:
        """Run performance benchmark tests"""
        print("\n" + "="*60)
        print("⚡ RUNNING PERFORMANCE TESTS")
        print("="*60)
        
        try:
            performance_tester = WorkflowPerformanceTester()
            results = performance_tester.run_performance_suite()
            
            # Calculate benchmark statistics
            benchmarks_met = 0
            total_benchmarks = 0
            
            for result in results.values():
                if isinstance(result, dict) and "benchmark_met" in result:
                    if result["benchmark_met"]:
                        benchmarks_met += 1
                    total_benchmarks += 1
            
            benchmark_success_rate = benchmarks_met / total_benchmarks if total_benchmarks > 0 else 0
            
            return {
                "category": "performance",
                "total_benchmarks": total_benchmarks,
                "passed_benchmarks": benchmarks_met,
                "failed_benchmarks": total_benchmarks - benchmarks_met,
                "benchmark_success_rate": benchmark_success_rate,
                "results": results,
                "status": "passed" if benchmark_success_rate >= 0.8 else "failed"  # 80% threshold
            }
            
        except Exception as e:
            print(f"❌ Performance tests failed: {str(e)}")
            return {
                "category": "performance",
                "status": "error",
                "error": str(e)
            }
    
    def run_regression_tests(self) -> Dict[str, Any]:
        """Run regression validation tests"""
        print("\n" + "="*60)
        print("🔍 RUNNING REGRESSION TESTS")
        print("="*60)
        
        try:
            # Import and run existing test modules
            import subprocess
            
            regression_tests = [
                ("API Endpoints", "test_endpoints.py"),
                ("Security Features", "test_security.py"),
                ("Agent Integration", "test_agent_integration.py"),
                ("HTTP Methods", "test_http_method_integration.py")
            ]
            
            results = {}
            total_passed = 0
            total_tests = len(regression_tests)
            
            for test_name, test_file in regression_tests:
                print(f"\n🧪 Running {test_name}...")
                
                try:
                    # Run test file
                    test_path = project_root / "tests" / test_file
                    if test_path.exists():
                        result = subprocess.run(
                            [sys.executable, str(test_path)],
                            capture_output=True,
                            text=True,
                            timeout=60
                        )
                        
                        success = result.returncode == 0
                        results[test_name] = {
                            "success": success,
                            "returncode": result.returncode,
                            "stdout": result.stdout,
                            "stderr": result.stderr
                        }
                        
                        if success:
                            total_passed += 1
                            print(f"   ✅ {test_name}: PASSED")
                        else:
                            print(f"   ❌ {test_name}: FAILED")
                    else:
                        results[test_name] = {
                            "success": False,
                            "error": f"Test file not found: {test_file}"
                        }
                        print(f"   ⚠️ {test_name}: SKIPPED (file not found)")
                        
                except Exception as e:
                    results[test_name] = {
                        "success": False,
                        "error": str(e)
                    }
                    print(f"   ❌ {test_name}: ERROR - {str(e)}")
            
            success_rate = total_passed / total_tests if total_tests > 0 else 0
            
            return {
                "category": "regression",
                "total_tests": total_tests,
                "passed_tests": total_passed,
                "failed_tests": total_tests - total_passed,
                "success_rate": success_rate,
                "results": results,
                "status": "passed" if success_rate >= 0.9 else "failed"  # 90% threshold for regression
            }
            
        except Exception as e:
            print(f"❌ Regression tests failed: {str(e)}")
            return {
                "category": "regression",
                "status": "error",
                "error": str(e)
            }
    
    def generate_test_report(self) -> str:
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("📊 GENERATING TEST REPORT")
        print("="*60)
        
        report_data = {
            "test_run_info": {
                "start_time": self.start_time.isoformat() if self.start_time else None,
                "end_time": self.end_time.isoformat() if self.end_time else None,
                "duration": (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else None,
                "timestamp": datetime.now().isoformat()
            },
            "test_results": self.test_results,
            "summary": self.calculate_overall_summary()
        }
        
        # Generate JSON report
        reports_dir = project_root / "tests" / "reports"
        reports_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = reports_dir / f"e2e_test_report_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        # Generate human-readable report
        text_report = self.generate_text_report(report_data)
        text_report_file = reports_dir / f"e2e_test_report_{timestamp}.txt"
        
        with open(text_report_file, 'w') as f:
            f.write(text_report)
        
        print(f"📄 JSON Report: {report_file}")
        print(f"📄 Text Report: {text_report_file}")
        
        return str(text_report_file)
    
    def generate_text_report(self, report_data: Dict[str, Any]) -> str:
        """Generate human-readable text report"""
        lines = []
        lines.append("BHIV HR PLATFORM - END-TO-END TEST REPORT")
        lines.append("=" * 60)
        lines.append("")
        
        # Test run info
        test_info = report_data["test_run_info"]
        lines.append("📅 TEST RUN INFORMATION")
        lines.append("-" * 30)
        lines.append(f"Start Time: {test_info.get('start_time', 'N/A')}")
        lines.append(f"End Time: {test_info.get('end_time', 'N/A')}")
        lines.append(f"Duration: {test_info.get('duration', 0):.2f} seconds")
        lines.append("")
        
        # Summary
        summary = report_data["summary"]
        lines.append("📊 OVERALL SUMMARY")
        lines.append("-" * 30)
        lines.append(f"Overall Status: {summary['overall_status'].upper()}")
        lines.append(f"Categories Tested: {summary['categories_tested']}")
        lines.append(f"Categories Passed: {summary['categories_passed']}")
        lines.append(f"Overall Success Rate: {summary['overall_success_rate']:.1%}")
        lines.append("")
        
        # Detailed results by category
        for category, result in self.test_results.items():
            category_name = self.test_categories.get(category, category.title())
            lines.append(f"🎯 {category_name.upper()}")
            lines.append("-" * 30)
            
            if result.get("status") == "error":
                lines.append(f"Status: ERROR - {result.get('error', 'Unknown error')}")
            else:
                lines.append(f"Status: {result.get('status', 'unknown').upper()}")
                
                if "total_tests" in result:
                    lines.append(f"Total Tests: {result['total_tests']}")
                    lines.append(f"Passed: {result['passed_tests']}")
                    lines.append(f"Failed: {result['failed_tests']}")
                    lines.append(f"Success Rate: {result['success_rate']:.1%}")
                
                if "total_benchmarks" in result:
                    lines.append(f"Total Benchmarks: {result['total_benchmarks']}")
                    lines.append(f"Passed: {result['passed_benchmarks']}")
                    lines.append(f"Failed: {result['failed_benchmarks']}")
                    lines.append(f"Benchmark Success Rate: {result['benchmark_success_rate']:.1%}")
            
            lines.append("")
        
        # Recommendations
        lines.append("💡 RECOMMENDATIONS")
        lines.append("-" * 30)
        
        if summary["overall_status"] == "passed":
            lines.append("✅ All tests passed! System is ready for production.")
            lines.append("✅ Multi-service workflows are functioning correctly.")
            lines.append("✅ Performance benchmarks are being met.")
        else:
            lines.append("❌ Some tests failed. Review the following:")
            
            for category, result in self.test_results.items():
                if result.get("status") == "failed":
                    category_name = self.test_categories.get(category, category.title())
                    lines.append(f"   • {category_name}: Requires attention")
        
        lines.append("")
        lines.append("🏁 End of Report")
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def calculate_overall_summary(self) -> Dict[str, Any]:
        """Calculate overall test summary"""
        categories_tested = len(self.test_results)
        categories_passed = sum(1 for result in self.test_results.values() if result.get("status") == "passed")
        
        overall_success_rate = categories_passed / categories_tested if categories_tested > 0 else 0
        overall_status = "passed" if overall_success_rate >= 0.8 else "failed"
        
        return {
            "categories_tested": categories_tested,
            "categories_passed": categories_passed,
            "categories_failed": categories_tested - categories_passed,
            "overall_success_rate": overall_success_rate,
            "overall_status": overall_status
        }
    
    def run_all_tests(self) -> bool:
        """Run all end-to-end tests"""
        print("🚀 BHIV HR PLATFORM - COMPREHENSIVE E2E TESTING")
        print("=" * 60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()
        
        self.start_time = datetime.now()
        
        # Setup test environment
        if not self.setup_test_environment():
            return False
        
        # Run test categories
        if self.config["run_workflow_tests"]:
            self.test_results["workflow"] = self.run_workflow_tests()
            
            if self.config["fail_fast"] and self.test_results["workflow"].get("status") == "failed":
                print("❌ Workflow tests failed - stopping due to fail_fast mode")
                return False
        
        if self.config["run_performance_tests"]:
            self.test_results["performance"] = self.run_performance_tests()
            
            if self.config["fail_fast"] and self.test_results["performance"].get("status") == "failed":
                print("❌ Performance tests failed - stopping due to fail_fast mode")
                return False
        
        if self.config["run_regression_tests"]:
            self.test_results["regression"] = self.run_regression_tests()
        
        self.end_time = datetime.now()
        
        # Generate report
        if self.config["generate_report"]:
            report_file = self.generate_test_report()
        
        # Print final summary
        self.print_final_summary()
        
        # Determine overall success
        summary = self.calculate_overall_summary()
        return summary["overall_status"] == "passed"
    
    def print_final_summary(self):
        """Print final test summary"""
        print("\n" + "="*60)
        print("🏁 FINAL E2E TEST SUMMARY")
        print("="*60)
        
        summary = self.calculate_overall_summary()
        
        print(f"📊 Categories Tested: {summary['categories_tested']}")
        print(f"✅ Categories Passed: {summary['categories_passed']}")
        print(f"❌ Categories Failed: {summary['categories_failed']}")
        print(f"📈 Overall Success Rate: {summary['overall_success_rate']:.1%}")
        
        if summary["overall_status"] == "passed":
            print("\n🎉 ALL E2E TESTS PASSED!")
            print("✅ Multi-service workflows verified")
            print("✅ Performance benchmarks met")
            print("✅ Regression tests passed")
            print("✅ System ready for production")
        else:
            print("\n❌ E2E TESTS FAILED")
            print("🔍 Review failed test categories")
            print("🚨 System requires fixes before production")
        
        duration = (self.end_time - self.start_time).total_seconds() if self.start_time and self.end_time else 0
        print(f"\n⏱️ Total Test Duration: {duration:.2f} seconds")
        print(f"🕐 Completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def main():
    """Main entry point for E2E test runner"""
    runner = E2ETestRunner()
    
    # Parse command line arguments
    import argparse
    parser = argparse.ArgumentParser(description="BHIV HR Platform E2E Test Runner")
    parser.add_argument("--workflow-only", action="store_true", help="Run only workflow tests")
    parser.add_argument("--performance-only", action="store_true", help="Run only performance tests")
    parser.add_argument("--regression-only", action="store_true", help="Run only regression tests")
    parser.add_argument("--fail-fast", action="store_true", help="Stop on first failure")
    parser.add_argument("--no-report", action="store_true", help="Skip report generation")
    
    args = parser.parse_args()
    
    # Configure test runner based on arguments
    if args.workflow_only:
        runner.config.update({"run_performance_tests": False, "run_regression_tests": False})
    elif args.performance_only:
        runner.config.update({"run_workflow_tests": False, "run_regression_tests": False})
    elif args.regression_only:
        runner.config.update({"run_workflow_tests": False, "run_performance_tests": False})
    
    if args.fail_fast:
        runner.config["fail_fast"] = True
    
    if args.no_report:
        runner.config["generate_report"] = False
    
    # Run tests
    success = runner.run_all_tests()
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())