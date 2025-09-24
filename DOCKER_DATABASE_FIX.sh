#!/bin/bash
# BHIV HR Platform - Docker Database Fix
# Fixes missing tables and connection pooling issues

echo "🔧 Fixing Docker Database Issues..."

# 1. Stop containers and remove volumes
echo "1️⃣ Stopping containers..."
docker-compose -f docker-compose.production.yml down -v

# 2. Update database init script
echo "2️⃣ Updating database schema..."
cat > services/db/init_complete.sql << 'EOF'
-- BHIV HR Platform - Fixed Database Schema
\c bhiv_hr_nqzb;

-- Create missing tables
CREATE TABLE IF NOT EXISTS candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE,
    phone VARCHAR(50),
    location VARCHAR(255),
    experience_years INTEGER DEFAULT 0,
    technical_skills TEXT,
    seniority_level VARCHAR(100),
    education_level VARCHAR(255),
    resume_path VARCHAR(500),
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    department VARCHAR(255),
    location VARCHAR(255),
    experience_level VARCHAR(100),
    requirements TEXT,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    client_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS interviews (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    interview_date TIMESTAMP,
    status VARCHAR(50) DEFAULT 'scheduled',
    notes TEXT,
    interviewer VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    candidate_id INTEGER REFERENCES candidates(id),
    job_id INTEGER REFERENCES jobs(id),
    integrity INTEGER CHECK (integrity >= 1 AND integrity <= 5),
    honesty INTEGER CHECK (honesty >= 1 AND honesty <= 5),
    discipline INTEGER CHECK (discipline >= 1 AND discipline <= 5),
    hard_work INTEGER CHECK (hard_work >= 1 AND hard_work <= 5),
    gratitude INTEGER CHECK (gratitude >= 1 AND gratitude <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS client_auth (
    id SERIAL PRIMARY KEY,
    client_id VARCHAR(100) UNIQUE NOT NULL,
    company_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Grant permissions
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO bhiv_user;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO bhiv_user;

-- Insert sample data
INSERT INTO candidates (name, email, technical_skills, experience_years) VALUES
('John Doe', 'john@example.com', 'Python, FastAPI', 5),
('Jane Smith', 'jane@example.com', 'JavaScript, React', 3)
ON CONFLICT (email) DO NOTHING;

INSERT INTO jobs (title, department, location, experience_level, requirements, description) VALUES
('Python Developer', 'Engineering', 'Remote', 'Senior', 'Python, FastAPI', 'Senior Python developer position'),
('Frontend Developer', 'Engineering', 'Remote', 'Mid-Level', 'React, JavaScript', 'Frontend developer position')
ON CONFLICT DO NOTHING;

INSERT INTO client_auth (client_id, company_name, email, password_hash) VALUES
('TECH001', 'Tech Solutions', 'admin@tech.com', '$2b$12$hash')
ON CONFLICT (client_id) DO NOTHING;
EOF

# 3. Fix database connection in gateway
echo "3️⃣ Fixing database connection..."
cat > services/gateway/app/database_connection_fix.py << 'EOF'
import os
from sqlalchemy import create_engine, text
from sqlalchemy.pool import QueuePool

def get_fixed_db_engine():
    """Fixed database engine with proper connection pooling"""
    environment = os.getenv("ENVIRONMENT", "development")
    
    if environment == "production":
        db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb"
    else:
        db_url = "postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@db:5432/bhiv_hr_nqzb"
    
    return create_engine(
        db_url,
        poolclass=QueuePool,
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
        pool_recycle=3600
    )

def test_connection():
    """Test database connection"""
    try:
        engine = get_fixed_db_engine()
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False
EOF

# 4. Start containers
echo "4️⃣ Starting containers..."
docker-compose -f docker-compose.production.yml up --build -d

# 5. Wait for services to start
echo "5️⃣ Waiting for services..."
sleep 30

# 6. Test connection
echo "6️⃣ Testing connection..."
python3 -c "
import sys
sys.path.append('services/gateway/app')
from database_connection_fix import test_connection
if test_connection():
    print('✅ Docker database fix successful')
    exit(0)
else:
    print('❌ Docker database fix failed')
    exit(1)
"

echo "🎯 Docker database fix complete!"