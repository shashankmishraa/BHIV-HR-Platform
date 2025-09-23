# BHIV HR Platform Gateway - Modular Implementation Guide v2.0

## 🎯 Overview
Complete step-by-step guide to refactor the monolithic gateway (5000+ lines, 151+ endpoints) into a production-ready modular architecture.

**Current State**: Single `main.py` with all endpoints
**Target State**: 10 modules with proper separation of concerns
**Timeline**: 5 weeks
**Zero Downtime**: Gradual migration approach

---

## 📋 Pre-Implementation Checklist

### Prerequisites
- [ ] Backup current `main.py` file
- [ ] Ensure all tests are passing
- [ ] Document current endpoint functionality
- [ ] Set up development branch: `git checkout -b feature/modular-refactor`

### Environment Setup
```bash
cd services/gateway
cp app/main.py app/main_monolithic_backup.py
git add app/main_monolithic_backup.py
git commit -m "Backup monolithic main.py before refactoring"
```

---

## 🏗️ Phase 1: Foundation Setup (Week 1)

### Step 1.1: Create Directory Structure

```bash
mkdir -p app/core
mkdir -p app/shared
mkdir -p app/modules/{core,auth,database/{jobs,candidates,interviews,management},ai_matching,monitoring,security,analytics,sessions,client_portal,enterprise}
mkdir -p app/tests/{unit,integration,performance}
```

### Step 1.2: Create Core Infrastructure

#### 1.2.1: Core Configuration (`app/core/config.py`)
```python
from pydantic import BaseSettings
from typing import List, Optional
import os

class Settings(BaseSettings):
    # Application
    app_name: str = "BHIV HR Platform Gateway"
    version: str = "3.2.0-modular"
    debug: bool = False
    
    # Database
    database_url: str = os.getenv("DATABASE_URL", 
        "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
        if os.getenv("ENVIRONMENT", "development") == "production"
        else "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
    )
    
    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    
    # Security
    secret_key: str = os.getenv("SECRET_KEY", "bhiv-hr-secret-key-2025")
    api_key: str = os.getenv("API_KEY", "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o")
    jwt_algorithm: str = "HS256"
    jwt_expiry_hours: int = 24
    
    # Performance
    cache_ttl: int = 300
    rate_limit_per_minute: int = 60
    connection_pool_size: int = 10
    max_overflow: int = 20
    
    # CORS
    cors_origins: List[str] = ["*"]
    cors_methods: List[str] = ["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"]
    cors_headers: List[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

#### 1.2.2: Middleware (`app/core/middleware.py`)
```python
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from .config import settings
import time
import uuid
import logging

logger = logging.getLogger(__name__)

async def http_method_handler(request: Request, call_next):
    """Handle HTTP methods including HEAD and OPTIONS"""
    method = request.method
    
    if method == "HEAD":
        get_request = Request(scope={**request.scope, "method": "GET"})
        response = await call_next(get_request)
        return Response("", response.status_code, response.headers, response.media_type)
    
    elif method == "OPTIONS":
        return Response("", 200, {
            "Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, HEAD, OPTIONS",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "86400"
        })
    
    elif method not in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
        return PlainTextResponse(
            f"Method {method} not allowed. Supported: GET, POST, PUT, DELETE, HEAD, OPTIONS",
            status_code=405,
            headers={"Allow": "GET, POST, PUT, DELETE, HEAD, OPTIONS"}
        )
    
    return await call_next(request)

async def correlation_middleware(request: Request, call_next):
    """Add correlation ID, timing, and request logging"""
    correlation_id = str(uuid.uuid4())
    request.state.correlation_id = correlation_id
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        response_time = time.time() - start_time
        
        # Add response headers
        response.headers["X-Correlation-ID"] = correlation_id
        response.headers["X-Response-Time"] = f"{response_time:.3f}s"
        response.headers["X-Gateway-Version"] = settings.version
        
        # Log request
        logger.info(
            f"Request processed - method={request.method}, path={request.url.path}, "
            f"status={response.status_code}, time={response_time:.3f}s, "
            f"client={request.client.host if request.client else 'unknown'}"
        )
        
        return response
        
    except Exception as e:
        response_time = time.time() - start_time
        logger.error(
            f"Request failed - method={request.method}, path={request.url.path}, "
            f"error={str(e)}, time={response_time:.3f}s"
        )
        raise

