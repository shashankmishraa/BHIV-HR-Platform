#!/usr/bin/env python3
"""
Simple test script to verify import fixes for deployment
"""
import sys
import os

def test_agent_imports():
    """Test agent service imports"""
    print("Testing agent service imports...")
    
    # Add agent service to path
    agent_path = os.path.join(os.path.dirname(__file__), 'services', 'agent')
    sys.path.insert(0, agent_path)
    
    try:
        # Test direct import from agent directory
        from phase3_engine import Phase3SemanticEngine
        print("SUCCESS: Agent service can import phase3_engine")
        return True
    except ImportError as e:
        print(f"FAILED: Agent service import failed: {e}")
        return False

def test_gateway_imports():
    """Test gateway service imports"""
    print("Testing gateway service imports...")
    
    # Add gateway service to path
    gateway_path = os.path.join(os.path.dirname(__file__), 'services', 'gateway')
    sys.path.insert(0, gateway_path)
    
    try:
        # Test direct import from gateway directory
        from phase3_engine import Phase3SemanticEngine
        print("SUCCESS: Gateway service can import phase3_engine")
        return True
    except ImportError as e:
        print(f"FAILED: Gateway service import failed: {e}")
        return False

def main():
    """Run all import tests"""
    print("=== Testing Import Fixes for Deployment ===")
    
    agent_success = test_agent_imports()
    gateway_success = test_gateway_imports()
    
    print("\n=== Test Results ===")
    print(f"Agent Service: {'PASS' if agent_success else 'FAIL'}")
    print(f"Gateway Service: {'PASS' if gateway_success else 'FAIL'}")
    
    if agent_success and gateway_success:
        print("\nAll import fixes are working correctly!")
        return 0
    else:
        print("\nSome import fixes need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())