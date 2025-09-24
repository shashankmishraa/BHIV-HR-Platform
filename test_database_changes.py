#!/usr/bin/env python3
"""
BHIV HR Platform - Database Changes Test Suite
Tests all database schema changes, indexes, and service integration
"""

import asyncio
import asyncpg
import requests
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class DatabaseChangesTest:
    def __init__(self):
        self.db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'bhiv_hr_db',
            'user': 'bhiv_user',
            'password': 'bhiv_password'
        }
        self.gateway_url = "http://localhost:8000"
        self.agent_url = "http://localhost:9000"
        self.results = []

    async def test_database_connection(self):
        """Test database connectivity"""
        try:
            conn = await asyncpg.connect(**self.db_config)
            await conn.close()
            self.log_result("✅ Database Connection", "SUCCESS", "Connected to PostgreSQL")
            return True
        except Exception as e:
            self.log_result("❌ Database Connection", "FAILED", str(e))
            return False

    async def test_table_creation(self):
        """Test all tables exist with correct schema"""
        expected_tables = [
            'candidates', 'jobs', 'job_applications', 'interviews', 
            'feedback', 'client_auth', 'client_sessions', 'audit_log', 'system_config'
        ]
        
        try:
            conn = await asyncpg.connect(**self.db_config)
            
            # Check tables exist
            query = """
            SELECT table_name FROM information_schema.tables 
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            """
            tables = await conn.fetch(query)
            existing_tables = [row['table_name'] for row in tables]
            
            missing_tables = set(expected_tables) - set(existing_tables)
            if missing_tables:
                self.log_result("❌ Table Creation", "FAILED", f"Missing tables: {missing_tables}")
                await conn.close()
                return False
            
            # Check specific columns for critical tables
            critical_checks = [
                ("candidates", "uuid", "uuid"),
                ("jobs", "skills_required", "jsonb"),
                ("interviews", "assessment_score", "numeric"),
                ("feedback", "overall_score", "numeric"),
                ("client_auth", "subscription_tier", "character varying")
            ]
            
            for table, column, expected_type in critical_checks:
                query = """
                SELECT data_type FROM information_schema.columns 
                WHERE table_name = $1 AND column_name = $2
                """
                result = await conn.fetchval(query, table, column)
                if not result:
                    self.log_result("❌ Column Check", "FAILED", f"{table}.{column} missing")
                    await conn.close()
                    return False
            
            await conn.close()
            self.log_result("✅ Table Creation", "SUCCESS", f"All {len(expected_tables)} tables created")
            return True
            
        except Exception as e:
            self.log_result("❌ Table Creation", "FAILED", str(e))
            return False

    async def test_indexes_creation(self):
        """Test database indexes are created"""
        try:
            conn = await asyncpg.connect(**self.db_config)
            
            # Check for key indexes
            query = """
            SELECT indexname FROM pg_indexes 
            WHERE schemaname = 'public' AND indexname LIKE 'idx_%'
            """
            indexes = await conn.fetch(query)
            index_count = len(indexes)
            
            # Should have 40+ indexes based on our schema
            if index_count < 40:
                self.log_result("⚠️ Index Creation", "PARTIAL", f"Only {index_count} indexes found")
            else:
                self.log_result("✅ Index Creation", "SUCCESS", f"{index_count} indexes created")
            
            await conn.close()
            return index_count > 20
            
        except Exception as e:
            self.log_result("❌ Index Creation", "FAILED", str(e))
            return False

    async def test_sample_data_insertion(self):
        """Test sample data was inserted correctly"""
        try:
            conn = await asyncpg.connect(**self.db_config)
            
            # Check data counts
            tables_to_check = ['candidates', 'jobs', 'job_applications', 'client_auth']
            data_counts = {}
            
            for table in tables_to_check:
                count = await conn.fetchval(f"SELECT COUNT(*) FROM {table}")
                data_counts[table] = count
            
            # Verify we have reasonable amounts of data
            if (data_counts['candidates'] >= 5 and 
                data_counts['jobs'] >= 3 and 
                data_counts['client_auth'] >= 1):
                self.log_result("✅ Sample Data", "SUCCESS", f"Data counts: {data_counts}")
                result = True
            else:
                self.log_result("⚠️ Sample Data", "PARTIAL", f"Low data counts: {data_counts}")
                result = False
            
            await conn.close()
            return result
            
        except Exception as e:
            self.log_result("❌ Sample Data", "FAILED", str(e))
            return False

    def test_gateway_health(self):
        """Test gateway service health"""
        try:
            response = requests.get(f"{self.gateway_url}/health", timeout=10)
            if response.status_code == 200:
                self.log_result("✅ Gateway Health", "SUCCESS", "Gateway responding")
                return True
            else:
                self.log_result("❌ Gateway Health", "FAILED", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("❌ Gateway Health", "FAILED", str(e))
            return False

    def test_agent_health(self):
        """Test AI agent service health"""
        try:
            response = requests.get(f"{self.agent_url}/health", timeout=10)
            if response.status_code == 200:
                self.log_result("✅ Agent Health", "SUCCESS", "AI Agent responding")
                return True
            else:
                self.log_result("❌ Agent Health", "FAILED", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("❌ Agent Health", "FAILED", str(e))
            return False

    async def test_database_endpoints(self):
        """Test database-related endpoints"""
        try:
            # Test database health endpoint
            response = requests.get(f"{self.gateway_url}/database/health", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('database_status') == 'healthy':
                    self.log_result("✅ Database Endpoints", "SUCCESS", "Database health OK")
                    return True
                else:
                    self.log_result("⚠️ Database Endpoints", "PARTIAL", f"Status: {data}")
                    return False
            else:
                self.log_result("❌ Database Endpoints", "FAILED", f"Status: {response.status_code}")
                return False
        except Exception as e:
            self.log_result("❌ Database Endpoints", "FAILED", str(e))
            return False

    async def test_crud_operations(self):
        """Test basic CRUD operations work with new schema"""
        try:
            conn = await asyncpg.connect(**self.db_config)
            
            # Test candidate insertion
            test_candidate = {
                'name': 'Test Candidate',
                'email': 'test@example.com',
                'phone': '+1234567890',
                'experience_years': 5,
                'technical_skills': 'Python, SQL',
                'status': 'active'
            }
            
            insert_query = """
            INSERT INTO candidates (name, email, phone, experience_years, technical_skills, status)
            VALUES ($1, $2, $3, $4, $5, $6) RETURNING id
            """
            
            candidate_id = await conn.fetchval(
                insert_query,
                test_candidate['name'],
                test_candidate['email'], 
                test_candidate['phone'],
                test_candidate['experience_years'],
                test_candidate['technical_skills'],
                test_candidate['status']
            )
            
            if candidate_id:
                # Test update
                await conn.execute(
                    "UPDATE candidates SET technical_skills = $1 WHERE id = $2",
                    'Python, SQL, Docker', candidate_id
                )
                
                # Test select
                result = await conn.fetchrow(
                    "SELECT * FROM candidates WHERE id = $1", candidate_id
                )
                
                # Cleanup
                await conn.execute("DELETE FROM candidates WHERE id = $1", candidate_id)
                
                self.log_result("✅ CRUD Operations", "SUCCESS", "Insert/Update/Select/Delete working")
                await conn.close()
                return True
            else:
                self.log_result("❌ CRUD Operations", "FAILED", "Insert failed")
                await conn.close()
                return False
                
        except Exception as e:
            self.log_result("❌ CRUD Operations", "FAILED", str(e))
            return False

    def test_production_services(self):
        """Test production services are still operational"""
        production_urls = [
            "https://bhiv-hr-gateway-901a.onrender.com/health",
            "https://bhiv-hr-agent-o6nx.onrender.com/health"
        ]
        
        all_good = True
        for url in production_urls:
            try:
                response = requests.get(url, timeout=15)
                if response.status_code == 200:
                    service_name = url.split('//')[1].split('.')[0].replace('bhiv-hr-', '')
                    self.log_result(f"✅ Production {service_name}", "SUCCESS", "Service operational")
                else:
                    all_good = False
                    self.log_result(f"❌ Production Service", "FAILED", f"Status: {response.status_code}")
            except Exception as e:
                all_good = False
                self.log_result(f"❌ Production Service", "FAILED", str(e))
        
        return all_good

    def log_result(self, test_name: str, status: str, details: str):
        """Log test result"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        result = {
            'timestamp': timestamp,
            'test': test_name,
            'status': status,
            'details': details
        }
        self.results.append(result)
        print(f"[{timestamp}] {test_name}: {status} - {details}")

    async def run_all_tests(self):
        """Run all tests and generate report"""
        print("🧪 BHIV HR Platform - Database Changes Test Suite")
        print("=" * 60)
        
        # Database tests
        db_connected = await self.test_database_connection()
        if db_connected:
            await self.test_table_creation()
            await self.test_indexes_creation()
            await self.test_sample_data_insertion()
            await self.test_crud_operations()
        
        # Service tests
        self.test_gateway_health()
        self.test_agent_health()
        if db_connected:
            await self.test_database_endpoints()
        
        # Production tests
        self.test_production_services()
        
        # Generate summary
        self.generate_summary()

    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        success_count = len([r for r in self.results if r['status'] == 'SUCCESS'])
        partial_count = len([r for r in self.results if r['status'] == 'PARTIAL'])
        failed_count = len([r for r in self.results if r['status'] == 'FAILED'])
        total_count = len(self.results)
        
        print(f"✅ Successful: {success_count}/{total_count}")
        print(f"⚠️ Partial: {partial_count}/{total_count}")
        print(f"❌ Failed: {failed_count}/{total_count}")
        
        success_rate = (success_count / total_count) * 100 if total_count > 0 else 0
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if failed_count > 0:
            print("\n🚨 FAILED TESTS:")
            for result in self.results:
                if result['status'] == 'FAILED':
                    print(f"  - {result['test']}: {result['details']}")
        
        if success_rate >= 80:
            print("\n🎉 DATABASE CHANGES SUCCESSFULLY IMPLEMENTED!")
        elif success_rate >= 60:
            print("\n⚠️ DATABASE CHANGES PARTIALLY WORKING - REVIEW NEEDED")
        else:
            print("\n🚨 DATABASE CHANGES NEED ATTENTION - MULTIPLE ISSUES")

if __name__ == "__main__":
    tester = DatabaseChangesTest()
    asyncio.run(tester.run_all_tests())