def setup_middleware(app):
    """Setup all middleware in correct order"""
    # HTTP method handler (first)
    app.middleware("http")(http_method_handler)
    
    # Correlation and logging (second)
    app.middleware("http")(correlation_middleware)
    
    # CORS (third)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=settings.cors_methods,
        allow_headers=settings.cors_headers,
        max_age=86400
    )
```

#### 1.2.3: Dependencies (`app/core/dependencies.py`)
```python
from fastapi import Depends, HTTPException, Security
from fastapi.security import HTTPBearer
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool
from .config import settings
from shared.cache import get_cache_manager
from shared.database import get_database_manager
import time
import logging

logger = logging.getLogger(__name__)
security = HTTPBearer()

# Database engine with connection pooling
_db_engine = None

def get_db_engine():
    """Get database engine with connection pooling"""
    global _db_engine
    if _db_engine is None:
        _db_engine = create_engine(
            settings.database_url,
            poolclass=QueuePool,
            pool_size=settings.connection_pool_size,
            max_overflow=settings.max_overflow,
            pool_pre_ping=True,
            pool_recycle=3600
        )
    return _db_engine

async def get_database():
    """Database dependency with proper connection handling"""
    engine = get_db_engine()
    try:
        with engine.connect() as connection:
            # Test connection
            connection.execute(text("SELECT 1"))
            yield connection
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise HTTPException(status_code=503, detail="Database unavailable")

async def get_api_key(credentials = Security(security)):
    """API key authentication dependency"""
    if not credentials:
        raise HTTPException(
            status_code=401, 
            detail="API key required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    # Validate API key
    if credentials.credentials != settings.api_key:
        logger.warning(f"Invalid API key attempt: {credentials.credentials[:8]}...")
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    return credentials.credentials

async def get_cache():
    """Cache dependency"""
    return get_cache_manager()

async def get_db_manager():
    """Database manager dependency"""
    return get_database_manager()

# Rate limiting dependency
_rate_limits = {}

async def check_rate_limit(request, limit: int = None):
    """Rate limiting dependency"""
    if limit is None:
        limit = settings.rate_limit_per_minute
    
    client_ip = request.client.host if request.client else "unknown"
    current_time = time.time()
    
    # Clean old entries
    if client_ip in _rate_limits:
        _rate_limits[client_ip] = [
            req_time for req_time in _rate_limits[client_ip]
            if current_time - req_time < 60
        ]
    else:
        _rate_limits[client_ip] = []
    
    # Check limit
    if len(_rate_limits[client_ip]) >= limit:
        raise HTTPException(
            status_code=429,
            detail=f"Rate limit exceeded: {limit} requests per minute"
        )
    
    # Record request
    _rate_limits[client_ip].append(current_time)
    return True
```

#### 1.2.4: Exception Handlers (`app/core/exceptions.py`)
```python
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from datetime import datetime, timezone
import logging
import traceback

logger = logging.getLogger(__name__)

class ModuleException(Exception):
    """Custom exception for module-specific errors"""
    def __init__(self, message: str, status_code: int = 500, module: str = "gateway", details: dict = None):
        self.message = message
        self.status_code = status_code
        self.module = module
        self.details = details or {}
        super().__init__(self.message)

class ValidationException(ModuleException):
    """Exception for validation errors"""
    def __init__(self, message: str, field: str = None, value: str = None):
        super().__init__(message, 422, "validation", {"field": field, "value": value})

class AuthenticationException(ModuleException):
    """Exception for authentication errors"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, 401, "auth")

class AuthorizationException(ModuleException):
    """Exception for authorization errors"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, 403, "auth")

async def module_exception_handler(request: Request, exc: ModuleException):
    """Handle module-specific exceptions"""
    logger.error(
        f"Module exception - module={exc.module}, status={exc.status_code}, "
        f"message={exc.message}, path={request.url.path}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.message,
            "module": exc.module,
            "details": exc.details,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": str(request.url.path),
            "correlation_id": getattr(request.state, 'correlation_id', None)
        }
    )

