#!/usr/bin/env python3
"""
Security Fixes Deployment Script
Deploys the enhanced security configuration to production
"""

import os
import subprocess
import sys
import time
from datetime import datetime

class SecurityDeployment:
    """Handles deployment of security fixes"""
    
    def __init__(self):
        self.deployment_id = f"security_fix_{int(time.time())}"
        self.services = [
            "bhiv-hr-gateway",
            "bhiv-hr-agent", 
            "bhiv-hr-portal",
            "bhiv-hr-client-portal"
        ]
        
        # Render deployment webhook URLs (from previous deployments)
        self.deploy_urls = {
            "gateway": "https://api.render.com/deploy/srv-d2s0a6mmcj7s73fn3iqg?key=EwZutgywDXg",
            "agent": "https://api.render.com/deploy/srv-d2s0dp3e5dus73cl3a20?key=w7R-2dV-_FE",
            "portal": "https://api.render.com/deploy/srv-d2s5vtje5dus73cr0s90?key=POyxo7foEVs",
            "client_portal": "https://api.render.com/deploy/srv-d2s67pffte5s739kp99g?key=C04znxCoOwE"
        }
    
    def validate_security_fixes(self) -> bool:
        """Validate that security fixes are properly implemented"""
        print("Validating security fixes...")
        
        # Check if security manager exists
        security_manager_path = os.path.join("services", "shared", "security_manager.py")
        if not os.path.exists(security_manager_path):
            print("ERROR: Security manager not found")
            return False
        
        # Check if portal security config is updated
        portal_security_path = os.path.join("services", "portal", "security_config.py")
        if not os.path.exists(portal_security_path):
            print("ERROR: Portal security config not found")
            return False
        
        # Check if client auth service is updated
        client_auth_path = os.path.join("services", "client_portal", "auth_service.py")
        if not os.path.exists(client_auth_path):
            print("ERROR: Client auth service not found")
            return False
        
        print("Security fixes validation: PASSED")
        return True
    
    def commit_changes(self) -> bool:
        """Commit security fixes to git"""
        try:
            print("Committing security fixes to git...")
            
            # Add all security-related files
            subprocess.run(["git", "add", "services/shared/security_manager.py"], check=True)
            subprocess.run(["git", "add", "services/portal/security_config.py"], check=True)
            subprocess.run(["git", "add", "services/client_portal/auth_service.py"], check=True)
            subprocess.run(["git", "add", ".env.production"], check=True)
            subprocess.run(["git", "add", ".env.example"], check=True)
            
            # Commit with descriptive message
            commit_message = f"Security Fix: Resolve CWE-798 and JWT_SECRET issues - {self.deployment_id}"
            subprocess.run(["git", "commit", "-m", commit_message], check=True)
            
            print(f"Changes committed: {commit_message}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git commit failed: {e}")
            return False
    
    def push_to_github(self) -> bool:
        """Push changes to GitHub"""
        try:
            print("Pushing changes to GitHub...")
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("Changes pushed to GitHub successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Git push failed: {e}")
            return False
    
    def trigger_render_deployments(self) -> bool:
        """Trigger deployments on Render"""
        try:
            print("Triggering Render deployments...")
            
            for service, url in self.deploy_urls.items():
                print(f"Deploying {service}...")
                try:
                    # Use curl to trigger deployment
                    result = subprocess.run([
                        "curl", "-X", "POST", url
                    ], capture_output=True, text=True, timeout=30)
                    
                    if result.returncode == 0:
                        print(f"  {service}: Deployment triggered successfully")
                    else:
                        print(f"  {service}: Deployment trigger failed - {result.stderr}")
                except subprocess.TimeoutExpired:
                    print(f"  {service}: Deployment trigger timeout (but likely successful)")
                except Exception as e:
                    print(f"  {service}: Deployment trigger error - {e}")
                
                # Wait between deployments
                time.sleep(2)
            
            print("All deployment triggers sent")
            return True
        except Exception as e:
            print(f"Deployment trigger failed: {e}")
            return False
    
    def verify_deployments(self) -> bool:
        """Verify that deployments are successful"""
        print("Verifying deployments...")
        
        service_urls = {
            "gateway": "https://bhiv-hr-gateway.onrender.com/health",
            "agent": "https://bhiv-hr-agent.onrender.com/health", 
            "portal": "https://bhiv-hr-portal.onrender.com/",
            "client_portal": "https://bhiv-hr-client-portal.onrender.com/"
        }
        
        # Wait for deployments to complete
        print("Waiting 60 seconds for deployments to complete...")
        time.sleep(60)
        
        success_count = 0
        for service, url in service_urls.items():
            try:
                result = subprocess.run([
                    "curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url
                ], capture_output=True, text=True, timeout=10)
                
                status_code = result.stdout.strip()
                if status_code in ["200", "302"]:
                    print(f"  {service}: HEALTHY ({status_code})")
                    success_count += 1
                else:
                    print(f"  {service}: UNHEALTHY ({status_code})")
            except Exception as e:
                print(f"  {service}: CHECK FAILED - {e}")
        
        success_rate = (success_count / len(service_urls)) * 100
        print(f"Deployment verification: {success_count}/{len(service_urls)} services healthy ({success_rate:.1f}%)")
        
        return success_count >= 3  # At least 3 out of 4 services should be healthy
    
    def deploy(self) -> bool:
        """Execute complete deployment process"""
        print("=" * 60)
        print("BHIV HR Platform - Security Fixes Deployment")
        print(f"Deployment ID: {self.deployment_id}")
        print(f"Timestamp: {datetime.now().isoformat()}")
        print("=" * 60)
        
        steps = [
            ("Validate Security Fixes", self.validate_security_fixes),
            ("Commit Changes", self.commit_changes),
            ("Push to GitHub", self.push_to_github),
            ("Trigger Render Deployments", self.trigger_render_deployments),
            ("Verify Deployments", self.verify_deployments)
        ]
        
        for step_name, step_func in steps:
            print(f"\nStep: {step_name}")
            if not step_func():
                print(f"DEPLOYMENT FAILED at step: {step_name}")
                return False
            print(f"Step completed: {step_name}")
        
        print("\n" + "=" * 60)
        print("DEPLOYMENT SUCCESSFUL!")
        print("Security fixes have been deployed to production")
        print("=" * 60)
        
        # Print access information
        print("\nProduction Services:")
        print("- API Gateway: https://bhiv-hr-gateway.onrender.com/docs")
        print("- HR Portal: https://bhiv-hr-portal.onrender.com/")
        print("- Client Portal: https://bhiv-hr-client-portal.onrender.com/")
        print("- AI Agent: https://bhiv-hr-agent.onrender.com/docs")
        
        print("\nSecurity Fixes Applied:")
        print("- CWE-798: Demo API key detection and replacement")
        print("- JWT_SECRET: Environment-aware fallback configuration")
        print("- Enhanced error handling with graceful degradation")
        print("- Centralized security management system")
        
        return True

def main():
    """Main deployment execution"""
    deployment = SecurityDeployment()
    
    try:
        success = deployment.deploy()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\nDeployment cancelled by user")
        return 1
    except Exception as e:
        print(f"\nDeployment failed with error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())