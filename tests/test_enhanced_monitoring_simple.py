#!/usr/bin/env python3
"""
BHIV HR Platform - Enhanced Monitoring Test Suite (Simplified)
Testing core monitoring functionality without external dependencies
"""

import sys
import os
import time
import json
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def test_logging_config():
    """Test logging configuration components"""
    print("Testing Logging Configuration...")
    
    try:
        # Test imports
        from services.shared.logging_config import (
            StructuredFormatter, CentralizedLogger, CorrelationContext
        )
        
        # Test correlation context
        CorrelationContext.set_correlation_id("test-123")
        CorrelationContext.set_user_id("user-456")
        
        assert CorrelationContext.get_correlation_id() == "test-123"
        assert CorrelationContext.get_user_id() == "user-456"
        
        CorrelationContext.clear()
        assert CorrelationContext.get_correlation_id() is None
        
        print("PASS: Logging Configuration")
        return True
        
    except Exception as e:
        print(f"FAIL: Logging Configuration - {e}")
        return False

def test_error_tracking():
    """Test error tracking components"""
    print("Testing Error Tracking...")
    
    try:
        from services.shared.error_tracking import (
            ErrorTracker, ErrorClassifier, ErrorCorrelator,
            ErrorSeverity, ErrorCategory, create_error_context
        )
        
        # Test error classification
        classifier = ErrorClassifier()
        category, severity = classifier.classify_error(
            "Connection to database failed",
            "DatabaseError", 
            "psycopg2.OperationalError"
        )
        
        assert category == ErrorCategory.DATABASE
        
        # Test error context creation
        context = create_error_context(
            service_name="test_service",
            endpoint="/test",
            user_id="test_user"
        )
        
        assert context.service_name == "test_service"
        assert context.endpoint == "/test"
        assert context.user_id == "test_user"
        
        # Test error tracking
        tracker = ErrorTracker("test_service")
        error_event = tracker.track_error(
            error_type="TestError",
            error_message="Test error message",
            stack_trace="Test stack trace",
            context=context
        )
        
        assert error_event.service_name == "test_service"
        assert error_event.error_type == "TestError"
        
        print("PASS: Error Tracking")
        return True
        
    except Exception as e:
        print(f"FAIL: Error Tracking - {e}")
        return False

def test_health_checks_basic():
    """Test basic health check components"""
    print("Testing Health Checks (Basic)...")
    
    try:
        from services.shared.health_checks import (
            HealthCheckManager, HealthStatus, BaseHealthCheck
        )
        
        # Test health status enum
        assert HealthStatus.HEALTHY.value == "healthy"
        assert HealthStatus.DEGRADED.value == "degraded"
        assert HealthStatus.UNHEALTHY.value == "unhealthy"
        
        # Test health manager creation
        manager = HealthCheckManager()
        assert manager is not None
        assert len(manager.checks) == 0
        
        # Test adding system resources check
        manager.add_system_resources_check()
        assert len(manager.checks) == 1
        
        print("PASS: Health Checks (Basic)")
        return True
        
    except Exception as e:
        print(f"FAIL: Health Checks (Basic) - {e}")
        return False

def test_monitoring_integration():
    """Test monitoring component integration"""
    print("Testing Monitoring Integration...")
    
    try:
        # Test that all components can be imported together
        from services.shared.logging_config import get_logger, CorrelationContext
        from services.shared.error_tracking import ErrorTracker, create_error_context
        from services.shared.health_checks import HealthCheckManager
        
        # Test integrated workflow
        logger = get_logger("integration_test")
        error_tracker = ErrorTracker("integration_test")
        health_manager = HealthCheckManager()
        
        # Set correlation context
        CorrelationContext.set_correlation_id("integration-123")
        
        # Log an event
        logger.info("Integration test started")
        
        # Track an error
        context = create_error_context(
            service_name="integration_test",
            endpoint="/test"
        )
        
        error_tracker.track_error(
            error_type="IntegrationError",
            error_message="Test integration error",
            stack_trace="Test stack trace",
            context=context
        )
        
        # Get error summary
        summary = error_tracker.get_error_summary(1)
        assert summary['total_errors'] >= 1
        
        # Clear context
        CorrelationContext.clear()
        
        print("PASS: Monitoring Integration")
        return True
        
    except Exception as e:
        print(f"FAIL: Monitoring Integration - {e}")
        return False

def test_performance_monitoring():
    """Test performance monitoring capabilities"""
    print("Testing Performance Monitoring...")
    
    try:
        from services.shared.logging_config import get_logger
        
        logger = get_logger("performance_test")
        
        # Test API request logging
        start_time = time.time()
        time.sleep(0.01)  # Simulate processing
        response_time = time.time() - start_time
        
        logger.log_api_request(
            method="GET",
            endpoint="/performance-test",
            status_code=200,
            response_time=response_time
        )
        
        # Test database operation logging
        logger.log_database_operation(
            operation="SELECT",
            table="test_table",
            duration=0.025,
            success=True
        )
        
        # Test business event logging
        logger.log_business_event(
            event_type="performance_test",
            entity_id="test-123",
            action="completed"
        )
        
        print("PASS: Performance Monitoring")
        return True
        
    except Exception as e:
        print(f"FAIL: Performance Monitoring - {e}")
        return False

def test_error_patterns():
    """Test error pattern detection"""
    print("Testing Error Pattern Detection...")
    
    try:
        from services.shared.error_tracking import ErrorCorrelator
        
        correlator = ErrorCorrelator()
        
        # Test fingerprint generation
        fingerprint1 = correlator.generate_fingerprint(
            "ValueError",
            "Invalid input: user ID 123 not found",
            "File test.py, line 10"
        )
        
        fingerprint2 = correlator.generate_fingerprint(
            "ValueError",
            "Invalid input: user ID 456 not found", 
            "File test.py, line 10"
        )
        
        # Should generate same fingerprint (normalized)
        assert fingerprint1 == fingerprint2
        
        print("PASS: Error Pattern Detection")
        return True
        
    except Exception as e:
        print(f"FAIL: Error Pattern Detection - {e}")
        return False

def run_all_tests():
    """Run all monitoring tests"""
    print("BHIV HR Platform - Enhanced Monitoring Test Suite")
    print("=" * 60)
    
    tests = [
        test_logging_config,
        test_error_tracking,
        test_health_checks_basic,
        test_monitoring_integration,
        test_performance_monitoring,
        test_error_patterns
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"FAIL: Test {test.__name__} failed with exception: {e}")
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests PASSED! Enhanced monitoring system is ready.")
        print("\nMonitoring Capabilities Verified:")
        print("   - Centralized structured logging")
        print("   - Advanced error tracking and classification")
        print("   - Health check infrastructure")
        print("   - Cross-service correlation")
        print("   - Performance monitoring")
        print("   - Error pattern detection")
    else:
        print(f"WARNING: {total - passed} tests failed. Please review implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)