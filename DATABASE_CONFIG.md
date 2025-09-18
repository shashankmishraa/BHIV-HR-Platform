# Database Configuration Guide

## Environment-Aware Database URLs

The BHIV HR Gateway service uses intelligent database URL configuration that adapts to different deployment environments:

### 🌐 Production (Render)
- **Detection**: `RENDER` environment variable or `DATABASE_URL` is set
- **Database URL**: Uses `DATABASE_URL` environment variable from Render
- **Example**: `postgresql://user:pass@dpg-xyz.oregon-postgres.render.com:5432/dbname`

### 🐳 Docker Environment
- **Detection**: `DOCKER_ENV` environment variable is set
- **Database URL**: `postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr`
- **Hostname**: `db` (Docker service name)

### 💻 Local Development
- **Detection**: No special environment variables
- **Database URL**: `postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr`
- **Hostname**: `localhost`

## Configuration Logic

```python
# Environment-aware database URL
default_db_url = "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr"  # Docker default

if os.getenv("RENDER") or os.getenv("DATABASE_URL"):
    # Production (Render) - use DATABASE_URL from environment
    database_url = os.getenv("DATABASE_URL", default_db_url)
elif os.getenv("DOCKER_ENV"):
    # Docker environment - use 'db' hostname
    database_url = default_db_url
else:
    # Local development - use localhost
    database_url = "postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr"
```

## Environment Variables

### For Render Deployment
```bash
DATABASE_URL=postgresql://user:pass@host:5432/dbname  # Set by Render automatically
```

### For Docker Deployment
```bash
DOCKER_ENV=true
DATABASE_URL=postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr
```

### For Local Development
```bash
# No special variables needed
# Will automatically use localhost
```

## Testing Database Connection

The gateway service includes graceful database connection handling:

1. **Production**: Must connect successfully
2. **Docker**: Must connect to 'db' service
3. **Local Development**: Connection failure is handled gracefully for testing

## Troubleshooting

### Render Deployment
- Ensure `DATABASE_URL` is set in Render environment variables
- Check Render PostgreSQL service is running
- Verify database credentials

### Docker Deployment
- Ensure PostgreSQL service is named 'db' in docker-compose.yml
- Check database service is running: `docker-compose ps`
- Verify network connectivity between services

### Local Development
- Install PostgreSQL locally or use Docker
- Create database: `createdb bhiv_hr`
- Create user: `createuser -P bhiv_user`
- Grant permissions: `GRANT ALL ON DATABASE bhiv_hr TO bhiv_user;`

## Current Status

✅ **Render**: Uses `DATABASE_URL` environment variable  
✅ **Docker**: Uses `db` hostname for service communication  
✅ **Local**: Uses `localhost` for development  
✅ **Fallback**: Graceful handling when database is unavailable  

This configuration ensures the gateway service works seamlessly across all deployment environments without code changes.