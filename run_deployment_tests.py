#!/usr/bin/env python3
"""
Master test runner for local deployment
"""
import subprocess
import sys
import time

def run_test_script(script_name):
    """Run a test script and return result"""
    print(f"\n{'='*50}")
    print(f"Running {script_name}")
    print('='*50)
    
    try:
        result = subprocess.run([sys.executable, script_name], timeout=600)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print(f"❌ {script_name} timed out")
        return False
    except Exception as e:
        print(f"❌ {script_name} failed: {e}")
        return False

def main():
    """Run all deployment tests"""
    print("🚀 BHIV HR Platform - Local Deployment Test Suite")
    print("Testing clean architecture implementation...")
    
    tests = [
        ("Clean Import Architecture", "test_clean_imports.py"),
        ("Docker Build Process", "test_docker_build.py"),
        ("Local Deployment", "test_local_deployment.py")
    ]
    
    results = {}
    
    for test_name, script in tests:
        print(f"\n🧪 Starting: {test_name}")
        success = run_test_script(script)
        results[test_name] = success
        
        if success:
            print(f"✅ {test_name}: PASSED")
        else:
            print(f"❌ {test_name}: FAILED")
        
        # Small delay between tests
        time.sleep(2)
    
    # Final summary
    print(f"\n{'='*60}")
    print("🏁 FINAL TEST RESULTS")
    print('='*60)
    
    passed = 0
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:.<40} {status}")
        if success:
            passed += 1
    
    print(f"\n📊 Summary: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Clean architecture deployment is working correctly")
        return 0
    else:
        print("⚠️  Some tests failed")
        print("❌ Check the output above for details")
        return 1

if __name__ == "__main__":
    sys.exit(main())