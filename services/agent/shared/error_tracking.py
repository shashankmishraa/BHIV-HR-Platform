#!/usr/bin/env python3
"""
BHIV HR Platform - Advanced Error Tracking and Analysis
Comprehensive error correlation, root cause analysis, and alerting
"""

from collections import defaultdict, deque
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import asyncio
import hashlib
import json
import re
import time
import traceback

from dataclasses import dataclass, asdict
from enum import Enum
class ErrorSeverity(Enum):
    """Error severity levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ErrorCategory(Enum):
    """Error categories for classification"""
    DATABASE = "database"
    NETWORK = "network"
    AUTHENTICATION = "authentication"
    VALIDATION = "validation"
    BUSINESS_LOGIC = "business_logic"
    EXTERNAL_SERVICE = "external_service"
    SYSTEM_RESOURCE = "system_resource"
    AI_MODEL = "ai_model"
    UNKNOWN = "unknown"

@dataclass
class ErrorContext:
    """Context information for error tracking"""
    service_name: str
    endpoint: str
    user_id: Optional[str]
    session_id: Optional[str]
    correlation_id: Optional[str]
    request_id: Optional[str]
    ip_address: Optional[str]
    user_agent: Optional[str]
    request_data: Optional[Dict[str, Any]]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

@dataclass
class ErrorEvent:
    """Individual error event"""
    error_id: str
    timestamp: datetime
    service_name: str
    error_type: str
    error_message: str
    stack_trace: str
    severity: ErrorSeverity
    category: ErrorCategory
    context: ErrorContext
    metadata: Dict[str, Any]
    fingerprint: str
    resolved: bool = False
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['timestamp'] = self.timestamp.isoformat()
        result['severity'] = self.severity.value
        result['category'] = self.category.value
        result['context'] = self.context.to_dict()
        return result

@dataclass
class ErrorPattern:
    """Identified error pattern"""
    pattern_id: str
    fingerprint: str
    error_type: str
    message_pattern: str
    occurrences: int
    first_seen: datetime
    last_seen: datetime
    affected_services: Set[str]
    severity: ErrorSeverity
    category: ErrorCategory
    
    def to_dict(self) -> Dict[str, Any]:
        result = asdict(self)
        result['first_seen'] = self.first_seen.isoformat()
        result['last_seen'] = self.last_seen.isoformat()
        result['affected_services'] = list(self.affected_services)
        result['severity'] = self.severity.value
        result['category'] = self.category.value
        return result

class ErrorClassifier:
    """Classifies errors into categories and determines severity"""
    
    def __init__(self):
        self.classification_rules = {
            # Database errors
            ErrorCategory.DATABASE: [
                r'connection.*refused',
                r'timeout.*database',
                r'deadlock',
                r'constraint.*violation',
                r'duplicate.*key',
                r'table.*not.*exist',
                r'column.*not.*exist',
                r'psycopg2',
                r'sqlalchemy'
            ],
            
            # Network errors
            ErrorCategory.NETWORK: [
                r'connection.*timeout',
                r'network.*unreachable',
                r'dns.*resolution',
                r'ssl.*error',
                r'certificate.*verify',
                r'connection.*reset',
                r'socket.*error'
            ],
            
            # Authentication errors
            ErrorCategory.AUTHENTICATION: [
                r'unauthorized',
                r'authentication.*failed',
                r'invalid.*token',
                r'expired.*token',
                r'permission.*denied',
                r'access.*denied',
                r'forbidden'
            ],
            
            # Validation errors
            ErrorCategory.VALIDATION: [
                r'validation.*error',
                r'invalid.*input',
                r'missing.*required',
                r'format.*error',
                r'type.*error',
                r'value.*error'
            ],
            
            # External service errors
            ErrorCategory.EXTERNAL_SERVICE: [
                r'external.*service',
                r'api.*error',
                r'http.*error',
                r'service.*unavailable',
                r'gateway.*timeout'
            ],
            
            # System resource errors
            ErrorCategory.SYSTEM_RESOURCE: [
                r'memory.*error',
                r'disk.*full',
                r'cpu.*limit',
                r'resource.*exhausted',
                r'out.*of.*memory'
            ],
            
            # AI model errors
            ErrorCategory.AI_MODEL: [
                r'model.*not.*found',
                r'prediction.*error',
                r'inference.*failed',
                r'model.*loading',
                r'embedding.*error'
            ]
        }
        
        self.severity_rules = {
            ErrorSeverity.CRITICAL: [
                r'system.*crash',
                r'service.*down',
                r'database.*unavailable',
                r'critical.*error',
                r'fatal.*error'
            ],
            ErrorSeverity.HIGH: [
                r'authentication.*failed',
                r'permission.*denied',
                r'data.*corruption',
                r'security.*violation'
            ],
            ErrorSeverity.MEDIUM: [
                r'timeout',
                r'connection.*failed',
                r'validation.*error',
                r'business.*logic'
            ]
        }
    
    def classify_error(self, error_message: str, error_type: str, stack_trace: str) -> tuple[ErrorCategory, ErrorSeverity]:
        """Classify error into category and severity"""
        full_text = f"{error_type} {error_message} {stack_trace}".lower()
        
        # Determine category
        category = ErrorCategory.UNKNOWN
        for cat, patterns in self.classification_rules.items():
            for pattern in patterns:
                if re.search(pattern, full_text, re.IGNORECASE):
                    category = cat
                    break
            if category != ErrorCategory.UNKNOWN:
                break
        
        # Determine severity
        severity = ErrorSeverity.LOW  # Default
        for sev, patterns in self.severity_rules.items():
            for pattern in patterns:
                if re.search(pattern, full_text, re.IGNORECASE):
                    severity = sev
                    break
            if severity != ErrorSeverity.LOW:
                break
        
        return category, severity

class ErrorCorrelator:
    """Correlates errors across services and identifies patterns"""
    
    def __init__(self):
        self.error_patterns: Dict[str, ErrorPattern] = {}
        self.correlation_window = timedelta(minutes=5)
    
    def generate_fingerprint(self, error_type: str, error_message: str, stack_trace: str) -> str:
        """Generate fingerprint for error grouping"""
        # Normalize error message (remove dynamic parts)
        normalized_message = self._normalize_error_message(error_message)
        
        # Extract key stack trace lines
        key_stack_lines = self._extract_key_stack_lines(stack_trace)
        
        # Create fingerprint
        fingerprint_data = f"{error_type}:{normalized_message}:{':'.join(key_stack_lines)}"
        return hashlib.md5(fingerprint_data.encode()).hexdigest()
    
    def _normalize_error_message(self, message: str) -> str:
        """Normalize error message by removing dynamic parts"""
        # Remove timestamps
        message = re.sub(r'\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2}', '[TIMESTAMP]', message)
        
        # Remove IDs and numbers
        message = re.sub(r'\b\d+\b', '[NUMBER]', message)
        
        # Remove file paths
        message = re.sub(r'[/\\][\w/\\.-]+', '[PATH]', message)
        
        # Remove URLs
        message = re.sub(r'https?://[^\s]+', '[URL]', message)
        
        # Remove IP addresses
        message = re.sub(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '[IP]', message)
        
        return message.strip()
    
    def _extract_key_stack_lines(self, stack_trace: str) -> List[str]:
        """Extract key lines from stack trace for fingerprinting"""
        lines = stack_trace.split('\n')
        key_lines = []
        
        for line in lines:
            line = line.strip()
            # Skip empty lines and common framework lines
            if (line and 
                not line.startswith('File') and 
                not line.startswith('  ') and
                'site-packages' not in line):
                key_lines.append(line)
        
        return key_lines[:3]  # Take first 3 key lines
    
    def correlate_error(self, error_event: ErrorEvent) -> Optional[ErrorPattern]:
        """Correlate error with existing patterns"""
        fingerprint = error_event.fingerprint
        
        if fingerprint in self.error_patterns:
            # Update existing pattern
            pattern = self.error_patterns[fingerprint]
            pattern.occurrences += 1
            pattern.last_seen = error_event.timestamp
            pattern.affected_services.add(error_event.service_name)
            
            # Update severity if this error is more severe
            if error_event.severity.value > pattern.severity.value:
                pattern.severity = error_event.severity
            
            return pattern
        else:
            # Create new pattern
            pattern = ErrorPattern(
                pattern_id=f"pattern_{fingerprint[:8]}",
                fingerprint=fingerprint,
                error_type=error_event.error_type,
                message_pattern=self._normalize_error_message(error_event.error_message),
                occurrences=1,
                first_seen=error_event.timestamp,
                last_seen=error_event.timestamp,
                affected_services={error_event.service_name},
                severity=error_event.severity,
                category=error_event.category
            )
            
            self.error_patterns[fingerprint] = pattern
            return pattern
    
    def find_related_errors(self, error_event: ErrorEvent, time_window: timedelta = None) -> List[ErrorEvent]:
        """Find related errors within time window"""
        if time_window is None:
            time_window = self.correlation_window
        
        # This would query the error storage for related errors
        # For now, return empty list
        return []

class ErrorAggregator:
    """Aggregates error statistics and trends"""
    
    def __init__(self):
        self.error_counts = defaultdict(int)
        self.service_errors = defaultdict(int)
        self.category_errors = defaultdict(int)
        self.hourly_errors = defaultdict(int)
    
    def aggregate_error(self, error_event: ErrorEvent):
        """Aggregate error statistics"""
        # Count by fingerprint
        self.error_counts[error_event.fingerprint] += 1
        
        # Count by service
        self.service_errors[error_event.service_name] += 1
        
        # Count by category
        self.category_errors[error_event.category.value] += 1
        
        # Count by hour
        hour_key = error_event.timestamp.strftime('%Y-%m-%d-%H')
        self.hourly_errors[hour_key] += 1
    
    def get_error_statistics(self, hours: int = 24) -> Dict[str, Any]:
        """Get error statistics for the last N hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        # Filter recent errors
        recent_hourly = {
            k: v for k, v in self.hourly_errors.items()
            if datetime.strptime(k, '%Y-%m-%d-%H') > cutoff_time
        }
        
        return {
            "total_errors": sum(recent_hourly.values()),
            "error_rate_per_hour": sum(recent_hourly.values()) / max(hours, 1),
            "hourly_breakdown": recent_hourly,
            "top_services": dict(sorted(self.service_errors.items(), key=lambda x: x[1], reverse=True)[:5]),
            "top_categories": dict(sorted(self.category_errors.items(), key=lambda x: x[1], reverse=True)[:5]),
            "top_error_patterns": self._get_top_patterns()
        }
    
    def _get_top_patterns(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top error patterns by occurrence"""
        sorted_patterns = sorted(
            self.error_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {'fingerprint': fingerprint, 'count': count}
            for fingerprint, count in sorted_patterns[:limit]
        ]

class ErrorTracker:
    """Main error tracking and analysis system"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.classifier = ErrorClassifier()
        self.correlator = ErrorCorrelator()
        self.aggregator = ErrorAggregator()
        self.error_buffer = deque(maxlen=10000)
        self.alert_thresholds = {
            'error_rate_per_minute': 10,
            'critical_errors_per_hour': 5,
            'pattern_occurrences': 20
        }
    
    def track_error(self, 
                   error_type: str,
                   error_message: str,
                   stack_trace: str,
                   context: ErrorContext,
                   metadata: Dict[str, Any] = None) -> ErrorEvent:
        """Track a new error event"""
        
        # Classify error
        category, severity = self.classifier.classify_error(
            error_message, error_type, stack_trace
        )
        
        # Generate fingerprint
        fingerprint = self.correlator.generate_fingerprint(
            error_type, error_message, stack_trace
        )
        
        # Create error event
        error_event = ErrorEvent(
            error_id=f"err_{int(time.time())}_{hash(fingerprint) % 10000}",
            timestamp=datetime.now(),
            service_name=self.service_name,
            error_type=error_type,
            error_message=error_message,
            stack_trace=stack_trace,
            severity=severity,
            category=category,
            context=context,
            metadata=metadata or {},
            fingerprint=fingerprint
        )
        
        # Store error
        self.error_buffer.append(error_event)
        
        # Correlate with patterns
        pattern = self.correlator.correlate_error(error_event)
        
        # Aggregate statistics
        self.aggregator.aggregate_error(error_event)
        
        # Check for alerts
        self._check_alert_conditions(error_event, pattern)
        
        return error_event
    
    def _check_alert_conditions(self, error_event: ErrorEvent, pattern: ErrorPattern):
        """Check if error triggers any alert conditions"""
        alerts = []
        
        # Critical error alert
        if error_event.severity == ErrorSeverity.CRITICAL:
            alerts.append({
                'type': 'CRITICAL_ERROR',
                'message': f"Critical error in {error_event.service_name}: {error_event.error_message}",
                'error_id': error_event.error_id
            })
        
        # Pattern frequency alert
        if pattern and pattern.occurrences >= self.alert_thresholds['pattern_occurrences']:
            alerts.append({
                'type': 'ERROR_PATTERN_SPIKE',
                'message': f"Error pattern {pattern.pattern_id} occurred {pattern.occurrences} times",
                'pattern_id': pattern.pattern_id
            })
        
        # Error rate alert
        recent_errors = [
            e for e in self.error_buffer
            if e.timestamp > datetime.now() - timedelta(minutes=1)
        ]
        
        if len(recent_errors) >= self.alert_thresholds['error_rate_per_minute']:
            alerts.append({
                'type': 'HIGH_ERROR_RATE',
                'message': f"High error rate: {len(recent_errors)} errors in last minute",
                'error_count': len(recent_errors)
            })
        
        # Process alerts (log, send notifications, etc.)
        for alert in alerts:
            self._process_alert(alert)
    
    def _process_alert(self, alert: Dict[str, Any]):
        """Process alert by logging or sending notifications"""
        # Log alert for now - can be extended for notifications
        print(f"ALERT [{alert['type']}]: {alert['message']}")
    alert in alerts:
        self._process_alert(alert)
    
    def _process_alert(self, alert: Dict[str, Any]):
        """Process alert (log, notify, etc.)"""
        # For now, just log the alert
        print(f"ALERT: {alert['type']} - {alert['message']}")
    
    def get_error_summary(self, hours: int = 24) -> Dict[str, Any]:
        """Get comprehensive error summary"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        recent_errors = [
            e for e in self.error_buffer
            if e.timestamp > cutoff_time
        ]
        
        # Get statistics
        stats = self.aggregator.get_error_statistics(hours)
        
        # Get recent patterns
        recent_patterns = [
            pattern.to_dict() for pattern in self.correlator.error_patterns.values()
            if pattern.last_seen > cutoff_time
        ]
        
        return {
            'time_period_hours': hours,
            'total_errors': len(recent_errors),
            'statistics': stats,
            'recent_patterns': recent_patterns,
            'severity_breakdown': self._get_severity_breakdown(recent_errors),
            'category_breakdown': self._get_category_breakdown(recent_errors),
            'top_affected_services': self._get_top_services(recent_errors)
        }
    
    def _get_severity_breakdown(self, errors: List[ErrorEvent]) -> Dict[str, int]:
        """Get breakdown of errors by severity"""
        breakdown = defaultdict(int)
        for error in errors:
            breakdown[error.severity.value] += 1
        return dict(breakdown)
    
    def _get_category_breakdown(self, errors: List[ErrorEvent]) -> Dict[str, int]:
        """Get breakdown of errors by category"""
        breakdown = defaultdict(int)
        for error in errors:
            breakdown[error.category.value] += 1
        return dict(breakdown)
    
    def _get_top_services(self, errors: List[ErrorEvent], limit: int = 5) -> List[Dict[str, Any]]:
        """Get top services by error count"""
        service_counts = defaultdict(int)
        for error in errors:
            service_counts[error.service_name] += 1
        
        sorted_services = sorted(
            service_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [
            {'service': service, 'error_count': count}
            for service, count in sorted_services[:limit]
        ]

# Convenience functions for easy integration
def create_error_context(service_name: str, endpoint: str, **kwargs) -> ErrorContext:
    """Create error context from request data"""
    return ErrorContext(
        service_name=service_name,
        endpoint=endpoint,
        user_id=kwargs.get('user_id'),
        session_id=kwargs.get('session_id'),
        correlation_id=kwargs.get('correlation_id'),
        request_id=kwargs.get('request_id'),
        ip_address=kwargs.get('ip_address'),
        user_agent=kwargs.get('user_agent'),
        request_data=kwargs.get('request_data')
    )

def track_exception(tracker: ErrorTracker, 
                   exception: Exception, 
                   context: ErrorContext,
                   metadata: Dict[str, Any] = None) -> ErrorEvent:
    """Track an exception with full context"""
    return tracker.track_error(
        error_type=type(exception).__name__,
        error_message=str(exception),
        stack_trace=traceback.format_exc(),
        context=context,
        metadata=metadata
    )