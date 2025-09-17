#!/usr/bin/env python3
"""
BHIV HR Platform - Centralized Logging Configuration
Enterprise-grade structured logging with ELK stack integration
"""

import logging
import json
import sys
import os
from datetime import datetime
from typing import Dict, Any, Optional
import traceback
from pathlib import Path
import socket
import threading
from logging.handlers import RotatingFileHandler, SysLogHandler
from pythonjsonlogger import jsonlogger

class StructuredFormatter(jsonlogger.JsonFormatter):
    """Custom JSON formatter for structured logging"""
    
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        
        # Add standard fields
        log_record['timestamp'] = datetime.utcnow().isoformat()
        log_record['service'] = os.getenv('SERVICE_NAME', 'unknown')
        log_record['environment'] = os.getenv('ENVIRONMENT', 'development')
        log_record['version'] = os.getenv('SERVICE_VERSION', '1.0.0')
        log_record['hostname'] = socket.gethostname()
        log_record['thread_id'] = threading.get_ident()
        
        # Add correlation ID if available
        correlation_id = getattr(record, 'correlation_id', None)
        if correlation_id:
            log_record['correlation_id'] = correlation_id
        
        # Add user context if available
        user_id = getattr(record, 'user_id', None)
        if user_id:
            log_record['user_id'] = user_id
        
        # Add request context if available
        request_id = getattr(record, 'request_id', None)
        if request_id:
            log_record['request_id'] = request_id

class CentralizedLogger:
    """Centralized logging manager with multiple output targets"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)
        
        # Clear existing handlers
        self.logger.handlers.clear()
        
        # Setup handlers
        self._setup_console_handler()
        self._setup_file_handler()
        self._setup_elk_handler()
        
        # Prevent duplicate logs
        self.logger.propagate = False
    
    def _setup_console_handler(self):
        """Setup console output with structured format"""
        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = StructuredFormatter(
            '%(timestamp)s %(service)s %(levelname)s %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)
    
    def _setup_file_handler(self):
        """Setup rotating file handler"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = RotatingFileHandler(
            log_dir / f"{self.service_name}.log",
            maxBytes=50*1024*1024,  # 50MB
            backupCount=10
        )
        
        file_formatter = StructuredFormatter()
        file_handler.setFormatter(file_formatter)
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
    
    def _setup_elk_handler(self):
        """Setup ELK stack integration"""
        elk_host = os.getenv('ELK_HOST')
        elk_port = int(os.getenv('ELK_PORT', '5044'))
        
        if elk_host:
            try:
                # Custom ELK handler (would integrate with Logstash)
                elk_handler = ELKHandler(elk_host, elk_port)
                elk_formatter = StructuredFormatter()
                elk_handler.setFormatter(elk_formatter)
                elk_handler.setLevel(logging.INFO)
                self.logger.addHandler(elk_handler)
            except Exception as e:
                self.logger.warning(f"Failed to setup ELK handler: {e}")
    
    def get_logger(self) -> logging.Logger:
        """Get configured logger instance"""
        return self.logger

class ELKHandler(logging.Handler):
    """Custom handler for ELK stack integration"""
    
    def __init__(self, host: str, port: int):
        super().__init__()
        self.host = host
        self.port = port
        self.buffer = []
        self.buffer_size = 100
    
    def emit(self, record):
        """Emit log record to ELK stack"""
        try:
            log_entry = self.format(record)
            self.buffer.append(log_entry)
            
            # Flush buffer when full
            if len(self.buffer) >= self.buffer_size:
                self._flush_buffer()
        except Exception:
            self.handleError(record)
    
    def _flush_buffer(self):
        """Flush log buffer to ELK stack"""
        if not self.buffer:
            return
        
        try:
            # In production, this would send to Logstash
            # For now, write to a file that Filebeat can pick up
            elk_log_file = Path("logs/elk_output.log")
            with open(elk_log_file, 'a') as f:
                for entry in self.buffer:
                    f.write(entry + '\n')
            
            self.buffer.clear()
        except Exception as e:
            print(f"Failed to flush ELK buffer: {e}")

