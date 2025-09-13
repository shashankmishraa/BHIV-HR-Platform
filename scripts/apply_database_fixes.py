#!/usr/bin/env python3
"""
Apply database schema fixes for BHIV HR Platform
Adds missing interviewer column and ensures proper schema
"""

import os
import psycopg2
from sqlalchemy import create_engine, text
import sys

def apply_database_fixes():
    """Apply database schema fixes"""
    print("🔧 Applying database schema fixes...")
    
    # Try different database connection methods
    database_urls = [
        os.getenv("DATABASE_URL"),
        "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr",
        "postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr"
    ]
    
    for db_url in database_urls:
        if not db_url:
            continue
            
        try:
            print(f"  Connecting to database...")
            engine = create_engine(db_url, pool_pre_ping=True)
            
            with engine.connect() as connection:
                print("  ✅ Database connected successfully")
                
                # Check if interviewer column exists
                check_query = text("""
                    SELECT column_name FROM information_schema.columns 
                    WHERE table_name = 'interviews' AND column_name = 'interviewer'
                """)
                result = connection.execute(check_query)
                
                if not result.fetchone():
                    print("  📝 Adding missing interviewer column...")
                    
                    # Add interviewer column
                    alter_query = text("ALTER TABLE interviews ADD COLUMN interviewer VARCHAR(255)")
                    connection.execute(alter_query)
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
                    check_col_query = text(f"""
                        SELECT column_name FROM information_schema.columns 
                        WHERE table_name = 'interviews' AND column_name = '{col_name}'
                    """)
                    result = connection.execute(check_col_query)
                    
                    if not result.fetchone():
                        print(f"  📝 Adding missing {col_name} column...")
                        alter_query = text(f"ALTER TABLE interviews ADD COLUMN {col_name} {col_type}")
                        connection.execute(alter_query)
                        connection.commit()
                        print(f"  ✅ Added {col_name} column")
                
                # Update any existing interviews without interviewer
                update_query = text("UPDATE interviews SET interviewer = 'HR Team' WHERE interviewer IS NULL")
                connection.execute(update_query)
                connection.commit()
                
                # Verify final schema
                verify_query = text("""
                    SELECT column_name, data_type, is_nullable, column_default 
                    FROM information_schema.columns 
                    WHERE table_name = 'interviews' 
                    ORDER BY ordinal_position
                """)
                result = connection.execute(verify_query)
                columns = result.fetchall()
                
                print("  📋 Final interviews table schema:")
                for col in columns:
                    print(f"    - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
                
                print("  ✅ Database schema fixes applied successfully!")
                return True
                
        except Exception as e:
            print(f"  ❌ Database connection failed: {str(e)}")
            continue
    
    print("  ⚠️ Could not connect to any database")
    return False

def main():
    """Main function"""
    print("🔧 BHIV HR Platform - Database Schema Fix")
    print("=" * 50)
    
    success = apply_database_fixes()
    
    if success:
        print("\n🎉 Database fixes applied successfully!")
        print("\nNext steps:")
        print("1. Restart the gateway service")
        print("2. Test interview scheduling functionality")
        print("3. Verify AI agent connectivity")
    else:
        print("\n❌ Database fixes failed!")
        print("\nTroubleshooting:")
        print("1. Check database connectivity")
        print("2. Verify DATABASE_URL environment variable")
        print("3. Ensure database permissions are correct")
        print("4. Run the SQL script manually if needed")

if __name__ == "__main__":
    main()