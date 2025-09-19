#!/usr/bin/env python3
"""
Live Endpoint Verification Script
Fetches actual endpoints from deployed services
"""

import requests
import json
from typing import Dict, List

def get_openapi_endpoints(service_url: str, service_name: str) -> Dict:
    """Get endpoints from OpenAPI docs"""
    try:
        # Try OpenAPI JSON endpoint
        response = requests.get(f"{service_url}/openapi.json", timeout=10)
        if response.status_code == 200:
            openapi_data = response.json()
            paths = openapi_data.get('paths', {})
            
            endpoints = []
            for path, methods in paths.items():
                for method, details in methods.items():
                    if method.upper() in ['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'HEAD', 'OPTIONS']:
                        endpoints.append({
                            'method': method.upper(),
                            'path': path,
                            'summary': details.get('summary', ''),
                            'tags': details.get('tags', [])
                        })
            
            return {
                'service': service_name,
                'url': service_url,
                'status': 'success',
                'total_endpoints': len(endpoints),
                'endpoints': endpoints
            }
    except Exception as e:
        return {
            'service': service_name,
            'url': service_url,
            'status': 'error',
            'error': str(e),
            'total_endpoints': 0,
            'endpoints': []
        }

def verify_service_health(service_url: str) -> bool:
    """Check if service is accessible"""
    try:
        response = requests.get(f"{service_url}/health", timeout=5)
        return response.status_code == 200
    except:
        try:
            response = requests.get(service_url, timeout=5)
            return response.status_code == 200
        except:
            return False

def main():
    services = [
        ("https://bhiv-hr-gateway.onrender.com", "Gateway Service"),
        ("https://bhiv-hr-agent.onrender.com", "AI Agent Service")
    ]
    
    results = {}
    
    print("Verifying Live Endpoints from Deployed Services")
    print("=" * 60)
    
    for service_url, service_name in services:
        print(f"\nChecking {service_name}: {service_url}")
        
        # Check health first
        is_healthy = verify_service_health(service_url)
        print(f"   Health Status: {'Online' if is_healthy else 'Offline'}")
        
        if is_healthy:
            # Get endpoints
            endpoint_data = get_openapi_endpoints(service_url, service_name)
            results[service_name] = endpoint_data
            
            print(f"   Total Endpoints: {endpoint_data['total_endpoints']}")
            
            # Group by tags
            tags_count = {}
            for endpoint in endpoint_data['endpoints']:
                for tag in endpoint.get('tags', ['Untagged']):
                    tags_count[tag] = tags_count.get(tag, 0) + 1
            
            print(f"   Endpoint Categories: {len(tags_count)}")
            for tag, count in sorted(tags_count.items()):
                print(f"     - {tag}: {count} endpoints")
        else:
            results[service_name] = {
                'service': service_name,
                'url': service_url,
                'status': 'offline',
                'total_endpoints': 0,
                'endpoints': []
            }
    
    # Generate summary
    total_endpoints = sum(r['total_endpoints'] for r in results.values())
    online_services = sum(1 for r in results.values() if r['status'] == 'success')
    
    print(f"\nSUMMARY")
    print(f"   Services Online: {online_services}/{len(services)}")
    print(f"   Total Live Endpoints: {total_endpoints}")
    
    # Save detailed results
    with open('live_endpoints_verification.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nDetailed results saved to: live_endpoints_verification.json")
    
    # Generate markdown report
    generate_markdown_report(results, total_endpoints)

def generate_markdown_report(results: Dict, total_endpoints: int):
    """Generate markdown report of live endpoints"""
    
    report = f"""# Live Endpoints Verification Report
**Generated**: {requests.get('http://worldtimeapi.org/api/timezone/UTC').json()['datetime'][:19] if True else 'Unknown'}
**Total Live Endpoints**: {total_endpoints}

## Service Status
"""
    
    for service_name, data in results.items():
        status_icon = "✅" if data['status'] == 'success' else "❌"
        report += f"- **{service_name}**: {data['status'].title()} ({data['total_endpoints']} endpoints)\n"
    
    report += "\n## Detailed Endpoint Listing\n\n"
    
    for service_name, data in results.items():
        if data['status'] == 'success':
            report += f"### {service_name} ({data['total_endpoints']} endpoints)\n"
            report += f"**Service URL**: {data['url']}\n\n"
            
            # Group by tags
            endpoints_by_tag = {}
            for endpoint in data['endpoints']:
                tags = endpoint.get('tags', ['Untagged'])
                for tag in tags:
                    if tag not in endpoints_by_tag:
                        endpoints_by_tag[tag] = []
                    endpoints_by_tag[tag].append(endpoint)
            
            for tag, endpoints in sorted(endpoints_by_tag.items()):
                report += f"#### {tag} ({len(endpoints)} endpoints)\n"
                for endpoint in sorted(endpoints, key=lambda x: (x['method'], x['path'])):
                    method_color = {
                        'GET': '[GET]', 'POST': '[POST]', 'PUT': '[PUT]', 
                        'DELETE': '[DELETE]', 'PATCH': '[PATCH]', 'HEAD': '[HEAD]', 'OPTIONS': '[OPTIONS]'
                    }.get(endpoint['method'], '[?]')
                    
                    summary = endpoint.get('summary', '').strip()
                    summary_text = f" - {summary}" if summary else ""
                    
                    report += f"- {method_color} `{endpoint['path']}`{summary_text}\n"
                report += "\n"
        else:
            report += f"### {service_name}\n"
            report += f"**Status**: {data['status'].title()}\n"
            report += f"**URL**: {data['url']}\n\n"
    
    # Save report
    with open('LIVE_ENDPOINTS_REPORT.md', 'w') as f:
        f.write(report)
    
    print(f"Markdown report saved to: LIVE_ENDPOINTS_REPORT.md")

if __name__ == "__main__":
    main()