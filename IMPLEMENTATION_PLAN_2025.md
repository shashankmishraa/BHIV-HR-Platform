# BHIV HR AI Platform - Implementation Plan 2025

## Phase 1: Foundation & Configuration (Week 1-2)

### 1.1 Centralized Configuration System

#### Create Configuration Manager
```python
# libs/config/manager.py
from typing import Dict, Any
import yaml
import os
from pathlib import Path

class ConfigManager:
    def __init__(self, env: str = None):
        self.env = env or os.getenv("ENVIRONMENT", "production")
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        base_config = self._load_yaml("config/base.yml")
        env_config = self._load_yaml(f"config/environments/{self.env}.yml")
        return self._merge_configs(base_config, env_config)
    
    def get(self, key: str, default: Any = None) -> Any:
        keys = key.split(".")
        value = self.config
        for k in keys:
            value = value.get(k, {})
        return value if value != {} else default
```

#### Environment Configuration Schema
```yaml
# config/base.yml
app:
  name: "BHIV HR Platform"
  version: "4.0.0"
  debug: false

database:
  pool_size: 20
  max_overflow: 30
  pool_timeout: 30
  echo: false

observability:
  metrics_enabled: true
  tracing_enabled: true
  log_level: "INFO"
  health_check_interval: 30

security:
  jwt_expiry: 3600
  api_rate_limit: 100
  cors_origins: ["*"]
  encryption_key: "${ENCRYPTION_KEY}"

services:
  gateway:
    port: 8000
    workers: 4
  agent:
    port: 9000
    workers: 2
```

### 1.2 Shared Libraries Structure

#### Database Layer
```python
# libs/database/connection.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager

class DatabaseManager:
    def __init__(self, config: dict):
        self.engine = create_async_engine(
            config["url"],
            pool_size=config.get("pool_size", 20),
            max_overflow=config.get("max_overflow", 30),
            pool_timeout=config.get("pool_timeout", 30),
            echo=config.get("echo", False)
        )
        self.session_factory = sessionmaker(
            self.engine, class_=AsyncSession, expire_on_commit=False
        )
    
    @asynccontextmanager
    async def get_session(self):
        async with self.session_factory() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()
```

#### Service Communication
```python
# libs/common/service_client.py
import aiohttp
from typing import Dict, Any, Optional
from libs.observability.tracing import trace_request

class ServiceClient:
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    @trace_request
    async def request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        async with self.session.request(method, url, **kwargs) as response:
            response.raise_for_status()
            return await response.json()
```

### 1.3 Enhanced CI/CD Pipeline

#### Unified Pipeline Configuration
```yaml
# .github/workflows/ci-cd-pipeline.yml
name: BHIV HR Platform CI/CD

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  PYTHON_VERSION: "3.12.7"
  NODE_VERSION: "18"

jobs:
  quality-gate:
    name: Quality Gate
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install Dependencies
        run: |
          pip install -r requirements-dev.txt
      
      - name: Code Quality
        run: |
          black --check .
          isort --check-only .
          flake8 .
          mypy .
      
      - name: Security Scan
        run: |
          bandit -r . -f json -o security-report.json
          safety check --json --output safety-report.json
      
      - name: Upload Reports
        uses: actions/upload-artifact@v4
        with:
          name: quality-reports
          path: "*-report.json"

  test-suite:
    name: Test Suite
    runs-on: ubuntu-latest
    needs: quality-gate
    
    services:
      postgres:
        image: postgres:17-alpine
        env:
          POSTGRES_PASSWORD: test_pass
          POSTGRES_USER: test_user
          POSTGRES_DB: test_db
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 3
    
    strategy:
      matrix:
        test-type: [unit, integration, e2e]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'
      
      - name: Install Dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-test.txt
      
      - name: Run Tests
        env:
          DATABASE_URL: postgresql://test_user:test_pass@localhost:5432/test_db
        run: |
          pytest tests/${{ matrix.test-type }}/ \
            --cov=src \
            --cov-report=xml \
            --cov-report=html \
            --junit-xml=test-results.xml
      
      - name: Upload Coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml

  build-images:
    name: Build Container Images
    runs-on: ubuntu-latest
    needs: test-suite
    if: github.ref == 'refs/heads/main'
    
    strategy:
      matrix:
        service: [gateway, agent, portal, client-portal]
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3
      
      - name: Build and Push
        uses: docker/build-push-action@v5
        with:
          context: ./apps/${{ matrix.service }}
          file: ./apps/${{ matrix.service }}/Dockerfile
          push: false
          tags: bhiv-${{ matrix.service }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    runs-on: ubuntu-latest
    needs: build-images
    if: github.ref == 'refs/heads/develop'
    
    environment:
      name: staging
      url: https://staging.bhiv-hr-platform.com
    
    steps:
      - name: Deploy to Staging
        run: |
          echo "Deploying to staging environment"
          # Deployment logic here

  deploy-production:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build-images
    if: github.ref == 'refs/heads/main'
    
    environment:
      name: production
      url: https://bhiv-hr-platform.com
    
    steps:
      - name: Deploy to Production
        run: |
          echo "Deploying to production environment"
          # Deployment logic here
```

