#!/usr/bin/env python3

import psycopg2
import os

def remove_duplicate_candidates():
    """Remove duplicate candidates, keeping only the first occurrence of each unique candidate"""
    
    # Database connection
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        database="bhiv_hr",
        user="bhiv_user",
        password="bhiv_pass"
    )
    
    try:
        cursor = conn.cursor()
        
        # Find duplicates and keep only the minimum ID for each unique candidate
        print("Identifying duplicate candidates...")
        
        # Get candidates to keep (minimum ID for each email+phone combination)
        cursor.execute("""
            SELECT MIN(id) as keep_id, email, phone, COUNT(*) as total_count
            FROM candidates 
            GROUP BY email, phone 
            HAVING COUNT(*) > 1
            ORDER BY MIN(id)
        """)
        
        duplicates_info = cursor.fetchall()
        print(f"Found {len(duplicates_info)} sets of duplicates")
        
        total_removed = 0
        
        for keep_id, email, phone, count in duplicates_info:
            # Delete all duplicates except the one with minimum ID
            cursor.execute("""
                DELETE FROM candidates 
                WHERE email = %s AND phone = %s AND id != %s
            """, (email, phone, keep_id))
            
            removed = cursor.rowcount
            total_removed += removed
            print(f"Kept candidate ID {keep_id}, removed {removed} duplicates for {email}")
        
        # Commit the changes
        conn.commit()
        
        # Get final count
        cursor.execute("SELECT COUNT(*) FROM candidates")
        final_count = cursor.fetchone()[0]
        
        print(f"\nCleanup completed!")
        print(f"Removed {total_removed} duplicate candidates")
        print(f"Final candidate count: {final_count}")
        
        return True
        
    except Exception as e:
        print(f"Error removing duplicates: {e}")
        conn.rollback()
        return False
        
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Starting duplicate candidate removal...")
    success = remove_duplicate_candidates()
    
    if success:
        print("Duplicate removal completed successfully!")
    else:
        print("Duplicate removal failed!")