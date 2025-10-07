#!/usr/bin/env python3
"""
BHIV HR Platform - Simple Codebase Audit
"""

import os
import json
import re
from datetime import datetime
from pathlib import Path

def audit_codebase():
    """Perform comprehensive codebase audit"""
    print("Starting comprehensive codebase audit...")
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'files_analyzed': 0,
        'issues_found': [],
        'endpoints_found': [],
        'recent_changes': [],
        'documentation_status': {}
    }
    
    # Key files to analyze
    key_files = [
        'services/gateway/app/main.py',
        'services/agent/app.py',
        'services/portal/app.py', 
        'services/client_portal/app.py',
        'README.md',
        'PROJECT_STRUCTURE.md',
        'COMPREHENSIVE_ROUTING_ANALYSIS.md'
    ]
    
    for file_path in key_files:
        if os.path.exists(file_path):
            print(f"Analyzing {file_path}...")
            analyze_file(file_path, results)
            results['files_analyzed'] += 1
    
    # Check for specific issues
    check_search_endpoint_issue(results)
    check_documentation_sync(results)
    
    # Generate report
    generate_report(results)
    
    return results

def analyze_file(file_path, results):
    """Analyze individual file"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check for recent changes
        recent_patterns = [
            'CandidateSearch',
            'pool_size=10',
            'timeout-keep-alive',
            '@validator',
            'comprehensive.*audit'
        ]
        
        for pattern in recent_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                results['recent_changes'].append({
                    'file': file_path,
                    'pattern': pattern
                })
        
        # Extract endpoints
        if file_path.endswith('.py') and 'app' in file_path:
            endpoint_matches = re.finditer(r'@app\.(get|post|put|delete)\("([^"]+)"', content)
            for match in endpoint_matches:
                results['endpoints_found'].append({
                    'file': file_path,
                    'method': match.group(1).upper(),
                    'path': match.group(2)
                })
        
        # Check for issues
        if 'CandidateSearch = Depends()' in content:
            results['issues_found'].append({
                'file': file_path,
                'type': 'search_endpoint_depends_issue',
                'description': 'Search endpoint uses Depends() which causes 422 errors',
                'severity': 'high',
                'fixed': 'skills: Optional[str] = None' in content
            })
        
    except Exception as e:
        results['issues_found'].append({
            'file': file_path,
            'type': 'file_read_error',
            'error': str(e)
        })

def check_search_endpoint_issue(results):
    """Check if the search endpoint issue has been resolved"""
    print("Checking search endpoint issue...")
    
    gateway_file = 'services/gateway/app/main.py'
    if os.path.exists(gateway_file):
        with open(gateway_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check current implementation
        if 'def search_candidates(' in content:
            # Extract the function signature
            func_match = re.search(r'def search_candidates\((.*?)\):', content, re.DOTALL)
            if func_match:
                signature = func_match.group(1)
                
                if 'CandidateSearch = Depends()' in signature:
                    results['issues_found'].append({
                        'type': 'search_endpoint_validation',
                        'description': 'Search endpoint still uses Depends() - causes 422 errors',
                        'status': 'UNRESOLVED',
                        'fix_needed': 'Replace with individual Optional parameters'
                    })
                elif 'skills: Optional[str] = None' in signature:
                    results['issues_found'].append({
                        'type': 'search_endpoint_validation', 
                        'description': 'Search endpoint has been fixed with Optional parameters',
                        'status': 'RESOLVED',
                        'fix_applied': 'Individual Optional parameters used'
                    })

def check_documentation_sync(results):
    """Check documentation synchronization"""
    print("Checking documentation sync...")
    
    # Check README
    if os.path.exists('README.md'):
        with open('README.md', 'r', encoding='utf-8') as f:
            readme_content = f.read()
        
        # Count actual endpoints
        total_endpoints = len(results['endpoints_found'])
        
        # Check if README reflects current state
        if '48 endpoints' in readme_content:
            if total_endpoints != 48:
                results['documentation_status']['readme_endpoint_count'] = {
                    'status': 'OUTDATED',
                    'readme_claims': 48,
                    'actual_found': total_endpoints
                }
            else:
                results['documentation_status']['readme_endpoint_count'] = {
                    'status': 'CURRENT'
                }
        
        # Check for recent features
        recent_features = [
            'connection pooling',
            'pydantic validation',
            'timeout optimization'
        ]
        
        for feature in recent_features:
            if feature.lower() in readme_content.lower():
                results['documentation_status'][f'{feature}_documented'] = True
            else:
                results['documentation_status'][f'{feature}_documented'] = False

def generate_report(results):
    """Generate audit report"""
    print("Generating audit report...")
    
    report = f"""# BHIV HR Platform - Codebase Audit Report

