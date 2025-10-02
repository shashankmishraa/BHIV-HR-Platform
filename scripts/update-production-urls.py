#!/usr/bin/env python3
"""
BHIV HR Platform - Production URLs Update Script
Updates all hardcoded URLs across the codebase to match current production deployment
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Tuple

class ProductionURLUpdater:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
        # Current production URLs
        self.production_urls = {
            'gateway': 'https://bhiv-hr-gateway-46pz.onrender.com',
            'agent': 'https://bhiv-hr-agent-m1me.onrender.com',
            'portal': 'https://bhiv-hr-portal-cead.onrender.com',
            'client_portal': 'https://bhiv-hr-client-portal-5g33.onrender.com',
            'database_external': 'postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu'
        }
        
        # Files that need URL updates
        self.files_to_update = [
            'README.md',
            'DEPLOYMENT_STATUS.md',
            'config/render-deployment.yml',
            'environments/production/.env.template',
            'docker-compose.production.yml',
            'POST_OPTIMIZATION_DEPLOYMENT_GUIDE.md',
            'QUICK_START_DEPLOYMENT.md',
            'scripts/production-validation.py'
        ]
    
    def update_file_urls(self, file_path: Path) -> Tuple[bool, List[str]]:
        """Update URLs in a specific file"""
        if not file_path.exists():
            return False, [f"File not found: {file_path}"]
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            changes = []
            
            # Update gateway URLs
            old_patterns = [
                r'https://bhiv-hr-gateway-[a-z0-9]+\.onrender\.com',
                r'bhiv-hr-gateway-[a-z0-9]+\.onrender\.com'
            ]
            for pattern in old_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if match != self.production_urls['gateway'].replace('https://', ''):
                        content = content.replace(match, self.production_urls['gateway'].replace('https://', ''))
                        changes.append(f"Updated gateway URL: {match} -> {self.production_urls['gateway']}")
            
            # Update agent URLs
            old_patterns = [
                r'https://bhiv-hr-agent-[a-z0-9]+\.onrender\.com',
                r'bhiv-hr-agent-[a-z0-9]+\.onrender\.com'
            ]
            for pattern in old_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if match != self.production_urls['agent'].replace('https://', ''):
                        content = content.replace(match, self.production_urls['agent'].replace('https://', ''))
                        changes.append(f"Updated agent URL: {match} -> {self.production_urls['agent']}")
            
            # Update portal URLs
            old_patterns = [
                r'https://bhiv-hr-portal-[a-z0-9]+\.onrender\.com',
                r'bhiv-hr-portal-[a-z0-9]+\.onrender\.com'
            ]
            for pattern in old_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if match != self.production_urls['portal'].replace('https://', ''):
                        content = content.replace(match, self.production_urls['portal'].replace('https://', ''))
                        changes.append(f"Updated portal URL: {match} -> {self.production_urls['portal']}")
            
            # Update client portal URLs
            old_patterns = [
                r'https://bhiv-hr-client-portal-[a-z0-9]+\.onrender\.com',
                r'bhiv-hr-client-portal-[a-z0-9]+\.onrender\.com'
            ]
            for pattern in old_patterns:
                matches = re.findall(pattern, content)
                for match in matches:
                    if match != self.production_urls['client_portal'].replace('https://', ''):
                        content = content.replace(match, self.production_urls['client_portal'].replace('https://', ''))
                        changes.append(f"Updated client portal URL: {match} -> {self.production_urls['client_portal']}")
            
            # Fix database URL (remove mailto: prefix)
            db_patterns = [
                r'postgresql://bhiv_user:mailto:mailto:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@',
                r'postgresql://bhiv_user:mailto:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@'
            ]
            for pattern in db_patterns:
                if pattern in content:
                    content = content.replace(pattern, 'postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@')
                    changes.append("Fixed database URL: Removed mailto: prefix")
            
            # Write updated content if changes were made
            if content != original_content:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                return True, changes
            else:
                return True, ["No changes needed"]
                
        except Exception as e:
            return False, [f"Error updating file: {str(e)}"]
    
    def update_all_files(self) -> Dict[str, Tuple[bool, List[str]]]:
        """Update URLs in all specified files"""
        results = {}
        
        for file_path in self.files_to_update:
            full_path = self.project_root / file_path
            success, changes = self.update_file_urls(full_path)
            results[file_path] = (success, changes)
        
        return results
    
    def generate_render_config_fix(self) -> str:
        """Generate the corrected Render environment configuration"""
        config = []
        config.append("RENDER ENVIRONMENT VARIABLES - CORRECTED CONFIGURATION")
        config.append("=" * 60)
        
        config.append("\n1. AGENT SERVICE (bhiv-hr-agent):")
        config.append("   REMOVE: JWT_SECRET, OBSERVABILITY_ENABLED, PYTHON_VERSION")
        config.append("   ADD: JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA")
        config.append("   ADD: GATEWAY_SERVICE_URL=https://bhiv-hr-gateway-46pz.onrender.com")
        config.append("   FIX: DATABASE_URL (remove mailto: prefix)")
        
        config.append("\n2. GATEWAY SERVICE (bhiv-hr-gateway):")
        config.append("   REMOVE: JWT_SECRET, OBSERVABILITY_ENABLED, PYTHON_VERSION, SECRET_KEY")
        config.append("   ADD: JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA")
        config.append("   FIX: DATABASE_URL (remove mailto: prefix)")
        
        config.append("\n3. PORTAL SERVICE (bhiv-hr-portal):")
        config.append("   REMOVE: JWT_SECRET, PYTHON_VERSION")
        config.append("   ADD: JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA")
        
        config.append("\n4. CLIENT PORTAL SERVICE (bhiv-hr-client-portal):")
        config.append("   REMOVE: JWT_SECRET, PYTHON_VERSION")
        config.append("   ADD: JWT_SECRET_KEY=prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA")
        config.append("   FIX: DATABASE_URL (remove mailto: prefix)")
        
        config.append("\nCORRECT DATABASE_URL (for all services that need it):")
        config.append("postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu")
        
        return "\n".join(config)

def main():
    project_root = Path(__file__).parent.parent
    updater = ProductionURLUpdater(project_root)
    
    print("BHIV HR Platform - Production URLs Update")
    print("=" * 50)
    
    # Update all files
    results = updater.update_all_files()
    
    # Display results
    total_files = len(results)
    successful_updates = 0
    total_changes = 0
    
    for file_path, (success, changes) in results.items():
        if success:
            successful_updates += 1
            if changes and changes != ["No changes needed"]:
                total_changes += len(changes)
                print(f"\nUPDATED: {file_path}")
                for change in changes:
                    print(f"  - {change}")
            else:
                print(f"OK: {file_path} (no changes needed)")
        else:
            print(f"FAILED: {file_path}")
            for error in changes:
                print(f"  - {error}")
    
    # Generate Render configuration fix
    render_config = updater.generate_render_config_fix()
    
    # Save render config to file
    config_file = project_root / 'RENDER_CONFIG_FIXES.txt'
    with open(config_file, 'w') as f:
        f.write(render_config)
    
    print(f"\nSUMMARY:")
    print(f"Files processed: {total_files}")
    print(f"Successful updates: {successful_updates}")
    print(f"Total changes made: {total_changes}")
    print(f"Render config saved to: {config_file}")
    
    if successful_updates == total_files and total_changes > 0:
        print("\nSUCCESS: All URLs updated successfully!")
        print("\nNEXT STEPS:")
        print("1. Review RENDER_CONFIG_FIXES.txt for environment variable changes")
        print("2. Update Render environment variables as specified")
        print("3. Commit and push the URL updates:")
        print("   git add .")
        print('   git commit -m "Update production URLs to match current deployment"')
        print("   git push")
    elif total_changes == 0:
        print("\nINFO: All URLs are already up to date")
    else:
        print("\nWARNING: Some files could not be updated")

if __name__ == '__main__':
    main()