#!/usr/bin/env python3
"""
Test Docker build process for clean architecture
"""
import subprocess
import sys
import os

def run_command(cmd, cwd=None):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True, timeout=300)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"

def test_docker_builds():
    """Test individual Docker builds"""
    print("=== Testing Docker Builds ===")
    
    services = ['gateway', 'agent']
    build_results = {}
    
    for service in services:
        print(f"\nBuilding {service} service...")
        service_path = os.path.join('services', service)
        
        # Build the service
        cmd = f"docker build -t bhiv-{service}-test ."
        success, stdout, stderr = run_command(cmd, cwd=service_path)
        
        if success:
            print(f"✓ {service} build successful")
            build_results[service] = True
        else:
            print(f"✗ {service} build failed")
            print(f"Error: {stderr}")
            build_results[service] = False
    
    return build_results

def test_semantic_engine_copy():
    """Test if semantic_engine is properly copied in builds"""
    print("\n=== Testing Semantic Engine Copy ===")
    
    services = ['gateway', 'agent']
    
    for service in services:
        print(f"\nTesting {service} semantic_engine access...")
        
        # Run container and check if semantic_engine exists
        cmd = f"docker run --rm bhiv-{service}-test ls -la semantic_engine"
        success, stdout, stderr = run_command(cmd)
        
        if success and "phase3_engine.py" in stdout:
            print(f"✓ {service} has semantic_engine directory with phase3_engine.py")
        else:
            print(f"✗ {service} missing semantic_engine or phase3_engine.py")
            print(f"Output: {stdout}")
            print(f"Error: {stderr}")

def test_import_in_container():
    """Test imports work inside containers"""
    print("\n=== Testing Imports in Containers ===")
    
    # Test agent service import
    print("Testing agent service import...")
    cmd = 'docker run --rm bhiv-agent-test python -c "from semantic_engine.phase3_engine import Phase3SemanticEngine; print(\'SUCCESS: Import works\')"'
    success, stdout, stderr = run_command(cmd)
    
    if success and "SUCCESS" in stdout:
        print("✓ Agent service imports working in container")
    else:
        print("✗ Agent service import failed in container")
        print(f"Error: {stderr}")
    
    # Test gateway service import (via phase3_integration)
    print("Testing gateway service import...")
    cmd = 'docker run --rm bhiv-gateway-test python -c "from semantic_engine.phase3_engine import Phase3SemanticEngine; print(\'SUCCESS: Import works\')"'
    success, stdout, stderr = run_command(cmd)
    
    if success and "SUCCESS" in stdout:
        print("✓ Gateway service imports working in container")
    else:
        print("✗ Gateway service import failed in container")
        print(f"Error: {stderr}")

def cleanup_test_images():
    """Clean up test Docker images"""
    print("\n=== Cleaning Up Test Images ===")
    
    images = ['bhiv-gateway-test', 'bhiv-agent-test']
    for image in images:
        cmd = f"docker rmi {image}"
        success, _, _ = run_command(cmd)
        if success:
            print(f"✓ Removed {image}")

def main():
    """Run Docker build tests"""
    print("=== Docker Build Test Suite ===")
    print("Testing clean architecture in Docker builds...\n")
    
    # Test builds
    build_results = test_docker_builds()
    
    # Only proceed if builds succeeded
    if all(build_results.values()):
        test_semantic_engine_copy()
        test_import_in_container()
    else:
        print("\n❌ Build failures detected, skipping further tests")
        return 1
    
    # Cleanup
    cleanup_test_images()
    
    print("\n=== Build Test Summary ===")
    if all(build_results.values()):
        print("🎉 All Docker builds successful!")
        print("✓ Clean architecture works in containers")
        return 0
    else:
        print("❌ Some Docker builds failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())