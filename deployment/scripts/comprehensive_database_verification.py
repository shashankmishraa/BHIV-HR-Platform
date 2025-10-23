#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Database Deployment Verification
Checks all live services and their database connections in depth
"""

import psycopg2
import requests
import json
import logging
from datetime import datetime

# Configure logging without unicode issues
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('database_verification.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# Database and Service Configuration
DATABASE_URL = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

SERVICES = {
    "Gateway": "https://bhiv-hr-gateway-46pz.onrender.com",
    "Agent": "https://bhiv-hr-agent-m1me.onrender.com",
    "HR Portal": "https://bhiv-hr-portal-cead.onrender.com",
    "Client Portal": "https://bhiv-hr-client-portal-5g33.onrender.com",
    "Candidate Portal": "https://bhiv-hr-candidate-portal.onrender.com"
}

def verify_database_connection():
    """Verify direct database connection and schema"""
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        logger.info("=== DATABASE CONNECTION VERIFICATION ===")
        
        # Check database version
        cursor.execute("SELECT version();")
        db_version = cursor.fetchone()[0]
        logger.info(f"Database Version: {db_version[:50]}...")
        
        # Check schema version
        cursor.execute("SELECT version, applied_at FROM schema_version ORDER BY applied_at DESC LIMIT 1;")
        schema_info = cursor.fetchone()
        logger.info(f"Schema Version: {schema_info[0]} (Applied: {schema_info[1]})")
        
        # Check all tables
        cursor.execute("""
            SELECT table_name, table_type 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        logger.info(f"Total Tables: {len(tables)}")
        
        # Core tables verification
        core_tables = [
            'candidates', 'jobs', 'feedback', 'interviews', 'offers',
            'users', 'clients', 'matching_cache', 'audit_logs', 
            'rate_limits', 'csp_violations', 'company_scoring_preferences',
            'schema_version'
        ]
        
        logger.info("=== CORE TABLES STATUS ===")
        for table in core_tables:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table};")
                count = cursor.fetchone()[0]
                logger.info(f"{table}: {count} records")
            except Exception as e:
                logger.error(f"{table}: ERROR - {e}")
        
        # Check indexes
        cursor.execute("""
            SELECT COUNT(*) FROM pg_indexes 
            WHERE schemaname = 'public';
        """)
        index_count = cursor.fetchone()[0]
        logger.info(f"Total Indexes: {index_count}")
        
        # Check constraints
        cursor.execute("""
            SELECT COUNT(*) FROM information_schema.check_constraints 
            WHERE constraint_schema = 'public';
        """)
        constraint_count = cursor.fetchone()[0]
        logger.info(f"Check Constraints: {constraint_count}")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        return False