async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle FastAPI HTTP exceptions"""
    logger.warning(
        f"HTTP exception - status={exc.status_code}, detail={exc.detail}, "
        f"path={request.url.path}"
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": str(request.url.path),
            "correlation_id": getattr(request.state, 'correlation_id', None)
        }
    )

async def general_exception_handler(request: Request, exc: Exception):
    """Handle unexpected exceptions"""
    logger.error(
        f"Unexpected exception - type={type(exc).__name__}, message={str(exc)}, "
        f"path={request.url.path}, traceback={traceback.format_exc()}"
    )
    
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "type": type(exc).__name__,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "path": str(request.url.path),
            "correlation_id": getattr(request.state, 'correlation_id', None)
        }
    )

def setup_exception_handlers(app):
    """Setup all exception handlers"""
    app.add_exception_handler(ModuleException, module_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(Exception, general_exception_handler)
```

#### 1.2.5: Module Loader (`app/core/module_loader.py`)
```python
from typing import List, Dict, Any, Optional
import importlib
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class ModuleConfig:
    """Configuration for a module"""
    name: str
    router: Any
    prefix: str = ""
    tags: List[str] = None
    dependencies: List[str] = None
    enabled: bool = True
    
    def __post_init__(self):
        if self.tags is None:
            self.tags = [self.name.replace('_', ' ').title()]
        if self.dependencies is None:
            self.dependencies = []

class ModuleLoader:
    """Dynamic module loader with dependency management"""
    
    def __init__(self):
        self.loaded_modules: Dict[str, ModuleConfig] = {}
        self.failed_modules: Dict[str, str] = {}
    
    def get_module_configs(self) -> List[tuple]:
        """Get module configurations in dependency order"""
        return [
            # Core modules (no dependencies)
            ("core", "", ["Core"], []),
            ("auth", "/v1/auth", ["Authentication"], []),
            
            # Database modules (depend on core)
            ("database", "/v1", ["Database"], ["core"]),
            
            # Business logic modules (depend on database and auth)
            ("ai_matching", "/v1", ["AI Matching"], ["database", "auth"]),
            ("sessions", "/v1/sessions", ["Sessions"], ["auth"]),
            ("client_portal", "/v1/client", ["Client Portal"], ["auth", "sessions"]),
            
            # Monitoring and security (depend on core)
            ("monitoring", "", ["Monitoring"], ["core"]),
            ("security", "/v1/security", ["Security"], ["core", "auth"]),
            ("analytics", "/v1", ["Analytics"], ["database", "monitoring"]),
            
            # Enterprise features (depend on all core modules)
            ("enterprise", "/v1/enterprise", ["Enterprise"], ["auth", "database", "security"]),
        ]
    
    def load_module(self, module_name: str, prefix: str, tags: List[str], dependencies: List[str]) -> Optional[ModuleConfig]:
        """Load a single module with error handling"""
        try:
            # Check dependencies
            for dep in dependencies:
                if dep not in self.loaded_modules:
                    logger.warning(f"⚠️ Module {module_name} dependency {dep} not loaded")
            
            # Import module
            module = importlib.import_module(f"modules.{module_name}")
            
            if not hasattr(module, 'router'):
                raise ImportError(f"Module {module_name} has no router attribute")
            
            config = ModuleConfig(
                name=module_name,
                router=module.router,
                prefix=prefix,
                tags=tags,
                dependencies=dependencies
            )
            
            self.loaded_modules[module_name] = config
            logger.info(f"✅ Loaded module: {module_name}")
            return config
            
        except ImportError as e:
            error_msg = f"Import failed: {str(e)}"
            self.failed_modules[module_name] = error_msg
            logger.warning(f"❌ Failed to load module {module_name}: {error_msg}")
            return None
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            self.failed_modules[module_name] = error_msg
            logger.error(f"❌ Failed to load module {module_name}: {error_msg}")
            return None
    
    def load_all_modules(self) -> List[ModuleConfig]:
        """Load all modules in dependency order"""
        modules = []
        module_configs = self.get_module_configs()
        
        for module_name, prefix, tags, dependencies in module_configs:
            config = self.load_module(module_name, prefix, tags, dependencies)
            if config:
                modules.append(config)
        
        logger.info(f"📊 Module loading complete: {len(modules)} loaded, {len(self.failed_modules)} failed")
        return modules
    
    def get_status(self) -> Dict[str, Any]:
        """Get module loading status"""
        return {
            "loaded_modules": list(self.loaded_modules.keys()),
            "failed_modules": self.failed_modules,
            "total_loaded": len(self.loaded_modules),
            "total_failed": len(self.failed_modules)
        }

# Global module loader instance
module_loader = ModuleLoader()

def load_modules() -> List[ModuleConfig]:
    """Load all available modules"""
    return module_loader.load_all_modules()

def get_module_status() -> Dict[str, Any]:
    """Get module loading status"""
    return module_loader.get_status()
```

### Step 1.3: Create Shared Utilities

#### 1.3.1: Database Utilities (`app/shared/database.py`)
```python
from sqlalchemy import create_engine, text, MetaData
from sqlalchemy.pool import QueuePool
from core.config import settings
import logging
from typing import Dict, Any, List

logger = logging.getLogger(__name__)

class DatabaseManager:
    """Database management utilities"""
    
    def __init__(self):
        self.engine = None
        self.metadata = MetaData()
    
    def get_engine(self):
        """Get database engine with connection pooling"""
        if self.engine is None:
            self.engine = create_engine(
                settings.database_url,
                poolclass=QueuePool,
                pool_size=settings.connection_pool_size,
                max_overflow=settings.max_overflow,
                pool_pre_ping=True,
                pool_recycle=3600
            )
        return self.engine
    
    def test_connection(self) -> bool:
        """Test database connection"""
        try:
            engine = self.get_engine()
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Database connection test failed: {e}")
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get database health status"""
        try:
            engine = self.get_engine()
            with engine.connect() as conn:
                # Test connection
                conn.execute(text("SELECT 1"))
                
                # Get table counts
                table_counts = {}
                tables = ["candidates", "jobs", "interviews", "feedback"]
                
                for table in tables:
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        table_counts[table] = result.fetchone()[0]
                    except Exception:
                        table_counts[table] = "N/A"
                
                return {
                    "status": "healthy",
                    "connection": "active",
                    "pool_size": settings.connection_pool_size,
                    "table_counts": table_counts,
                    "timestamp": "2025-01-18T10:00:00Z"
                }
        except Exception as e:
            return {
                "status": "unhealthy",
                "error": str(e),
                "timestamp": "2025-01-18T10:00:00Z"
            }
    
    def validate_schema(self) -> Dict[str, Any]:
        """Validate database schema"""
        try:
            engine = self.get_engine()
            with engine.connect() as conn:
                # Check required tables
                required_tables = ["candidates", "jobs", "interviews", "feedback"]
                missing_tables = []
                
                for table in required_tables:
                    try:
                        conn.execute(text(f"SELECT 1 FROM {table} LIMIT 1"))
                    except Exception:
                        missing_tables.append(table)
                
                return {
                    "valid": len(missing_tables) == 0,
                    "missing_tables": missing_tables,
                    "missing_columns": []  # TODO: Implement column validation
                }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
                "missing_tables": [],
                "missing_columns": []
            }

