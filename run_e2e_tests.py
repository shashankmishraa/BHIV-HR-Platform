#!/usr/bin/env python3
"""
BHIV HR Platform - E2E Test Execution Script
Main entry point for running comprehensive end-to-end tests
"""

import sys
import os
import argparse
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "tests"))

def main():
    """Main entry point for E2E testing"""
    
    parser = argparse.ArgumentParser(
        description="BHIV HR Platform - Comprehensive End-to-End Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run_e2e_tests.py                    # Run all tests
  python run_e2e_tests.py --workflow-only   # Run only workflow tests
  python run_e2e_tests.py --performance     # Run only performance tests
  python run_e2e_tests.py --regression      # Run only regression tests
  python run_e2e_tests.py --fail-fast       # Stop on first failure
  python run_e2e_tests.py --environment production  # Test production environment
        """
    )
    
    # Test selection arguments
    test_group = parser.add_mutually_exclusive_group()
    test_group.add_argument(
        "--workflow-only", 
        action="store_true",
        help="Run only end-to-end workflow tests"
    )
    test_group.add_argument(
        "--performance", 
        action="store_true",
        help="Run only performance benchmark tests"
    )
    test_group.add_argument(
        "--regression", 
        action="store_true",
        help="Run only regression validation tests"
    )
    
    # Test execution options
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop testing on first failure"
    )
    parser.add_argument(
        "--no-report",
        action="store_true", 
        help="Skip generating test reports"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    # Environment options
    parser.add_argument(
        "--environment",
        choices=["local", "staging", "production"],
        default="local",
        help="Target environment for testing (default: local)"
    )
    
    # Performance options
    parser.add_argument(
        "--performance-profile",
        choices=["light", "normal", "stress"],
        default="normal",
        help="Performance testing profile (default: normal)"
    )
    
    # Data options
    parser.add_argument(
        "--data-volume",
        choices=["small", "medium", "large"],
        default="medium",
        help="Test data volume (default: medium)"
    )
    
    args = parser.parse_args()
    
    # Import test runner
    try:
        from tests.test_runner_e2e import E2ETestRunner
    except ImportError as e:
        print(f"❌ Failed to import test runner: {e}")
        print("Make sure you're running from the project root directory")
        return 1
    
    # Configure test runner
    runner = E2ETestRunner()
    
    # Apply command line arguments
    if args.workflow_only:
        runner.config.update({
            "run_performance_tests": False,
            "run_regression_tests": False
        })
        print("🎯 Running workflow tests only")
        
    elif args.performance:
        runner.config.update({
            "run_workflow_tests": False,
            "run_regression_tests": False
        })
        print("⚡ Running performance tests only")
        
    elif args.regression:
        runner.config.update({
            "run_workflow_tests": False,
            "run_performance_tests": False
        })
        print("🔍 Running regression tests only")
    
    if args.fail_fast:
        runner.config["fail_fast"] = True
        print("🚨 Fail-fast mode enabled")
    
    if args.no_report:
        runner.config["generate_report"] = False
        print("📄 Report generation disabled")
    
    if args.verbose:
        print("📢 Verbose mode enabled")
    
    # Environment configuration
    if args.environment != "local":
        print(f"🌐 Testing environment: {args.environment}")
        # Update service URLs based on environment
        from tests.test_config import TestEnvironments
        env_config = TestEnvironments.get_environment(args.environment)
        
        # Update test configuration (this would need to be implemented in the test classes)
        print(f"   API Base: {env_config['api_base']}")
        print(f"   AI Base: {env_config['ai_base']}")
    
    # Performance profile
    if args.performance_profile != "normal":
        print(f"⚡ Performance profile: {args.performance_profile}")
    
    # Data volume
    if args.data_volume != "medium":
        print(f"📊 Data volume: {args.data_volume}")
    
    print()
    
    # Run tests
    try:
        success = runner.run_all_tests()
        
        if success:
            print("\n🎉 All E2E tests completed successfully!")
            return 0
        else:
            print("\n❌ Some E2E tests failed!")
            return 1
            
    except KeyboardInterrupt:
        print("\n⚠️ Tests interrupted by user")
        return 130
    except Exception as e:
        print(f"\n💥 Unexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())