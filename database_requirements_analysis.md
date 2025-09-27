# Database Requirements Analysis - UI Portal Functionalities

Based on the comprehensive scan of HR Portal and Client Portal components, here are the required database tables:

## Current Database Status
✅ **Existing Tables**: candidates, jobs, interviews, feedback
❌ **Missing Tables**: clients, users, sessions, audit_logs, notifications

## Required Database Tables Analysis

### 1. **Core HR Tables** (✅ Existing)

#### `candidates` - ✅ Complete
- **Purpose**: Store candidate information and profiles
- **UI Components**: Candidate upload, search, AI matching, values assessment
- **Fields**: id, name, email, phone, location, technical_skills, experience_years, seniority_level, education_level, resume_path, status, created_at, updated_at

#### `jobs` - ✅ Complete  
- **Purpose**: Store job postings from clients
- **UI Components**: Job creation, job monitoring, candidate matching
- **Fields**: id, title, department, location, experience_level, requirements, description, client_id, employment_type, status, created_at, updated_at

#### `interviews` - ✅ Structure Complete (Empty)
- **Purpose**: Schedule and track interviews
- **UI Components**: Interview management, scheduling
- **Fields**: id, candidate_id, job_id, interview_date, interviewer, status, notes, created_at, updated_at

#### `feedback` - ✅ Structure Complete (Empty)
- **Purpose**: Store values-based assessments
- **UI Components**: Values assessment form
- **Fields**: id, candidate_id, job_id, integrity, honesty, discipline, hard_work, gratitude, comments, created_at, updated_at

### 2. **Missing Critical Tables** (❌ Required)

#### `clients` - ❌ Missing
```sql
CREATE TABLE clients (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(50) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```
- **Purpose**: Client authentication and company management
- **UI Components**: Client portal login, registration, job posting
- **Required for**: Client authentication, job ownership tracking

#### `users` - ❌ Missing  
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'hr_user',
    full_name VARCHAR(255),
    status VARCHAR(50) DEFAULT 'active',
    last_login TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```
- **Purpose**: HR portal user management
- **UI Components**: HR portal authentication, user sessions
- **Required for**: HR user authentication, role-based access

#### `sessions` - ❌ Missing
```sql
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    user_id INTEGER,
    client_id INTEGER,
    user_type VARCHAR(50) NOT NULL, -- 'hr_user' or 'client'
    token_hash VARCHAR(255),
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (client_id) REFERENCES clients(id) ON DELETE CASCADE
);
```
- **Purpose**: Session management and JWT token tracking
- **UI Components**: Login persistence, secure logout
- **Required for**: Session security, token validation

### 3. **Enhanced Tables** (⚠️ Needs Extension)

#### `job_applications` - ❌ Missing
```sql
CREATE TABLE job_applications (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER NOT NULL,
    job_id INTEGER NOT NULL,
    status VARCHAR(50) DEFAULT 'applied',
    ai_score DECIMAL(5,2),
    applied_at TIMESTAMP DEFAULT NOW(),
    reviewed_at TIMESTAMP,
    reviewer_id INTEGER,
    notes TEXT,
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    FOREIGN KEY (reviewer_id) REFERENCES users(id)
);
```
- **Purpose**: Track candidate applications and AI matching results
- **UI Components**: Candidate review, match results, application pipeline
- **Required for**: Application tracking, AI score storage

#### `audit_logs` - ❌ Missing
```sql
CREATE TABLE audit_logs (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    client_id INTEGER,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id INTEGER,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (client_id) REFERENCES clients(id)
);
```
- **Purpose**: Security auditing and activity tracking
- **UI Components**: All portal activities
- **Required for**: Security compliance, activity monitoring

### 4. **Optional Enhancement Tables**

#### `notifications` - ❌ Missing
```sql
CREATE TABLE notifications (
    id SERIAL PRIMARY KEY,
    recipient_type VARCHAR(20) NOT NULL, -- 'user' or 'client'
    recipient_id INTEGER NOT NULL,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    read_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);
```
- **Purpose**: System notifications and alerts
- **UI Components**: Dashboard notifications, real-time updates

#### `file_uploads` - ❌ Missing
```sql
CREATE TABLE file_uploads (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER,
    filename VARCHAR(255) NOT NULL,
    original_filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size INTEGER,
    mime_type VARCHAR(100),
    uploaded_by INTEGER,
    created_at TIMESTAMP DEFAULT NOW(),
    FOREIGN KEY (candidate_id) REFERENCES candidates(id) ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by) REFERENCES users(id)
);
```
- **Purpose**: Resume and document management
- **UI Components**: Batch upload, candidate upload, file management

## Priority Implementation Order

### **Priority 1 - Critical (Immediate)**
1. `clients` - Required for client portal functionality
2. `users` - Required for HR portal authentication  
3. `sessions` - Required for secure authentication
4. `job_applications` - Required for application tracking

### **Priority 2 - Important (Next Sprint)**
1. `audit_logs` - Required for security compliance
2. `notifications` - Enhances user experience
3. `file_uploads` - Improves file management

### **Priority 3 - Enhancement (Future)**
1. Additional indexes for performance
2. Materialized views for analytics
3. Partitioning for large datasets

## Database Schema Gaps Impact

### **Current Limitations**:
- ❌ No client authentication (hardcoded fallbacks)
- ❌ No HR user management
- ❌ No session persistence
- ❌ No application tracking
- ❌ No audit trail
- ❌ No file management

### **Functional Impact**:
- Client portal uses hardcoded authentication
- HR portal lacks user management
- No persistent sessions across restarts
- AI matching results not stored
- No security audit trail
- Resume uploads not tracked in database

## Recommended Next Steps

1. **Create missing core tables** (clients, users, sessions, job_applications)
2. **Update existing API endpoints** to use new tables
3. **Implement proper authentication** flows
4. **Add audit logging** throughout the application
5. **Test end-to-end workflows** with complete database schema

This analysis shows the database is 40% complete - core HR functionality exists but authentication, session management, and application tracking are missing.