# Global database manager instance
_db_manager = None

def get_database_manager() -> DatabaseManager:
    """Get database manager instance"""
    global _db_manager
    if _db_manager is None:
        _db_manager = DatabaseManager()
    return _db_manager
```

#### 1.3.2: Cache Utilities (`app/shared/cache.py`)
```python
import time
import json
import hashlib
from typing import Any, Optional, Dict
import logging

logger = logging.getLogger(__name__)

class CacheManager:
    """In-memory cache manager with TTL support"""
    
    def __init__(self):
        self._cache: Dict[str, Any] = {}
        self._ttl: Dict[str, float] = {}
        self._stats = {
            "hits": 0,
            "misses": 0,
            "sets": 0,
            "deletes": 0,
            "clears": 0
        }
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        current_time = time.time()
        
        if key in self._cache:
            if key in self._ttl and current_time > self._ttl[key]:
                # Expired
                del self._cache[key]
                del self._ttl[key]
                self._stats["misses"] += 1
                return None
            else:
                # Valid
                self._stats["hits"] += 1
                return self._cache[key]
        else:
            self._stats["misses"] += 1
            return None
    
    def set(self, key: str, value: Any, ttl: int = 300) -> None:
        """Set value in cache with TTL"""
        self._cache[key] = value
        self._ttl[key] = time.time() + ttl
        self._stats["sets"] += 1
    
    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
            if key in self._ttl:
                del self._ttl[key]
            self._stats["deletes"] += 1
            return True
        return False
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
        self._ttl.clear()
        self._stats["clears"] += 1
    
    def cleanup_expired(self) -> int:
        """Remove expired entries"""
        current_time = time.time()
        expired_keys = []
        
        for key, expiry_time in self._ttl.items():
            if current_time > expiry_time:
                expired_keys.append(key)
        
        for key in expired_keys:
            if key in self._cache:
                del self._cache[key]
            del self._ttl[key]
        
        return len(expired_keys)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_requests = self._stats["hits"] + self._stats["misses"]
        hit_rate = (self._stats["hits"] / total_requests * 100) if total_requests > 0 else 0
        
        return {
            "total_entries": len(self._cache),
            "total_requests": total_requests,
            "hits": self._stats["hits"],
            "misses": self._stats["misses"],
            "hit_rate_percent": round(hit_rate, 2),
            "sets": self._stats["sets"],
            "deletes": self._stats["deletes"],
            "clears": self._stats["clears"]
        }
    
    def generate_key(self, *args, **kwargs) -> str:
        """Generate cache key from arguments"""
        key_data = {
            "args": args,
            "kwargs": sorted(kwargs.items())
        }
        key_string = json.dumps(key_data, sort_keys=True, default=str)
        return hashlib.md5(key_string.encode()).hexdigest()

