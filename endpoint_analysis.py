#!/usr/bin/env python3
"""
Comprehensive Endpoint Analysis Tool
Tests all live service endpoints and identifies non-functional ones
"""

import asyncio
import httpx
import json
import time
from typing import Dict, List, Any
from datetime import datetime


class EndpointAnalyzer:
    def __init__(self):
        self.gateway_url = "https://bhiv-hr-gateway-901a.onrender.com"
        self.agent_url = "https://bhiv-hr-agent-o6nx.onrender.com"
        self.portal_url = "https://bhiv-hr-portal-xk2k.onrender.com"
        self.client_portal_url = "https://bhiv-hr-client-portal-zdbt.onrender.com"

        self.api_key = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        self.results = {
            "functional": [],
            "non_functional": [],
            "errors": [],
            "summary": {},
        }

    async def test_endpoint(
        self, client: httpx.AsyncClient, method: str, url: str, data: Dict = None
    ) -> Dict:
        """Test a single endpoint"""
        try:
            start_time = time.time()

            if method.upper() == "GET":
                response = await client.get(url, headers=self.headers, timeout=10.0)
            elif method.upper() == "POST":
                response = await client.post(
                    url, headers=self.headers, json=data, timeout=10.0
                )
            elif method.upper() == "PUT":
                response = await client.put(
                    url, headers=self.headers, json=data, timeout=10.0
                )
            elif method.upper() == "DELETE":
                response = await client.delete(url, headers=self.headers, timeout=10.0)
            else:
                return {"error": f"Unsupported method: {method}"}

            response_time = time.time() - start_time

            return {
                "method": method,
                "url": url,
                "status_code": response.status_code,
                "response_time": response_time,
                "success": 200 <= response.status_code < 300,
                "response_size": len(response.content),
                "headers": dict(response.headers),
                "content": response.text[:500] if response.text else "",
            }

        except Exception as e:
            return {"method": method, "url": url, "error": str(e), "success": False}

    async def test_gateway_endpoints(self, client: httpx.AsyncClient):
        """Test Gateway Service endpoints"""
        endpoints = [
            # Core endpoints
            ("GET", f"{self.gateway_url}/health"),
            ("GET", f"{self.gateway_url}/"),
            ("GET", f"{self.gateway_url}/docs"),
            # Jobs endpoints
            ("GET", f"{self.gateway_url}/v1/jobs"),
            (
                "POST",
                f"{self.gateway_url}/v1/jobs",
                {
                    "title": "Test Job",
                    "description": "Test Description",
                    "requirements": ["Python", "FastAPI"],
                    "location": "Remote",
                    "salary_range": {"min": 50000, "max": 80000},
                },
            ),
            ("GET", f"{self.gateway_url}/v1/jobs/1"),
            # Candidates endpoints
            ("GET", f"{self.gateway_url}/v1/candidates"),
            (
                "POST",
                f"{self.gateway_url}/v1/candidates",
                {
                    "name": "Test Candidate",
                    "email": "test@example.com",
                    "skills": ["Python", "FastAPI"],
                    "experience": 3,
                },
            ),
            ("GET", f"{self.gateway_url}/v1/candidates/1"),
            # Auth endpoints
            (
                "POST",
                f"{self.gateway_url}/v1/auth/login",
                {"username": "test", "password": "test123"},
            ),
            ("GET", f"{self.gateway_url}/v1/auth/me"),
            # Monitoring endpoints
            ("GET", f"{self.gateway_url}/health/detailed"),
            ("GET", f"{self.gateway_url}/monitoring/errors"),
            ("GET", f"{self.gateway_url}/monitoring/dependencies"),
            ("GET", f"{self.gateway_url}/metrics"),
            # Workflow endpoints
            ("GET", f"{self.gateway_url}/v1/workflows"),
            (
                "POST",
                f"{self.gateway_url}/v1/workflows/trigger",
                {"workflow_type": "candidate_screening", "data": {"candidate_id": 1}},
            ),
        ]

        for method, url, *data in endpoints:
            payload = data[0] if data else None
            result = await self.test_endpoint(client, method, url, payload)

            if result.get("success"):
                self.results["functional"].append(result)
            else:
                self.results["non_functional"].append(result)

    async def test_agent_endpoints(self, client: httpx.AsyncClient):
        """Test AI Agent Service endpoints"""
        endpoints = [
            # Core endpoints
            ("GET", f"{self.agent_url}/health"),
            ("GET", f"{self.agent_url}/"),
            ("GET", f"{self.agent_url}/docs"),
            # Matching endpoints
            (
                "POST",
                f"{self.agent_url}/v1/match/candidates",
                {"job_id": 1, "requirements": ["Python", "FastAPI"], "limit": 5},
            ),
            (
                "POST",
                f"{self.agent_url}/v1/match/score",
                {"candidate_id": 1, "job_id": 1},
            ),
            (
                "POST",
                f"{self.agent_url}/v1/match/bulk",
                {"job_ids": [1, 2], "candidate_ids": [1, 2, 3]},
            ),
            # Analytics endpoints
            ("GET", f"{self.agent_url}/v1/analytics/performance"),
            ("GET", f"{self.agent_url}/v1/analytics/metrics"),
        ]

        for method, url, *data in endpoints:
            payload = data[0] if data else None
            result = await self.test_endpoint(client, method, url, payload)

            if result.get("success"):
                self.results["functional"].append(result)
            else:
                self.results["non_functional"].append(result)

    async def test_portal_endpoints(self, client: httpx.AsyncClient):
        """Test Portal accessibility"""
        endpoints = [("GET", self.portal_url), ("GET", self.client_portal_url)]

        for method, url in endpoints:
            result = await self.test_endpoint(client, method, url)

            if result.get("success"):
                self.results["functional"].append(result)
            else:
                self.results["non_functional"].append(result)

    async def run_analysis(self):
        """Run comprehensive endpoint analysis"""
        print("🔍 Starting Comprehensive Endpoint Analysis...")

        async with httpx.AsyncClient() as client:
            # Test all services
            await self.test_gateway_endpoints(client)
            await self.test_agent_endpoints(client)
            await self.test_portal_endpoints(client)

        # Generate summary
        total_endpoints = len(self.results["functional"]) + len(
            self.results["non_functional"]
        )
        functional_count = len(self.results["functional"])
        non_functional_count = len(self.results["non_functional"])

        self.results["summary"] = {
            "total_endpoints": total_endpoints,
            "functional": functional_count,
            "non_functional": non_functional_count,
            "success_rate": (
                (functional_count / total_endpoints * 100) if total_endpoints > 0 else 0
            ),
            "timestamp": datetime.now().isoformat(),
        }

        return self.results

    def print_results(self):
        """Print analysis results"""
        print("\n" + "=" * 80)
        print("📊 ENDPOINT ANALYSIS RESULTS")
        print("=" * 80)

        summary = self.results["summary"]
        print(f"Total Endpoints Tested: {summary['total_endpoints']}")
        print(f"Functional: {summary['functional']} ({summary['success_rate']:.1f}%)")
        print(f"Non-Functional: {summary['non_functional']}")

        if self.results["non_functional"]:
            print("\n❌ NON-FUNCTIONAL ENDPOINTS:")
            print("-" * 50)
            for endpoint in self.results["non_functional"]:
                print(f"  {endpoint['method']} {endpoint['url']}")
                if "status_code" in endpoint:
                    print(f"    Status: {endpoint['status_code']}")
                if "error" in endpoint:
                    print(f"    Error: {endpoint['error']}")
                print()

        if self.results["functional"]:
            print("\n✅ FUNCTIONAL ENDPOINTS:")
            print("-" * 50)
            for endpoint in self.results["functional"][:10]:  # Show first 10
                print(
                    f"  {endpoint['method']} {endpoint['url']} - {endpoint['status_code']} ({endpoint.get('response_time', 0):.2f}s)"
                )

            if len(self.results["functional"]) > 10:
                print(f"  ... and {len(self.results['functional']) - 10} more")


async def main():
    analyzer = EndpointAnalyzer()
    results = await analyzer.run_analysis()
    analyzer.print_results()

    # Save results to file
    with open("endpoint_analysis_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print(f"\n📄 Detailed results saved to: endpoint_analysis_results.json")


if __name__ == "__main__":
    asyncio.run(main())
