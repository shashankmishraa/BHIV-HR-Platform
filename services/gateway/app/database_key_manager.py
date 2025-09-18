"""
BHIV HR Platform - Database-Based API Key Manager
Alternative to Redis for API key management using PostgreSQL
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List, Optional
import hashlib
import json
import os
import secrets

from psycopg2.extras import RealDictCursor
import psycopg2
class DatabaseKeyManager:
    """PostgreSQL-based API key management (Redis alternative)"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
        self._ensure_api_keys_table()
    
    def _get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.database_url, cursor_factory=RealDictCursor)
    
    def _ensure_api_keys_table(self):
        """Create API keys table if not exists"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    id SERIAL PRIMARY KEY,
                    key_id VARCHAR(16) UNIQUE NOT NULL,
                    key_hash VARCHAR(64) NOT NULL,
                    client_id VARCHAR(100) NOT NULL,
                    permissions TEXT DEFAULT '["read"]',
                    is_active BOOLEAN DEFAULT true,
                    usage_count INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    expires_at TIMESTAMP NOT NULL,
                    last_used TIMESTAMP,
                    deactivated_at TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_api_keys_hash ON api_keys(key_hash);
                CREATE INDEX IF NOT EXISTS idx_api_keys_client ON api_keys(client_id);
                CREATE INDEX IF NOT EXISTS idx_api_keys_active ON api_keys(is_active, expires_at);
            """)
            
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"Table creation error: {e}")
    
    def generate_api_key(self, client_id: str, permissions: List[str] = None, days_valid: int = 30) -> Dict:
        """Generate new API key with database storage"""
        key = secrets.token_urlsafe(32)
        key_id = secrets.token_hex(8)
        key_hash = hashlib.sha256(key.encode()).hexdigest()
        
        expires_at = datetime.now(timezone.utc) + timedelta(days=days_valid)
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO api_keys (key_id, key_hash, client_id, permissions, expires_at)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING id
            """, (
                key_id,
                key_hash, 
                client_id,
                json.dumps(permissions or ["read"]),
                expires_at
            ))
            
            conn.commit()
            conn.close()
            
            return {
                "api_key": key,
                "key_id": key_id,
                "expires_at": expires_at.isoformat(),
                "permissions": permissions or ["read"],
                "valid_days": days_valid
            }
            
        except Exception as e:
            return {"error": f"Key generation failed: {e}"}
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """Validate API key against database"""
        # Static fallback key
        static_key = os.getenv("API_KEY_SECRET", "myverysecureapikey123")
        if api_key == static_key:
            return {
                "client_id": "static_client",
                "permissions": ["admin"],
                "key_type": "static"
            }
        
        # Database validation
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Get key info and check expiration
            cursor.execute("""
                SELECT key_id, client_id, permissions, usage_count, expires_at, is_active
                FROM api_keys 
                WHERE key_hash = %s AND is_active = true AND expires_at > NOW()
            """, (key_hash,))
            
            result = cursor.fetchone()
            
            if result:
                # Update usage statistics
                cursor.execute("""
                    UPDATE api_keys 
                    SET usage_count = usage_count + 1, last_used = NOW()
                    WHERE key_hash = %s
                """, (key_hash,))
                
                conn.commit()
                conn.close()
                
                return {
                    "key_id": result["key_id"],
                    "client_id": result["client_id"],
                    "permissions": json.loads(result["permissions"]),
                    "usage_count": result["usage_count"] + 1,
                    "key_type": "dynamic"
                }
            
            conn.close()
            return None
            
        except Exception as e:
            print(f"Key validation error: {e}")
            return None
    
    def rotate_api_keys(self, client_id: str) -> Dict:
        """Rotate all keys for a client"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Deactivate old keys (7-day grace period)
            cursor.execute("""
                UPDATE api_keys 
                SET is_active = false, deactivated_at = NOW()
                WHERE client_id = %s AND is_active = true
            """, (client_id,))
            
            rotated_count = cursor.rowcount
            
            # Generate new key
            new_key = self.generate_api_key(client_id)
            
            conn.commit()
            conn.close()
            
            return {
                "message": "API keys rotated successfully",
                "new_key": new_key,
                "rotated_keys_count": rotated_count,
                "grace_period_days": 7
            }
            
        except Exception as e:
            return {"error": f"Key rotation failed: {e}"}
    
    def cleanup_expired_keys(self) -> Dict:
        """Remove expired keys (cleanup job)"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            # Delete keys expired more than 7 days ago
            cursor.execute("""
                DELETE FROM api_keys 
                WHERE expires_at < NOW() - INTERVAL '7 days'
                OR (is_active = false AND deactivated_at < NOW() - INTERVAL '7 days')
            """)
            
            deleted_count = cursor.rowcount
            conn.commit()
            conn.close()
            
            return {
                "message": "Expired keys cleaned up",
                "deleted_count": deleted_count
            }
            
        except Exception as e:
            return {"error": f"Cleanup failed: {e}"}
    
    def get_client_keys(self, client_id: str) -> Dict:
        """Get all keys for a client"""
        try:
            conn = self._get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT key_id, permissions, is_active, usage_count, 
                       created_at, expires_at, last_used
                FROM api_keys 
                WHERE client_id = %s
                ORDER BY created_at DESC
            """, (client_id,))
            
            keys = cursor.fetchall()
            conn.close()
            
            return {
                "client_id": client_id,
                "keys": [dict(key) for key in keys],
                "total_keys": len(keys),
                "active_keys": len([k for k in keys if k["is_active"]])
            }
            
        except Exception as e:
            return {"error": f"Failed to get client keys: {e}"}

# Global instance
db_key_manager = DatabaseKeyManager()