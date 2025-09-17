#!/usr/bin/env python3
"""
BHIV HR Platform - Security Audit Tool
Comprehensive security audit for environment configuration and secrets
"""

import os
import sys
import subprocess
from pathlib import Path
from typing import Dict, List, Any
import re

class SecurityAuditor:
    """Comprehensive security audit tool"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.audit_results = {
            "committed_secrets": [],
            "insecure_configs": [],
            "missing_protections": [],
            "recommendations": []
        }
    
    def audit_committed_files(self) -> Dict[str, Any]:
        """Audit repository for committed secrets and sensitive files"""
        print("Auditing committed files for secrets...")
        
        # Files that should never be committed
        sensitive_files = [
            ".env",
            "config/.env.render",
            "config/production.env",
            "secrets.json",
            "credentials.json"
        ]
        
        # Check if files are tracked by git
        for file_path in sensitive_files:
            full_path = self.project_root / file_path
            if full_path.exists():
                if self._is_file_tracked(file_path):
                    self.audit_results["committed_secrets"].append({
                        "file": file_path,
                        "risk": "HIGH",
                        "issue": "Sensitive file committed to repository"
                    })
        
        return self.audit_results["committed_secrets"]
    
    def audit_secret_patterns(self) -> Dict[str, Any]:
        """Scan files for secret patterns"""
        print("Scanning for secret patterns in code...")
        
        secret_patterns = {
            "api_key": r"api[_-]?key['\"]?\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})",
            "password": r"password['\"]?\s*[:=]\s*['\"]?([^'\"\\s]{8,})",
            "secret": r"secret['\"]?\s*[:=]\s*['\"]?([a-zA-Z0-9]{16,})",
            "token": r"token['\"]?\s*[:=]\s*['\"]?([a-zA-Z0-9]{20,})",
            "database_url": r"postgresql://[^\\s'\"]+:[^\\s'\"]+@"
        }
        
        # Scan Python files
        for py_file in self.project_root.rglob("*.py"):
            if "venv" in str(py_file) or "__pycache__" in str(py_file):
                continue
                
            try:
                content = py_file.read_text()
                for pattern_name, pattern in secret_patterns.items():
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        self.audit_results["insecure_configs"].append({
                            "file": str(py_file.relative_to(self.project_root)),
                            "line": content[:match.start()].count('\n') + 1,
                            "pattern": pattern_name,
                            "risk": "MEDIUM",
                            "issue": f"Potential {pattern_name} found in code"
                        })
            except:
                continue
        
        return self.audit_results["insecure_configs"]
    
    def audit_environment_security(self) -> Dict[str, Any]:
        """Audit environment configuration security"""
        print("Auditing environment security...")
        
        # Check for .gitignore
        gitignore_path = self.project_root / ".gitignore"
        if not gitignore_path.exists():
            self.audit_results["missing_protections"].append({
                "protection": ".gitignore file",
                "risk": "HIGH",
                "issue": "No .gitignore file to prevent secret commits"
            })
        else:
            # Check if .gitignore includes environment files
            gitignore_content = gitignore_path.read_text()
            required_patterns = [".env", "*.env", "secrets/"]
            for pattern in required_patterns:
                if pattern not in gitignore_content:
                    self.audit_results["missing_protections"].append({
                        "protection": f".gitignore pattern: {pattern}",
                        "risk": "MEDIUM",
                        "issue": f"Missing {pattern} in .gitignore"
                    })
        
        # Check environment variables
        insecure_env_vars = self._check_environment_variables()
        self.audit_results["insecure_configs"].extend(insecure_env_vars)
        
        return self.audit_results["missing_protections"]
    
    def _is_file_tracked(self, file_path: str) -> bool:
        """Check if file is tracked by git"""
        try:
            result = subprocess.run(
                ["git", "ls-files", file_path],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            return bool(result.stdout.strip())
        except:
            return False
    
    def _check_environment_variables(self) -> List[Dict[str, Any]]:
        """Check current environment variables for security issues"""
        issues = []
        
        # Check for insecure values
        insecure_checks = {
            "API_KEY_SECRET": ["myverysecureapikey123", "demo123", "test123"],
            "DATABASE_URL": ["bhiv_pass", "password", "your_password"],
            "CLIENT_ACCESS_CODE": ["google123", "demo123", "test123"]
        }
        
        for var_name, insecure_values in insecure_checks.items():
            env_value = os.getenv(var_name, "")
            if env_value:
                for insecure_value in insecure_values:
                    if insecure_value in env_value:
                        issues.append({
                            "variable": var_name,
                            "risk": "HIGH",
                            "issue": f"Using insecure default value: {insecure_value}"
                        })
        
        return issues
    
    def generate_remediation_plan(self) -> List[str]:
        """Generate step-by-step remediation plan"""
        remediation_steps = []
        
        # Step 1: Remove committed secrets
        if self.audit_results["committed_secrets"]:
            remediation_steps.extend([
                "# IMMEDIATE ACTION REQUIRED - Remove Committed Secrets",
                "git rm --cached .env",
                "git rm --cached config/.env.render", 
                "git rm --cached config/production.env",
                "git add .gitignore",
                "git commit -m 'Security: Remove committed environment files'",
                ""
            ])
        
        # Step 2: Secure environment configuration
        remediation_steps.extend([
            "# Create secure environment configuration",
            "cp .env.example .env",
            "# Edit .env with secure values (DO NOT COMMIT)",
            ""
        ])
        
        # Step 3: Rotate exposed secrets
        if any(item["risk"] == "HIGH" for item in self.audit_results["insecure_configs"]):
            remediation_steps.extend([
                "# CRITICAL: Rotate all exposed secrets immediately",
                "# Generate new API keys, database passwords, etc.",
                "# Update production environment variables",
                ""
            ])
        
        # Step 4: Implement security measures
        remediation_steps.extend([
            "# Implement ongoing security measures",
            "python tools/security_audit.py  # Run regular audits",
            "python config/env-management.py  # Validate configuration",
            ""
        ])
        
        return remediation_steps
    
    def run_comprehensive_audit(self) -> Dict[str, Any]:
        """Run complete security audit"""
        print("BHIV HR Platform - Security Audit")
        print("=" * 40)
        
        # Run all audit checks
        self.audit_committed_files()
        self.audit_secret_patterns()
        self.audit_environment_security()
        
        # Generate summary
        total_issues = (
            len(self.audit_results["committed_secrets"]) +
            len(self.audit_results["insecure_configs"]) +
            len(self.audit_results["missing_protections"])
        )
        
        high_risk_issues = sum(
            1 for category in self.audit_results.values()
            if isinstance(category, list)
            for item in category
            if isinstance(item, dict) and item.get("risk") == "HIGH"
        )
        
        audit_summary = {
            "total_issues": total_issues,
            "high_risk_issues": high_risk_issues,
            "committed_secrets": len(self.audit_results["committed_secrets"]),
            "insecure_configs": len(self.audit_results["insecure_configs"]),
            "missing_protections": len(self.audit_results["missing_protections"]),
            "security_score": max(0, 100 - (high_risk_issues * 25) - (total_issues * 5))
        }
        
        return {
            "summary": audit_summary,
            "details": self.audit_results,
            "remediation_plan": self.generate_remediation_plan()
        }

def main():
    """Main security audit interface"""
    auditor = SecurityAuditor()
    results = auditor.run_comprehensive_audit()
    
    # Print results
    summary = results["summary"]
    
    print(f"\nSecurity Audit Results:")
    print(f"Security Score: {summary['security_score']}/100")
    print(f"Total Issues: {summary['total_issues']}")
    print(f"High Risk Issues: {summary['high_risk_issues']}")
    
    if summary["committed_secrets"] > 0:
        print(f"\n! CRITICAL: {summary['committed_secrets']} committed secrets found")
        for secret in results["details"]["committed_secrets"]:
            print(f"  - {secret['file']}: {secret['issue']}")
    
    if summary["insecure_configs"] > 0:
        print(f"\n! WARNING: {summary['insecure_configs']} insecure configurations found")
        for config in results["details"]["insecure_configs"][:5]:  # Show first 5
            print(f"  - {config.get('file', config.get('variable', 'Unknown'))}: {config['issue']}")
    
    if summary["missing_protections"] > 0:
        print(f"\n! INFO: {summary['missing_protections']} missing security protections")
        for protection in results["details"]["missing_protections"]:
            print(f"  - {protection['protection']}: {protection['issue']}")
    
    # Print remediation plan
    if summary["total_issues"] > 0:
        print(f"\nRemediation Plan:")
        for step in results["remediation_plan"]:
            print(step)
    else:
        print("\n+ No security issues found!")
    
    return 0 if summary["high_risk_issues"] == 0 else 1

if __name__ == "__main__":
    sys.exit(main())