## Phase 2: Core Services Refactoring (Week 3-4)

### 2.1 Enhanced Gateway Service

#### Modular Router System
```python
# apps/gateway/src/modules/base.py
from abc import ABC, abstractmethod
from fastapi import APIRouter
from libs.config.manager import ConfigManager
from libs.observability.logger import get_logger

class BaseModule(ABC):
    def __init__(self, config: ConfigManager):
        self.config = config
        self.logger = get_logger(self.__class__.__name__)
        self.router = APIRouter()
        self._setup_routes()
    
    @abstractmethod
    def _setup_routes(self):
        pass
    
    @property
    def name(self) -> str:
        return self.__class__.__name__.lower().replace("module", "")
```

#### Candidates Module Implementation
```python
# apps/gateway/src/modules/candidates.py
from typing import List, Optional
from fastapi import Depends, HTTPException, status
from libs.database.connection import DatabaseManager
from libs.common.service_client import ServiceClient
from .base import BaseModule

class CandidatesModule(BaseModule):
    def _setup_routes(self):
        @self.router.post("/candidates", response_model=CandidateResponse)
        async def create_candidate(
            candidate: CandidateCreate,
            db: DatabaseManager = Depends(get_database)
        ):
            async with db.get_session() as session:
                # Create candidate logic
                pass
        
        @self.router.get("/candidates/{candidate_id}")
        async def get_candidate(candidate_id: int):
            # Get candidate logic
            pass
        
        @self.router.get("/candidates/{candidate_id}/matches")
        async def get_candidate_matches(candidate_id: int):
            async with ServiceClient(self.config.get("services.agent.url")) as client:
                return await client.request("POST", "/match", json={"candidate_id": candidate_id})
```

### 2.2 Service Discovery Implementation

#### Service Registry
```python
# libs/common/service_registry.py
from typing import Dict, Optional
import aiohttp
from libs.observability.metrics import counter, histogram
from libs.common.circuit_breaker import CircuitBreaker

class ServiceRegistry:
    def __init__(self, config: dict):
        self.services = {}
        self.circuit_breakers = {}
        
        for name, service_config in config.items():
            self.services[name] = ServiceEndpoint(
                name=name,
                url=service_config["url"],
                timeout=service_config.get("timeout", 30)
            )
            self.circuit_breakers[name] = CircuitBreaker(
                failure_threshold=service_config.get("failure_threshold", 5),
                timeout=service_config.get("circuit_timeout", 60)
            )
    
    @counter("service_calls_total")
    @histogram("service_call_duration_seconds")
    async def call_service(self, service_name: str, endpoint: str, **kwargs):
        if service_name not in self.services:
            raise ValueError(f"Service {service_name} not registered")
        
        circuit_breaker = self.circuit_breakers[service_name]
        service = self.services[service_name]
        
        return await circuit_breaker.call(service.request, endpoint, **kwargs)
```

