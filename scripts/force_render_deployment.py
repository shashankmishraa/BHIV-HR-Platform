#!/usr/bin/env python3
"""
Force Render deployment by creating a deployment trigger
"""

import os
import subprocess
import sys
from datetime import datetime

def main():
    print("BHIV HR Platform - Force Deployment Script")
    print("=" * 50)
    
    # Check if we're in a git repository
    try:
        result = subprocess.run(['git', 'status'], capture_output=True, text=True, cwd='c:\\bhiv hr ai platform')
        if result.returncode != 0:
            print("ERROR: Not in a git repository or git not available")
            return False
    except Exception as e:
        print(f"ERROR: Git not available: {e}")
        return False
    
    print("1. Checking current git status...")
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True, cwd='c:\\bhiv hr ai platform')
    if result.stdout.strip():
        print("   Found uncommitted changes:")
        print(result.stdout)
        
        print("2. Adding all changes...")
        subprocess.run(['git', 'add', '.'], cwd='c:\\bhiv hr ai platform')
        
        print("3. Committing changes...")
        commit_msg = f"Fix endpoints and deployment issues - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], cwd='c:\\bhiv hr ai platform')
    else:
        print("   No uncommitted changes found")
    
    print("4. Pushing to trigger deployment...")
    result = subprocess.run(['git', 'push'], capture_output=True, text=True, cwd='c:\\bhiv hr ai platform')
    
    if result.returncode == 0:
        print("   ✓ Successfully pushed to repository")
        print("   → This should trigger automatic deployment on Render")
        print("\n5. Monitoring deployment...")
        print("   Check Render dashboard for deployment progress")
        print("   URL: https://dashboard.render.com/")
        return True
    else:
        print(f"   ✗ Push failed: {result.stderr}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✓ Deployment trigger sent successfully")
        print("Wait 2-3 minutes for deployment to complete, then test endpoints")
    else:
        print("\n✗ Failed to trigger deployment")
    sys.exit(0 if success else 1)