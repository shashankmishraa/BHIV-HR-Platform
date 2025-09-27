# Database Schemas v4.1.0

**Updated**: January 18, 2025 | **Database**: PostgreSQL 17 | **Status**: ✅ Production Ready

## 🗄️ Schema Management

### **Current Production Database**
- **Host**: dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com
- **Database**: bhiv_hr_jcuu
- **Version**: PostgreSQL 17
- **Status**: ✅ Connected and operational

### **Schema Files**
- **create_database_schema.sql**: Complete database schema
- **Migration scripts**: Version-controlled schema updates
- **Index definitions**: Performance optimization
- **Constraint definitions**: Data integrity rules

### **Core Tables**
```sql
-- Main entities
CREATE TABLE candidates (...);  -- Candidate profiles
CREATE TABLE jobs (...);        -- Job postings
CREATE TABLE interviews (...);  -- Interview management
CREATE TABLE users (...);       -- User accounts
CREATE TABLE sessions (...);    -- Session management
```

### **Schema Validation**
- **Integrity**: Foreign key constraints
- **Performance**: Optimized indexes
- **Security**: Role-based access control
- **Backup**: Automated backup procedures
