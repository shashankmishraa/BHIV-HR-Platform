# 🔗 Database Connection Architecture - BHIV HR Platform

## 📊 Visual Connection Overview

```
🏢 BHIV HR Platform Database Architecture
┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATABASE CONNECTIONS                              │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  🏠 LOCAL DEVELOPMENT                    ☁️  PRODUCTION (RENDER)            │
│  ┌─────────────────────────┐            ┌─────────────────────────────────┐ │
│  │  🐳 Docker Container    │            │  🌐 Render PostgreSQL Service  │ │
│  │  ┌─────────────────────┐│            │  ┌─────────────────────────────┐│ │
│  │  │ PostgreSQL 15       ││            │  │ PostgreSQL 17               ││ │
│  │  │ Host: localhost     ││            │  │ Host: dpg-d3bfmj8dl3ps...   ││ │
│  │  │ Port: 5432          ││            │  │ Port: 5432                  ││ │
│  │  │ DB: bhiv_hr         ││            │  │ DB: bhiv_hr_jcuu            ││ │
│  │  │ User: bhiv_user     ││            │  │ User: bhiv_user             ││ │
│  │  │ SSL: Disabled       ││            │  │ SSL: Required               ││ │
│  │  └─────────────────────┘│            │  └─────────────────────────────┘│ │
│  └─────────────────────────┘            └─────────────────────────────────┘ │
│           │                                           │                     │
│           ▼                                           ▼                     │
│  ┌─────────────────────────┐            ┌─────────────────────────────────┐ │
│  │  🔧 DBeaver Local       │            │  🔧 DBeaver Production          │ │
│  │  Connection Name:       │            │  Connection Name:               │ │
│  │  "BHIV HR - Local Dev"  │            │  "BHIV HR - Production"         │ │
│  │  Color: 🔵 Blue         │            │  Color: 🔴 Red                  │ │
│  └─────────────────────────┘            └─────────────────────────────────┘ │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## 🗄️ Database Schema Structure (v4.1.0)

```
📊 BHIV HR Platform Schema
├── 🏢 Core Business Tables (5)
│   ├── 👥 candidates
│   │   ├── id (SERIAL PRIMARY KEY)
│   │   ├── name, email, phone, location
│   │   ├── experience_years, technical_skills
│   │   ├── average_score (DECIMAL 3,2)
│   │   └── status, created_at, updated_at
│   │
│   ├── 💼 jobs
│   │   ├── id (SERIAL PRIMARY KEY)
│   │   ├── title, department, location
│   │   ├── experience_level, requirements
│   │   ├── client_id (FK to clients)
│   │   └── status, created_at, updated_at
│   │
│   ├── 📝 feedback (Values Assessment)
│   │   ├── id (SERIAL PRIMARY KEY)
│   │   ├── candidate_id (FK), job_id (FK)
│   │   ├── integrity, honesty, discipline
│   │   ├── hard_work, gratitude (1-5 scale)
│   │   └── average_score (GENERATED)
│   │
│   ├── 🎤 interviews
│   │   ├── id (SERIAL PRIMARY KEY)
│   │   ├── candidate_id (FK), job_id (FK)
│   │   ├── interview_date, interviewer
│   │   └── interview_type, status, notes
│   │
│   └── 💰 offers
│       ├── id (SERIAL PRIMARY KEY)
│       ├── candidate_id (FK), job_id (FK)
│       ├── salary, start_date, terms
│       └── status, created_at, updated_at
│
├── 🔐 Authentication & Security (5)
│   ├── 👤 users (Internal HR)
│   │   ├── username, email, password_hash
│   │   ├── totp_secret, is_2fa_enabled
│   │   └── role, status, last_login
│   │
│   ├── 🏢 clients (External Companies)
│   │   ├── client_id, company_name
│   │   ├── password_hash, email, phone
│   │   ├── two_factor_enabled, backup_codes
│   │   └── status, failed_login_attempts
│   │
│   ├── 📋 audit_logs
│   │   ├── user_id, client_id, action
│   │   ├── resource, ip_address, user_agent
│   │   └── success, error_message, details
│   │
│   ├── ⚡ rate_limits
│   │   ├── ip_address, endpoint, user_tier
│   │   ├── request_count, window_start
│   │   └── blocked_until
│   │
│   └── 🛡️ csp_violations
│       ├── violated_directive, blocked_uri
│       ├── document_uri, ip_address
│       └── user_agent, timestamp
│
├── 🤖 AI & Performance (1)
│   └── 💾 matching_cache
│       ├── job_id (FK), candidate_id (FK)
│       ├── match_score, skills_match_score
│       ├── experience_match_score, location_match_score
│       ├── values_alignment_score, algorithm_version
│       └── reasoning, created_at
│
├── 🧠 Phase 3 Learning Engine (1)
│   └── 📊 company_scoring_preferences
│       ├── client_id (FK), scoring_weights (JSONB)
│       ├── avg_satisfaction, feedback_count
│       └── preferred_experience, updated_at
│
└── 📈 System Management (1)
    └── 🏷️ schema_version
        ├── version (PRIMARY KEY)
        ├── applied_at, description
        └── Current: v4.1.0
