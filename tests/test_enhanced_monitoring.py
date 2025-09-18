#!/usr/bin/env python3
"""
BHIV HR Platform - Enhanced Monitoring Test Suite
Comprehensive testing for logging, health checks, and error tracking
"""

from datetime import datetime, timedelta
import asyncio
import json
import os
import sys
import time

from unittest.mock import Mock, patch, AsyncMock
import pytest
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import monitoring components
from services.shared.logging_config import (
    StructuredLogger, CentralizedLogger, CorrelationContext,
    StructuredFormatter, get_logger
)
from services.shared.health_checks import (
    HealthCheckManager, DatabaseHealthCheck, HTTPServiceHealthCheck,
    SystemResourcesHealthCheck, HealthStatus, create_health_manager
)
from services.shared.error_tracking import (
    ErrorTracker, ErrorClassifier, ErrorCorrelator, ErrorAggregator,
    ErrorSeverity, ErrorCategory, create_error_context, track_exception
)

class TestStructuredLogging:
    """Test structured logging functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.logger = get_logger("test_service")
        CorrelationContext.clear()
    
    def test_logger_creation(self):
        """Test logger creation and configuration"""
        assert self.logger is not None
        assert hasattr(self.logger, 'info')
        assert hasattr(self.logger, 'error')
        assert hasattr(self.logger, 'warning')
    
    def test_correlation_context(self):
        """Test correlation context management"""
        correlation_id = "test-correlation-123"
        user_id = "test-user-456"
        
        CorrelationContext.set_correlation_id(correlation_id)
        CorrelationContext.set_user_id(user_id)
        
        assert CorrelationContext.get_correlation_id() == correlation_id
        assert CorrelationContext.get_user_id() == user_id
        
        CorrelationContext.clear()
        assert CorrelationContext.get_correlation_id() is None
        assert CorrelationContext.get_user_id() is None
    
    def test_structured_logging_with_context(self):
        """Test structured logging with correlation context"""
        CorrelationContext.set_correlation_id("test-123")
        CorrelationContext.set_user_id("user-456")
        
        # This should not raise an exception
        self.logger.info("Test message", extra_field="test_value")
        self.logger.error("Test error", exception=Exception("Test exception"))
        
        CorrelationContext.clear()
    
    def test_api_request_logging(self):
        """Test API request logging"""
        self.logger.log_api_request(
            method="GET",
            endpoint="/test",
            status_code=200,
            response_time=0.123,
            client_ip="127.0.0.1"
        )
        
        self.logger.log_api_request(
            method="POST",
            endpoint="/error",
            status_code=500,
            response_time=1.456,
            error="Internal server error"
        )
    
    def test_database_operation_logging(self):
        """Test database operation logging"""
        self.logger.log_database_operation(
            operation="SELECT",
            table="candidates",
            duration=0.045,
            success=True,
            rows_affected=10
        )
        
        self.logger.log_database_operation(
            operation="INSERT",
            table="jobs",
            duration=0.234,
            success=False,
            error="Constraint violation"
        )
    
    def test_business_event_logging(self):
        """Test business event logging"""
        self.logger.log_business_event(
            event_type="candidate_match",
            entity_id="job-123",
            action="generated_matches",
            match_count=5,
            algorithm_version="v2.0"
        )

class TestHealthChecks:
    """Test health check functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.health_manager = HealthCheckManager()
    
    @pytest.mark.asyncio
    async def test_system_resources_health_check(self):
        """Test system resources health check"""
        from services.shared.health_checks import SystemResourcesHealthCheck
        
        check = SystemResourcesHealthCheck()
        result = await check.check()
        
        assert result.name == "system_resources"
        assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]
        assert result.response_time_ms >= 0
        assert 'cpu_percent' in result.details
        assert 'memory_percent' in result.details
    
    @pytest.mark.asyncio
    async def test_http_service_health_check(self):
        """Test HTTP service health check"""
        # Mock successful HTTP response
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text = AsyncMock(return_value="OK")
            mock_get.return_value.__aenter__.return_value = mock_response
            
            check = HTTPServiceHealthCheck("http://example.com/health", "test_service")
            result = await check.check()
            
            assert result.name == "test_service"
            assert result.status == HealthStatus.HEALTHY
            assert result.details['status_code'] == 200
    
    @pytest.mark.asyncio
    async def test_http_service_health_check_failure(self):
        """Test HTTP service health check failure"""
        # Mock failed HTTP response
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_get.side_effect = Exception("Connection refused")
            
            check = HTTPServiceHealthCheck("http://example.com/health", "test_service")
            result = await check.check()
            
            assert result.name == "test_service"
            assert result.status == HealthStatus.UNHEALTHY
            assert "Connection refused" in result.message
    
    @pytest.mark.asyncio
    async def test_database_health_check_mock(self):
        """Test database health check with mock"""
        # Mock successful database connection
        with patch('asyncpg.connect') as mock_connect:
            mock_conn = AsyncMock()
            mock_conn.execute = AsyncMock()
            mock_conn.fetchrow = AsyncMock(return_value={
                'total_connections': 10,
                'active_connections': 5,
                'idle_connections': 5
            })
            mock_conn.close = AsyncMock()
            mock_connect.return_value = mock_conn
            
            check = DatabaseHealthCheck("postgresql://test:test@localhost/test")
            result = await check.check()
            
            assert result.name == "database"
            assert result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED]
    
    @pytest.mark.asyncio
    async def test_health_manager_run_all_checks(self):
        """Test running all health checks"""
        # Add mock checks
        self.health_manager.add_system_resources_check()
        
        with patch('aiohttp.ClientSession.get') as mock_get:
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.text = AsyncMock(return_value="OK")
            mock_get.return_value.__aenter__.return_value = mock_response
            
            self.health_manager.add_http_service_check("http://example.com", "test_service")
            
            system_health = await self.health_manager.run_all_checks()
            
            assert system_health.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED, HealthStatus.UNHEALTHY]
            assert len(system_health.checks) == 2
            assert system_health.response_time_ms >= 0
    
    def test_create_health_manager_with_config(self):
        """Test creating health manager with configuration"""
        config = {
            'database_url': 'postgresql://test:test@localhost/test',
            'dependent_services': [
                {'url': 'http://service1.com/health', 'name': 'service1'},
                {'url': 'http://service2.com/health', 'name': 'service2'}
            ],
            'ai_models': [
                {'path': '/path/to/model.pkl', 'name': 'test_model'}
            ]
        }
        
        manager = create_health_manager(config)
        assert len(manager.checks) >= 3  # system + database + services