### 2.3 Enhanced Observability

#### Structured Logging
```python
# libs/observability/logger.py
import structlog
import logging
from typing import Any, Dict
from datetime import datetime

def configure_logging(service_name: str, log_level: str = "INFO"):
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper())
    )

def get_logger(name: str) -> structlog.BoundLogger:
    return structlog.get_logger(name)
```

#### Metrics Collection
```python
# libs/observability/metrics.py
from prometheus_client import Counter, Histogram, Gauge, start_http_server
from functools import wraps
import time

# Define metrics
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('active_connections', 'Active database connections')

def counter(metric_name: str, labels: list = None):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            REQUEST_COUNT.labels(method='POST', endpoint=func.__name__, status='200').inc()
            return await func(*args, **kwargs)
        return wrapper
    return decorator

def histogram(metric_name: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = await func(*args, **kwargs)
                return result
            finally:
                REQUEST_DURATION.observe(time.time() - start_time)
        return wrapper
    return decorator
```

## Phase 3: Advanced Features (Week 5-6)

### 3.1 Distributed Tracing

#### OpenTelemetry Integration
```python
# libs/observability/tracing.py
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

def setup_tracing(service_name: str, jaeger_endpoint: str):
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=14268,
    )
    
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    return tracer

def trace_request(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        tracer = trace.get_tracer(__name__)
        with tracer.start_as_current_span(func.__name__) as span:
            span.set_attribute("function.name", func.__name__)
            try:
                result = await func(*args, **kwargs)
                span.set_attribute("function.result", "success")
                return result
            except Exception as e:
                span.set_attribute("function.result", "error")
                span.set_attribute("error.message", str(e))
                raise
    return wrapper
```

### 3.2 Caching Layer

#### Redis Cache Manager
```python
# libs/cache/manager.py
import aioredis
import json
from typing import Any, Optional, Union
from datetime import timedelta

class CacheManager:
    def __init__(self, redis_url: str):
        self.redis = aioredis.from_url(redis_url)
    
    async def get(self, key: str) -> Optional[Any]:
        value = await self.redis.get(key)
        return json.loads(value) if value else None
    
    async def set(self, key: str, value: Any, ttl: Union[int, timedelta] = 3600):
        if isinstance(ttl, timedelta):
            ttl = int(ttl.total_seconds())
        await self.redis.setex(key, ttl, json.dumps(value))
    
    async def delete(self, key: str):
        await self.redis.delete(key)
    
    async def get_or_set(self, key: str, factory, ttl: Union[int, timedelta] = 3600):
        value = await self.get(key)
        if value is None:
            value = await factory()
            await self.set(key, value, ttl)
        return value
```

### 3.3 Async Task Processing

#### Celery Integration
```python
# libs/tasks/manager.py
from celery import Celery
from typing import Any, Dict
import asyncio

class TaskManager:
    def __init__(self, broker_url: str, result_backend: str):
        self.celery = Celery(
            'bhiv_tasks',
            broker=broker_url,
            backend=result_backend
        )
        self._configure_celery()
    
    def _configure_celery(self):
        self.celery.conf.update(
            task_serializer='json',
            accept_content=['json'],
            result_serializer='json',
            timezone='UTC',
            enable_utc=True,
            task_routes={
                'bhiv_tasks.ai_matching': {'queue': 'ai_queue'},
                'bhiv_tasks.email_notifications': {'queue': 'email_queue'},
            }
        )
    
    def enqueue_task(self, task_name: str, *args, **kwargs):
        return self.celery.send_task(task_name, args, kwargs)
    
    @self.celery.task(name='bhiv_tasks.ai_matching')
    def process_ai_matching(candidate_id: int, job_id: int):
        # AI matching logic
        pass
```

## Phase 4: Container Optimization (Week 7-8)

### 4.1 Multi-Stage Dockerfile

