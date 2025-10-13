# 🗄️ DBeaver Database Setup Guide - BHIV HR Platform

**Complete guide for connecting to both Local and Production databases using DBeaver**

## 📋 Overview

This guide provides step-by-step instructions for setting up DBeaver connections to visualize and manage the BHIV HR Platform databases:

- **Local Database**: PostgreSQL 15 running in Docker container
- **Production Database**: PostgreSQL 17 hosted on Render Cloud Platform

### 🏗️ Database Architecture
- **Schema Version**: v4.1.0 with Phase 3 learning engine
- **Total Tables**: 17 (12 core + 5 additional)
- **Extensions**: uuid-ossp, pg_stat_statements, pg_trgm
- **Features**: Triggers, indexes, audit logging, rate limiting

---

## 🚀 Quick Setup Summary

| Environment | Host | Port | Database | Username | Status |
|-------------|------|------|----------|----------|--------|
| **Local** | localhost | 5432 | bhiv_hr | bhiv_user | ✅ Active |
| **Production** | dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com | 5432 | bhiv_hr_jcuu | bhiv_user | ✅ Active |

---

## 📥 Prerequisites

### 1. Install DBeaver
```bash
# Download from official website
https://dbeaver.io/download/

# Or using package managers
# Windows (Chocolatey)
choco install dbeaver

# macOS (Homebrew)
brew install --cask dbeaver-community

# Ubuntu/Debian
sudo snap install dbeaver-ce
```

### 2. Verify Local Environment
```bash
# Check if local database is running
docker ps | grep postgres

# Start local environment if needed
cd c:\BHIV-HR-Platform
docker-compose -f deployment\docker\docker-compose.production.yml up -d db

# Verify database health
curl http://localhost:8000/health
```

---

## 🏠 Local Database Connection Setup

### Step 1: Create New Connection
1. **Open DBeaver**
2. **Click** "New Database Connection" (plug icon) or `Ctrl+Shift+N`
3. **Select** "PostgreSQL" from the database list
4. **Click** "Next"

### Step 2: Configure Connection Details
```
Connection Settings:
┌─────────────────────────────────────────┐
│ Server Host:     localhost              │
│ Port:           5432                    │
│ Database:       bhiv_hr                 │
│ Username:       bhiv_user               │
│ Password:       bhiv_local_password_2025│
│ Show all databases: ☑                  │
└─────────────────────────────────────────┘
```

### Step 3: Advanced Settings
1. **Click** "Driver properties" tab
2. **Set** these properties:
   ```
   ssl: false
   sslmode: disable
   ApplicationName: DBeaver-BHIV-Local
   ```

### Step 4: Test Connection
1. **Click** "Test Connection"
2. **Expected Result**: ✅ "Connected" message
3. **If prompted**: Download PostgreSQL driver
4. **Click** "OK" to save connection

### Step 5: Connection Name
- **Name**: `BHIV HR - Local Development`
- **Color**: Blue (for local identification)

---

## ☁️ Production Database Connection Setup

### Step 1: Create New Connection
1. **Open DBeaver**
2. **Click** "New Database Connection"
3. **Select** "PostgreSQL"
4. **Click** "Next"

### Step 2: Configure Production Details
```
Connection Settings:
┌─────────────────────────────────────────────────────────────────────┐
│ Server Host: dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com  │
│ Port:        5432                                                   │
│ Database:    bhiv_hr_jcuu                                          │
│ Username:    bhiv_user                                             │
│ Password:    3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2                      │
│ Show all databases: ☑                                             │
└─────────────────────────────────────────────────────────────────────┘
```

### Step 3: SSL Configuration (Required for Render)
1. **Click** "SSL" tab (next to Driver properties)
2. **Configure SSL settings**:
   ```
   SSL mode: require (from dropdown)
   SSL Factory: org.postgresql.ssl.DefaultJavaSSLFactory (from dropdown)
   ```
3. **Leave certificate fields empty** (CA Certificate, Client Certificate, Client Private Key)
4. **Note**: All SSL parameters are optional for Render PostgreSQL

