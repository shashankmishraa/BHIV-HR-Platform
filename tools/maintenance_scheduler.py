#!/usr/bin/env python3
"""
BHIV HR Platform - Maintenance Scheduler
Automated repository maintenance and cleanup scheduling
"""

import subprocess
import schedule
import time
from datetime import datetime
from pathlib import Path

class MaintenanceScheduler:
    """Automated maintenance scheduling"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
    
    def daily_cleanup(self):
        """Daily maintenance tasks"""
        print(f"Running daily cleanup: {datetime.now()}")
        subprocess.run(["python", "tools/repo_cleanup.py"], cwd=self.project_root)
    
    def weekly_optimization(self):
        """Weekly optimization tasks"""
        print(f"Running weekly optimization: {datetime.now()}")
        subprocess.run(["python", "tools/data_manager.py"], cwd=self.project_root)
        subprocess.run(["python", "tools/security_audit.py"], cwd=self.project_root)
    
    def setup_schedule(self):
        """Setup maintenance schedule"""
        schedule.every().day.at("02:00").do(self.daily_cleanup)
        schedule.every().sunday.at("03:00").do(self.weekly_optimization)
    
    def run_scheduler(self):
        """Run the maintenance scheduler"""
        self.setup_schedule()
        while True:
            schedule.run_pending()
            time.sleep(3600)  # Check every hour

if __name__ == "__main__":
    scheduler = MaintenanceScheduler()
    scheduler.run_scheduler()