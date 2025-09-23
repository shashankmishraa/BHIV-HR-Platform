# BHIV HR Platform Gateway - Modular Structure

## Overview
The gateway application has been restructured into a clean, modular architecture for better maintainability, testing, and scalability.

## Module Structure

### Core Files
- **`main.py`** - Clean main application with middleware and router inclusion
- **`__init__.py`** - Package initialization

### Modular Components

#### 1. Core Endpoints (`core_endpoints.py`)
- **Purpose**: Basic API endpoints and health checks
- **Endpoints**: 
  - `/` - API root information
  - `/health` - Health check (GET/HEAD)
  - `/test-candidates` - Database test with sample data
  - `/http-methods-test` - HTTP methods testing
  - `/favicon.ico` - Favicon serving

#### 2. Authentication (`auth_clean.py`)
- **Purpose**: All authentication and authorization logic
- **Features**:
  - User login/logout
  - JWT token management
  - 2FA setup and verification
  - Password validation and reset
  - API key authentication
- **Endpoints**: 15+ authentication endpoints

#### 3. Database Operations (`database_clean.py`)
- **Purpose**: Database operations and data management
- **Features**:
  - Job management (CRUD)
  - Candidate management (CRUD + bulk operations)
  - Interview scheduling
  - Feedback submission
  - Database health checks and migrations
- **Endpoints**: 20+ database endpoints

#### 4. AI Matching (`ai_matching.py`)
- **Purpose**: AI-powered candidate matching and scoring
- **Features**:
  - Job-specific candidate matching
  - Advanced scoring algorithms
  - Skills and experience matching
  - Values assessment integration
  - Performance caching
- **Endpoints**: 5+ AI matching endpoints

#### 5. Monitoring (`monitoring_clean.py`)
- **Purpose**: System monitoring, metrics, and health checks
- **Features**:
  - Prometheus metrics export
  - Health checks (simple and detailed)
  - Error analytics
  - Performance monitoring
  - Log searching
  - Dependency checking
- **Endpoints**: 10+ monitoring endpoints

#### 6. Security Configuration (`security_config_clean.py`)
- **Purpose**: Security settings and configurations
- **Features**:
  - CORS configuration
  - API key management
  - Session management
  - Cookie security settings

#### 7. Performance Optimization (`performance_optimizer_clean.py`)
- **Purpose**: Performance monitoring and caching
- **Features**:
  - In-memory caching with TTL
  - Async health checking
  - Performance metrics collection
  - System resource monitoring

## Benefits of Modular Structure

### 1. **Maintainability**
- Each module has a single responsibility
- Easy to locate and modify specific functionality
- Reduced code complexity per file

### 2. **Testability**
- Individual modules can be tested in isolation
- Mock dependencies easily
- Better test coverage

### 3. **Scalability**
- Easy to add new modules
- Can split modules into separate services
- Better resource allocation

### 4. **Development Efficiency**
- Multiple developers can work on different modules
- Reduced merge conflicts
- Faster development cycles

### 5. **Error Isolation**
- Failures in one module don't affect others
- Better error tracking and debugging
- Graceful degradation

## Import Strategy

The main application uses a fallback import strategy:

```python
try:
    # Try relative imports first (package mode)
    from .core_endpoints import router as core_router
    from .auth_clean import router as auth_router
    # ... other imports
except ImportError:
    # Fallback to direct imports (standalone mode)
    from core_endpoints import router as core_router
    from auth_clean import router as auth_router
    # ... other imports
```

## Router Organization

Each module exports a FastAPI router that gets included in the main application:

```python
# In main.py
app.include_router(core_router, prefix="", tags=["Core"])
app.include_router(auth_router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(database_router, prefix="/v1", tags=["Database"])
app.include_router(ai_router, prefix="/v1", tags=["AI Matching"])
app.include_router(monitoring_router, prefix="", tags=["Monitoring"])
```

## Endpoint Distribution

- **Core Endpoints**: 5 endpoints
- **Authentication**: 15+ endpoints
- **Database Operations**: 20+ endpoints
- **AI Matching**: 5+ endpoints
- **Monitoring**: 10+ endpoints
- **Total**: 55+ endpoints (modular)

## Configuration

Each module handles its own configuration and dependencies:
- Database connections
- Authentication settings
- Caching configuration
- Security policies

## Future Enhancements

1. **Service Separation**: Modules can be extracted into separate microservices
2. **Plugin Architecture**: Dynamic module loading
3. **Configuration Management**: Centralized config management
4. **Event System**: Inter-module communication via events
5. **API Versioning**: Version-specific modules

## Usage

The modular structure maintains full backward compatibility while providing a clean, maintainable codebase for future development.

```bash
# Run the application
python -m uvicorn main:app --host 0.0.0.0 --port 8000

# Or directly
python main.py
```

## Dependencies

Each module manages its own dependencies, with fallbacks for missing components to ensure the application remains functional even if some modules are unavailable.