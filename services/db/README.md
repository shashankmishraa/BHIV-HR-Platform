# Database Service

**PostgreSQL 17**  
**Schema Version**: v4.1.0  
**Tables**: 17 total  
**Status**: ✅ Operational  

## Overview

PostgreSQL database with comprehensive schema for HR platform operations.

## Schema Structure

### Core Application Tables (12)
- **candidates**: Candidate profiles with authentication
- **jobs**: Job postings from clients and HR
- **feedback**: Values assessment (5-point BHIV values)
- **interviews**: Interview scheduling and management
- **offers**: Job offer management
- **users**: Internal HR users with 2FA support
- **clients**: External client companies with JWT auth
- **audit_logs**: Security and compliance tracking
- **rate_limits**: API rate limiting by IP and endpoint
- **csp_violations**: Content Security Policy monitoring
- **matching_cache**: AI matching results cache
- **company_scoring_preferences**: Phase 3 learning engine

### System Tables (5)
- **client_auth**: Enhanced authentication
- **client_sessions**: Session management
- **schema_version**: Version tracking (v4.1.0)
- **pg_stat_statements**: Performance monitoring
- **pg_stat_statements_info**: Statistics metadata

## Key Features

- **Constraints**: CHECK constraints for data validation
- **Indexes**: 25+ performance indexes including GIN for full-text search
- **Triggers**: Auto-update timestamps and audit logging
- **Functions**: PostgreSQL functions for complex operations
- **Generated Columns**: Automatic average score calculation

## Local Development

```bash
# Using Docker
docker run -d --name bhiv-db \
  -e POSTGRES_DB=bhiv_hr \
  -e POSTGRES_USER=bhiv_user \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:17-alpine

# Initialize schema
psql postgresql://bhiv_user:password@localhost:5432/bhiv_hr -f consolidated_schema.sql
```