class CorrelationContext:
    """Thread-local correlation context for request tracing"""
    
    _context = threading.local()
    
    @classmethod
    def set_correlation_id(cls, correlation_id: str):
        """Set correlation ID for current thread"""
        cls._context.correlation_id = correlation_id
    
    @classmethod
    def get_correlation_id(cls) -> Optional[str]:
        """Get correlation ID for current thread"""
        return getattr(cls._context, 'correlation_id', None)
    
    @classmethod
    def set_user_id(cls, user_id: str):
        """Set user ID for current thread"""
        cls._context.user_id = user_id
    
    @classmethod
    def get_user_id(cls) -> Optional[str]:
        """Get user ID for current thread"""
        return getattr(cls._context, 'user_id', None)
    
    @classmethod
    def set_request_id(cls, request_id: str):
        """Set request ID for current thread"""
        cls._context.request_id = request_id
    
    @classmethod
    def get_request_id(cls) -> Optional[str]:
        """Get request ID for current thread"""
        return getattr(cls._context, 'request_id', None)
    
    @classmethod
    def clear(cls):
        """Clear all context"""
        for attr in ['correlation_id', 'user_id', 'request_id']:
            if hasattr(cls._context, attr):
                delattr(cls._context, attr)

class StructuredLogger:
    """High-level structured logging interface"""
    
    def __init__(self, service_name: str):
        self.centralized_logger = CentralizedLogger(service_name)
        self.logger = self.centralized_logger.get_logger()
    
    def _add_context(self, extra: Dict[str, Any]) -> Dict[str, Any]:
        """Add correlation context to log extra data"""
        context = {
            'correlation_id': CorrelationContext.get_correlation_id(),
            'user_id': CorrelationContext.get_user_id(),
            'request_id': CorrelationContext.get_request_id()
        }
        
        # Remove None values
        context = {k: v for k, v in context.items() if v is not None}
        
        if extra:
            context.update(extra)
        
        return context
    
    def info(self, message: str, **kwargs):
        """Log info message with context"""
        extra = self._add_context(kwargs)
        self.logger.info(message, extra=extra)
    
    def warning(self, message: str, **kwargs):
        """Log warning message with context"""
        extra = self._add_context(kwargs)
        self.logger.warning(message, extra=extra)
    
    def error(self, message: str, exception: Exception = None, **kwargs):
        """Log error message with context and exception details"""
        extra = self._add_context(kwargs)
        
        if exception:
            extra.update({
                'exception_type': type(exception).__name__,
                'exception_message': str(exception),
                'stack_trace': traceback.format_exc()
            })
        
        self.logger.error(message, extra=extra)
    
    def debug(self, message: str, **kwargs):
        """Log debug message with context"""
        extra = self._add_context(kwargs)
        self.logger.debug(message, extra=extra)
    
    def critical(self, message: str, **kwargs):
        """Log critical message with context"""
        extra = self._add_context(kwargs)
        self.logger.critical(message, extra=extra)
    
    def log_api_request(self, method: str, endpoint: str, status_code: int, 
                       response_time: float, **kwargs):
        """Log API request with structured data"""
        extra = self._add_context(kwargs)
        extra.update({
            'event_type': 'api_request',
            'http_method': method,
            'endpoint': endpoint,
            'status_code': status_code,
            'response_time_ms': response_time * 1000,
            'success': status_code < 400
        })
        
        level = 'info' if status_code < 400 else 'error'
        message = f"{method} {endpoint} - {status_code} ({response_time:.3f}s)"
        
        getattr(self.logger, level)(message, extra=extra)
    
    def log_database_operation(self, operation: str, table: str, duration: float, 
                              success: bool, **kwargs):
        """Log database operation with structured data"""
        extra = self._add_context(kwargs)
        extra.update({
            'event_type': 'database_operation',
            'operation': operation,
            'table': table,
            'duration_ms': duration * 1000,
            'success': success
        })
        
        level = 'info' if success else 'error'
        message = f"DB {operation} on {table} - {'SUCCESS' if success else 'FAILED'} ({duration:.3f}s)"
        
        getattr(self.logger, level)(message, extra=extra)
    
    def log_business_event(self, event_type: str, entity_id: str, action: str, **kwargs):
        """Log business event with structured data"""
        extra = self._add_context(kwargs)
        extra.update({
            'event_type': 'business_event',
            'business_event_type': event_type,
            'entity_id': entity_id,
            'action': action
        })
        
        message = f"Business Event: {event_type} - {action} for {entity_id}"
        self.logger.info(message, extra=extra)

# Factory function for easy logger creation
def get_logger(service_name: str) -> StructuredLogger:
    """Get structured logger for service"""
    return StructuredLogger(service_name)