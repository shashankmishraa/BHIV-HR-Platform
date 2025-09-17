#!/usr/bin/env python3
"""
BHIV HR Platform - Environment Configuration Management
Secure environment variable handling and validation
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import json

class EnvironmentManager:
    """Secure environment configuration management"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_dir = self.project_root / "config"
        self.required_vars = {
            "DATABASE_URL": "Database connection string",
            "API_KEY_SECRET": "API authentication key"
        }
        self.optional_vars = {
            "GATEWAY_URL": "http://gateway:8000",
            "AGENT_URL": "http://agent:9000",
            "LOG_LEVEL": "INFO",
            "ENABLE_SEMANTIC": "false"
        }
    
    def validate_environment(self) -> Dict[str, Any]:
        """Validate current environment configuration"""
        validation_result = {
            "valid": True,
            "missing_required": [],
            "missing_optional": [],
            "security_issues": [],
            "recommendations": []
        }
        
        # Check required variables
        for var_name, description in self.required_vars.items():
            value = os.getenv(var_name)
            if not value:
                validation_result["missing_required"].append({
                    "name": var_name,
                    "description": description
                })
                validation_result["valid"] = False
            elif self._is_insecure_value(value):
                validation_result["security_issues"].append({
                    "name": var_name,
                    "issue": "Using default/insecure value"
                })
        
        # Check optional variables
        for var_name, default_value in self.optional_vars.items():
            value = os.getenv(var_name)
            if not value:
                validation_result["missing_optional"].append({
                    "name": var_name,
                    "default": default_value
                })
        
        # Security recommendations
        if validation_result["security_issues"]:
            validation_result["recommendations"].append(
                "Update insecure default values with production-ready secrets"
            )
        
        return validation_result
    
    def _is_insecure_value(self, value: str) -> bool:
        """Check if value appears to be insecure default"""
        insecure_patterns = [
            "myverysecureapikey123",
            "bhiv_pass",
            "your_password",
            "demo123",
            "test123",
            "password",
            "secret"
        ]
        return any(pattern in value.lower() for pattern in insecure_patterns)
    
    def generate_secure_template(self) -> str:
        """Generate secure .env template"""
        template_lines = [
            "# BHIV HR Platform - Environment Configuration",
            "# SECURITY: Never commit this file with actual values",
            "",
            "# Required Variables",
        ]
        
        for var_name, description in self.required_vars.items():
            template_lines.extend([
                f"# {description}",
                f"{var_name}=CHANGE_ME_TO_SECURE_VALUE",
                ""
            ])
        
        template_lines.append("# Optional Variables")
        for var_name, default_value in self.optional_vars.items():
            template_lines.extend([
                f"{var_name}={default_value}",
            ])
        
        return "\n".join(template_lines)
    
    def create_environment_template(self, template_path: str):
        """Create secure environment template file"""
        template_content = self.generate_secure_template()
        
        with open(template_path, 'w') as f:
            f.write(template_content)
        
        print(f"Created secure environment template: {template_path}")
    
    def audit_committed_files(self) -> Dict[str, Any]:
        """Audit repository for committed environment files"""
        audit_result = {
            "committed_env_files": [],
            "security_risks": [],
            "recommendations": []
        }
        
        # Check for committed .env files
        env_patterns = [".env", "*.env", "config/*.env"]
        
        # Scan for environment files
        for pattern in [".env*", "config/.env*", "config/production.env"]:
            for file_path in self.project_root.glob(pattern):
                if file_path.is_file() and not file_path.name.endswith('.example'):
                    audit_result["committed_env_files"].append(str(file_path))
                    
                    # Check if file contains secrets
                    if self._file_contains_secrets(file_path):
                        audit_result["security_risks"].append({
                            "file": str(file_path),
                            "risk": "Contains potential secrets"
                        })
        
        if audit_result["committed_env_files"]:
            audit_result["recommendations"].extend([
                "Remove committed environment files from repository",
                "Add files to .gitignore",
                "Use environment-specific configuration management"
            ])
        
        return audit_result
    
    def _file_contains_secrets(self, file_path: Path) -> bool:
        """Check if file contains potential secrets"""
        try:
            content = file_path.read_text()
            secret_indicators = [
                "password=",
                "secret=",
                "key=",
                "token=",
                "api_key="
            ]
            return any(indicator in content.lower() for indicator in secret_indicators)
        except:
            return False
    
    def cleanup_committed_secrets(self) -> List[str]:
        """Generate cleanup commands for committed secrets"""
        commands = []
        
        # Files to remove from tracking
        files_to_remove = [
            ".env",
            "config/.env.render", 
            "config/production.env"
        ]
        
        for file_path in files_to_remove:
            if (self.project_root / file_path).exists():
                commands.extend([
                    f"git rm --cached {file_path}",
                    f"# Move {file_path} to secure location outside repository"
                ])
        
        commands.extend([
            "git add .gitignore",
            "git commit -m 'Security: Remove committed environment files and add .gitignore'",
            "# IMPORTANT: Rotate all exposed secrets immediately"
        ])
        
        return commands

def main():
    """Main environment management interface"""
    manager = EnvironmentManager()
    
    print("BHIV HR Platform - Environment Security Audit")
    print("=" * 50)
    
    # Validate current environment
    validation = manager.validate_environment()
    
    print("\nEnvironment Validation:")
    if validation["valid"]:
        print("+ Environment configuration is valid")
    else:
        print("- Environment configuration has issues")
        
        if validation["missing_required"]:
            print("\nMissing Required Variables:")
            for var in validation["missing_required"]:
                print(f"  - {var['name']}: {var['description']}")
        
        if validation["security_issues"]:
            print("\nSecurity Issues:")
            for issue in validation["security_issues"]:
                print(f"  ! {issue['name']}: {issue['issue']}")
    
    # Audit committed files
    audit = manager.audit_committed_files()
    
    print(f"\nCommitted Environment Files Audit:")
    if audit["committed_env_files"]:
        print("- Found committed environment files:")
        for file_path in audit["committed_env_files"]:
            print(f"  ! {file_path}")
        
        if audit["security_risks"]:
            print("\nSecurity Risks:")
            for risk in audit["security_risks"]:
                print(f"  ! {risk['file']}: {risk['risk']}")
        
        print("\nCleanup Commands:")
        cleanup_commands = manager.cleanup_committed_secrets()
        for cmd in cleanup_commands:
            print(f"  {cmd}")
    else:
        print("+ No committed environment files found")
    
    # Generate secure template
    template_path = manager.project_root / ".env.template"
    manager.create_environment_template(template_path)

if __name__ == "__main__":
    main()