### Step 4: Advanced Properties (Optional)
1. **Click** "Driver properties" tab
2. **Optionally set** these properties:
   ```
   ApplicationName: DBeaver-BHIV-Production
   connectTimeout: 30
   socketTimeout: 30
   ```
3. **Note**: SSL properties are configured in the SSL tab, not here

### Step 5: Test Production Connection
1. **Click** "Test Connection"
2. **Expected Result**: ✅ "Connected" message
3. **If SSL errors**: Verify SSL settings above
4. **Click** "OK" to save

### Step 6: Connection Name
- **Name**: `BHIV HR - Production (Render)`
- **Color**: Red (for production identification)

---

## 🔍 Database Schema Exploration

### Core Tables Structure
```
BHIV HR Platform Schema v4.1.0
├── 📊 Core Business Tables (5)
│   ├── candidates (Primary entity)
│   ├── jobs (Job postings)
│   ├── feedback (Values assessment)
│   ├── interviews (Interview management)
│   └── offers (Job offers)
├── 🔐 Authentication Tables (2)
│   ├── users (Internal HR users)
│   └── clients (External companies)
├── 🤖 AI & Performance Tables (1)
│   └── matching_cache (AI results cache)
├── 🛡️ Security & Audit Tables (3)
│   ├── audit_logs (Security tracking)
│   ├── rate_limits (API rate limiting)
│   └── csp_violations (Security policy)
├── 🧠 Phase 3 Learning Engine (1)
│   └── company_scoring_preferences
└── 📈 System Tables (1)
    └── schema_version (Version tracking)
```

### Key Relationships
```sql
-- Primary relationships to explore
candidates ←→ feedback (candidate_id)
candidates ←→ interviews (candidate_id)
candidates ←→ offers (candidate_id)
jobs ←→ feedback (job_id)
jobs ←→ interviews (job_id)
jobs ←→ offers (job_id)
clients ←→ jobs (client_id)
```

---

## 📊 Essential Queries for Data Exploration

### 1. Schema Verification
```sql
-- Check schema version
SELECT * FROM schema_version ORDER BY applied_at DESC;

-- Count all tables
SELECT schemaname, tablename, tableowner 
FROM pg_tables 
WHERE schemaname = 'public' 
ORDER BY tablename;

-- Table sizes
SELECT 
    schemaname,
    tablename,
    attname,
    n_distinct,
    correlation
FROM pg_stats 
WHERE schemaname = 'public'
ORDER BY tablename, attname;
```

### 2. Data Overview
```sql
-- Quick data counts
SELECT 
    'candidates' as table_name, COUNT(*) as record_count FROM candidates
UNION ALL
SELECT 'jobs', COUNT(*) FROM jobs
UNION ALL
SELECT 'feedback', COUNT(*) FROM feedback
UNION ALL
SELECT 'interviews', COUNT(*) FROM interviews
UNION ALL
SELECT 'offers', COUNT(*) FROM offers
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'clients', COUNT(*) FROM clients;
```

### 3. Sample Data Exploration
```sql
-- Recent candidates with scores
SELECT 
    c.id,
    c.name,
    c.email,
    c.location,
    c.experience_years,
    c.average_score,
    c.status,
    c.created_at
FROM candidates c
ORDER BY c.created_at DESC
LIMIT 10;

-- Active jobs with client info
SELECT 
    j.id,
    j.title,
    j.department,
    j.location,
    j.experience_level,
    c.company_name,
    j.status,
    j.created_at
FROM jobs j
LEFT JOIN clients c ON j.client_id = c.client_id
WHERE j.status = 'active'
ORDER BY j.created_at DESC;
```

### 4. Performance Analysis
```sql
-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_scan,
    idx_tup_read,
    idx_tup_fetch
FROM pg_stat_user_indexes
WHERE schemaname = 'public'
ORDER BY idx_scan DESC;

-- Table activity
SELECT 
    schemaname,
    tablename,
    n_tup_ins,
    n_tup_upd,
    n_tup_del,
    n_live_tup,
    n_dead_tup
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC;
```

---

## 🎯 DBeaver Workspace Setup

