#!/usr/bin/env python3
"""
Test script to verify import fixes for deployment
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
        # Test the import logic from app.py
        semantic_engine_path = "/app/services/semantic_engine"
        services_path = "/app/services"
        local_semantic_path = os.path.join(os.path.dirname(__file__), 'services', 'semantic_engine')
        
        # Add paths for both local and deployment
        sys.path.insert(0, semantic_engine_path)
        sys.path.insert(0, services_path)
        sys.path.insert(0, local_semantic_path)
        sys.path.insert(0, "/app")
        
        # Try multiple import strategies
        PHASE3_AVAILABLE = False
        Phase3SemanticEngine = None
        
        try:
            from semantic_engine.phase3_engine import Phase3SemanticEngine
            PHASE3_AVAILABLE = True
            print("✓ Successfully imported from semantic_engine.phase3_engine")
        except ImportError:
            try:
                from phase3_engine import Phase3SemanticEngine
                PHASE3_AVAILABLE = True
                print("✓ Successfully imported from phase3_engine")
            except ImportError:
                try:
                    # Try direct file import
                    import importlib.util
                    phase3_file = os.path.join(agent_path, 'phase3_engine.py')
                    if os.path.exists(phase3_file):
                        spec = importlib.util.spec_from_file_location("phase3_engine", phase3_file)
                        phase3_module = importlib.util.module_from_spec(spec)
                        spec.loader.exec_module(phase3_module)
                        
                        Phase3SemanticEngine = phase3_module.Phase3SemanticEngine
                        PHASE3_AVAILABLE = True
                        print("✓ Successfully imported via direct file import")
                except Exception as e:
                    print(f"✗ Phase 3 engine not available: {e}")
                    PHASE3_AVAILABLE = False
        
        if PHASE3_AVAILABLE:
            print("✓ Agent service imports working correctly")
            return True
        else:
            print("✗ Agent service imports failed")
            return False
            
    except Exception as e:
        print(f"✗ Agent service import test failed: {e}")
        return False

def test_gateway_imports():
    """Test gateway service imports"""
    print("\nTesting gateway service imports...")
    
    # Add gateway service to path
    gateway_path = os.path.join(os.path.dirname(__file__), 'services', 'gateway')
    sys.path.insert(0, gateway_path)
    
    try:
        # Test the import logic from phase3_integration.py
        try:
            from semantic_engine.phase3_engine import Phase3SemanticEngine
            PHASE3_AVAILABLE = True
            print("✓ Successfully imported from semantic_engine.phase3_engine")
        except ImportError:
            try:
                from phase3_engine import Phase3SemanticEngine
                PHASE3_AVAILABLE = True
                print("✓ Successfully imported from phase3_engine")
            except ImportError:
                try:
                    # Try to import from semantic_engine directory
                    semantic_path = os.path.join(os.path.dirname(__file__), 'services', 'semantic_engine')
                    sys.path.insert(0, semantic_path)
                    from phase3_engine import Phase3SemanticEngine
                    PHASE3_AVAILABLE = True
                    print("✓ Successfully imported from semantic_engine directory")
                except ImportError:
                    PHASE3_AVAILABLE = False
                    Phase3SemanticEngine = None
                    print("✗ Phase 3 engine not available for gateway")
        
        if PHASE3_AVAILABLE:
            print("✓ Gateway service imports working correctly")
            return True
        else:
            print("✗ Gateway service imports failed")
            return False
            
    except Exception as e:
        print(f"✗ Gateway service import test failed: {e}")
        return False

def main():
    """Run all import tests"""
    print("=== Testing Import Fixes for Deployment ===\n")
    
    agent_success = test_agent_imports()
    gateway_success = test_gateway_imports()
    
    print(f"\n=== Test Results ===")
    print(f"Agent Service: {'✓ PASS' if agent_success else '✗ FAIL'}")
    print(f"Gateway Service: {'✓ PASS' if gateway_success else '✗ FAIL'}")
    
    if agent_success and gateway_success:
        print("\n🎉 All import fixes are working correctly!")
        return 0
    else:
        print("\n❌ Some import fixes need attention")
        return 1

if __name__ == "__main__":
    sys.exit(main())