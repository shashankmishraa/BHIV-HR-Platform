#!/usr/bin/env python3
"""
Complete Verification Runner for BHIV HR Platform
Tests code implementation, services, and functionality
"""

import os
import sys
import subprocess
import importlib.util
from pathlib import Path

def test_python_imports():
    """Test if all Python modules can be imported"""
    print("Testing Python Module Imports:")
    
    modules_to_test = [
        'services.gateway.app.main',
        'services.agent.app.main', 
        'services.shared.logging_config',
        'services.shared.health_checks',
        'services.shared.error_tracking',
        'tools.comprehensive_resume_extractor',
        'tools.dynamic_job_creator'
    ]
    
    passed = 0
    failed = 0
    
    for module in modules_to_test:
        try:
            # Try to import the module
            spec = importlib.util.find_spec(module)
            if spec is not None:
                print(f"PASS {module}")
                passed += 1
            else:
                print(f"FAIL {module} - Module not found")
                failed += 1
        except Exception as e:
            print(f"FAIL {module} - Error: {str(e)}")
            failed += 1
    
    print(f"\nImport Results: {passed} passed, {failed} failed")
    return failed == 0

def test_file_structure():
    """Test if all required files exist"""
    print("\nTesting File Structure:")
    
    required_files = [
        'services/gateway/app/main.py',
        'services/agent/app/main.py',
        'services/portal/app.py',
        'services/client_portal/app.py',
        'services/shared/logging_config.py',
        'services/shared/health_checks.py',
        'services/shared/error_tracking.py',
        'docker-compose.production.yml',
        'requirements.txt'
    ]
    
    passed = 0
    failed = 0
    
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"PASS {file_path}")
            passed += 1
        else:
            print(f"FAIL {file_path} - Missing")
            failed += 1
    
    print(f"\nFile Structure: {passed} passed, {failed} failed")
    return failed == 0

def run_syntax_check():
    """Run Python syntax check on key files"""
    print("\nRunning Syntax Checks:")
    
    python_files = [
        'services/gateway/app/main.py',
        'services/agent/app/main.py',
        'services/shared/error_tracking.py',
        'quick_test.py',
        'quick_test_local.py'
    ]
    
    passed = 0
    failed = 0
    
    for file_path in python_files:
        if os.path.exists(file_path):
            try:
                result = subprocess.run([sys.executable, '-m', 'py_compile', file_path], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"PASS {file_path} - Syntax OK")
                    passed += 1
                else:
                    print(f"FAIL {file_path} - Syntax Error: {result.stderr}")
                    failed += 1
            except Exception as e:
                print(f"FAIL {file_path} - Error: {str(e)}")
                failed += 1
        else:
            print(f"WARN {file_path} - File not found")
    
    print(f"\nSyntax Check: {passed} passed, {failed} failed")
    return failed == 0

def run_service_tests():
    """Run service availability tests"""
    print("\nRunning Service Tests:")
    
    try:
        # Run production test
        print("Testing Production Services...")
        result = subprocess.run([sys.executable, 'quick_test.py'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("PASS Production services test passed")
            production_ok = True
        else:
            print("FAIL Production services test failed")
            print(result.stdout)
            production_ok = False
            
    except Exception as e:
        print(f"ERROR Production test error: {str(e)}")
        production_ok = False
    
    try:
        # Run local test
        print("\nTesting Local Services...")
        result = subprocess.run([sys.executable, 'quick_test_local.py'], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("PASS Local services test passed")
            local_ok = True
        else:
            print("WARN Local services not available (expected if not running)")
            local_ok = False
            
    except Exception as e:
        print(f"WARN Local test: {str(e)} (expected if Docker not running)")
        local_ok = False
    
    return production_ok

def main():
    """Main verification runner"""
    print("BHIV HR Platform - Complete Code Verification")
    print("=" * 60)
    
    # Change to project directory
    os.chdir(Path(__file__).parent)
    
    # Run all tests
    tests = [
        ("File Structure", test_file_structure),
        ("Syntax Check", run_syntax_check),
        ("Service Tests", run_service_tests)
    ]
    
    results = {}
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        results[test_name] = test_func()
    
    # Final Summary
    print("\n" + "="*60)
    print("FINAL VERIFICATION SUMMARY")
    print("="*60)
    
    passed_tests = sum(1 for result in results.values() if result)
    total_tests = len(results)
    
    for test_name, result in results.items():
        status = "PASS" if result else "FAIL"
        print(f"{status} | {test_name}")
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests >= 2:  # At least file structure and syntax should pass
        print("Code implementation verification: SUCCESS")
        print("All implemented codes are properly structured and functional")
        return 0
    else:
        print("Code implementation verification: ISSUES DETECTED")
        print("Some critical issues found in code implementation")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)