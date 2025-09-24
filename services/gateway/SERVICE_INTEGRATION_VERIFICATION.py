#!/usr/bin/env python3
"""
BHIV HR Platform - Service Integration Verification
Checks if all services are in sync and properly integrated after database changes
"""

import asyncio
import aiohttp
import json
import time
from datetime import datetime
from typing import Dict, List, Any

class ServiceIntegrationVerifier:
    def __init__(self):
        self.services = {
            "gateway": {
                "local": "http://localhost:8000",
                "production": "https://bhiv-hr-gateway-901a.onrender.com"
            },
            "agent": {
                "local": "http://localhost:9000", 
                "production": "https://bhiv-hr-agent-o6nx.onrender.com"
            },
            "portal": {
                "local": "http://localhost:8501",
                "production": "https://bhiv-hr-portal-xk2k.onrender.com"
            },
            "client_portal": {
                "local": "http://localhost:8502",
                "production": "https://bhiv-hr-client-portal-zdbt.onrender.com"
            }
        }
        
        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {"Authorization": f"Bearer {self.api_key}"}
        
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "services": {},
            "integration_tests": {},
            "database_sync": {},
            "overall_status": "unknown"
        }

    async def check_service_health(self, session: aiohttp.ClientSession, service: str, env: str) -> Dict[str, Any]:
        """Check individual service health"""
        url = self.services[service][env]
        health_endpoint = f"{url}/health"
        
        try:
            async with session.get(health_endpoint, timeout=10) as response:
                if response.status == 200:
                    data = await response.json()
                    return {
                        "status": "healthy",
                        "response_time": response.headers.get("X-Response-Time", "unknown"),
                        "data": data
                    }
                else:
                    return {
                        "status": "unhealthy",
                        "error": f"HTTP {response.status}",
                        "response_time": "timeout"
                    }
        except Exception as e:
            return {
                "status": "unreachable",
                "error": str(e),
                "response_time": "timeout"
            }

    async def check_database_integration(self, session: aiohttp.ClientSession, env: str) -> Dict[str, Any]:
        """Check database integration across services"""
        gateway_url = self.services["gateway"][env]
        
        tests = {
            "database_health": f"{gateway_url}/v1/health",
            "database_stats": f"{gateway_url}/v1/stats", 
            "candidates_list": f"{gateway_url}/v1/candidates",
            "jobs_list": f"{gateway_url}/v1/jobs",
            "interviews_list": f"{gateway_url}/v1/interviews"
        }
        
        results = {}
        
        for test_name, url in tests.items():
            try:
                async with session.get(url, headers=self.headers, timeout=10) as response:
                    if response.status == 200:
                        data = await response.json()
                        results[test_name] = {
                            "status": "success",
                            "data_count": len(data.get("candidates", data.get("jobs", data.get("interviews", [])))),
                            "response_time": response.headers.get("X-Response-Time", "unknown")
                        }
                    else:
                        results[test_name] = {
                            "status": "failed",
                            "error": f"HTTP {response.status}"
                        }
            except Exception as e:
                results[test_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results

    async def test_ai_matching_integration(self, session: aiohttp.ClientSession, env: str) -> Dict[str, Any]:
        """Test AI matching service integration"""
        gateway_url = self.services["gateway"][env]
        agent_url = self.services["agent"][env]
        
        tests = {
            "gateway_ai_endpoint": f"{gateway_url}/v1/match/1/top?limit=5",
            "agent_health": f"{agent_url}/health",
            "agent_matching": f"{agent_url}/match/candidates/1?limit=5"
        }
        
        results = {}
        
        for test_name, url in tests.items():
            try:
                headers = self.headers if "gateway" in test_name else {}
                async with session.get(url, headers=headers, timeout=15) as response:
                    if response.status == 200:
                        data = await response.json()
                        results[test_name] = {
                            "status": "success",
                            "matches_count": len(data.get("matches", data.get("top_candidates", []))),
                            "algorithm_version": data.get("algorithm_version", "unknown")
                        }
                    else:
                        results[test_name] = {
                            "status": "failed", 
                            "error": f"HTTP {response.status}"
                        }
            except Exception as e:
                results[test_name] = {
                    "status": "error",
                    "error": str(e)
                }
        
        return results

    async def test_portal_integration(self, session: aiohttp.ClientSession, env: str) -> Dict[str, Any]:
        """Test portal integration with gateway"""
        portal_url = self.services["portal"][env]
        client_portal_url = self.services["client_portal"][env]
        
        tests = {
            "hr_portal": portal_url,
            "client_portal": client_portal_url
        }
        
        results = {}
        
        for test_name, url in tests.items():
            try:
                async with session.get(url, timeout=10) as response:
                    results[test_name] = {
                        "status": "accessible" if response.status == 200 else "inaccessible",
                        "http_status": response.status,
                        "content_type": response.headers.get("content-type", "unknown")
                    }
            except Exception as e:
                results[test_name] = {
                    "status": "unreachable",
                    "error": str(e)
                }
        
        return results

    async def test_crud_operations(self, session: aiohttp.ClientSession, env: str) -> Dict[str, Any]:
        """Test CRUD operations to verify database sync"""
        gateway_url = self.services["gateway"][env]
        
        # Test job creation
        job_data = {
            "title": "Integration Test Job",
            "department": "Testing",
            "location": "Remote",
            "experience_level": "Mid-Level",
            "requirements": "Integration testing skills",
            "description": "Test job for integration verification"
        }
        
        results = {}
        
        try:
            # Create job
            async with session.post(
                f"{gateway_url}/v1/jobs",
                headers={**self.headers, "Content-Type": "application/json"},
                json=job_data,
                timeout=10
            ) as response:
                if response.status == 200:
                    job_result = await response.json()
                    job_id = job_result.get("job_id")
                    results["job_creation"] = {
                        "status": "success",
                        "job_id": job_id
                    }
                    
                    # Test job retrieval
                    async with session.get(f"{gateway_url}/v1/jobs", headers=self.headers, timeout=10) as get_response:
                        if get_response.status == 200:
                            jobs_data = await get_response.json()
                            job_found = any(job.get("id") == job_id for job in jobs_data.get("jobs", []))
                            results["job_retrieval"] = {
                                "status": "success" if job_found else "failed",
                                "job_found": job_found,
                                "total_jobs": len(jobs_data.get("jobs", []))
                            }
                        else:
                            results["job_retrieval"] = {"status": "failed", "error": f"HTTP {get_response.status}"}
                else:
                    results["job_creation"] = {"status": "failed", "error": f"HTTP {response.status}"}
                    
        except Exception as e:
            results["crud_operations"] = {"status": "error", "error": str(e)}
        
        return results

    async def verify_environment(self, env: str) -> Dict[str, Any]:
        """Verify all services in specific environment"""
        print(f"\n🔍 Verifying {env.upper()} environment...")
        
        async with aiohttp.ClientSession() as session:
            env_results = {
                "environment": env,
                "services": {},
                "database_integration": {},
                "ai_matching": {},
                "portal_integration": {},
                "crud_operations": {}
            }
            
            # Check individual service health
            for service in self.services.keys():
                print(f"  Checking {service}...")
                env_results["services"][service] = await self.check_service_health(session, service, env)
            
            # Check database integration
            print(f"  Checking database integration...")
            env_results["database_integration"] = await self.check_database_integration(session, env)
            
            # Check AI matching integration
            print(f"  Checking AI matching integration...")
            env_results["ai_matching"] = await self.test_ai_matching_integration(session, env)
            
            # Check portal integration
            print(f"  Checking portal integration...")
            env_results["portal_integration"] = await self.test_portal_integration(session, env)
            
            # Test CRUD operations
            print(f"  Testing CRUD operations...")
            env_results["crud_operations"] = await self.test_crud_operations(session, env)
            
            return env_results

    def analyze_results(self, results: Dict[str, Any]) -> str:
        """Analyze verification results and determine overall status"""
        issues = []
        healthy_services = 0
        total_services = 0
        
        for env, env_data in results.items():
            if env == "timestamp":
                continue
                
            for service, service_data in env_data.get("services", {}).items():
                total_services += 1
                if service_data.get("status") == "healthy":
                    healthy_services += 1
                else:
                    issues.append(f"{env}/{service}: {service_data.get('status', 'unknown')}")
            
            # Check database integration
            db_tests = env_data.get("database_integration", {})
            failed_db_tests = [test for test, result in db_tests.items() if result.get("status") != "success"]
            if failed_db_tests:
                issues.append(f"{env}/database: {len(failed_db_tests)} tests failed")
            
            # Check AI matching
            ai_tests = env_data.get("ai_matching", {})
            failed_ai_tests = [test for test, result in ai_tests.items() if result.get("status") != "success"]
            if failed_ai_tests:
                issues.append(f"{env}/ai_matching: {len(failed_ai_tests)} tests failed")
        
        if not issues:
            return "✅ ALL_SERVICES_SYNCHRONIZED"
        elif len(issues) <= 2:
            return "⚠️ MINOR_ISSUES_DETECTED"
        else:
            return "❌ MAJOR_INTEGRATION_ISSUES"

    async def run_verification(self) -> Dict[str, Any]:
        """Run complete service integration verification"""
        print("🚀 Starting BHIV HR Platform Service Integration Verification")
        print("=" * 60)
        
        start_time = time.time()
        
        # Verify both environments
        for env in ["production", "local"]:
            try:
                self.results[env] = await self.verify_environment(env)
            except Exception as e:
                print(f"❌ Failed to verify {env} environment: {e}")
                self.results[env] = {"error": str(e)}
        
        # Analyze results
        self.results["overall_status"] = self.analyze_results(self.results)
        self.results["verification_time"] = f"{time.time() - start_time:.2f}s"
        
        return self.results

    def print_summary(self):
        """Print verification summary"""
        print("\n" + "=" * 60)
        print("📊 SERVICE INTEGRATION VERIFICATION SUMMARY")
        print("=" * 60)
        
        print(f"🕐 Timestamp: {self.results['timestamp']}")
        print(f"⏱️ Verification Time: {self.results.get('verification_time', 'unknown')}")
        print(f"🎯 Overall Status: {self.results['overall_status']}")
        
        for env in ["production", "local"]:
            if env in self.results and "services" in self.results[env]:
                print(f"\n🌍 {env.upper()} Environment:")
                
                services = self.results[env]["services"]
                healthy = sum(1 for s in services.values() if s.get("status") == "healthy")
                total = len(services)
                print(f"  Services: {healthy}/{total} healthy")
                
                for service, data in services.items():
                    status_icon = "✅" if data.get("status") == "healthy" else "❌"
                    print(f"    {status_icon} {service}: {data.get('status', 'unknown')}")
                
                # Database integration
                db_tests = self.results[env].get("database_integration", {})
                db_success = sum(1 for t in db_tests.values() if t.get("status") == "success")
                db_total = len(db_tests)
                if db_total > 0:
                    print(f"  Database Integration: {db_success}/{db_total} tests passed")
                
                # AI matching
                ai_tests = self.results[env].get("ai_matching", {})
                ai_success = sum(1 for t in ai_tests.values() if t.get("status") == "success")
                ai_total = len(ai_tests)
                if ai_total > 0:
                    print(f"  AI Matching: {ai_success}/{ai_total} tests passed")

async def main():
    """Main verification function"""
    verifier = ServiceIntegrationVerifier()
    
    try:
        results = await verifier.run_verification()
        verifier.print_summary()
        
        # Save results to file
        with open("service_integration_results.json", "w") as f:
            json.dump(results, f, indent=2)
        
        print(f"\n💾 Detailed results saved to: service_integration_results.json")
        
        # Return exit code based on status
        if "ALL_SERVICES_SYNCHRONIZED" in results["overall_status"]:
            return 0
        elif "MINOR_ISSUES" in results["overall_status"]:
            return 1
        else:
            return 2
            
    except Exception as e:
        print(f"❌ Verification failed: {e}")
        return 3

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    exit(exit_code)