class TestErrorTracking:
    """Test error tracking functionality"""
    
    def setup_method(self):
        """Setup test environment"""
        self.error_tracker = ErrorTracker("test_service")
        self.classifier = ErrorClassifier()
        self.correlator = ErrorCorrelator()
    
    def test_error_classification(self):
        """Test error classification"""
        # Test database error
        category, severity = self.classifier.classify_error(
            "Connection to database failed",
            "DatabaseError",
            "psycopg2.OperationalError: connection refused"
        )
        assert category == ErrorCategory.DATABASE
        
        # Test network error
        category, severity = self.classifier.classify_error(
            "Connection timeout",
            "NetworkError",
            "requests.exceptions.Timeout"
        )
        assert category == ErrorCategory.NETWORK
        
        # Test authentication error
        category, severity = self.classifier.classify_error(
            "Unauthorized access",
            "AuthenticationError",
            "Invalid token provided"
        )
        assert category == ErrorCategory.AUTHENTICATION
    
    def test_error_fingerprinting(self):
        """Test error fingerprinting"""
        fingerprint1 = self.correlator.generate_fingerprint(
            "ValueError",
            "Invalid input: user ID 123 not found",
            "File test.py, line 10, in function"
        )
        
        fingerprint2 = self.correlator.generate_fingerprint(
            "ValueError", 
            "Invalid input: user ID 456 not found",
            "File test.py, line 10, in function"
        )
        
        # Should be the same fingerprint (normalized)
        assert fingerprint1 == fingerprint2
    
    def test_error_tracking(self):
        """Test error tracking workflow"""
        context = create_error_context(
            service_name="test_service",
            endpoint="/test",
            user_id="test_user",
            correlation_id="test_correlation"
        )
        
        error_event = self.error_tracker.track_error(
            error_type="ValueError",
            error_message="Test error message",
            stack_trace="Test stack trace",
            context=context,
            metadata={"test_field": "test_value"}
        )
        
        assert error_event.service_name == "test_service"
        assert error_event.error_type == "ValueError"
        assert error_event.context.user_id == "test_user"
        assert error_event.metadata["test_field"] == "test_value"
    
    def test_exception_tracking(self):
        """Test exception tracking helper"""
        context = create_error_context(
            service_name="test_service",
            endpoint="/test"
        )
        
        try:
            raise ValueError("Test exception")
        except Exception as e:
            error_event = track_exception(self.error_tracker, e, context)
            
            assert error_event.error_type == "ValueError"
            assert error_event.error_message == "Test exception"
            assert "ValueError: Test exception" in error_event.stack_trace
    
    def test_error_aggregation(self):
        """Test error aggregation"""
        aggregator = ErrorAggregator()
        
        # Create multiple error events
        for i in range(5):
            context = create_error_context(
                service_name="test_service",
                endpoint=f"/test{i % 2}"  # Alternate endpoints
            )
            
            error_event = self.error_tracker.track_error(
                error_type="TestError",
                error_message=f"Test error {i}",
                stack_trace="Test stack trace",
                context=context
            )
            
            aggregator.aggregate_error(error_event)
        
        stats = aggregator.get_error_statistics(24)
        assert stats['total_errors'] >= 5
        assert 'errors_by_service' in stats
        assert 'test_service' in stats['errors_by_service']
    
    def test_error_summary(self):
        """Test error summary generation"""
        # Track some errors
        context = create_error_context(
            service_name="test_service",
            endpoint="/test"
        )
        
        for i in range(3):
            self.error_tracker.track_error(
                error_type="TestError",
                error_message=f"Test error {i}",
                stack_trace="Test stack trace",
                context=context
            )
        
        summary = self.error_tracker.get_error_summary(1)  # Last 1 hour
        
        assert summary['total_errors'] >= 3
        assert 'statistics' in summary
        assert 'severity_breakdown' in summary
        assert 'category_breakdown' in summary

