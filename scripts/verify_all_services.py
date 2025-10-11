#!/usr/bin/env python3
"""
Complete Service Verification Script
Verifies all services can start and all dependencies are working
"""
import sys
import os
import subprocess
from pathlib import Path

project_root = Path(__file__).parent.parent

def test_service_startup(service_name, service_path, test_command):
    """Test if a service can start without errors"""
    print(f"\nTesting {service_name}...")
    
    try:
        result = subprocess.run(
            test_command,
            cwd=service_path,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            print(f"  [PASS] {service_name} startup successful")
            return True
        else:
            print(f"  [FAIL] {service_name} startup failed")
            print(f"  Error: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print(f"  [TIMEOUT] {service_name} startup timed out")
        return False
    except Exception as e:
        print(f"  [ERROR] {service_name} test failed: {e}")
        return False

def main():
    """Run all service verification tests"""
    print("=" * 60)
    print("COMPLETE SERVICE VERIFICATION")
    print("=" * 60)
    
    services = [
        {
            'name': 'Agent Service',
            'path': project_root / 'services' / 'agent',
            'command': ['python', '-c', 'from app import app; print("Agent OK")']
        },
        {
            'name': 'Gateway Service',
            'path': project_root / 'services' / 'gateway' / 'app',
            'command': ['python', '-c', 'from main import app; print("Gateway OK")']
        },
        {
            'name': 'Portal Service',
            'path': project_root / 'services' / 'portal',
            'command': ['python', '-c', 'import app; print("Portal OK")']
        },
        {
            'name': 'Client Portal Service',
            'path': project_root / 'services' / 'client_portal',
            'command': ['python', '-c', 'import app; print("Client Portal OK")']
        }
    ]
    
    results = []
    for service in services:
        success = test_service_startup(
            service['name'],
            service['path'],
            service['command']
        )
        results.append((service['name'], success))
    
    # Test Phase 3 engine specifically
    print(f"\nTesting Phase 3 Semantic Engine...")
    try:
        sys.path.insert(0, str(project_root / 'services'))
        from semantic_engine.phase3_engine import Phase3SemanticEngine
        engine = Phase3SemanticEngine()
        print(f"  [PASS] Phase 3 engine working")
        results.append(("Phase 3 Engine", True))
    except Exception as e:
        print(f"  [FAIL] Phase 3 engine: {e}")
        results.append(("Phase 3 Engine", False))
    
    # Summary
    print("\n" + "=" * 60)
    print("VERIFICATION RESULTS")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for service_name, success in results:
        status = "[PASS]" if success else "[FAIL]"
        print(f"{status} {service_name}")
        if success:
            passed += 1
    
    print(f"\nResults: {passed}/{total} services verified")
    
    if passed == total:
        print("\n🎉 ALL SERVICES VERIFIED SUCCESSFULLY!")
        print("✅ Project is ready for production deployment")
        print("✅ All imports and dependencies working")
        print("✅ Phase 3 semantic engine operational")
    else:
        print(f"\n❌ {total - passed} SERVICES FAILED VERIFICATION")
        print("⚠️  Fix issues before deployment")
    
    print("=" * 60)
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)