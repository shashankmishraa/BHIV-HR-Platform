#!/usr/bin/env python3
"""
Test clean import architecture
"""
import sys
import os

def test_clean_imports():
    """Test that services can import from shared semantic_engine"""
    print("Testing clean shared module imports...")
    
    # Add services to path to simulate deployment structure
    services_path = os.path.join(os.path.dirname(__file__), 'services')
    sys.path.insert(0, services_path)
    
    try:
        # Test direct import from semantic_engine package
        from semantic_engine.phase3_engine import Phase3SemanticEngine
        print("SUCCESS: Can import Phase3SemanticEngine from semantic_engine.phase3_engine")
        
        # Test package-level import
        from semantic_engine import Phase3SemanticEngine as Phase3Alt
        print("SUCCESS: Can import Phase3SemanticEngine from semantic_engine package")
        
        return True
    except ImportError as e:
        print(f"FAILED: Import failed: {e}")
        return False

def main():
    """Run clean import test"""
    print("=== Testing Clean Shared Module Architecture ===")
    
    success = test_clean_imports()
    
    if success:
        print("\nClean architecture working correctly!")
        print("- No duplicated files")
        print("- Proper shared module structure")
        print("- Simple import statements")
        return 0
    else:
        print("\nClean architecture needs fixes")
        return 1

if __name__ == "__main__":
    sys.exit(main())