```

## 🔗 Connection Flow Diagram

```
🔄 Application → Database Connection Flow

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   🖥️ DBeaver    │    │  🐳 Docker/☁️   │    │  🗄️ PostgreSQL  │
│   Client Tool   │────│   Network       │────│   Database      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ Connection      │    │ SSL/TLS         │    │ Authentication  │
│ Configuration   │    │ Encryption      │    │ & Authorization │
│ - Host/Port     │    │ - Local: None   │    │ - Username      │
│ - Database      │    │ - Prod: Required│    │ - Password      │
│ - Credentials   │    │ - Certificates  │    │ - Permissions   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 📋 Connection Parameters Reference

### 🏠 Local Development Connection
```yaml
Connection Type: PostgreSQL
Host: localhost
Port: 5432
Database: bhiv_hr
Username: bhiv_user
Password: bhiv_local_password_2025
SSL Mode: disable
Application Name: DBeaver-BHIV-Local
Connection Timeout: 30 seconds
```

### ☁️ Production Connection (Render)
```yaml
Connection Type: PostgreSQL
Host: dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com
Port: 5432
Database: bhiv_hr_jcuu
Username: bhiv_user
Password: 3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2
SSL Mode: require
SSL Factory: org.postgresql.ssl.DefaultJavaSSLFactory
Application Name: DBeaver-BHIV-Production
Connection Timeout: 30 seconds
Socket Timeout: 30 seconds
```

## 🎯 Key Relationships Visualization

```
🔗 Primary Foreign Key Relationships

candidates (1) ←→ (N) feedback
    │
    ├─ candidate_id → feedback.candidate_id
    ├─ candidate_id → interviews.candidate_id  
    └─ candidate_id → offers.candidate_id

jobs (1) ←→ (N) feedback
    │
    ├─ job_id → feedback.job_id
    ├─ job_id → interviews.job_id
    ├─ job_id → offers.job_id
    └─ job_id → matching_cache.job_id

clients (1) ←→ (N) jobs
    │
    ├─ client_id → jobs.client_id
    └─ client_id → company_scoring_preferences.client_id

users (1) ←→ (N) audit_logs
    │
    └─ user_id → audit_logs.user_id
```

## 🚀 Quick Connection Test Commands

### Local Database Health Check
```bash
# Test Docker container
docker ps | grep postgres

# Test database connection
docker exec -it bhiv-hr-platform-db-1 psql -U bhiv_user -d bhiv_hr -c "SELECT version();"

# Test from application
curl http://localhost:8000/health
```

### Production Database Health Check
```bash
# Test production API
curl https://bhiv-hr-gateway-46pz.onrender.com/health

# Test database schema endpoint
curl -H "Authorization: Bearer prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o" \
     https://bhiv-hr-gateway-46pz.onrender.com/v1/database/schema
```

## 📊 Data Volume Overview

```
📈 Expected Data Volumes (Production)

candidates:     ~100-1000 records
jobs:          ~50-200 records  
feedback:      ~200-2000 records
interviews:    ~100-500 records
offers:        ~50-200 records
users:         ~5-20 records
clients:       ~10-50 records
audit_logs:    ~1000-10000 records
matching_cache: ~5000-50000 records
rate_limits:   ~100-1000 records
```

## 🔧 Performance Optimization

### Index Strategy
```sql
-- High-performance indexes for common queries
CREATE INDEX idx_candidates_email ON candidates(email);           -- Login/search
CREATE INDEX idx_candidates_skills_gin ON candidates USING gin(to_tsvector('english', technical_skills)); -- Full-text search
CREATE INDEX idx_feedback_candidate_job ON feedback(candidate_id, job_id); -- Composite lookup
CREATE INDEX idx_matching_score ON matching_cache(match_score DESC); -- Top matches
CREATE INDEX idx_audit_timestamp ON audit_logs(timestamp DESC);   -- Recent activity
```

### Connection Pool Settings
```yaml
Local Development:
  max_connections: 5
  connection_timeout: 30000ms
  idle_timeout: 600000ms

Production:
  max_connections: 10
  connection_timeout: 30000ms
  idle_timeout: 300000ms
  max_lifetime: 1800000ms
```

---

**Connection Architecture Complete** ✅

*Built with Integrity, Honesty, Discipline, Hard Work & Gratitude*