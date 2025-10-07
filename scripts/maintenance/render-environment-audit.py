#!/usr/bin/env python3
"""
BHIV HR Platform - Render Environment Variables Audit & Fix
Analyzes current Render config vs codebase requirements
"""

import os
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
import json

class RenderEnvironmentAuditor:
    def __init__(self, project_root: Path):
        self.project_root = project_root
        
        # Current Render Environment Variables (sanitized)
        self.current_render_config = {
            'agent': {
                'API_KEY_SECRET': '<REDACTED>',
                'DATABASE_URL': '<REDACTED>',
                'ENVIRONMENT': 'production',
                'JWT_SECRET': '<REDACTED>',
                'LOG_LEVEL': 'INFO',
                'OBSERVABILITY_ENABLED': 'true',
                'PYTHON_VERSION': '3.12.7'
            },
            'gateway': {
                'AGENT_SERVICE_URL': 'https://bhiv-hr-agent-m1me.onrender.com',
                'API_KEY_SECRET': '<REDACTED>',
                'DATABASE_URL': '<REDACTED>',
                'ENVIRONMENT': 'production',
                'JWT_SECRET': '<REDACTED>',
                'LOG_LEVEL': 'INFO',
                'OBSERVABILITY_ENABLED': 'true',
                'PYTHON_VERSION': '3.12.7',
                'SECRET_KEY': '<REDACTED>'
            },
            'portal': {
                'AGENT_SERVICE_URL': 'https://bhiv-hr-agent-m1me.onrender.com',
                'API_KEY_SECRET': '<REDACTED>',
                'ENVIRONMENT': 'production',
                'GATEWAY_URL': 'https://bhiv-hr-gateway-46pz.onrender.com',
                'JWT_SECRET': '<REDACTED>',
                'LOG_LEVEL': 'INFO',
                'PYTHON_VERSION': '3.12.7'
            },
            'client_portal': {
                'AGENT_SERVICE_URL': 'https://bhiv-hr-agent-m1me.onrender.com',
                'API_KEY_SECRET': '<REDACTED>',
                'DATABASE_URL': '<REDACTED>',
                'ENVIRONMENT': 'production',
                'GATEWAY_URL': 'https://bhiv-hr-gateway-46pz.onrender.com',
                'JWT_SECRET': '<REDACTED>',
                'LOG_LEVEL': 'INFO',
                'PYTHON_VERSION': '3.12.7'
            }
        }
        
        # Production URLs
        self.production_urls = {
            'AGENT_SERVICE_URL': 'https://bhiv-hr-agent-m1me.onrender.com',
            'GATEWAY_SERVICE_URL': 'https://bhiv-hr-gateway-46pz.onrender.com',
            'PORTAL_SERVICE_URL': 'https://bhiv-hr-portal-cead.onrender.com',
            'CLIENT_PORTAL_SERVICE_URL': 'https://bhiv-hr-client-portal-5g33.onrender.com',
            'DATABASE_URL': '<REDACTED>'
        }
    
    def scan_codebase_for_env_vars(self) -> Dict[str, Set[str]]:
        """Scan all files for environment variable usage"""
        env_vars_found = {}
        
        # File patterns to scan
        patterns = ['*.py', '*.yml', '*.yaml', '*.env*', '*.md']
        
        for pattern in patterns:
            for file_path in self.project_root.rglob(pattern):
                if any(skip in str(file_path) for skip in ['.git', '__pycache__', 'node_modules']):
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # Find environment variables
                    env_vars = re.findall(r'os\.getenv\(["\']([^"\']+)["\']', content)
                    env_vars.extend(re.findall(r'os\.environ\[["\']([^"\']+)["\']\]', content))
                    env_vars.extend(re.findall(r'\$\{([^}]+)\}', content))
                    env_vars.extend(re.findall(r'([A-Z_]+)=', content))
                    
                    if env_vars:
                        env_vars_found[str(file_path)] = set(env_vars)
                        
                except Exception:
                    continue
        
        return env_vars_found
    
    def analyze_missing_variables(self) -> Dict[str, List[str]]:
        """Analyze what variables are missing from Render config"""
        codebase_vars = self.scan_codebase_for_env_vars()
        
        # Extract all unique environment variables from codebase
        all_codebase_vars = set()
        for file_vars in codebase_vars.values():
            all_codebase_vars.update(file_vars)
        
        # Filter to relevant variables (exclude system vars)
        relevant_vars = {var for var in all_codebase_vars 
                        if any(keyword in var.upper() for keyword in 
                              ['API', 'DATABASE', 'JWT', 'SECRET', 'URL', 'SERVICE', 'GATEWAY', 'AGENT', 'PORTAL'])}
        
        missing_by_service = {}
        
        for service, config in self.current_render_config.items():
            current_vars = set(config.keys())
            missing = relevant_vars - current_vars
            if missing:
                missing_by_service[service] = list(missing)
        
        return missing_by_service
    
    def generate_recommended_config(self) -> Dict[str, Dict[str, str]]:
        """Generate recommended Render environment configuration"""
        return {
            'agent': {
                'API_KEY_SECRET': '<REDACTED>',
                'DATABASE_URL': '<REDACTED>',
                'ENVIRONMENT': 'production',
                'JWT_SECRET_KEY': '<REDACTED>',
                'LOG_LEVEL': 'INFO',
                'GATEWAY_SERVICE_URL': 'https://bhiv-hr-gateway-46pz.onrender.com'
            },
            'gateway': {
                'API_KEY_SECRET': '<REDACTED>',
                'DATABASE_URL': '<REDACTED>',
                'ENVIRONMENT': 'production',
                'JWT_SECRET_KEY': '<REDACTED>',
                'LOG_LEVEL': 'INFO',
                'AGENT_SERVICE_URL': 'https://bhiv-hr-agent-m1me.onrender.com'
            },
            'portal': {
                'API_KEY_SECRET': '<REDACTED>',
                'ENVIRONMENT': 'production',
                'GATEWAY_URL': 'https://bhiv-hr-gateway-46pz.onrender.com',
                'JWT_SECRET_KEY': '<REDACTED>',
                'LOG_LEVEL': 'INFO',
                'AGENT_SERVICE_URL': 'https://bhiv-hr-agent-m1me.onrender.com'
            },
            'client_portal': {
                'API_KEY_SECRET': '<REDACTED>',
                'DATABASE_URL': '<REDACTED>',
                'ENVIRONMENT': 'production',
                'GATEWAY_URL': 'https://bhiv-hr-gateway-46pz.onrender.com',
                'JWT_SECRET_KEY': '<REDACTED>',
                'LOG_LEVEL': 'INFO',
                'AGENT_SERVICE_URL': 'https://bhiv-hr-agent-m1me.onrender.com'
            }
        }
    
    def generate_audit_report(self) -> str:
        """Generate comprehensive audit report"""
        missing_vars = self.analyze_missing_variables()
        recommended_config = self.generate_recommended_config()
        
        report = []
        report.append("BHIV HR Platform - Render Environment Variables Audit")
        report.append("=" * 60)
        
        # Issues found
        report.append("\nISSUES IDENTIFIED:")
        report.append("1. JWT_SECRET should be JWT_SECRET_KEY (standardization)")
        report.append("2. Missing AGENT_SERVICE_URL in some services")
        report.append("3. Inconsistent variable naming across services")
        report.append("4. DATABASE_URL has malformed mailto: prefix")
        
        # Current vs Recommended
        report.append("\nCURRENT vs RECOMMENDED CONFIG:")
        
        for service in ['agent', 'gateway', 'portal', 'client_portal']:
            report.append(f"\n{service.upper()} SERVICE:")
            current = self.current_render_config[service]
            recommended = recommended_config[service]
            
            # Variables to add
            to_add = set(recommended.keys()) - set(current.keys())
            if to_add:
                report.append(f"   ADD: {', '.join(to_add)}")
            
            # Variables to modify
            to_modify = []
            for key in set(current.keys()) & set(recommended.keys()):
                if current[key] != recommended[key]:
                    to_modify.append(key)
            if to_modify:
                report.append(f"   MODIFY: {', '.join(to_modify)}")
            
            # Variables to remove
            to_remove = set(current.keys()) - set(recommended.keys())
            if to_remove:
                report.append(f"   REMOVE: {', '.join(to_remove)}")
        
        # Detailed recommendations
        report.append("\nDETAILED RECOMMENDATIONS:")
        
        report.append("\n1. STANDARDIZE JWT VARIABLE:")
        report.append("   - Change JWT_SECRET → JWT_SECRET_KEY in all services")
        
        report.append("\n2. FIX DATABASE URL:")
        report.append("   - Remove 'mailto:' prefix from DATABASE_URL")
        report.append("   - Use proper PostgreSQL connection string format")
        
        report.append("\n3. ADD MISSING VARIABLES:")
        report.append("   - Add AGENT_SERVICE_URL to all services that need it")
        report.append("   - Add GATEWAY_SERVICE_URL to agent service")
        
        report.append("\n4. REMOVE UNNECESSARY VARIABLES:")
        report.append("   - Remove OBSERVABILITY_ENABLED (not used in code)")
        report.append("   - Remove PYTHON_VERSION (managed by Render)")
        report.append("   - Remove SECRET_KEY from gateway (duplicate)")
        
        return "\n".join(report)

def main():
    project_root = Path(__file__).parent.parent
    auditor = RenderEnvironmentAuditor(project_root)
    
    print("BHIV HR Platform - Render Environment Audit")
    print("=" * 50)
    
    # Generate and display report
    report = auditor.generate_audit_report()
    print(report)
    
    # Save report
    report_file = project_root / 'render_environment_audit.txt'
    with open(report_file, 'w') as f:
        f.write(report)
    
    print(f"\n📄 Report saved to: {report_file}")
    
    # Generate recommended config JSON
    recommended_config = auditor.generate_recommended_config()
    config_file = project_root / 'recommended_render_config.json'
    with open(config_file, 'w') as f:
        json.dump(recommended_config, f, indent=2)
    
    print(f"📄 Recommended config saved to: {config_file}")

if __name__ == '__main__':
    main()