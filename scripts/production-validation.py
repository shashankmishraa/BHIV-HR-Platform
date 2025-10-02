#!/usr/bin/env python3
"""
BHIV HR Platform - Production Validation Script
Comprehensive testing of production deployment
"""

import requests
import time
import sys
from typing import Dict, List, Tuple
import argparse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductionValidator:
    """Validates production deployment"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_urls = {
            'gateway': 'bhiv-hr-gateway-46pz.onrender.com',
            'agent': 'bhiv-hr-agent-m1me.onrender.com',
            'portal': 'bhiv-hr-portal-cead.onrender.com',
            'client_portal': 'bhiv-hr-client-portal-5g33.onrender.com'
        }
        self.headers = {'Authorization': f'Bearer {api_key}'}
        self.results = []
    
    def test_endpoint(self, name: str, method: str, url: str, headers: Dict = None, 
                     data: Dict = None, timeout: int = 30) -> Tuple[bool, str, int]:
        """Test a single endpoint"""
        try:
            if method.upper() == 'GET':
                response = requests.get(url, headers=headers, timeout=timeout)
            elif method.upper() == 'POST':
                response = requests.post(url, headers=headers, json=data, timeout=timeout)
            else:
                return False, f"Unsupported method: {method}", 0
            
            success = response.status_code in [200, 201]
            message = f"Status: {response.status_code}"
            
            if success and response.headers.get('content-type', '').startswith('application/json'):
                try:
                    json_data = response.json()
                    if 'status' in json_data:
                        message += f", Service: {json_data.get('status', 'unknown')}"
                except:
                    pass
            
            return success, message, response.status_code
            
        except requests.exceptions.Timeout:
            return False, "Request timeout", 408
        except requests.exceptions.ConnectionError:
            return False, "Connection failed", 0
        except Exception as e:
            return False, f"Error: {str(e)}", 0
    
    def validate_gateway(self) -> List[Tuple[str, bool, str]]:
        """Validate API Gateway"""
        logger.info("🔍 Validating API Gateway...")
        
        tests = [
            ("Health Check", "GET", f"{self.base_urls['gateway']}/health", None),
            ("Jobs List", "GET", f"{self.base_urls['gateway']}/v1/jobs", self.headers),
            ("Candidates Search", "GET", f"{self.base_urls['gateway']}/v1/candidates/search", self.headers),
            ("Rate Limit Status", "GET", f"{self.base_urls['gateway']}/v1/security/rate-limit-status", self.headers),
            ("Metrics", "GET", f"{self.base_urls['gateway']}/metrics", None),
            ("Detailed Health", "GET", f"{self.base_urls['gateway']}/health/detailed", None)
        ]
        
        results = []
        for test_name, method, url, headers in tests:
            success, message, status_code = self.test_endpoint(test_name, method, url, headers)
            results.append((test_name, success, message))
            
            if success:
                logger.info(f"✅ {test_name}: {message}")
            else:
                logger.error(f"❌ {test_name}: {message}")
            
            time.sleep(1)  # Rate limiting
        
        return results
    
    def validate_ai_agent(self) -> List[Tuple[str, bool, str]]:
        """Validate AI Agent"""
        logger.info("🤖 Validating AI Agent...")
        
        tests = [
            ("Health Check", "GET", f"{self.base_urls['agent']}/health", None),
            ("Database Test", "GET", f"{self.base_urls['agent']}/test-db", None),
            ("AI Matching", "POST", f"{self.base_urls['agent']}/match", None, {"job_id": 1})
        ]
        
        results = []
        for test_name, method, url, headers, *data in tests:
            test_data = data[0] if data else None
            success, message, status_code = self.test_endpoint(test_name, method, url, headers, test_data, timeout=60)
            results.append((test_name, success, message))
            
            if success:
                logger.info(f"✅ {test_name}: {message}")
            else:
                logger.error(f"❌ {test_name}: {message}")
            
            time.sleep(2)  # AI agent needs more time
        
        return results
    
    def validate_portals(self) -> List[Tuple[str, bool, str]]:
        """Validate Web Portals"""
        logger.info("🌐 Validating Web Portals...")
        
        tests = [
            ("HR Portal", "GET", self.base_urls['portal'], None),
            ("Client Portal", "GET", self.base_urls['client_portal'], None)
        ]
        
        results = []
        for test_name, method, url, headers in tests:
            success, message, status_code = self.test_endpoint(test_name, method, url, headers, timeout=45)
            results.append((test_name, success, message))
            
            if success:
                logger.info(f"✅ {test_name}: {message}")
            else:
                logger.error(f"❌ {test_name}: {message}")
            
            time.sleep(2)
        
        return results
    
    def validate_security_features(self) -> List[Tuple[str, bool, str]]:
        """Validate Security Features"""
        logger.info("🔒 Validating Security Features...")
        
        tests = [
            ("2FA Demo Setup", "GET", f"{self.base_urls['gateway']}/v1/2fa/demo-setup", self.headers),
            ("Password Policy", "GET", f"{self.base_urls['gateway']}/v1/password/policy", self.headers),
            ("Security Headers", "GET", f"{self.base_urls['gateway']}/v1/security/security-headers-test", self.headers),
            ("Input Validation", "POST", f"{self.base_urls['gateway']}/v1/security/test-input-validation", 
             self.headers, {"input_data": "test input"})
        ]
        
        results = []
        for test_name, method, url, headers, *data in tests:
            test_data = data[0] if data else None
            success, message, status_code = self.test_endpoint(test_name, method, url, headers, test_data)
            results.append((test_name, success, message))
            
            if success:
                logger.info(f"✅ {test_name}: {message}")
            else:
                logger.error(f"❌ {test_name}: {message}")
            
            time.sleep(1)
        
        return results
    
    def run_comprehensive_validation(self) -> Dict[str, List[Tuple[str, bool, str]]]:
        """Run all validation tests"""
        logger.info("🚀 Starting Comprehensive Production Validation")
        logger.info("=" * 60)
        
        validation_results = {}
        
        # Test Gateway
        validation_results['gateway'] = self.validate_gateway()
        
        # Test AI Agent
        validation_results['agent'] = self.validate_ai_agent()
        
        # Test Portals
        validation_results['portals'] = self.validate_portals()
        
        # Test Security
        validation_results['security'] = self.validate_security_features()
        
        return validation_results
    
    def generate_report(self, results: Dict[str, List[Tuple[str, bool, str]]]) -> str:
        """Generate validation report"""
        report = []
        report.append("BHIV HR Platform - Production Validation Report")
        report.append("=" * 60)
        report.append(f"Validation Time: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}")
        report.append("")
        
        total_tests = 0
        passed_tests = 0
        
        for category, test_results in results.items():
            report.append(f"📊 {category.upper()} VALIDATION")
            report.append("-" * 30)
            
            category_passed = 0
            for test_name, success, message in test_results:
                status = "✅ PASS" if success else "❌ FAIL"
                report.append(f"{status} {test_name}: {message}")
                
                total_tests += 1
                if success:
                    passed_tests += 1
                    category_passed += 1
            
            success_rate = (category_passed / len(test_results)) * 100 if test_results else 0
            report.append(f"Category Success Rate: {success_rate:.1f}% ({category_passed}/{len(test_results)})")
            report.append("")
        
        # Overall summary
        overall_success_rate = (passed_tests / total_tests) * 100 if total_tests else 0
        report.append("📈 OVERALL SUMMARY")
        report.append("-" * 20)
        report.append(f"Total Tests: {total_tests}")
        report.append(f"Passed: {passed_tests}")
        report.append(f"Failed: {total_tests - passed_tests}")
        report.append(f"Success Rate: {overall_success_rate:.1f}%")
        report.append("")
        
        if overall_success_rate >= 90:
            report.append("🎉 PRODUCTION STATUS: EXCELLENT")
        elif overall_success_rate >= 75:
            report.append("✅ PRODUCTION STATUS: GOOD")
        elif overall_success_rate >= 60:
            report.append("⚠️  PRODUCTION STATUS: NEEDS ATTENTION")
        else:
            report.append("❌ PRODUCTION STATUS: CRITICAL ISSUES")
        
        report.append("")
        report.append("🌐 Production URLs:")
        for service, url in self.base_urls.items():
            report.append(f"   - {service.title()}: {url}")
        
        report.append("")
        report.append("🔑 Test Credentials:")
        report.append("   - Client Portal: TECH001 / demo123")
        
        return "\n".join(report)

def main():
    parser = argparse.ArgumentParser(description='BHIV HR Platform Production Validation')
    parser.add_argument('--api-key', required=True, help='Production API key for testing')
    parser.add_argument('--output', '-o', help='Output file for report')
    parser.add_argument('--quick', action='store_true', help='Run quick validation (skip AI tests)')
    
    args = parser.parse_args()
    
    validator = ProductionValidator(args.api_key)
    
    if args.quick:
        logger.info("🏃 Running quick validation (skipping AI tests)")
        results = {
            'gateway': validator.validate_gateway(),
            'portals': validator.validate_portals(),
            'security': validator.validate_security_features()
        }
    else:
        results = validator.run_comprehensive_validation()
    
    # Generate report
    report = validator.generate_report(results)
    
    # Output report
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        logger.info(f"📄 Report saved to: {args.output}")
    else:
        print("\n" + report)
    
    # Exit with appropriate code
    total_tests = sum(len(test_results) for test_results in results.values())
    passed_tests = sum(sum(1 for _, success, _ in test_results if success) for test_results in results.values())
    success_rate = (passed_tests / total_tests) * 100 if total_tests else 0
    
    if success_rate >= 90:
        logger.info("🎉 Validation completed successfully!")
        sys.exit(0)
    elif success_rate >= 75:
        logger.warning("⚠️  Validation completed with warnings")
        sys.exit(0)
    else:
        logger.error("❌ Validation failed - critical issues detected")
        sys.exit(1)

if __name__ == '__main__':
    main()