**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Files Analyzed**: {results['files_analyzed']}

## Summary

### Issues Analysis
- **Total Issues Found**: {len(results['issues_found'])}
- **High Severity**: {len([i for i in results['issues_found'] if i.get('severity') == 'high'])}
- **Resolved Issues**: {len([i for i in results['issues_found'] if i.get('status') == 'RESOLVED'])}

### Endpoints Detected
- **Total Endpoints**: {len(results['endpoints_found'])}

### Recent Changes
- **Modifications Detected**: {len(results['recent_changes'])}

## Detailed Findings

### Search Endpoint Issue Status
"""
    
    # Check search endpoint status
    search_issues = [i for i in results['issues_found'] if 'search_endpoint' in i.get('type', '')]
    if search_issues:
        for issue in search_issues:
            status = issue.get('status', 'UNKNOWN')
            report += f"- **Status**: {status}\n"
            report += f"- **Description**: {issue['description']}\n"
            if 'fix_applied' in issue:
                report += f"- **Fix Applied**: {issue['fix_applied']}\n"
            elif 'fix_needed' in issue:
                report += f"- **Fix Needed**: {issue['fix_needed']}\n"
    else:
        report += "- No search endpoint issues detected\n"
    
    report += """

### Documentation Status
"""
    
    for key, value in results['documentation_status'].items():
        if isinstance(value, dict):
            report += f"- **{key}**: {value.get('status', 'Unknown')}\n"
        else:
            status = "DOCUMENTED" if value else "MISSING"
            report += f"- **{key}**: {status}\n"
    
    report += """

### Endpoints by Service
"""
    
    # Group endpoints by service
    endpoints_by_service = {}
    for endpoint in results['endpoints_found']:
        service = endpoint['file'].split('/')[1] if '/' in endpoint['file'] else 'root'
        if service not in endpoints_by_service:
            endpoints_by_service[service] = []
        endpoints_by_service[service].append(endpoint)
    
    for service, endpoints in endpoints_by_service.items():
        report += f"- **{service}**: {len(endpoints)} endpoints\n"
    
    # Save report
    with open('CODEBASE_AUDIT_REPORT.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Save JSON results
    with open('audit_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print("Report saved to CODEBASE_AUDIT_REPORT.md")
    print("Results saved to audit_results.json")

def main():
    results = audit_codebase()
    
    print("\n" + "="*50)
    print("AUDIT COMPLETE")
    print("="*50)
    print(f"Files Analyzed: {results['files_analyzed']}")
    print(f"Issues Found: {len(results['issues_found'])}")
    print(f"Endpoints Found: {len(results['endpoints_found'])}")
    print(f"Recent Changes: {len(results['recent_changes'])}")
    
    # Show critical findings
    high_severity = [i for i in results['issues_found'] if i.get('severity') == 'high']
    if high_severity:
        print(f"\nCRITICAL ISSUES: {len(high_severity)}")
        for issue in high_severity:
            print(f"  - {issue.get('description', 'Unknown issue')}")
    
    resolved_issues = [i for i in results['issues_found'] if i.get('status') == 'RESOLVED']
    if resolved_issues:
        print(f"\nRESOLVED ISSUES: {len(resolved_issues)}")
        for issue in resolved_issues:
            print(f"  - {issue.get('description', 'Unknown issue')}")

if __name__ == "__main__":
    main()