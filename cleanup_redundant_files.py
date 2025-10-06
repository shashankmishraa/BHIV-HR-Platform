#!/usr/bin/env python3
"""
Cleanup redundant files from BHIV HR Platform
Run: python cleanup_redundant_files.py
"""

import os
import shutil

def cleanup_redundant_files():
    redundant_files = [
        # JSON reports
        "codebase_analysis_report.json",
        "comprehensive_analysis_report.json", 
        "final_analysis_report.json",
        "service_audit_report.json",
        "test_report_3a9c011b.json",
        "documentation_update_report.json",
        
        # Duplicate documentation
        "COMPREHENSIVE_DEEP_ANALYSIS_REPORT.md",
        "CORRECTED_VERIFICATION_REPORT.md",
        "FINAL_SYSTEM_ANALYSIS_SUMMARY.md",
        "FINAL_VERIFICATION_SUMMARY.md",
        "COMPREHENSIVE_FEATURE_ANALYSIS.md",
        "COMPREHENSIVE_ROUTING_ANALYSIS.md",
        "COMPREHENSIVE_FILE_STATUS_GUIDE.md",
        
        # Temporary files
        "database_fixes.sql",
        "endpoint_fixes.py",
        "SERVICE_ROUTING_AUDIT.py",
        "simple_routing_audit.py",
        
        # Summary files
        "AUDIT_SUMMARY.md",
        "CLEANUP_OPERATIONS_SUMMARY.md",
        "DEPLOYMENT_OPTIMIZATION_SUMMARY.md",
        "FINAL_CLEANUP_SUMMARY.md",
        "FINAL_UPDATE_SUMMARY.md",
        "UPDATE_SUMMARY.md"
    ]
    
    redundant_folders = [
        "docs/archive"
    ]
    
    deleted_count = 0
    
    # Delete files
    for file in redundant_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Deleted: {file}")
            deleted_count += 1
    
    # Delete folders
    for folder in redundant_folders:
        if os.path.exists(folder):
            shutil.rmtree(folder)
            print(f"🗑️ Deleted folder: {folder}")
            deleted_count += 1
    
    print(f"\n✅ Cleanup complete! Removed {deleted_count} redundant files/folders")
    print("✅ Project is now cleaner and more organized")

if __name__ == "__main__":
    cleanup_redundant_files()