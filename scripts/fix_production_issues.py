#!/usr/bin/env python3
"""
BHIV HR Platform - Production Issues Fix Script
Fixes:
1. AI Agent connection issues (service discovery)
2. Database schema issues (missing interviewer column)
"""

import os
import sys
import psycopg2
from sqlalchemy import create_engine, text
import requests
import time

def test_ai_agent_connection():
    """Test AI agent connectivity"""
    print("🔍 Testing AI Agent connectivity...")
    
    agent_urls = [
        "https://bhiv-hr-agent.onrender.com",
        "http://agent:9000",  # Docker fallback
        "http://localhost:9000"  # Local fallback
    ]
    
    for url in agent_urls:
        try:
            print(f"  Testing: {url}")
            response = requests.get(f"{url}/health", timeout=10)
            if response.status_code == 200:
                print(f"  ✅ AI Agent accessible at: {url}")
                return url
            else:
                print(f"  ❌ AI Agent returned {response.status_code}")
        except Exception as e:
            print(f"  ❌ Connection failed: {str(e)}")
    
    print("  ⚠️ AI Agent not accessible from any URL")
    return None

def fix_database_schema():
    """Fix database schema issues"""
    print("🔧 Fixing database schema...")
    
    # Try different database URLs
    database_urls = [
        os.getenv("DATABASE_URL"),
        "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr",
        "postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr"
    ]
    
    for db_url in database_urls:
        if not db_url:
            continue
            
        try:
            print(f"  Connecting to: {db_url[:50]}...")
            engine = create_engine(db_url, pool_pre_ping=True)
            
            with engine.connect() as connection:
                # Check if interviewer column exists
                result = connection.execute(text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'interviews' AND column_name = 'interviewer'
                """))
                
                if not result.fetchone():
                    print("  📝 Adding missing interviewer column...")
                    connection.execute(text("""
                        ALTER TABLE interviews ADD COLUMN interviewer VARCHAR(255)
                    """))
                    connection.commit()
                    print("  ✅ Added interviewer column")
                else:
                    print("  ✅ Interviewer column already exists")
                
                # Ensure other required columns exist
                required_columns = [
                    ("interview_type", "VARCHAR(100)"),
                    ("notes", "TEXT"),
                    ("status", "VARCHAR(50) DEFAULT 'scheduled'"),
                    ("created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
                ]
                
                for col_name, col_type in required_columns:
                    result = connection.execute(text(f"""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name = 'interviews' AND column_name = '{col_name}'
                    """))
                    
                    if not result.fetchone():
                        print(f"  📝 Adding missing {col_name} column...")
                        connection.execute(text(f"""
                            ALTER TABLE interviews ADD COLUMN {col_name} {col_type}
                        """))
                        connection.commit()
                        print(f"  ✅ Added {col_name} column")
                
                # Update any existing interviews without interviewer
                connection.execute(text("""
                    UPDATE interviews SET interviewer = 'HR Team' WHERE interviewer IS NULL
                """))
                connection.commit()
                
                print("  ✅ Database schema fixed successfully")
                return True
                
        except Exception as e:
            print(f"  ❌ Database connection failed: {str(e)}")
            continue
    
    print("  ⚠️ Could not connect to database")
    return False

def test_api_endpoints():
    """Test critical API endpoints"""
    print("🧪 Testing API endpoints...")
    
    gateway_urls = [
        "https://bhiv-hr-gateway.onrender.com",
        "http://gateway:8000",
        "http://localhost:8000"
    ]
    
    api_key = os.getenv("API_KEY_SECRET", "myverysecureapikey123")
    headers = {"Authorization": f"Bearer {api_key}"}
    
    for base_url in gateway_urls:
        try:
            print(f"  Testing Gateway: {base_url}")
            
            # Test health endpoint
            response = requests.get(f"{base_url}/health", timeout=10)
            if response.status_code == 200:
                print(f"  ✅ Gateway health check passed")
                
                # Test protected endpoint
                response = requests.get(f"{base_url}/test-candidates", headers=headers, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    print(f"  ✅ Database connectivity: {data.get('total_candidates', 0)} candidates")
                else:
                    print(f"  ⚠️ Protected endpoint failed: {response.status_code}")
                
                return base_url
            else:
                print(f"  ❌ Gateway returned {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Gateway connection failed: {str(e)}")
    
    print("  ⚠️ No gateway accessible")
    return None

def create_environment_config():
    """Create production environment configuration"""
    print("📝 Creating environment configuration...")
    
    config_content = """# BHIV HR Platform - Production Environment
GATEWAY_URL=https://bhiv-hr-gateway.onrender.com
AGENT_URL=https://bhiv-hr-agent.onrender.com
API_KEY_SECRET=myverysecureapikey123
HR_PORTAL_URL=https://bhiv-hr-portal.onrender.com
CLIENT_PORTAL_URL=https://bhiv-hr-client-portal.onrender.com
"""
    
    config_dir = "config"
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    
    config_file = os.path.join(config_dir, ".env.production")
    with open(config_file, "w") as f:
        f.write(config_content)
    
    print(f"  ✅ Created {config_file}")

def main():
    """Main fix script"""
    print("🚀 BHIV HR Platform - Production Issues Fix")
    print("=" * 50)
    
    # Test current status
    print("\n1. Testing current system status...")
    gateway_url = test_api_endpoints()
    agent_url = test_ai_agent_connection()
    
    # Fix database schema
    print("\n2. Fixing database schema...")
    db_fixed = fix_database_schema()
    
    # Create environment config
    print("\n3. Creating environment configuration...")
    create_environment_config()
    
    # Summary
    print("\n" + "=" * 50)
    print("🎯 Fix Summary:")
    print(f"  Gateway API: {'✅ Working' if gateway_url else '❌ Issues'}")
    print(f"  AI Agent: {'✅ Working' if agent_url else '❌ Issues'}")
    print(f"  Database Schema: {'✅ Fixed' if db_fixed else '❌ Issues'}")
    print(f"  Environment Config: ✅ Created")
    
    if gateway_url and agent_url and db_fixed:
        print("\n🎉 All issues resolved! Platform should work correctly now.")
        print("\nNext steps:")
        print("1. Restart the portal service")
        print("2. Test AI matching functionality")
        print("3. Test interview scheduling")
    else:
        print("\n⚠️ Some issues remain. Check the logs above for details.")
        
        if not agent_url:
            print("\nAI Agent Fix:")
            print("- Ensure AI agent service is running")
            print("- Check network connectivity")
            print("- Verify service URLs in environment")
        
        if not db_fixed:
            print("\nDatabase Fix:")
            print("- Run the SQL migration script manually")
            print("- Check database connectivity")
            print("- Verify database permissions")

if __name__ == "__main__":
    main()