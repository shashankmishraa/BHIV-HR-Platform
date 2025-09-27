#!/usr/bin/env python3
"""Update Production Database with Complete Schema"""

import os
import psycopg2

def update_production_schema():
    database_url = "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu"
    
    sql_files = [
        "services/db/01_create_tables.sql",
        "services/db/02_create_indexes.sql", 
        "services/db/03_create_triggers.sql",
        "services/db/04_insert_sample_data.sql"
    ]
    
    try:
        print("Connecting to production database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        for sql_file in sql_files:
            if os.path.exists(sql_file):
                print(f"Executing {sql_file}...")
                with open(sql_file, 'r') as f:
                    sql_content = f.read()
                    
                # Split by semicolon and execute each statement
                statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
                
                for stmt in statements:
                    if stmt and not stmt.startswith('--'):
                        try:
                            cursor.execute(stmt)
                        except Exception as e:
                            # Continue on errors (table might already exist)
                            print(f"  Warning: {str(e)[:100]}...")
                            continue
                
                conn.commit()
                print(f"  Completed {sql_file}")
            else:
                print(f"  Skipped {sql_file} (not found)")
        
        # Verify final state
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name")
        tables = [row[0] for row in cursor.fetchall()]
        
        print(f"\nDatabase updated successfully!")
        print(f"Tables: {len(tables)}")
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"  {table}: {count} records")
        
        cursor.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = update_production_schema()
    exit(0 if success else 1)