#!/usr/bin/env python3
"""
Database backup and recovery procedures for BHIV HR Platform
"""

import os
import subprocess
import datetime
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseBackup:
    """Database backup and recovery utilities"""
    
    def __init__(self):
        self.db_host = os.getenv('DB_HOST', 'localhost')
        self.db_port = os.getenv('DB_PORT', '5432')
        self.db_name = os.getenv('POSTGRES_DB', 'bhiv_hr')
        self.db_user = os.getenv('POSTGRES_USER', 'bhiv_user')
        self.db_password = os.getenv('POSTGRES_PASSWORD', 'bhiv_pass')
        self.backup_dir = Path('backups')
        self.backup_dir.mkdir(exist_ok=True)
    
    def create_backup(self) -> str:
        """Create database backup"""
        timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = self.backup_dir / f"bhiv_hr_backup_{timestamp}.sql"
        
        try:
            # Set password environment variable
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_password
            
            # Run pg_dump
            cmd = [
                'pg_dump',
                '-h', self.db_host,
                '-p', self.db_port,
                '-U', self.db_user,
                '-d', self.db_name,
                '--no-password',
                '-f', str(backup_file)
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Backup created successfully: {backup_file}")
                return str(backup_file)
            else:
                logger.error(f"Backup failed: {result.stderr}")
                return None
                
        except Exception as e:
            logger.error(f"Backup error: {str(e)}")
            return None
    
    def restore_backup(self, backup_file: str) -> bool:
        """Restore database from backup"""
        try:
            # Set password environment variable
            env = os.environ.copy()
            env['PGPASSWORD'] = self.db_password
            
            # Run psql to restore
            cmd = [
                'psql',
                '-h', self.db_host,
                '-p', self.db_port,
                '-U', self.db_user,
                '-d', self.db_name,
                '--no-password',
                '-f', backup_file
            ]
            
            result = subprocess.run(cmd, env=env, capture_output=True, text=True)
            
            if result.returncode == 0:
                logger.info(f"Database restored successfully from: {backup_file}")
                return True
            else:
                logger.error(f"Restore failed: {result.stderr}")
                return False
                
        except Exception as e:
            logger.error(f"Restore error: {str(e)}")
            return False
    
    def list_backups(self) -> list:
        """List available backups"""
        backups = []
        for backup_file in self.backup_dir.glob("*.sql"):
            stat = backup_file.stat()
            backups.append({
                'file': str(backup_file),
                'size': stat.st_size,
                'created': datetime.datetime.fromtimestamp(stat.st_ctime)
            })
        return sorted(backups, key=lambda x: x['created'], reverse=True)
    
    def cleanup_old_backups(self, keep_days: int = 30):
        """Remove backups older than specified days"""
        cutoff_date = datetime.datetime.now() - datetime.timedelta(days=keep_days)
        
        for backup_file in self.backup_dir.glob("*.sql"):
            stat = backup_file.stat()
            if datetime.datetime.fromtimestamp(stat.st_ctime) < cutoff_date:
                backup_file.unlink()
                logger.info(f"Removed old backup: {backup_file}")

def main():
    """Main backup function"""
    backup_manager = DatabaseBackup()
    
    # Create backup
    backup_file = backup_manager.create_backup()
    if backup_file:
        print(f"Backup created: {backup_file}")
    
    # List backups
    backups = backup_manager.list_backups()
    print(f"Total backups: {len(backups)}")
    
    # Cleanup old backups
    backup_manager.cleanup_old_backups()

if __name__ == "__main__":
    main()