### 1. Create Project Structure
```
DBeaver Projects:
├── 📁 BHIV-HR-Platform
│   ├── 🔵 Local Development
│   │   ├── 📊 Core Tables
│   │   ├── 🔐 Security Tables
│   │   ├── 🤖 AI Tables
│   │   └── 📝 Custom Queries
│   └── 🔴 Production (Render)
│       ├── 📊 Core Tables
│       ├── 🔐 Security Tables
│       ├── 🤖 AI Tables
│       └── 📈 Monitoring Queries
```

### 2. Bookmark Important Queries
1. **Right-click** on connection
2. **Select** "SQL Editor" → "New SQL Script"
3. **Save** queries with descriptive names:
   - `schema_overview.sql`
   - `data_counts.sql`
   - `performance_check.sql`
   - `recent_activity.sql`

### 3. Configure Data Viewer
```
Preferences → Data Viewer:
├── Result Sets
│   ├── Max rows: 1000
│   ├── Auto-fetch next segment: ☑
│   └── Show row numbers: ☑
├── Data Formatting
│   ├── Date format: yyyy-MM-dd HH:mm:ss
│   ├── Number format: #,##0.00
│   └── Boolean format: true/false
└── Data Editor
    ├── Auto-save: ☑
    └── Confirm data changes: ☑
```

---

## 🔧 Troubleshooting

### Common Connection Issues

#### 1. Local Database Not Accessible
```bash
# Check if Docker is running
docker ps

# Start database service
cd c:\BHIV-HR-Platform
docker-compose -f deployment\docker\docker-compose.production.yml up -d db

# Check database logs
docker logs bhiv-hr-platform-db-1
```

#### 2. Production SSL Connection Errors
```
Error: SSL connection required
Solution: Configure SSL in DBeaver connection settings
- Click SSL tab (next to Driver properties)
- SSL mode: require (from dropdown)
- SSL Factory: org.postgresql.ssl.DefaultJavaSSLFactory
- Leave certificate fields empty
```

#### 3. Authentication Failed
```
Error: password authentication failed
Solution: Verify credentials
- Local: bhiv_user / bhiv_local_password_2025
- Production: bhiv_user / 3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2
```

#### 4. Connection Timeout
```
Error: Connection timeout
Solution: Increase timeout values
- Driver properties → connectTimeout: 30
- Driver properties → socketTimeout: 30
```

### Performance Optimization

#### 1. Connection Pool Settings
```
Driver Properties:
├── maxConnections: 5
├── connectionTimeout: 30000
├── idleTimeout: 600000
└── maxLifetime: 1800000
```

#### 2. Query Optimization
```sql
-- Use LIMIT for large tables
SELECT * FROM candidates LIMIT 100;

-- Use indexes for filtering
SELECT * FROM candidates WHERE email = 'specific@email.com';

-- Avoid SELECT * on large tables
SELECT id, name, email FROM candidates;
```

---

## 📈 Monitoring and Maintenance

### 1. Database Health Checks
```sql
-- Connection count
SELECT count(*) as active_connections 
FROM pg_stat_activity 
WHERE state = 'active';

-- Database size
SELECT 
    pg_database.datname,
    pg_size_pretty(pg_database_size(pg_database.datname)) AS size
FROM pg_database
WHERE datname = 'bhiv_hr' OR datname = 'bhiv_hr_jcuu';

-- Table sizes
SELECT 
    tablename,
    pg_size_pretty(pg_total_relation_size(tablename::regclass)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(tablename::regclass) DESC;
```

### 2. Performance Monitoring
```sql
-- Slow queries (if pg_stat_statements enabled)
SELECT 
    query,
    calls,
    total_time,
    mean_time,
    rows
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Lock monitoring
SELECT 
    blocked_locks.pid AS blocked_pid,
    blocked_activity.usename AS blocked_user,
    blocking_locks.pid AS blocking_pid,
    blocking_activity.usename AS blocking_user,
    blocked_activity.query AS blocked_statement,
    blocking_activity.query AS current_statement_in_blocking_process
FROM pg_catalog.pg_locks blocked_locks
JOIN pg_catalog.pg_stat_activity blocked_activity ON blocked_activity.pid = blocked_locks.pid
JOIN pg_catalog.pg_locks blocking_locks ON blocking_locks.locktype = blocked_locks.locktype
JOIN pg_catalog.pg_stat_activity blocking_activity ON blocking_activity.pid = blocking_locks.pid
WHERE NOT blocked_locks.granted;
```

