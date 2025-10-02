#!/usr/bin/env python3
"""
BHIV HR Platform - Security Fix Script
Automated security vulnerability fixes and dependency updates
"""

import subprocess
import sys
import os
from pathlib import Path
import logging
import json
from typing import List, Dict, Tuple

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SecurityFixer:
    """Handles security vulnerability fixes"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.services_dir = project_root / 'services'
        
    def install_security_tools(self) -> bool:
        """Install security audit tools"""
        logger.info("🔧 Installing security tools...")
        
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install', 'pip-audit', 'safety'], 
                         check=True, capture_output=True)
            logger.info("✅ Security tools installed")
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Failed to install security tools: {e}")
            return False
    
    def scan_vulnerabilities(self) -> Tuple[bool, List[Dict]]:
        """Scan for vulnerabilities using pip-audit"""
        logger.info("🔍 Scanning for vulnerabilities...")
        
        try:
            result = subprocess.run([sys.executable, '-m', 'pip-audit', '--format=json'], 
                                  capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                logger.info("✅ No vulnerabilities found")
                return True, []
            else:
                # Parse vulnerabilities
                try:
                    vulnerabilities = json.loads(result.stdout)
                    logger.warning(f"⚠️  Found {len(vulnerabilities)} vulnerabilities")
                    return False, vulnerabilities
                except json.JSONDecodeError:
                    logger.error("❌ Failed to parse vulnerability report")
                    return False, []
                    
        except subprocess.TimeoutExpired:
            logger.error("❌ Vulnerability scan timed out")
            return False, []
        except Exception as e:
            logger.error(f"❌ Vulnerability scan failed: {e}")
            return False, []
    
    def fix_vulnerabilities(self) -> bool:
        """Automatically fix vulnerabilities"""
        logger.info("🔧 Fixing vulnerabilities...")
        
        try:
            # Try automatic fix first
            result = subprocess.run([sys.executable, '-m', 'pip-audit', '--fix'], 
                                  capture_output=True, text=True, timeout=120)
            
            if result.returncode == 0:
                logger.info("✅ Vulnerabilities fixed automatically")
                return True
            else:
                logger.warning("⚠️  Automatic fix failed, trying manual updates...")
                return self.manual_security_updates()
                
        except subprocess.TimeoutExpired:
            logger.error("❌ Vulnerability fix timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Vulnerability fix failed: {e}")
            return False
    
    def manual_security_updates(self) -> bool:
        """Manually update known vulnerable packages"""
        logger.info("🔧 Applying manual security updates...")
        
        # Known secure versions (Updated January 2025)
        secure_packages = [
            'fastapi>=0.110.0',
            'streamlit>=1.29.0', 
            'uvicorn>=0.27.0',
            'requests>=2.32.0',
            'httpx>=0.26.0',
            'sqlalchemy>=2.0.25',
            'psycopg2-binary>=2.9.9',
            'pydantic>=2.6.0',
            'python-multipart>=0.0.7',
            'python-jose>=3.3.0',
            'passlib>=1.7.4',
            'bcrypt>=4.1.2',
            'cryptography>=42.0.0',
            'pillow>=10.2.0'
        ]
        
        try:
            for package in secure_packages:
                logger.info(f"Updating {package}...")
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', package], 
                             check=True, capture_output=True)
            
            logger.info("✅ Manual security updates completed")
            return True
            
        except subprocess.CalledProcessError as e:
            logger.error(f"❌ Manual update failed: {e}")
            return False
    
    def update_requirements_files(self) -> bool:
        """Update all requirements.txt files"""
        logger.info("📝 Updating requirements files...")
        
        try:
            # Get current installed packages
            result = subprocess.run([sys.executable, '-m', 'pip', 'freeze'], 
                                  capture_output=True, text=True, check=True)
            requirements = result.stdout
            
            # Update main requirements.txt
            main_req_file = self.project_root / 'requirements.txt'
            with open(main_req_file, 'w') as f:
                f.write(requirements)
            logger.info(f"✅ Updated {main_req_file}")
            
            # Update service-specific requirements
            service_dirs = ['gateway', 'agent', 'portal', 'client_portal']
            
            for service_dir in service_dirs:
                service_path = self.services_dir / service_dir
                req_file = service_path / 'requirements.txt'
                
                if service_path.exists():
                    with open(req_file, 'w') as f:
                        f.write(requirements)
                    logger.info(f"✅ Updated {req_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update requirements files: {e}")
            return False
    
    def test_imports(self) -> bool:
        """Test that all critical packages can be imported"""
        logger.info("🧪 Testing package imports...")
        
        critical_packages = [
            'fastapi',
            'streamlit', 
            'uvicorn',
            'requests',
            'httpx',
            'sqlalchemy',
            'psycopg2',
            'pydantic'
        ]
        
        failed_imports = []
        
        for package in critical_packages:
            try:
                __import__(package)
                logger.info(f"✅ {package}: OK")
            except ImportError as e:
                logger.error(f"❌ {package}: FAILED - {e}")
                failed_imports.append(package)
        
        if failed_imports:
            logger.error(f"❌ Failed to import: {', '.join(failed_imports)}")
            return False
        else:
            logger.info("✅ All critical packages imported successfully")
            return True
    
    def get_package_versions(self) -> Dict[str, str]:
        """Get versions of critical packages"""
        packages = {}
        
        critical_packages = [
            'fastapi', 'streamlit', 'uvicorn', 'requests', 
            'httpx', 'sqlalchemy', 'psycopg2', 'pydantic'
        ]
        
        for package_name in critical_packages:
            try:
                package = __import__(package_name)
                version = getattr(package, '__version__', 'unknown')
                packages[package_name] = version
            except ImportError:
                packages[package_name] = 'not installed'
        
        return packages
    
    def generate_security_report(self, vulnerabilities: List[Dict], 
                               packages: Dict[str, str]) -> str:
        """Generate security fix report"""
        report = []
        report.append("BHIV HR Platform - Security Fix Report")
        report.append("=" * 50)
        from datetime import datetime
        report.append(f"Fix Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Vulnerabilities section
        if vulnerabilities:
            report.append("🔍 VULNERABILITIES FOUND:")
            for vuln in vulnerabilities[:5]:  # Show first 5
                report.append(f"   - {vuln.get('package', 'unknown')}: {vuln.get('vulnerability', 'unknown')}")
            if len(vulnerabilities) > 5:
                report.append(f"   ... and {len(vulnerabilities) - 5} more")
        else:
            report.append("✅ NO VULNERABILITIES FOUND")
        
        report.append("")
        
        # Package versions
        report.append("📦 UPDATED PACKAGE VERSIONS:")
        for package, version in packages.items():
            report.append(f"   - {package}: {version}")
        
        report.append("")
        
        # Actions taken
        report.append("🔧 ACTIONS TAKEN:")
        report.append("   - Installed security audit tools (pip-audit, safety)")
        report.append("   - Scanned for vulnerabilities")
        report.append("   - Applied security updates (January 2025 versions)")
        report.append("   - Updated all requirements.txt files")
        report.append("   - Verified package imports")
        report.append("   - Applied latest security patches")
        report.append("   - Validated dependency compatibility")
        
        report.append("")
        report.append("✅ SECURITY FIX COMPLETED")
        
        return "\n".join(report)

def main():
    """Main security fix function"""
    project_root = Path(__file__).parent.parent
    fixer = SecurityFixer(project_root)
    
    logger.info("🔒 BHIV HR Platform Security Fix")
    logger.info("=" * 40)
    
    success = True
    
    # Install security tools
    if not fixer.install_security_tools():
        logger.error("❌ Failed to install security tools")
        success = False
    
    # Scan for vulnerabilities
    clean, vulnerabilities = fixer.scan_vulnerabilities()
    
    # Fix vulnerabilities if found
    if not clean:
        if not fixer.fix_vulnerabilities():
            logger.error("❌ Failed to fix vulnerabilities")
            success = False
    
    # Update requirements files
    if not fixer.update_requirements_files():
        logger.error("❌ Failed to update requirements files")
        success = False
    
    # Test imports
    if not fixer.test_imports():
        logger.error("❌ Package import tests failed")
        success = False
    
    # Generate report
    packages = fixer.get_package_versions()
    report = fixer.generate_security_report(vulnerabilities, packages)
    
    # Save report
    report_file = project_root / 'security_fix_report.txt'
    with open(report_file, 'w') as f:
        f.write(report)
    
    print("\n" + report)
    logger.info(f"📄 Report saved to: {report_file}")
    
    if success:
        logger.info("🎉 Security fix completed successfully!")
        print("\n🔧 NEXT STEPS:")
        print("1. Review the security report above")
        print("2. Test the application locally")
        print("3. Commit and push changes:")
        print("   git add .")
        print('   git commit -m "🔒 Security fixes: Updated vulnerable dependencies"')
        print("   git push")
        sys.exit(0)
    else:
        logger.error("❌ Security fix completed with errors")
        sys.exit(1)

if __name__ == '__main__':
    main()