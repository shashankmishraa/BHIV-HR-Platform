#!/usr/bin/env python3
"""
Comprehensive Credential Verification Script
Validates all updated credentials and service configurations
"""

import os
import json
import asyncio
import aiohttp
import psycopg2
from typing import Dict, List, Tuple
import yaml
import re
from datetime import datetime

class CredentialVerifier:
    def __init__(self):
        self.results = {
            "environment_files": {},
            "database_connection": {},
            "service_urls": {},
            "api_keys": {},
            "docker_configs": {},
            "github_workflows": {},
            "application_code": {},
            "integration_tests": {}
        }
        
        # New credentials to verify
        self.new_credentials = {
            "gateway_url": "https://bhiv-hr-gateway-46pz.onrender.com",
            "agent_url": "https://bhiv-hr-agent-m1me.onrender.com",
            "portal_url": "https://bhiv-hr-portal-cead.onrender.com",
            "client_portal_url": "https://bhiv-hr-client-portal-5g33.onrender.com",
            "database_url": "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu",
            "api_key": "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o",
            "jwt_secret": "prod_jwt_Ova9A8L-OU4uIcAero0v3ZLQRckNr3xBDuO0OXF6uwA"
        }
        
        # Old credentials that should NOT exist
        self.old_credentials = [
            "bhiv-hr-gateway-901a.onrender.com",
            "bhiv-hr-agent-o6nx.onrender.com", 
            "bhiv-hr-portal-xk2k.onrender.com",
            "bhiv-hr-client-portal-zdbt.onrender.com",
            "B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J",
            "dpg-d373qrogjchc73bu9gug-a",
            "bhiv_hr_nqzb"
        ]

    def verify_environment_files(self) -> Dict:
        """Verify all .env files contain new credentials"""
        env_files = [
            ".env",
            ".env.production", 
            "services/gateway/.env.production",
            "services/agent/.env.production",
            "services/portal/.env.production",
            "services/client_portal/.env.production"
        ]
        
        results = {}
        for env_file in env_files:
            if os.path.exists(env_file):
                with open(env_file, 'r') as f:
                    content = f.read()
                
                # Check for old credentials
                old_found = [old for old in self.old_credentials if old in content]
                
                # Check for new credentials
                new_found = []
                if "46pz.onrender.com" in content:
                    new_found.append("gateway_url")
                if "m1me.onrender.com" in content:
                    new_found.append("agent_url")
                if "3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2" in content:
                    new_found.append("database_password")
                
                results[env_file] = {
                    "status": "PASS" if not old_found else "FAIL",
                    "old_credentials_found": old_found,
                    "new_credentials_found": new_found
                }
            else:
                results[env_file] = {"status": "NOT_FOUND"}
        
        return results

    async def verify_database_connection(self) -> Dict:
        """Test database connection with new credentials"""
        try:
            conn = psycopg2.connect(self.new_credentials["database_url"])
            cursor = conn.cursor()
            cursor.execute("SELECT version();")
            version = cursor.fetchone()
            cursor.close()
            conn.close()
            
            return {
                "status": "PASS",
                "connection": "SUCCESS",
                "version": version[0] if version else "Unknown"
            }
        except Exception as e:
            return {
                "status": "FAIL", 
                "error": str(e),
                "connection": "FAILED"
            }

    async def verify_service_urls(self) -> Dict:
        """Test all service URLs for accessibility"""
        services = {
            "gateway": f"{self.new_credentials['gateway_url']}/health",
            "agent": f"{self.new_credentials['agent_url']}/health", 
            "portal": self.new_credentials['portal_url'],
            "client_portal": self.new_credentials['client_portal_url']
        }
        
        results = {}
        async with aiohttp.ClientSession() as session:
            for service, url in services.items():
                try:
                    async with session.get(url, timeout=10) as response:
                        results[service] = {
                            "status": "PASS" if response.status < 400 else "FAIL",
                            "http_status": response.status,
                            "url": url,
                            "accessible": response.status < 400
                        }
                except Exception as e:
                    results[service] = {
                        "status": "FAIL",
                        "error": str(e),
                        "url": url,
                        "accessible": False
                    }
        
        return results

    def verify_config_files(self) -> Dict:
        """Verify configuration files have new credentials"""
        config_files = [
            "config/environments.yml",
            "config/settings.json", 
            "config/render-deployment-config.yml"
        ]
        
        results = {}
        for config_file in config_files:
            if os.path.exists(config_file):
                with open(config_file, 'r') as f:
                    content = f.read()
                
                old_found = [old for old in self.old_credentials if old in content]
                new_found = "46pz.onrender.com" in content and "m1me.onrender.com" in content
                
                results[config_file] = {
                    "status": "PASS" if not old_found and new_found else "FAIL",
                    "old_credentials_found": old_found,
                    "has_new_credentials": new_found
                }
        
        return results

    def verify_docker_configs(self) -> Dict:
        """Verify Docker Compose files"""
        docker_files = [
            "docker-compose.yml",
            "docker-compose.production.yml"
        ]
        
        results = {}
        for docker_file in docker_files:
            if os.path.exists(docker_file):
                with open(docker_file, 'r') as f:
                    content = f.read()
                
                old_found = [old for old in self.old_credentials if old in content]
                
                results[docker_file] = {
                    "status": "PASS" if not old_found else "FAIL", 
                    "old_credentials_found": old_found
                }
        
        return results

    def verify_application_code(self) -> Dict:
        """Scan application code for credential references"""
        code_files = [
            "services/shared/config.py",
            "services/shared/database.py",
            "services/portal/app.py",
            "services/client_portal/app.py",
            "services/agent/app.py"
        ]
        
        results = {}
        for code_file in code_files:
            if os.path.exists(code_file):
                with open(code_file, 'r') as f:
                    content = f.read()
                
                old_found = [old for old in self.old_credentials if old in content]
                
                results[code_file] = {
                    "status": "PASS" if not old_found else "FAIL",
                    "old_credentials_found": old_found
                }
        
        return results

    async def run_verification(self) -> Dict:
        """Run complete verification suite"""
        print("🔍 Starting Comprehensive Credential Verification...")
        
        # 1. Environment Files
        print("1. Verifying environment files...")
        self.results["environment_files"] = self.verify_environment_files()
        
        # 2. Database Connection
        print("2. Testing database connection...")
        self.results["database_connection"] = await self.verify_database_connection()
        
        # 3. Service URLs
        print("3. Testing service URLs...")
        self.results["service_urls"] = await self.verify_service_urls()
        
        # 4. Config Files
        print("4. Verifying configuration files...")
        self.results["config_files"] = self.verify_config_files()
        
        # 5. Docker Configs
        print("5. Verifying Docker configurations...")
        self.results["docker_configs"] = self.verify_docker_configs()
        
        # 6. Application Code
        print("6. Scanning application code...")
        self.results["application_code"] = self.verify_application_code()
        
        return self.results

    def generate_report(self) -> str:
        """Generate verification report"""
        report = f"""
# 🔍 Credential Verification Report
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Summary
"""
        
        total_checks = 0
        passed_checks = 0
        
        for category, results in self.results.items():
            if isinstance(results, dict):
                for item, result in results.items():
                    total_checks += 1
                    if result.get("status") == "PASS":
                        passed_checks += 1
        
        report += f"- **Total Checks**: {total_checks}\n"
        report += f"- **Passed**: {passed_checks}\n"
        report += f"- **Failed**: {total_checks - passed_checks}\n"
        report += f"- **Success Rate**: {(passed_checks/total_checks*100):.1f}%\n\n"
        
        # Detailed Results
        for category, results in self.results.items():
            report += f"## {category.replace('_', ' ').title()}\n"
            
            if isinstance(results, dict):
                for item, result in results.items():
                    status_icon = "✅" if result.get("status") == "PASS" else "❌"
                    report += f"- {status_icon} **{item}**: {result.get('status', 'UNKNOWN')}\n"
                    
                    if result.get("old_credentials_found"):
                        report += f"  - ⚠️ Old credentials found: {result['old_credentials_found']}\n"
                    
                    if result.get("error"):
                        report += f"  - 🚨 Error: {result['error']}\n"
            
            report += "\n"
        
        return report

async def main():
    verifier = CredentialVerifier()
    results = await verifier.run_verification()
    
    # Generate and save report
    report = verifier.generate_report()
    
    with open("CREDENTIAL_VERIFICATION_REPORT.md", "w") as f:
        f.write(report)
    
    print("✅ Verification complete. Report saved to CREDENTIAL_VERIFICATION_REPORT.md")
    
    # Print summary
    print("\n📊 Quick Summary:")
    for category, results in results.items():
        if isinstance(results, dict):
            passed = sum(1 for r in results.values() if r.get("status") == "PASS")
            total = len(results)
            print(f"  {category}: {passed}/{total} passed")

if __name__ == "__main__":
    asyncio.run(main())