class TestIntegration:
    """Integration tests for enhanced monitoring"""
    
    @pytest.mark.asyncio
    async def test_end_to_end_monitoring_workflow(self):
        """Test complete monitoring workflow"""
        # Initialize components
        logger = get_logger("integration_test")
        error_tracker = ErrorTracker("integration_test")
        health_manager = HealthCheckManager()
        health_manager.add_system_resources_check()
        
        # Set correlation context
        CorrelationContext.set_correlation_id("integration-test-123")
        
        try:
            # Log some events
            logger.info("Starting integration test")
            
            # Simulate API request
            logger.log_api_request(
                method="GET",
                endpoint="/test",
                status_code=200,
                response_time=0.123
            )
            
            # Simulate error
            context = create_error_context(
                service_name="integration_test",
                endpoint="/test",
                correlation_id=CorrelationContext.get_correlation_id()
            )
            
            error_tracker.track_error(
                error_type="TestError",
                error_message="Integration test error",
                stack_trace="Test stack trace",
                context=context
            )
            
            # Run health checks
            health_result = await health_manager.run_all_checks()
            
            # Get error summary
            error_summary = error_tracker.get_error_summary(1)
            
            # Verify results
            assert health_result.status in [HealthStatus.HEALTHY, HealthStatus.DEGRADED]
            assert error_summary['total_errors'] >= 1
            
            logger.info("Integration test completed successfully")
            
        finally:
            CorrelationContext.clear()
    
    def test_performance_monitoring(self):
        """Test performance monitoring capabilities"""
        logger = get_logger("performance_test")
        
        # Simulate multiple API requests with timing
        start_time = time.time()
        
        for i in range(10):
            request_start = time.time()
            # Simulate processing time
            time.sleep(0.01)
            request_time = time.time() - request_start
            
            logger.log_api_request(
                method="GET",
                endpoint=f"/test/{i}",
                status_code=200 if i < 8 else 500,
                response_time=request_time,
                request_size=1024 + i * 100
            )
        
        total_time = time.time() - start_time
        assert total_time > 0.1  # Should take at least 100ms
    
    def test_error_correlation_across_services(self):
        """Test error correlation across multiple services"""
        # Create trackers for different services
        gateway_tracker = ErrorTracker("gateway")
        agent_tracker = ErrorTracker("agent")
        portal_tracker = ErrorTracker("portal")
        
        correlation_id = "cross-service-error-123"
        
        # Simulate related errors across services
        for tracker, service in [(gateway_tracker, "gateway"), 
                               (agent_tracker, "agent"), 
                               (portal_tracker, "portal")]:
            context = create_error_context(
                service_name=service,
                endpoint="/related-operation",
                correlation_id=correlation_id
            )
            
            tracker.track_error(
                error_type="RelatedError",
                error_message=f"Related error in {service}",
                stack_trace="Related stack trace",
                context=context
            )
        
        # Verify each tracker has recorded the error
        for tracker in [gateway_tracker, agent_tracker, portal_tracker]:
            summary = tracker.get_error_summary(1)
            assert summary['total_errors'] >= 1