def verify_gateway_database_endpoints():
    """Verify Gateway service database endpoints"""
    logger.info("=== GATEWAY DATABASE ENDPOINTS ===")
    
    headers = {"Authorization": f"Bearer {API_KEY}"}
    base_url = SERVICES["Gateway"]
    
    endpoints = [
        ("/health", "Health Check"),
        ("/v1/database/schema", "Database Schema"),
        ("/v1/candidates", "Candidates List"),
        ("/v1/jobs", "Jobs List"),
        ("/v1/interviews", "Interviews List"),
        ("/test-candidates", "Test Candidates")
    ]
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/v1/database/schema":
                    logger.info(f"{description}: Schema v{data.get('schema_version')} - {data.get('total_tables')} tables")
                elif endpoint == "/v1/candidates":
                    logger.info(f"{description}: {len(data)} candidates")
                elif endpoint == "/v1/jobs":
                    jobs = data.get('jobs', []) if isinstance(data, dict) else data
                    logger.info(f"{description}: {len(jobs)} jobs")
                elif endpoint == "/test-candidates":
                    logger.info(f"{description}: {data.get('total_candidates', 0)} total candidates")
                else:
                    logger.info(f"{description}: OK")
            else:
                logger.error(f"{description}: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"{description}: {e}")

def verify_agent_database_connection():
    """Verify Agent service database connection"""
    logger.info("=== AGENT DATABASE CONNECTION ===")
    
    base_url = SERVICES["Agent"]
    
    try:
        # Health check
        response = requests.get(f"{base_url}/health", timeout=30)
        if response.status_code == 200:
            logger.info("Agent Health: OK")
        
        # Database test endpoint
        response = requests.get(f"{base_url}/test-db", timeout=30)
        if response.status_code == 200:
            data = response.json()
            logger.info(f"Agent DB Test: {data.get('status', 'Unknown')}")
            if 'candidates_count' in data:
                logger.info(f"Agent sees {data['candidates_count']} candidates")
        
        # Test AI matching (requires database)
        response = requests.post(f"{base_url}/match", 
                               json={"job_id": 1}, 
                               timeout=30)
        if response.status_code == 200:
            data = response.json()
            candidates = data.get('top_candidates', [])
            logger.info(f"AI Matching: {len(candidates)} candidates matched")
        else:
            logger.warning(f"AI Matching: HTTP {response.status_code}")
            
    except Exception as e:
        logger.error(f"Agent verification failed: {e}")

def verify_portal_database_connections():
    """Verify all portal database connections"""
    logger.info("=== PORTAL DATABASE CONNECTIONS ===")
    
    portals = {
        "HR Portal": SERVICES["HR Portal"],
        "Client Portal": SERVICES["Client Portal"], 
        "Candidate Portal": SERVICES["Candidate Portal"]
    }
    
    for portal_name, portal_url in portals.items():
        try:
            # Check if portal is accessible
            response = requests.get(portal_url, timeout=30)
            if response.status_code == 200:
                logger.info(f"{portal_name}: Portal accessible")
                
                # Check if portal can reach Gateway (indirect database test)
                if "streamlit" in response.text.lower():
                    logger.info(f"{portal_name}: Streamlit app running")
                else:
                    logger.warning(f"{portal_name}: May not be Streamlit app")
            else:
                logger.error(f"{portal_name}: HTTP {response.status_code}")
                
        except Exception as e:
            logger.error(f"{portal_name}: {e}")

def test_database_operations():
    """Test database operations that portals use"""
    logger.info("=== DATABASE OPERATIONS TEST ===")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Test queries that portals typically use
        test_queries = [
            ("Active Jobs", "SELECT COUNT(*) FROM jobs WHERE status = 'active';"),
            ("Applied Candidates", "SELECT COUNT(*) FROM candidates WHERE status = 'applied';"),
            ("Active Clients", "SELECT COUNT(*) FROM clients WHERE status = 'active';"),
            ("Scheduled Interviews", "SELECT COUNT(*) FROM interviews WHERE status = 'scheduled';"),
            ("Recent Feedback", "SELECT COUNT(*) FROM feedback WHERE created_at > NOW() - INTERVAL '30 days';"),
            ("Client Authentication", "SELECT client_id, company_name FROM clients WHERE status = 'active' LIMIT 3;"),
            ("Job Titles", "SELECT title, department FROM jobs WHERE status = 'active' LIMIT 5;")
        ]
        
        for description, query in test_queries:
            try:
                cursor.execute(query)
                result = cursor.fetchall()
                if len(result) == 1 and len(result[0]) == 1:
                    logger.info(f"{description}: {result[0][0]}")
                else:
                    logger.info(f"{description}: {len(result)} records")
            except Exception as e:
                logger.error(f"{description}: {e}")
        
        # Test data integrity
        cursor.execute("""
            SELECT 
                c.name, c.email, j.title, j.department
            FROM candidates c
            JOIN jobs j ON j.id = 1
            WHERE c.status = 'applied'
            LIMIT 3;
        """)
        sample_data = cursor.fetchall()
        logger.info(f"Sample Data Integrity: {len(sample_data)} candidate-job combinations")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Database operations test failed: {e}")

def check_portal_specific_database_usage():
    """Check portal-specific database usage patterns"""
    logger.info("=== PORTAL-SPECIFIC DATABASE USAGE ===")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # HR Portal specific queries
        logger.info("HR Portal Database Usage:")
        cursor.execute("SELECT COUNT(*) FROM candidates;")
        logger.info(f"  - Total candidates for dashboard: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'active';")
        logger.info(f"  - Active jobs for management: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT COUNT(*) FROM interviews;")
        logger.info(f"  - Interviews for scheduling: {cursor.fetchone()[0]}")
        
        # Client Portal specific queries
        logger.info("Client Portal Database Usage:")
        cursor.execute("SELECT COUNT(*) FROM clients WHERE status = 'active';")
        logger.info(f"  - Active clients for authentication: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT client_id, COUNT(*) FROM jobs GROUP BY client_id;")
        client_jobs = cursor.fetchall()
        logger.info(f"  - Jobs by client: {len(client_jobs)} clients have jobs")
        
        # Candidate Portal specific queries
        logger.info("Candidate Portal Database Usage:")
        cursor.execute("SELECT COUNT(*) FROM candidates WHERE password_hash IS NOT NULL;")
        logger.info(f"  - Candidates with accounts: {cursor.fetchone()[0]}")
        
        cursor.execute("SELECT status, COUNT(*) FROM candidates GROUP BY status;")
        status_counts = cursor.fetchall()
        logger.info(f"  - Candidate statuses: {len(status_counts)} different statuses")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Portal-specific database check failed: {e}")

def generate_deployment_report():
    """Generate comprehensive deployment report"""
    logger.info("=== DEPLOYMENT VERIFICATION REPORT ===")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "database_status": "Unknown",
        "services_status": {},
        "database_metrics": {},
        "issues_found": []
    }
    
    try:
        # Database metrics
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';")
        report["database_metrics"]["total_tables"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM candidates;")
        report["database_metrics"]["candidates"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM jobs;")
        report["database_metrics"]["jobs"] = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM clients;")
        report["database_metrics"]["clients"] = cursor.fetchone()[0]
        
        report["database_status"] = "Connected"
        cursor.close()
        conn.close()
        
    except Exception as e:
        report["database_status"] = f"Error: {e}"
        report["issues_found"].append(f"Database connection failed: {e}")
    
    # Service status
    for service_name, service_url in SERVICES.items():
        try:
            response = requests.get(f"{service_url}/health" if service_name in ["Gateway", "Agent"] else service_url, timeout=10)
            report["services_status"][service_name] = {
                "status": "OK" if response.status_code == 200 else f"HTTP {response.status_code}",
                "response_time": response.elapsed.total_seconds()
            }
        except Exception as e:
            report["services_status"][service_name] = {
                "status": f"Error: {e}",
                "response_time": None
            }
            report["issues_found"].append(f"{service_name} not accessible: {e}")
    
    # Save report
    with open('deployment_verification_report.json', 'w') as f:
        json.dump(report, f, indent=2, default=str)
    
    logger.info("Report saved to deployment_verification_report.json")
    
    # Summary
    logger.info("=== VERIFICATION SUMMARY ===")
    logger.info(f"Database Status: {report['database_status']}")
    logger.info(f"Total Tables: {report['database_metrics'].get('total_tables', 'Unknown')}")
    logger.info(f"Candidates: {report['database_metrics'].get('candidates', 'Unknown')}")
    logger.info(f"Jobs: {report['database_metrics'].get('jobs', 'Unknown')}")
    logger.info(f"Issues Found: {len(report['issues_found'])}")
    
    for service, status in report["services_status"].items():
        logger.info(f"{service}: {status['status']}")

def main():
    """Main verification function"""
    logger.info("Starting comprehensive database deployment verification...")
    logger.info(f"Timestamp: {datetime.now()}")
    
    # Run all verification steps
    verify_database_connection()
    verify_gateway_database_endpoints()
    verify_agent_database_connection()
    verify_portal_database_connections()
    test_database_operations()
    check_portal_specific_database_usage()
    generate_deployment_report()
    
    logger.info("Comprehensive verification completed!")

if __name__ == "__main__":
    main()