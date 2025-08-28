import os
from sqlalchemy import create_engine, text
import time

def update_database_schema():
    """Update database schema to include enhanced candidate fields"""
    
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            print("Updating candidates table schema...")
            
            # Add enhanced fields to candidates table
            alter_queries = [
                "ALTER TABLE candidates ADD COLUMN IF NOT EXISTS phone VARCHAR(50)",
                "ALTER TABLE candidates ADD COLUMN IF NOT EXISTS location VARCHAR(255)",
                "ALTER TABLE candidates ADD COLUMN IF NOT EXISTS experience_years INTEGER DEFAULT 0",
                "ALTER TABLE candidates ADD COLUMN IF NOT EXISTS education_level VARCHAR(100)",
                "ALTER TABLE candidates ADD COLUMN IF NOT EXISTS technical_skills TEXT",
                "ALTER TABLE candidates ADD COLUMN IF NOT EXISTS seniority_level VARCHAR(50)"
            ]
            
            for query in alter_queries:
                try:
                    connection.execute(text(query))
                    print(f"  ✓ {query.split('ADD COLUMN IF NOT EXISTS')[1].split()[0] if 'ADD COLUMN' in query else 'Query'}")
                except Exception as e:
                    print(f"  ✗ Error: {e}")
            
            connection.commit()
            print("Schema update complete!")
            
            # Verify the updated schema
            result = connection.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name = 'candidates'"))
            columns = [row[0] for row in result]
            print(f"\nUpdated candidates table columns: {', '.join(columns)}")
            
    except Exception as e:
        print(f"Error updating schema: {e}")

def clear_and_reload_candidates():
    """Clear existing candidates and reload with enhanced data"""
    
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as connection:
            # Clear existing candidates
            connection.execute(text("DELETE FROM candidates"))
            connection.commit()
            print("Cleared existing candidates")
            
    except Exception as e:
        print(f"Error clearing candidates: {e}")

if __name__ == "__main__":
    print("Database Schema Update Script")
    print("=" * 40)
    
    # Update schema
    update_database_schema()
    
    # Clear existing data
    clear_and_reload_candidates()
    
    print("\nNow run: python upload_enhanced_candidates.py")