# Global cache manager instance
_cache_manager = None

def get_cache_manager() -> CacheManager:
    """Get cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager
```

#### 1.3.3: Security Utilities (`app/shared/security.py`)
```python
import hashlib
import secrets
import re
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone, timedelta
import jwt
from core.config import settings
import logging

logger = logging.getLogger(__name__)

class SecurityManager:
    """Security utilities and helpers"""
    
    def __init__(self):
        self.blocked_ips: List[str] = []
        self.failed_attempts: Dict[str, List[float]] = {}
    
    def sanitize_input(self, input_string: str, max_length: int = 1000) -> str:
        """Sanitize user input"""
        if not input_string:
            return ""
        
        # Truncate to max length
        sanitized = str(input_string)[:max_length]
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>"\']', '', sanitized)
        
        # Remove SQL injection patterns
        sql_patterns = [
            r'union\s+select', r'drop\s+table', r'insert\s+into',
            r'delete\s+from', r'update\s+set', r'exec\s*\(',
            r'script\s*>', r'javascript:', r'vbscript:'
        ]
        
        for pattern in sql_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        pattern = r'^\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}$'
        return bool(re.match(pattern, phone))
    
    def hash_password(self, password: str) -> str:
        """Hash password with salt"""
        salt = secrets.token_hex(16)
        password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return f"{salt}:{password_hash.hex()}"
    
    def verify_password(self, password: str, hashed: str) -> bool:
        """Verify password against hash"""
        try:
            salt, password_hash = hashed.split(':')
            new_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
            return password_hash == new_hash.hex()
        except Exception:
            return False
    
    def generate_jwt_token(self, user_id: str, permissions: List[str] = None) -> str:
        """Generate JWT token"""
        if permissions is None:
            permissions = ["read"]
        
        payload = {
            "user_id": user_id,
            "permissions": permissions,
            "exp": datetime.utcnow() + timedelta(hours=settings.jwt_expiry_hours),
            "iat": datetime.utcnow(),
            "iss": settings.app_name
        }
        
        return jwt.encode(payload, settings.secret_key, algorithm=settings.jwt_algorithm)
    
    def validate_jwt_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate JWT token"""
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.jwt_algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("JWT token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid JWT token")
            return None
    
    def check_rate_limit(self, identifier: str, limit: int = 60, window: int = 60) -> bool:
        """Check rate limit for identifier"""
        current_time = time.time()
        
        # Clean old attempts
        if identifier in self.failed_attempts:
            self.failed_attempts[identifier] = [
                attempt for attempt in self.failed_attempts[identifier]
                if current_time - attempt < window
            ]
        else:
            self.failed_attempts[identifier] = []
        
        # Check limit
        if len(self.failed_attempts[identifier]) >= limit:
            return False
        
        # Record attempt
        self.failed_attempts[identifier].append(current_time)
        return True
    
    def is_ip_blocked(self, ip: str) -> bool:
        """Check if IP is blocked"""
        return ip in self.blocked_ips
    
    def block_ip(self, ip: str) -> None:
        """Block IP address"""
        if ip not in self.blocked_ips:
            self.blocked_ips.append(ip)
            logger.warning(f"IP blocked: {ip}")
    
    def unblock_ip(self, ip: str) -> None:
        """Unblock IP address"""
        if ip in self.blocked_ips:
            self.blocked_ips.remove(ip)
            logger.info(f"IP unblocked: {ip}")
    
    def get_security_headers(self) -> Dict[str, str]:
        """Get security headers"""
        return {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline'",
            "Referrer-Policy": "strict-origin-when-cross-origin"
        }

# Global security manager instance
_security_manager = None

def get_security_manager() -> SecurityManager:
    """Get security manager instance"""
    global _security_manager
    if _security_manager is None:
        _security_manager = SecurityManager()
    return _security_manager
