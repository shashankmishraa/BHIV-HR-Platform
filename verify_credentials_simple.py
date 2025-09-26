#!/usr/bin/env python3
"""
Simple Credential Verification Script
"""

import os
import json
import requests
from datetime import datetime

def verify_environment_files():
    """Verify all .env files contain new credentials"""
    env_files = [
        ".env",
        ".env.production", 
        "services/gateway/.env.production",
        "services/agent/.env.production",
        "services/portal/.env.production",
        "services/client_portal/.env.production"
    ]
    
    old_credentials = [
        "bhiv-hr-gateway-901a.onrender.com",
        "bhiv-hr-agent-o6nx.onrender.com", 
        "bhiv-hr-portal-xk2k.onrender.com",
        "bhiv-hr-client-portal-zdbt.onrender.com",
        "B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J",
        "dpg-d373qrogjchc73bu9gug-a",
        "bhiv_hr_nqzb"
    ]
    
    results = {}
    for env_file in env_files:
        if os.path.exists(env_file):
            with open(env_file, 'r') as f:
                content = f.read()
            
            old_found = [old for old in old_credentials if old in content]
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

def verify_service_urls():
    """Test service URLs"""
    services = {
        "gateway": "https://bhiv-hr-gateway-46pz.onrender.com/health",
        "agent": "https://bhiv-hr-agent-m1me.onrender.com/health", 
        "portal": "https://bhiv-hr-portal-cead.onrender.com",
        "client_portal": "https://bhiv-hr-client-portal-5g33.onrender.com"
    }
    
    results = {}
    for service, url in services.items():
        try:
            response = requests.get(url, timeout=10)
            results[service] = {
                "status": "PASS" if response.status_code < 400 else "FAIL",
                "http_status": response.status_code,
                "url": url,
                "accessible": response.status_code < 400
            }
        except Exception as e:
            results[service] = {
                "status": "FAIL",
                "error": str(e),
                "url": url,
                "accessible": False
            }
    
    return results

def verify_config_files():
    """Verify configuration files"""
    config_files = [
        "config/environments.yml",
        "config/settings.json", 
        "config/render-deployment-config.yml"
    ]
    
    old_credentials = [
        "bhiv-hr-gateway-901a.onrender.com",
        "bhiv-hr-agent-o6nx.onrender.com", 
        "B7iZSA0S3y6QCopt0UTxmnEQsJmxtf9J"
    ]
    
    results = {}
    for config_file in config_files:
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                content = f.read()
            
            old_found = [old for old in old_credentials if old in content]
            new_found = "46pz.onrender.com" in content and "m1me.onrender.com" in content
            
            results[config_file] = {
                "status": "PASS" if not old_found and new_found else "FAIL",
                "old_credentials_found": old_found,
                "has_new_credentials": new_found
            }
    
    return results

def main():
    print("Starting Credential Verification...")
    
    # Run verifications
    env_results = verify_environment_files()
    url_results = verify_service_urls()
    config_results = verify_config_files()
    
    # Generate report
    report = f"""# Credential Verification Report
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Environment Files
"""
    
    for file, result in env_results.items():
        status_icon = "PASS" if result.get("status") == "PASS" else "FAIL"
        report += f"- {status_icon}: {file}\n"
        if result.get("old_credentials_found"):
            report += f"  - Old credentials found: {result['old_credentials_found']}\n"
    
    report += "\n## Service URLs\n"
    for service, result in url_results.items():
        status_icon = "PASS" if result.get("status") == "PASS" else "FAIL"
        report += f"- {status_icon}: {service} ({result.get('http_status', 'ERROR')})\n"
        if result.get("error"):
            report += f"  - Error: {result['error']}\n"
    
    report += "\n## Configuration Files\n"
    for file, result in config_results.items():
        status_icon = "PASS" if result.get("status") == "PASS" else "FAIL"
        report += f"- {status_icon}: {file}\n"
        if result.get("old_credentials_found"):
            report += f"  - Old credentials found: {result['old_credentials_found']}\n"
    
    # Save report
    with open("CREDENTIAL_VERIFICATION_REPORT.md", "w") as f:
        f.write(report)
    
    print("Verification complete. Report saved to CREDENTIAL_VERIFICATION_REPORT.md")
    
    # Print summary
    total_env = len(env_results)
    passed_env = sum(1 for r in env_results.values() if r.get("status") == "PASS")
    
    total_url = len(url_results)
    passed_url = sum(1 for r in url_results.values() if r.get("status") == "PASS")
    
    total_config = len(config_results)
    passed_config = sum(1 for r in config_results.values() if r.get("status") == "PASS")
    
    print(f"\nSummary:")
    print(f"Environment Files: {passed_env}/{total_env} passed")
    print(f"Service URLs: {passed_url}/{total_url} passed")
    print(f"Config Files: {passed_config}/{total_config} passed")

if __name__ == "__main__":
    main()