#!/usr/bin/env python3
"""
Project Directory Cleanup Analysis
"""

import os

def main():
    """Analyze project files for cleanup"""
    
    print("PROJECT CLEANUP ANALYSIS")
    print("=" * 60)
    
    # Files to KEEP (essential)
    keep_files = [
        'README.md',
        'PROJECT_STRUCTURE.md', 
        'DEPLOYMENT_GUIDE.md',
        'services/',
        'docs/QUICK_START_GUIDE.md',
        'docs/CURRENT_FEATURES.md',
        'tools/comprehensive_resume_extractor.py',
        'tests/test_endpoints.py',
        'docker-compose.production.yml',
        'render.yaml'
    ]
    
    # Files to REMOVE (duplicates/outdated)
    remove_files = [
        'aggressive_endpoint_test.py',
        'comprehensive_endpoint_test.py', 
        'quick_endpoint_test.py',
        'test_fixes.py',
        'test_gateway.py',
        'quick_test.py',
        'run_verification.py',
        'check_deployment.py',
        'check_db_schema.py',
        'simple_db_check.py',
        'endpoint_analysis.py',
        'AGGRESSIVE_TESTING_REPORT.md',
        'DEPLOYMENT_STATUS_LATEST.md',
        'ENDPOINT_FIXES_SUMMARY.md',
        'FIXES_RESOLUTION_REPORT.md',
        'POST_DEPLOYMENT_ISSUES.md',
        'DATABASE_CONFIG.md',
        'SECURITY_IMPLEMENTATION.md',
        'DB_SCHEMA_ANALYSIS.md',
        'ENDPOINT_ANALYSIS_REPORT.md',
        '.env',
        '.env.render',
        '.env.security',
        'test_requirements.txt'
    ]
    
    # Files to UPDATE
    update_files = [
        'DEPLOYMENT_STATUS.md',
        'docs/TECHNICAL_RESOLUTIONS.md',
        'docs/SECURITY_AUDIT.md'
    ]
    
    print("KEEP (Essential Files)")
    print("-" * 40)
    for file in keep_files:
        print(f"KEEP {file}")
    
    print(f"\nREMOVE (Duplicates/Outdated) - {len(remove_files)} files")
    print("-" * 40)
    existing_remove = 0
    for file in remove_files:
        if os.path.exists(file):
            print(f"REMOVE {file}")
            existing_remove += 1
        else:
            print(f"SKIP {file} (not found)")
    
    print(f"\nUPDATE (Needs Revision) - {len(update_files)} files")
    print("-" * 40)
    for file in update_files:
        print(f"UPDATE {file}")
    
    print(f"\nCLEANUP COMMANDS")
    print("-" * 40)
    for file in remove_files:
        if os.path.exists(file):
            print(f'del "{file}"')
    
    print(f"\nSUMMARY")
    print("-" * 40)
    print(f"Files to keep: {len(keep_files)}")
    print(f"Files to remove: {existing_remove}")
    print(f"Files to update: {len(update_files)}")
    print(f"Total cleanup actions: {existing_remove + len(update_files)}")

if __name__ == "__main__":
    main()