---

## 🎨 Visual Data Exploration

### 1. Entity Relationship Diagram
1. **Right-click** on database
2. **Select** "View Diagram"
3. **Drag tables** to canvas
4. **DBeaver will auto-detect** foreign key relationships

### 2. Data Export Options
```
Export Formats:
├── 📊 Excel (.xlsx)
├── 📄 CSV (.csv)
├── 🗄️ SQL Insert Statements
├── 📋 JSON (.json)
└── 📈 HTML Report
```

### 3. Custom Dashboards
```sql
-- Create views for common queries
CREATE VIEW candidate_summary AS
SELECT 
    c.id,
    c.name,
    c.email,
    c.location,
    c.experience_years,
    c.average_score,
    COUNT(f.id) as feedback_count,
    COUNT(i.id) as interview_count,
    COUNT(o.id) as offer_count
FROM candidates c
LEFT JOIN feedback f ON c.id = f.candidate_id
LEFT JOIN interviews i ON c.id = i.candidate_id
LEFT JOIN offers o ON c.id = o.candidate_id
GROUP BY c.id, c.name, c.email, c.location, c.experience_years, c.average_score;
```

---

## 🔐 Security Best Practices

### 1. Connection Security
- ✅ Configure SSL for production connections (SSL tab → SSL mode: require)
- ✅ Store credentials securely in DBeaver
- ✅ Enable connection encryption via SSL settings
- ✅ Use read-only users when possible

### 2. Query Safety
- ✅ Always use LIMIT for exploratory queries
- ✅ Avoid running UPDATE/DELETE without WHERE
- ✅ Test queries on local before production
- ✅ Use transactions for data modifications

### 3. Access Control
```sql
-- Create read-only user for analysis
CREATE USER analyst WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE bhiv_hr TO analyst;
GRANT USAGE ON SCHEMA public TO analyst;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst;
```

---

## 📚 Additional Resources

### Documentation Links
- **[Project Structure](../../PROJECT_STRUCTURE.md)** - Complete architecture
- **[Database Schema](../../services/db/consolidated_schema.sql)** - Full schema
- **[API Documentation](../api/API_DOCUMENTATION.md)** - API endpoints
- **[Deployment Guide](../deployment/RENDER_DEPLOYMENT_GUIDE.md)** - Production setup

### Quick Reference
```bash
# Local database URL
postgresql://bhiv_user:bhiv_local_password_2025@localhost:5432/bhiv_hr

# Production database URL  
postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com:5432/bhiv_hr_jcuu

# Health check endpoints
curl http://localhost:8000/health                    # Local gateway
curl https://bhiv-hr-gateway-46pz.onrender.com/health # Production gateway
```

---

## ✅ Setup Verification Checklist

### Local Connection ✅
- [ ] DBeaver installed and running
- [ ] Docker containers started
- [ ] Local connection created and tested
- [ ] Can view all 17 tables
- [ ] Sample queries execute successfully
- [ ] Schema version shows v4.1.0

### Production Connection ✅
- [ ] Production connection created with SSL
- [ ] Connection test successful
- [ ] Can access production data
- [ ] Read-only access confirmed
- [ ] Performance queries working
- [ ] Monitoring queries functional

### Data Exploration ✅
- [ ] Entity relationships visible
- [ ] Sample data queries working
- [ ] Export functionality tested
- [ ] Custom views created
- [ ] Bookmarks organized
- [ ] Performance monitoring active

---

**BHIV HR Platform Database Setup Complete** 🎉

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*

**Last Updated**: October 14, 2025 | **Schema Version**: v4.1.0 | **Tables**: 17 | **Status**: ✅ Production Ready