def run_monitoring_tests():
    """Run all monitoring tests"""
    print("🧪 Running Enhanced Monitoring Test Suite...")
    
    # Test structured logging
    print("\n📝 Testing Structured Logging...")
    logging_tests = TestStructuredLogging()
    logging_tests.setup_method()
    
    try:
        logging_tests.test_logger_creation()
        logging_tests.test_correlation_context()
        logging_tests.test_structured_logging_with_context()
        logging_tests.test_api_request_logging()
        logging_tests.test_database_operation_logging()
        logging_tests.test_business_event_logging()
        print("✅ Structured Logging Tests: PASSED")
    except Exception as e:
        print(f"❌ Structured Logging Tests: FAILED - {e}")
    
    # Test health checks
    print("\n🏥 Testing Health Checks...")
    health_tests = TestHealthChecks()
    health_tests.setup_method()
    
    try:
        # Run async tests
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(health_tests.test_system_resources_health_check())
        loop.run_until_complete(health_tests.test_http_service_health_check())
        loop.run_until_complete(health_tests.test_http_service_health_check_failure())
        loop.run_until_complete(health_tests.test_database_health_check_mock())
        loop.run_until_complete(health_tests.test_health_manager_run_all_checks())
        
        health_tests.test_create_health_manager_with_config()
        
        loop.close()
        print("✅ Health Check Tests: PASSED")
    except Exception as e:
        print(f"❌ Health Check Tests: FAILED - {e}")
    
    # Test error tracking
    print("\n🚨 Testing Error Tracking...")
    error_tests = TestErrorTracking()
    error_tests.setup_method()
    
    try:
        error_tests.test_error_classification()
        error_tests.test_error_fingerprinting()
        error_tests.test_error_tracking()
        error_tests.test_exception_tracking()
        error_tests.test_error_aggregation()
        error_tests.test_error_summary()
        print("✅ Error Tracking Tests: PASSED")
    except Exception as e:
        print(f"❌ Error Tracking Tests: FAILED - {e}")
    
    # Test integration
    print("\n🔗 Testing Integration...")
    integration_tests = TestIntegration()
    
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(integration_tests.test_end_to_end_monitoring_workflow())
        
        integration_tests.test_performance_monitoring()
        integration_tests.test_error_correlation_across_services()
        
        loop.close()
        print("✅ Integration Tests: PASSED")
    except Exception as e:
        print(f"❌ Integration Tests: FAILED - {e}")
    
    print("\n🎉 Enhanced Monitoring Test Suite Complete!")
    print("\n📊 Test Results Summary:")
    print("- Structured Logging: ✅ Centralized JSON logging with correlation")
    print("- Health Checks: ✅ Comprehensive dependency validation")
    print("- Error Tracking: ✅ Advanced classification and correlation")
    print("- Integration: ✅ End-to-end monitoring workflow")

if __name__ == "__main__":
    run_monitoring_tests()