```

#### 1.3.4: Monitoring Utilities (`app/shared/monitoring.py`)
```python
import time
import psutil
from typing import Dict, Any, List
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class MonitoringManager:
    """Monitoring and observability utilities"""
    
    def __init__(self):
        self.metrics = {
            "requests_total": 0,
            "requests_success": 0,
            "requests_error": 0,
            "response_times": [],
            "errors": []
        }
        self.start_time = time.time()
    
    def record_request(self, method: str, path: str, status_code: int, response_time: float):
        """Record request metrics"""
        self.metrics["requests_total"] += 1
        
        if 200 <= status_code < 400:
            self.metrics["requests_success"] += 1
        else:
            self.metrics["requests_error"] += 1
        
        self.metrics["response_times"].append(response_time)
        
        # Keep only last 1000 response times
        if len(self.metrics["response_times"]) > 1000:
            self.metrics["response_times"] = self.metrics["response_times"][-1000:]
    
    def record_error(self, error_type: str, message: str, module: str = "gateway"):
        """Record error"""
        error_record = {
            "type": error_type,
            "message": message,
            "module": module,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        self.metrics["errors"].append(error_record)
        
        # Keep only last 100 errors
        if len(self.metrics["errors"]) > 100:
            self.metrics["errors"] = self.metrics["errors"][-100:]
    
    def get_system_metrics(self) -> Dict[str, Any]:
        """Get system resource metrics"""
        try:
            return {
                "cpu_percent": psutil.cpu_percent(interval=1),
                "memory_percent": psutil.virtual_memory().percent,
                "disk_percent": psutil.disk_usage('/').percent,
                "network_io": dict(psutil.net_io_counters()._asdict()),
                "process_count": len(psutil.pids()),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
    
    def get_application_metrics(self) -> Dict[str, Any]:
        """Get application metrics"""
        response_times = self.metrics["response_times"]
        
        if response_times:
            avg_response_time = sum(response_times) / len(response_times)
            max_response_time = max(response_times)
            min_response_time = min(response_times)
        else:
            avg_response_time = max_response_time = min_response_time = 0
        
        uptime = time.time() - self.start_time
        
        return {
            "uptime_seconds": uptime,
            "requests_total": self.metrics["requests_total"],
            "requests_success": self.metrics["requests_success"],
            "requests_error": self.metrics["requests_error"],
            "success_rate_percent": (
                (self.metrics["requests_success"] / self.metrics["requests_total"] * 100)
                if self.metrics["requests_total"] > 0 else 0
            ),
            "avg_response_time_ms": round(avg_response_time * 1000, 2),
            "max_response_time_ms": round(max_response_time * 1000, 2),
            "min_response_time_ms": round(min_response_time * 1000, 2),
            "recent_errors": self.metrics["errors"][-10:],  # Last 10 errors
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    def export_prometheus_metrics(self) -> str:
        """Export metrics in Prometheus format"""
        metrics = self.get_application_metrics()
        
        prometheus_metrics = f"""# HELP gateway_requests_total Total number of requests
# TYPE gateway_requests_total counter
gateway_requests_total {metrics['requests_total']}

# HELP gateway_requests_success_total Total number of successful requests
# TYPE gateway_requests_success_total counter
gateway_requests_success_total {metrics['requests_success']}

# HELP gateway_requests_error_total Total number of error requests
# TYPE gateway_requests_error_total counter
gateway_requests_error_total {metrics['requests_error']}

# HELP gateway_response_time_avg Average response time in milliseconds
# TYPE gateway_response_time_avg gauge
gateway_response_time_avg {metrics['avg_response_time_ms']}

# HELP gateway_uptime_seconds Application uptime in seconds
# TYPE gateway_uptime_seconds gauge
gateway_uptime_seconds {metrics['uptime_seconds']}
"""
        return prometheus_metrics
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get overall health status"""
        system_metrics = self.get_system_metrics()
        app_metrics = self.get_application_metrics()
        
        # Determine health status
        status = "healthy"
        issues = []
        
        if "error" in system_metrics:
            status = "degraded"
            issues.append("System metrics unavailable")
        else:
            if system_metrics["cpu_percent"] > 80:
                status = "degraded"
                issues.append("High CPU usage")
            
            if system_metrics["memory_percent"] > 85:
                status = "degraded"
                issues.append("High memory usage")
        
        if app_metrics["success_rate_percent"] < 95:
            status = "degraded"
            issues.append("Low success rate")
        
        return {
            "status": status,
            "issues": issues,
            "system_metrics": system_metrics,
            "application_metrics": app_metrics,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# Global monitoring manager instance
_monitoring_manager = None

def get_monitoring_manager() -> MonitoringManager:
    """Get monitoring manager instance"""
    global _monitoring_manager
    if _monitoring_manager is None:
        _monitoring_manager = MonitoringManager()
    return _monitoring_manager
```

### Step 1.4: Create Clean Main Application

#### Create Main Application (`app/main.py`)
```python
from fastapi import FastAPI
from core.middleware import setup_middleware
from core.exceptions import setup_exception_handlers
from core.module_loader import load_modules, get_module_status
from core.config import settings
from shared.monitoring import get_monitoring_manager
from datetime import datetime, timezone
import logging
import uvicorn

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Enterprise HR Platform - Modular Architecture",
    debug=settings.debug
)

# Setup middleware and exception handlers
setup_middleware(app)
setup_exception_handlers(app)

# Initialize monitoring
monitoring = get_monitoring_manager()

# Load and register modules
modules = load_modules()
module_status = get_module_status()

for module in modules:
    try:
        app.include_router(
            module.router,
            prefix=module.prefix,
            tags=module.tags
        )
        logger.info(f"✅ Registered module: {module.name} ({module.prefix})")
    except Exception as e:
        logger.error(f"❌ Failed to register module {module.name}: {e}")

# Fallback endpoints if no modules loaded
if not modules:
    logger.warning("⚠️ No modules loaded, creating fallback endpoints")
    
    @app.get("/")
    def fallback_root():
        return {
            "message": settings.app_name,
            "version": settings.version,
            "status": "fallback_mode",
            "modules_loaded": 0,
            "error": "No modules available",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    
    @app.get("/health")
    def fallback_health():
        return {
            "status": "degraded",
            "mode": "fallback",
            "modules_loaded": 0,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }

# System endpoints
@app.get("/module-status")
async def get_modules_status():
    """Get module loading status"""
    return {
        **module_status,
        "environment": settings.environment,
        "version": settings.version,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/system/info")
async def get_system_info():
    """Get system information"""
    return {
        "application": {
            "name": settings.app_name,
            "version": settings.version,
            "environment": settings.environment,
            "debug": settings.debug
        },
        "modules": {
            "loaded": len(modules),
            "failed": len(module_status["failed_modules"]),
            "total_endpoints": sum(len(getattr(m.router, 'routes', [])) for m in modules)
        },
        "configuration": {
            "cache_ttl": settings.cache_ttl,
            "rate_limit": settings.rate_limit_per_minute,
            "jwt_expiry_hours": settings.jwt_expiry_hours
        },
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Application startup"""
    startup_info = {
        "service": settings.app_name,
        "version": settings.version,
        "environment": settings.environment,
        "modules_loaded": len(modules),
        "modules_failed": len(module_status["failed_modules"]),
        "total_endpoints": sum(len(getattr(m.router, 'routes', [])) for m in modules)
    }
    
    logger.info(f"🚀 {settings.app_name} starting up")
    logger.info(f"📊 Startup info: {startup_info}")
    
    # Test database connection
    from shared.database import get_database_manager
    db_manager = get_database_manager()
    if db_manager.test_connection():
        logger.info("✅ Database connection successful")
    else:
        logger.error("❌ Database connection failed")

@app.on_event("shutdown")
async def shutdown_event():
    """Application shutdown"""
    logger.info(f"🛑 {settings.app_name} shutting down")

# Run application
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    logger.info(f"🌐 Starting server on port {port}")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=settings.debug,
        log_level="info"
    )
```

### Step 1.5: Foundation Testing

#### Create Foundation Test (`app/test_foundation.py`)
```python
#!/usr/bin/env python3
"""Test the modular foundation"""

import sys
import os
import asyncio
sys.path.append(os.path.dirname(__file__))

def test_imports():
    """Test that all core modules can be imported"""
    try:
        from core.config import settings
        from core.middleware import setup_middleware
        from core.dependencies import get_api_key, get_cache
        from core.exceptions import setup_exception_handlers
        from core.module_loader import load_modules
        from shared.database import get_database_manager
        from shared.cache import get_cache_manager
        from shared.security import get_security_manager
        from shared.monitoring import get_monitoring_manager
        print("✅ All core imports successful")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from core.config import settings
        assert settings.environment in ["development", "production"]
        assert settings.database_url
        assert settings.app_name
        assert settings.version
        print("✅ Configuration test passed")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_database():
    """Test database manager"""
    try:
        from shared.database import get_database_manager
        db_manager = get_database_manager()
        engine = db_manager.get_engine()
        assert engine is not None
        print("✅ Database manager test passed")
        return True
    except Exception as e:
        print(f"❌ Database manager test failed: {e}")
        return False

def test_cache():
    """Test cache manager"""
    try:
        from shared.cache import get_cache_manager
        cache = get_cache_manager()
        
        # Test basic operations
        cache.set("test_key", "test_value", 60)
        value = cache.get("test_key")
        assert value == "test_value"
        
        stats = cache.get_stats()
        assert stats["total_entries"] >= 1
        
        print("✅ Cache manager test passed")
        return True
    except Exception as e:
        print(f"❌ Cache manager test failed: {e}")
        return False

def test_security():
    """Test security manager"""
    try:
        from shared.security import get_security_manager
        security = get_security_manager()
        
        # Test input sanitization
        clean_input = security.sanitize_input("<script>alert('xss')</script>")
        assert "<script>" not in clean_input
        
        # Test email validation
        assert security.validate_email("test@example.com") == True
        assert security.validate_email("invalid-email") == False
        
        print("✅ Security manager test passed")
        return True
    except Exception as e:
        print(f"❌ Security manager test failed: {e}")
        return False

def test_monitoring():
    """Test monitoring manager"""
    try:
        from shared.monitoring import get_monitoring_manager
        monitoring = get_monitoring_manager()
        
        # Test metrics recording
        monitoring.record_request("GET", "/test", 200, 0.1)
        metrics = monitoring.get_application_metrics()
        assert metrics["requests_total"] >= 1
        
        print("✅ Monitoring manager test passed")
        return True
    except Exception as e:
        print(f"❌ Monitoring manager test failed: {e}")
        return False

def test_module_loader():
    """Test module loader"""
    try:
        from core.module_loader import load_modules, get_module_status
        modules = load_modules()
        status = get_module_status()
        
        print(f"✅ Module loader test passed - {len(modules)} modules found")
        print(f"   Loaded: {status['loaded_modules']}")
        print(f"   Failed: {list(status['failed_modules'].keys())}")
        return True
    except Exception as e:
        print(f"❌ Module loader test failed: {e}")
        return False

async def test_main_app():
    """Test main application"""
    try:
        from main import app
        assert app is not None
        assert app.title == "BHIV HR Platform API Gateway"
        print("✅ Main application test passed")
        return True
    except Exception as e:
        print(f"❌ Main application test failed: {e}")
        return False

async def run_all_tests():
    """Run all tests"""
    print("🧪 Testing modular foundation...")
    print("=" * 50)
    
    sync_tests = [
        test_imports,
        test_config,
        test_database,
        test_cache,
        test_security,
        test_monitoring,
        test_module_loader
    ]
    
    async_tests = [
        test_main_app
    ]
    
    # Run synchronous tests
    sync_passed = sum(test() for test in sync_tests)
    
    # Run asynchronous tests
    async_passed = 0
    for test in async_tests:
        try:
            result = await test()
            if result:
                async_passed += 1
        except Exception as e:
            print(f"❌ Async test failed: {e}")
    
    total_tests = len(sync_tests) + len(async_tests)
    total_passed = sync_passed + async_passed
    
    print("=" * 50)
    print(f"📊 Results: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 Foundation is ready for module extraction!")
        return True
    else:
        print("❌ Foundation needs fixes before proceeding")
        print("\nNext steps:")
        print("1. Fix failing tests")
        print("2. Ensure all dependencies are installed")
        print("3. Check database connection")
        return False

if __name__ == "__main__":
    success = asyncio.run(run_all_tests())
    sys.exit(0 if success else 1)
```

#### Run Foundation Test
```bash
cd app
python test_foundation.py
```

**✅ Week 1 Checkpoint**: 
- Foundation infrastructure created
- All shared utilities implemented
- Clean main application ready
- Tests passing
- Ready for module extraction

---

## 📝 Next Steps

After completing Week 1 foundation setup:

1. **Week 2**: Extract Core and Auth modules
2. **Week 3**: Extract Database module (jobs, candidates, interviews, management)
3. **Week 4**: Extract AI Matching and Monitoring modules
4. **Week 5**: Extract Security, Analytics, Sessions, Client Portal, and Enterprise modules

Each week will follow the same pattern:
- Create module structure
- Extract endpoints from monolithic file
- Implement handlers and services
- Add tests
- Validate functionality

The foundation is now ready to support the complete modular architecture with proper error handling, monitoring, caching, and security utilities.