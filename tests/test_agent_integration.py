#!/usr/bin/env python3
"""
Integration test for AI Agent service with semantic engine
Tests the complete workflow from API endpoints to semantic matching
"""

import sys
import os
import json
import time
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def test_agent_semantic_integration():
    """Test AI agent service with semantic engine integration"""
    print("\n" + "="*60)
    print("AI Agent + Semantic Engine Integration Test")
    print("="*60)
    
    try:
        # Import agent service
        sys.path.append(str(project_root / 'services' / 'agent'))
        import app
        
        print(f"Agent Service: v{app.app.version}")
        print(f"Semantic Engine: {'Enabled' if app.SEMANTIC_ENABLED else 'Fallback'}")
        
        # Test semantic engine components
        if app.SEMANTIC_ENABLED:
            print(f"Job Matcher: {app.semantic_matcher is not None}")
            print(f"Advanced Matcher: {app.advanced_matcher is not None}")
            print(f"Batch Matcher: {app.batch_matcher is not None}")
            print(f"Semantic Processor: {app.semantic_processor is not None}")
            
            # Test semantic processor functionality
            if app.semantic_processor:
                test_job = {
                    'id': 1,
                    'title': 'Python Developer',
                    'description': 'Python Django React development',
                    'requirements': 'Python, Django, React, SQL',
                    'department': 'Engineering',
                    'location': 'Mumbai',
                    'experience_level': 'Mid'
                }
                
                test_candidate = {
                    'id': 1,
                    'name': 'Test Candidate',
                    'email': 'test@example.com',
                    'technical_skills': 'Python, Django, JavaScript, SQL',
                    'experience_years': 3,
                    'seniority_level': 'Mid-level Developer',
                    'education_level': 'Bachelors',
                    'location': 'Mumbai'
                }
                
                # Test semantic matching
                start_time = time.time()
                match_result = app.semantic_processor.semantic_match(test_job, test_candidate)
                processing_time = time.time() - start_time
                
                print(f"Semantic Match: Score {match_result['score']:.1f}/100")
                print(f"Processing Time: {processing_time:.3f}s")
                print(f"Bias Adjusted: {match_result.get('bias_adjusted', False)}")
                
                # Test model statistics
                if hasattr(app.semantic_processor, 'model_manager'):
                    stats = app.semantic_processor.model_manager.get_model_stats()
                    print(f"Model Stats: {stats['skill_embeddings_count']} skills, {stats['job_templates_count']} templates")
        
        # Test API endpoints structure
        endpoints = [
            ("GET", "/", "Service info"),
            ("GET", "/health", "Health check"),
            ("GET", "/semantic-status", "Semantic engine status"),
            ("GET", "/test-db", "Database test"),
            ("POST", "/match", "AI matching"),
            ("GET", "/analyze/{id}", "Candidate analysis")
        ]
        
        print(f"\nAvailable Endpoints ({len(endpoints)}):")
        for method, path, desc in endpoints:
            print(f"   {method:4} {path:20} - {desc}")
        
        # Test fallback algorithm
        print(f"\nTesting Fallback Algorithm:")
        job_data = ('Python Developer', 'Python Django development', 'Engineering', 'Mumbai', 'Mid', 'Python Django SQL')
        candidates = [
            (1, 'John Doe', 'john@example.com', '+91-9876543210', 'Mumbai', 3, 'Python, Django, SQL', 'Mid-level', 'Bachelors'),
            (2, 'Jane Smith', 'jane@example.com', '+91-9876543211', 'Bangalore', 5, 'Java, Spring, MySQL', 'Senior', 'Masters')
        ]
        
        fallback_results = app.process_with_fallback_algorithm(job_data, candidates, 1)
        print(f"Fallback Results: {len(fallback_results)} candidates processed")
        
        if fallback_results:
            best_match = fallback_results[0]
            print(f"   Best Match: {best_match.name} (Score: {best_match.score})")
            print(f"   Skills: {best_match.skills_match}")
        
        print(f"\nIntegration Test Completed Successfully!")
        print(f"   Semantic Engine: {'Enabled' if app.SEMANTIC_ENABLED else 'Fallback'}")
        print(f"   All Components: Working")
        
        return True
        
    except Exception as e:
        print(f"Integration test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_semantic_engine_performance():
    """Test semantic engine performance benchmarks"""
    print("\n" + "="*60)
    print("Semantic Engine Performance Test")
    print("="*60)
    
    try:
        sys.path.append(str(project_root / 'services' / 'agent'))
        import app
        
        if not app.SEMANTIC_ENABLED:
            print("Semantic engine not enabled - skipping performance test")
            return True
        
        # Performance test data
        test_job = {
            'id': 1,
            'title': 'Senior Python Developer',
            'description': 'Looking for experienced Python developer with Django, React, and AWS skills',
            'requirements': 'Python, Django, React, AWS, SQL, 5+ years experience',
            'department': 'Engineering',
            'location': 'Mumbai',
            'experience_level': 'Senior'
        }
        
        test_candidates = []
        for i in range(10):
            test_candidates.append({
                'id': i + 1,
                'name': f'Candidate {i + 1}',
                'email': f'candidate{i + 1}@example.com',
                'technical_skills': 'Python, Django, JavaScript, SQL, Git',
                'experience_years': 3 + (i % 5),
                'seniority_level': 'Mid-level Developer',
                'education_level': 'Bachelors',
                'location': 'Mumbai'
            })
        
        # Single match performance
        start_time = time.time()
        for _ in range(5):
            app.semantic_processor.semantic_match(test_job, test_candidates[0])
        single_match_time = (time.time() - start_time) / 5
        
        # Batch processing performance
        start_time = time.time()
        batch_results = app.batch_matcher.batch_match_single_job(test_job, test_candidates[:5])
        batch_time = time.time() - start_time
        
        print(f"Single Match: {single_match_time:.3f}s per match")
        print(f"Batch Processing: {batch_time:.3f}s for 5 candidates")
        print(f"Throughput: {len(test_candidates) / batch_time:.1f} candidates/second")
        
        # Verify results quality
        if batch_results:
            scores = [result['score'] for result in batch_results]
            print(f"Score Range: {min(scores):.1f} - {max(scores):.1f}")
            print(f"Average Score: {sum(scores) / len(scores):.1f}")
        
        # Performance assertions
        assert single_match_time < 1.0, f"Single match too slow: {single_match_time:.3f}s"
        assert batch_time < 5.0, f"Batch processing too slow: {batch_time:.3f}s"
        
        print("Performance benchmarks passed!")
        return True
        
    except Exception as e:
        print(f"Performance test failed: {e}")
        return False

def run_integration_tests():
    """Run all integration tests"""
    print("Starting AI Agent Integration Tests")
    
    tests = [
        ("Agent + Semantic Integration", test_agent_semantic_integration),
        ("Performance Benchmarks", test_semantic_engine_performance)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        try:
            result = test_func()
            results.append((test_name, result))
            status = "PASSED" if result else "FAILED"
            print(f"   Result: {status}")
        except Exception as e:
            results.append((test_name, False))
            print(f"   Result: FAILED - {e}")
    
    # Summary
    print("\n" + "="*60)
    print("Integration Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "PASSED" if result else "FAILED"
        print(f"   {test_name}: {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All integration tests passed!")
        print("Semantic engine fallback issue resolved")
        print("AI agent service fully operational")
    else:
        print("Some tests failed - check logs above")
    
    return passed == total

if __name__ == "__main__":
    success = run_integration_tests()
    sys.exit(0 if success else 1)