#### Optimized Gateway Dockerfile
```dockerfile
# apps/gateway/Dockerfile
# Build stage
FROM python:3.12.7-slim as builder

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Set work directory
WORKDIR /build

# Copy requirements
COPY requirements.txt .
COPY requirements-prod.txt .

# Install Python dependencies
RUN pip install --user --no-cache-dir -r requirements-prod.txt

# Production stage
FROM python:3.12.7-slim as production

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd --create-home --shell /bin/bash app

# Copy Python packages from builder
COPY --from=builder /root/.local /home/app/.local

# Set environment
ENV PATH=/home/app/.local/bin:$PATH
ENV PYTHONPATH=/app

# Switch to non-root user
USER app
WORKDIR /app

# Copy application code
COPY --chown=app:app src/ ./src/
COPY --chown=app:app libs/ ./libs/

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Expose port
EXPOSE 8000

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
```

### 4.2 Docker Compose for Local Development

#### Development Environment
```yaml
# docker-compose.dev.yml
version: '3.8'

services:
  postgres:
    image: postgres:17-alpine
    environment:
      POSTGRES_DB: bhiv_hr_dev
      POSTGRES_USER: bhiv_user
      POSTGRES_PASSWORD: password
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./services/db/init_db.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  gateway:
    build:
      context: ./apps/gateway
      dockerfile: Dockerfile.dev
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://bhiv_user:password@postgres:5432/bhiv_hr_dev
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis
    volumes:
      - ./apps/gateway/src:/app/src
      - ./libs:/app/libs

  agent:
    build:
      context: ./apps/agent
      dockerfile: Dockerfile.dev
    ports:
      - "9000:9000"
    environment:
      - ENVIRONMENT=development
      - DATABASE_URL=postgresql://bhiv_user:password@postgres:5432/bhiv_hr_dev
    depends_on:
      - postgres
    volumes:
      - ./apps/agent/src:/app/src
      - ./libs:/app/libs

volumes:
  postgres_data:
```

## Implementation Timeline

### Week 1: Foundation Setup
- [ ] Create centralized configuration system
- [ ] Set up shared libraries structure
- [ ] Implement database connection pooling
- [ ] Create basic CI/CD pipeline

### Week 2: Core Infrastructure
- [ ] Implement service registry and discovery
- [ ] Set up structured logging
- [ ] Create metrics collection system
- [ ] Implement circuit breaker pattern

### Week 3: Gateway Refactoring
- [ ] Refactor gateway service with modular architecture
- [ ] Implement enhanced middleware
- [ ] Add comprehensive error handling
- [ ] Set up API documentation

### Week 4: Service Communication
- [ ] Implement async service communication
- [ ] Add request/response validation
- [ ] Set up service health monitoring
- [ ] Implement retry mechanisms

### Week 5: Advanced Features
- [ ] Implement distributed tracing
- [ ] Set up caching layer
- [ ] Add async task processing
- [ ] Implement rate limiting

### Week 6: Security & Performance
- [ ] Implement zero-trust security model
- [ ] Add comprehensive input validation
- [ ] Set up performance monitoring
- [ ] Implement load balancing

### Week 7: Container Optimization
- [ ] Create optimized Docker images
- [ ] Set up multi-stage builds
- [ ] Implement security hardening
- [ ] Add health checks

### Week 8: Deployment & Testing
- [ ] Set up blue-green deployment
- [ ] Implement comprehensive testing
- [ ] Performance tuning
- [ ] Documentation and training

## Success Criteria

### Technical Metrics
- **Response Time**: < 100ms (95th percentile)
- **Availability**: > 99.9% uptime
- **Error Rate**: < 0.1% of requests
- **Test Coverage**: > 80% code coverage
- **Security**: Zero critical vulnerabilities

### Operational Metrics
- **Deployment Frequency**: Daily deployments
- **Lead Time**: < 1 hour from commit to production
- **MTTR**: < 15 minutes mean time to recovery
- **Developer Productivity**: 50% reduction in setup time

This implementation plan provides a structured approach to transforming the BHIV HR AI Platform into a truly enterprise-grade system with enhanced scalability, maintainability, and performance.