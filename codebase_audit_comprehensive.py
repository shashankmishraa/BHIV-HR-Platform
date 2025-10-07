#!/usr/bin/env python3
"""
BHIV HR Platform - Comprehensive Codebase Audit & Documentation Sync
Performs thorough analysis of all code changes and updates documentation
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path
import hashlib

class CodebaseAuditor:
    def __init__(self):
        self.root_path = Path(".")
        self.audit_results = {
            'timestamp': datetime.now().isoformat(),
            'files_analyzed': 0,
            'code_changes': [],
            'documentation_updates_needed': [],
            'new_features': [],
            'modified_endpoints': [],
            'config_changes': [],
            'issues_found': []
        }
        
        # Track recent changes
        self.recent_changes = []
        
    def scan_codebase(self):
        """Recursively scan all files for changes"""
        print("🔍 Starting comprehensive codebase audit...")
        
        # Key directories to analyze
        key_dirs = [
            'services/gateway',
            'services/agent', 
            'services/portal',
            'services/client_portal',
            'services/db',
            'docs',
            'tests',
            'tools',
            'config'
        ]
        
        for dir_path in key_dirs:
            if os.path.exists(dir_path):
                self.analyze_directory(dir_path)
        
        # Analyze root files
        self.analyze_root_files()
        
        return self.audit_results
    
    def analyze_directory(self, dir_path):
        """Analyze specific directory for changes"""
        print(f"📁 Analyzing {dir_path}...")
        
        for root, dirs, files in os.walk(dir_path):
            for file in files:
                file_path = os.path.join(root, file)
                if self.should_analyze_file(file_path):
                    self.analyze_file(file_path)
                    self.audit_results['files_analyzed'] += 1
    
    def should_analyze_file(self, file_path):
        """Determine if file should be analyzed"""
        # Include key file types
        extensions = ['.py', '.md', '.yml', '.yaml', '.json', '.sql', '.txt', '.env']
        exclude_patterns = ['__pycache__', '.git', 'node_modules', '.pytest_cache']
        
        # Check extension
        if not any(file_path.endswith(ext) for ext in extensions):
            return False
            
        # Check exclude patterns
        if any(pattern in file_path for pattern in exclude_patterns):
            return False
            
        return True
    
    def analyze_file(self, file_path):
        """Analyze individual file for changes and issues"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                
            # Check for recent modifications based on content patterns
            self.check_recent_changes(file_path, content)
            
            # Check for specific issues
            self.check_for_issues(file_path, content)
            
            # Extract API endpoints
            if file_path.endswith('.py') and 'app' in file_path:
                self.extract_endpoints(file_path, content)
                
            # Check configuration files
            if any(config in file_path for config in ['config', '.env', 'docker', 'requirements']):
                self.analyze_config_file(file_path, content)
                
        except Exception as e:
            self.audit_results['issues_found'].append({
                'file': file_path,
                'type': 'file_read_error',
                'error': str(e)
            })
    
    def check_recent_changes(self, file_path, content):
        """Check for patterns indicating recent changes"""
        recent_patterns = [
            r'# TODO:',
            r'# FIXME:',
            r'# NOTE:',
            r'@validator',
            r'CandidateSearch',
            r'pool_size=10',
            r'timeout-keep-alive',
            r'comprehensive.*audit',
            r'routing.*analysis'
        ]
        
        for pattern in recent_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                self.recent_changes.append({
                    'file': file_path,
                    'pattern': pattern,
                    'type': 'recent_modification'
                })
    
    def check_for_issues(self, file_path, content):
        """Check for specific issues in code"""
        issues = []
        
        # Check for the search endpoint issue
        if 'candidates/search' in content and '@app.get' in content:
            if 'CandidateSearch = Depends()' in content:
                issues.append({
                    'type': 'search_endpoint_issue',
                    'description': 'Search endpoint uses Depends() which may cause 422 errors',
                    'line': self.find_line_number(content, 'CandidateSearch = Depends()'),
                    'severity': 'medium'
                })
        
        # Check for missing imports
        if '@validator' in content and 'from pydantic import' in content:
            if 'validator' not in content.split('from pydantic import')[1].split('\n')[0]:
                issues.append({
                    'type': 'missing_import',
                    'description': 'validator used but not imported from pydantic',
                    'severity': 'high'
                })
        
        # Check for hardcoded values
        hardcoded_patterns = [
            r'prod_api_key_[A-Za-z0-9_-]+',
            r'postgresql://[^"\']+',
            r'https://[^"\']+\.onrender\.com'
        ]
        
        for pattern in hardcoded_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                issues.append({
                    'type': 'hardcoded_value',
                    'description': f'Hardcoded value found: {match.group()[:50]}...',
                    'line': self.find_line_number(content, match.group()),
                    'severity': 'low'
                })
        
        if issues:
            self.audit_results['issues_found'].extend([
                {**issue, 'file': file_path} for issue in issues
            ])
    
    def extract_endpoints(self, file_path, content):
        """Extract API endpoints from Python files"""
        endpoint_patterns = [
            r'@app\.(get|post|put|delete)\("([^"]+)"',
            r'@router\.(get|post|put|delete)\("([^"]+)"'
        ]
        
        for pattern in endpoint_patterns:
            matches = re.finditer(pattern, content)
            for match in matches:
                method = match.group(1).upper()
                path = match.group(2)
                
                self.audit_results['modified_endpoints'].append({
                    'file': file_path,
                    'method': method,
                    'path': path,
                    'line': self.find_line_number(content, match.group())
                })
    
    def analyze_config_file(self, file_path, content):
        """Analyze configuration files for changes"""
        config_items = []
        
        if file_path.endswith('.yml') or file_path.endswith('.yaml'):
            # Docker compose or other YAML configs
            if 'pool_size' in content or 'timeout-keep-alive' in content:
                config_items.append('database_optimization')
            if 'version:' in content:
                version_match = re.search(r'version:\s*["\']?([^"\']+)["\']?', content)
                if version_match:
                    config_items.append(f"version_{version_match.group(1)}")
        
        elif file_path.endswith('requirements.txt'):
            # Check for new dependencies
            lines = content.split('\n')
            for line in lines:
                if '==' in line and any(pkg in line for pkg in ['pydantic', 'fastapi', 'sqlalchemy']):
                    config_items.append(f"dependency_{line.strip()}")
        
        if config_items:
            self.audit_results['config_changes'].append({
                'file': file_path,
                'changes': config_items
            })
    
    def find_line_number(self, content, search_text):
        """Find line number of text in content"""
        lines = content.split('\n')
        for i, line in enumerate(lines, 1):
            if search_text in line:
                return i
        return None
    
    def analyze_root_files(self):
        """Analyze root documentation files"""
        root_files = [
            'README.md',
            'PROJECT_STRUCTURE.md', 
            'DEPLOYMENT_STATUS.md',
            'COMPREHENSIVE_ROUTING_ANALYSIS.md'
        ]
        
        for file_name in root_files:
            if os.path.exists(file_name):
                self.analyze_file(file_name)
    
    def check_documentation_sync(self):
        """Check if documentation is in sync with code changes"""
        print("📚 Checking documentation synchronization...")
        
        # Check if README reflects current endpoints
        if os.path.exists('README.md'):
            with open('README.md', 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            # Check endpoint count
            if '48 endpoints' in readme_content:
                actual_endpoints = len(self.audit_results['modified_endpoints'])
                if actual_endpoints != 48:
                    self.audit_results['documentation_updates_needed'].append({
                        'file': 'README.md',
                        'issue': f'Endpoint count mismatch: README says 48, found {actual_endpoints}',
                        'priority': 'medium'
                    })
        
        # Check if recent changes are documented
        recent_features = [
            'connection pooling',
            'pydantic validation', 
            'timeout optimization',
            'routing analysis'
        ]
        
        for feature in recent_features:
            if not self.is_feature_documented(feature):
                self.audit_results['documentation_updates_needed'].append({
                    'feature': feature,
                    'issue': f'Recent feature "{feature}" not documented',
                    'priority': 'high'
                })
    
    def is_feature_documented(self, feature):
        """Check if feature is documented in main files"""
        doc_files = ['README.md', 'PROJECT_STRUCTURE.md', 'DEPLOYMENT_STATUS.md']
        
        for doc_file in doc_files:
            if os.path.exists(doc_file):
                try:
                    with open(doc_file, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        if feature.lower() in content:
                            return True
                except:
                    continue
        return False
    
    def generate_report(self):
        """Generate comprehensive audit report"""
        print("📊 Generating audit report...")
        
        report = f"""# BHIV HR Platform - Comprehensive Codebase Audit Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Files Analyzed**: {self.audit_results['files_analyzed']}

## 🔍 Audit Summary

### Recent Changes Detected
- **Modified Endpoints**: {len(self.audit_results['modified_endpoints'])}
- **Configuration Changes**: {len(self.audit_results['config_changes'])}
- **Issues Found**: {len(self.audit_results['issues_found'])}
- **Documentation Updates Needed**: {len(self.audit_results['documentation_updates_needed'])}

### 🚨 Critical Issues Found

"""
        
        # Add critical issues
        critical_issues = [issue for issue in self.audit_results['issues_found'] 
                          if issue.get('severity') == 'high']
        
        if critical_issues:
            for issue in critical_issues:
                report += f"- **{issue['file']}**: {issue['description']}\n"
        else:
            report += "✅ No critical issues found\n"
        
        report += f"""

### 📊 Endpoint Analysis
Total endpoints found: {len(self.audit_results['modified_endpoints'])}

"""
        
        # Group endpoints by service
        endpoints_by_service = {}
        for endpoint in self.audit_results['modified_endpoints']:
            service = endpoint['file'].split('/')[1] if '/' in endpoint['file'] else 'root'
            if service not in endpoints_by_service:
                endpoints_by_service[service] = []
            endpoints_by_service[service].append(endpoint)
        
        for service, endpoints in endpoints_by_service.items():
            report += f"**{service.title()}**: {len(endpoints)} endpoints\n"
        
        report += """

### 🔧 Configuration Changes Detected

"""
        
        if self.audit_results['config_changes']:
            for config in self.audit_results['config_changes']:
                report += f"- **{config['file']}**: {', '.join(config['changes'])}\n"
        else:
            report += "No configuration changes detected\n"
        
        report += """

### 📚 Documentation Sync Status

"""
        
        if self.audit_results['documentation_updates_needed']:
            for doc_update in self.audit_results['documentation_updates_needed']:
                priority = doc_update.get('priority', 'medium')
                issue = doc_update.get('issue', doc_update.get('feature', 'Unknown'))
                report += f"- **{priority.upper()}**: {issue}\n"
        else:
            report += "✅ Documentation is in sync with codebase\n"
        
        return report
    
    def save_results(self):
        """Save audit results to files"""
        # Save JSON results
        with open('codebase_audit_results.json', 'w') as f:
            json.dump(self.audit_results, f, indent=2)
        
        # Save report
        report = self.generate_report()
        with open('CODEBASE_AUDIT_REPORT.md', 'w') as f:
            f.write(report)
        
        print(f"📄 Results saved to:")
        print(f"  - codebase_audit_results.json")
        print(f"  - CODEBASE_AUDIT_REPORT.md")

def main():
    auditor = CodebaseAuditor()
    
    # Perform comprehensive scan
    results = auditor.scan_codebase()
    
    # Check documentation sync
    auditor.check_documentation_sync()
    
    # Generate and save report
    auditor.save_results()
    
    # Print summary
    print("\n" + "="*60)
    print("📊 AUDIT COMPLETE")
    print("="*60)
    print(f"Files Analyzed: {results['files_analyzed']}")
    print(f"Issues Found: {len(results['issues_found'])}")
    print(f"Endpoints Detected: {len(results['modified_endpoints'])}")
    print(f"Config Changes: {len(results['config_changes'])}")
    print(f"Doc Updates Needed: {len(results['documentation_updates_needed'])}")
    
    # Show critical issues
    critical = [i for i in results['issues_found'] if i.get('severity') == 'high']
    if critical:
        print(f"\n🚨 CRITICAL ISSUES: {len(critical)}")
        for issue in critical[:3]:
            print(f"  - {issue['file']}: {issue['description']}")
    else:
        print("\n✅ NO CRITICAL ISSUES FOUND")

if __name__ == "__main__":
    main()