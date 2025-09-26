#!/usr/bin/env python3
"""
BHIV HR Platform - Service Connection and Routing Audit
Performs detailed verification of all service endpoints, routing, and integrations
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime, timezone
from typing import Dict, List, Any
import requests
import aiohttp
from pathlib import Path

class ServiceConnectionAuditor:
    def __init__(self):
        self.results = {
            "audit_timestamp": datetime.now(timezone.utc).isoformat(),
            "audit_version": "1.0.0",
            "services": {},
            "routing_verification": {},
            "integration_points": {},
            "issues_found": [],
            "recommendations": [],
            "summary": {}
        }
        
        # Production service URLs
        self.services = {
            "gateway": {
                "name": "API Gateway",
                "url": "https://bhiv-hr-gateway-901a.onrender.com",
                "health_endpoint": "/health",
                "docs_endpoint": "/docs",
                "expected_modules": ["core", "candidates", "jobs", "auth", "workflows", "monitoring"]
            },
            "agent": {
                "name": "AI Agent",
                "url": "https://bhiv-hr-agent-o6nx.onrender.com",
                "health_endpoint": "/health",
                "docs_endpoint": "/docs",
                "expected_endpoints": ["/match", "/analyze", "/semantic-status"]
            },
            "portal": {
                "name": "HR Portal",
                "url": "https://bhiv-hr-portal-xk2k.onrender.com",
                "health_endpoint": "/health",
                "expected_components": ["dashboard", "candidate_management", "job_creation"]
            },
            "client_portal": {
                "name": "Client Portal",
                "url": "https://bhiv-hr-client-portal-zdbt.onrender.com",
                "health_endpoint": "/health",
                "expected_features": ["login", "job_search", "application_tracking"]
            }
        }

    async def audit_service_health(self, service_name: str, service_config: Dict) -> Dict:
        """Audit individual service health and connectivity"""
        print(f"[INFO] Auditing {service_config['name']}...")
        
        service_result = {
            "name": service_config["name"],
            "url": service_config["url"],
            "status": "unknown",
            "response_time": None,
            "endpoints_verified": [],
            "issues": [],
            "capabilities": {}
        }
        
        try:
            # Test basic connectivity
            start_time = time.time()
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
                # Test root endpoint
                try:
                    async with session.get(service_config["url"]) as response:
                        service_result["response_time"] = round((time.time() - start_time) * 1000, 2)
                        service_result["status"] = "reachable" if response.status == 200 else f"error_{response.status}"
                        
                        if response.status == 200:
                            try:
                                data = await response.json()
                                service_result["capabilities"] = data
                            except:
                                service_result["capabilities"] = {"content_type": response.content_type}
                        
                        service_result["endpoints_verified"].append({
                            "endpoint": "/",
                            "status": response.status,
                            "response_time": service_result["response_time"]
                        })
                except Exception as e:
                    service_result["issues"].append(f"Root endpoint error: {str(e)}")
                
                # Test health endpoint
                if "health_endpoint" in service_config:
                    try:
                        health_url = service_config["url"] + service_config["health_endpoint"]
                        start_health = time.time()
                        async with session.get(health_url) as response:
                            health_time = round((time.time() - start_health) * 1000, 2)
                            service_result["endpoints_verified"].append({
                                "endpoint": service_config["health_endpoint"],
                                "status": response.status,
                                "response_time": health_time
                            })
                            
                            if response.status == 200:
                                try:
                                    health_data = await response.json()
                                    service_result["health_status"] = health_data
                                except:
                                    service_result["health_status"] = "non_json_response"
                            else:
                                service_result["issues"].append(f"Health endpoint returned {response.status}")
                    except Exception as e:
                        service_result["issues"].append(f"Health endpoint error: {str(e)}")
        
        except Exception as e:
            service_result["status"] = "unreachable"
            service_result["issues"].append(f"Service unreachable: {str(e)}")
        
        return service_result

    async def verify_gateway_routing(self) -> Dict:
        """Verify API Gateway routing and module integration"""
        print("[INFO] Verifying Gateway Routing...")
        
        routing_result = {
            "modules_verified": [],
            "endpoints_tested": [],
            "routing_issues": [],
            "module_integration": {}
        }
        
        gateway_url = self.services["gateway"]["url"]
        
        # Test module endpoints
        module_endpoints = [
            "/system/modules",
            "/system/architecture", 
            "/health/detailed",
            "/metrics",
            "/health/probe"
        ]
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            for endpoint in module_endpoints:
                try:
                    url = gateway_url + endpoint
                    async with session.get(url) as response:
                        routing_result["endpoints_tested"].append({
                            "endpoint": endpoint,
                            "status": response.status,
                            "accessible": response.status == 200
                        })
                        
                        if response.status == 200 and endpoint == "/system/modules":
                            try:
                                data = await response.json()
                                routing_result["module_integration"] = data
                                if "modules" in data:
                                    routing_result["modules_verified"] = [m["name"] for m in data["modules"]]
                            except:
                                routing_result["routing_issues"].append("Failed to parse modules response")
                        elif response.status != 200:
                            routing_result["routing_issues"].append(f"{endpoint} returned {response.status}")
                            
                except Exception as e:
                    routing_result["routing_issues"].append(f"{endpoint} error: {str(e)}")
        
        return routing_result

    async def verify_agent_integration(self) -> Dict:
        """Verify AI Agent service integration and endpoints"""
        print("[INFO] Verifying AI Agent Integration...")
        
        agent_result = {
            "ai_endpoints_verified": [],
            "semantic_engine_status": None,
            "database_connectivity": None,
            "integration_issues": []
        }
        
        agent_url = self.services["agent"]["url"]
        
        # Test AI-specific endpoints
        ai_endpoints = [
            "/semantic-status",
            "/test-db",
            "/status",
            "/version",
            "/v1/models/status"
        ]
        
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            for endpoint in ai_endpoints:
                try:
                    url = agent_url + endpoint
                    async with session.get(url) as response:
                        agent_result["ai_endpoints_verified"].append({
                            "endpoint": endpoint,
                            "status": response.status,
                            "accessible": response.status == 200
                        })
                        
                        if response.status == 200:
                            try:
                                data = await response.json()
                                if endpoint == "/semantic-status":
                                    agent_result["semantic_engine_status"] = data
                                elif endpoint == "/test-db":
                                    agent_result["database_connectivity"] = data
                            except:
                                pass
                        else:
                            agent_result["integration_issues"].append(f"{endpoint} returned {response.status}")
                            
                except Exception as e:
                    agent_result["integration_issues"].append(f"{endpoint} error: {str(e)}")
        
        return agent_result

    def analyze_project_structure(self) -> Dict:
        """Analyze project structure for routing and configuration issues"""
        print("[INFO] Analyzing Project Structure...")
        
        structure_result = {
            "configuration_files": [],
            "routing_files": [],
            "missing_files": [],
            "structure_issues": []
        }
        
        # Check for critical configuration files
        critical_files = [
            "services/gateway/app/main.py",
            "services/agent/app.py", 
            "services/shared/observability.py",
            "services/shared/config.py",
            "config/settings.json"
        ]
        
        project_root = Path("c:/bhiv hr ai platform")
        
        for file_path in critical_files:
            full_path = project_root / file_path
            if full_path.exists():
                structure_result["configuration_files"].append({
                    "file": file_path,
                    "exists": True,
                    "size": full_path.stat().st_size
                })
            else:
                structure_result["missing_files"].append(file_path)
                structure_result["structure_issues"].append(f"Missing critical file: {file_path}")
        
        return structure_result

    async def run_comprehensive_audit(self) -> Dict:
        """Run the complete service audit"""
        print("=" * 80)
        print("COMPREHENSIVE SERVICE CONNECTION AND ROUTING AUDIT")
        print("=" * 80)
        
        # Audit individual services
        for service_name, service_config in self.services.items():
            service_result = await self.audit_service_health(service_name, service_config)
            self.results["services"][service_name] = service_result
        
        # Verify routing
        self.results["routing_verification"] = await self.verify_gateway_routing()
        
        # Verify integrations
        agent_integration = await self.verify_agent_integration()
        
        self.results["integration_points"] = {
            "agent_integration": agent_integration
        }
        
        # Analyze project structure
        self.results["project_structure"] = self.analyze_project_structure()
        
        # Collect all issues
        all_issues = []
        for service_result in self.results["services"].values():
            all_issues.extend(service_result.get("issues", []))
        
        all_issues.extend(self.results["routing_verification"].get("routing_issues", []))
        all_issues.extend(self.results["integration_points"]["agent_integration"].get("integration_issues", []))
        all_issues.extend(self.results["project_structure"].get("structure_issues", []))
        
        self.results["issues_found"] = all_issues
        
        # Generate summary
        self.results["summary"] = {
            "total_services_audited": len(self.services),
            "services_reachable": len([s for s in self.results["services"].values() if s.get("status") == "reachable"]),
            "total_issues_found": len(all_issues),
            "critical_issues": len([i for i in all_issues if "error" in i.lower() or "failed" in i.lower()]),
            "routing_modules_verified": len(self.results["routing_verification"].get("modules_verified", [])),
            "audit_status": "completed",
            "overall_health": "healthy" if len(all_issues) < 5 else "needs_attention"
        }
        
        return self.results

    def save_audit_report(self, filename: str = None):
        """Save audit results to file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"service_connection_audit_report_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"[INFO] Audit report saved to: {filename}")

    def print_audit_summary(self):
        """Print a formatted audit summary"""
        print("\n" + "=" * 80)
        print("SERVICE CONNECTION AUDIT SUMMARY")
        print("=" * 80)
        
        summary = self.results["summary"]
        print(f"Audit Timestamp: {self.results['audit_timestamp']}")
        print(f"Services Audited: {summary['total_services_audited']}")
        print(f"Services Reachable: {summary['services_reachable']}/{summary['total_services_audited']}")
        print(f"Total Issues Found: {summary['total_issues_found']}")
        print(f"Critical Issues: {summary['critical_issues']}")
        print(f"Routing Modules Verified: {summary['routing_modules_verified']}")
        print(f"Overall Health: {summary['overall_health'].upper()}")
        
        print("\nSERVICE STATUS:")
        for service_name, service_result in self.results["services"].items():
            status_icon = "[OK]" if service_result.get("status") == "reachable" else "[ERROR]"
            response_time = service_result.get("response_time", "N/A")
            print(f"  {status_icon} {service_result['name']}: {service_result.get('status', 'unknown')} ({response_time}ms)")
        
        if self.results["issues_found"]:
            print("\nISSUES FOUND:")
            for i, issue in enumerate(self.results["issues_found"][:10], 1):
                print(f"  {i}. {issue}")
            if len(self.results["issues_found"]) > 10:
                print(f"  ... and {len(self.results['issues_found']) - 10} more issues")
        
        print("\n" + "=" * 80)

async def main():
    """Main audit execution"""
    auditor = ServiceConnectionAuditor()
    
    try:
        # Run comprehensive audit
        results = await auditor.run_comprehensive_audit()
        
        # Print summary
        auditor.print_audit_summary()
        
        # Save detailed report
        auditor.save_audit_report()
        
        print("\n[SUCCESS] Comprehensive Service Connection and Routing Audit Completed!")
        
    except Exception as e:
        print(f"[ERROR] Audit failed with error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())