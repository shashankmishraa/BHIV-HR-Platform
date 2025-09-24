#!/usr/bin/env python3
"""Check database schema and identify missing components"""

import asyncpg
import asyncio
import os

async def check_database_schema():
    """Check database schema and identify missing components"""
    try:
        # Connect to database
        conn = await asyncpg.connect(
            'postgresql://bhiv_user:B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J@dpg-d373qrogjchc73bu9gug-a.oregon-postgres.render.com/bhiv_hr_nqzb'
        )
        
        print("=== DATABASE SCHEMA ANALYSIS ===")
        
        # 1. Check existing tables
        tables_query = """
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name;
        """
        tables = await conn.fetch(tables_query)
        existing_tables = [t['table_name'] for t in tables]
        print(f"Existing tables: {existing_tables}")
        
        # 2. Required tables for endpoints
        required_tables = ['candidates', 'jobs', 'interviews', 'feedback', 'client_auth']
        missing_tables = [t for t in required_tables if t not in existing_tables]
        print(f"Missing tables: {missing_tables}")
        
        # 3. Check jobs table structure (most critical for 422 errors)
        if 'jobs' in existing_tables:
            print("\n=== JOBS TABLE ANALYSIS ===")
            columns_query = """
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns 
            WHERE table_name = 'jobs'
            ORDER BY ordinal_position;
            """
            columns = await conn.fetch(columns_query)
            
            existing_columns = [c['column_name'] for c in columns]
            print(f"Existing columns: {existing_columns}")
            
            # Required columns for API validation
            required_columns = [
                'id', 'title', 'description', 'requirements', 'location',
                'department', 'experience_level', 'salary_min', 'salary_max',
                'job_type', 'company_id', 'status', 'created_at'
            ]
            
            missing_columns = [c for c in required_columns if c not in existing_columns]
            print(f"Missing columns: {missing_columns}")
            
            # Check column details
            for col in columns:
                nullable = "NULL" if col['is_nullable'] == 'YES' else "NOT NULL"
                default = f"DEFAULT {col['column_default']}" if col['column_default'] else ""
                print(f"  {col['column_name']}: {col['data_type']} {nullable} {default}")
        
        # 4. Check candidates table structure
        if 'candidates' in existing_tables:
            print("\n=== CANDIDATES TABLE ANALYSIS ===")
            columns_query = """
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns 
            WHERE table_name = 'candidates'
            ORDER BY ordinal_position;
            """
            columns = await conn.fetch(columns_query)
            existing_columns = [c['column_name'] for c in columns]
            print(f"Existing columns: {existing_columns}")
            
            required_columns = ['id', 'name', 'email', 'phone', 'skills', 'experience_years', 'location']
            missing_columns = [c for c in required_columns if c not in existing_columns]
            print(f"Missing columns: {missing_columns}")
        
        # 5. Check data counts
        print("\n=== DATA ANALYSIS ===")
        for table in existing_tables:
            if table in required_tables:
                count_query = f"SELECT COUNT(*) as count FROM {table};"
                result = await conn.fetchrow(count_query)
                print(f"{table}: {result['count']} records")
        
        # 6. Test a sample query that might be failing
        print("\n=== ENDPOINT SIMULATION ===")
        try:
            # Simulate job creation validation
            test_job = {
                'title': 'Test Job',
                'description': 'Test Description',
                'requirements': ['Python'],
                'location': 'Remote',
                'department': 'Engineering',
                'experience_level': 'Mid-level',
                'salary_min': 100000,
                'salary_max': 150000
            }
            
            # Check if we can insert this (without actually inserting)
            if 'jobs' in existing_tables:
                insert_query = """
                SELECT column_name FROM information_schema.columns 
                WHERE table_name = 'jobs' AND column_name = ANY($1);
                """
                test_columns = list(test_job.keys())
                available_columns = await conn.fetch(insert_query, test_columns)
                available_column_names = [c['column_name'] for c in available_columns]
                
                print(f"Test job fields: {test_columns}")
                print(f"Available in DB: {available_column_names}")
                missing_in_db = [c for c in test_columns if c not in available_column_names]
                print(f"Missing in DB: {missing_in_db}")
        
        except Exception as e:
            print(f"Endpoint simulation error: {e}")
        
        await conn.close()
        
    except Exception as e:
        print(f"Database connection error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    asyncio.run(check_database_schema())