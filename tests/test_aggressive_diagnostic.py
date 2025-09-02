"""
Aggressive Enterprise Diagnostic Suite
Comprehensive internal and external port 8000 analysis
"""

import subprocess
import socket
import time
import requests
import json
from typing import Dict, List, Tuple
import concurrent.futures

class AggressiveDiagnostic:
    """Enterprise-level aggressive diagnostic for port 8000 issues"""
    
    def __init__(self):
        self.results = {}
        self.critical_issues = []
        self.warnings = []
    
    def run_full_diagnostic(self) -> Dict:
        """Run complete aggressive diagnostic suite"""
        print("=" * 80)
        print("AGGRESSIVE ENTERPRISE DIAGNOSTIC - PORT 8000 ANALYSIS")
        print("=" * 80)
        
        diagnostics = [
            ("Docker Container Status", self.check_docker_containers),
            ("Port Binding Analysis", self.check_port_binding),
            ("Network Connectivity", self.check_network_connectivity),
            ("Service Health Internal", self.check_service_health_internal),
            ("Process Analysis", self.check_process_analysis),
            ("Container Logs Analysis", self.check_container_logs),
            ("Network Interface Check", self.check_network_interfaces),
            ("Firewall Analysis", self.check_firewall_status),
            ("DNS Resolution", self.check_dns_resolution),
            ("External Connectivity", self.check_external_connectivity),
            ("Load Testing", self.perform_load_testing),
            ("Security Scan", self.perform_security_scan)
        ]
        
        for name, diagnostic_func in diagnostics:
            print(f"\n[CHECKING] {name}...")
            try:
                result = diagnostic_func()
                self.results[name] = result
                if not result.get("status", False):
                    self.critical_issues.append(f"{name}: {result.get('error', 'Unknown issue')}")
                elif result.get("warning"):
                    self.warnings.append(f"{name}: {result.get('warning')}")
            except Exception as e:
                error_msg = f"{name}: FAILED - {str(e)}"
                self.critical_issues.append(error_msg)
                self.results[name] = {"status": False, "error": str(e)}
        
        return self.generate_report()
    
    def check_docker_containers(self) -> Dict:
        """Check Docker container status"""
        try:
            # Check if containers are running
            result = subprocess.run(
                ["docker", "ps", "--format", "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}"],
                capture_output=True, text=True, cwd="c:\\bhiv hr ai platform"
            )
            
            if result.returncode != 0:
                return {"status": False, "error": f"Docker command failed: {result.stderr}"}
            
            containers = result.stdout
            gateway_running = "bhivhraiplatform-gateway-1" in containers
            
            # Check specific gateway container
            gateway_result = subprocess.run(
                ["docker", "inspect", "bhivhraiplatform-gateway-1"],
                capture_output=True, text=True, cwd="c:\\bhiv hr ai platform"
            )
            
            gateway_info = {}
            if gateway_result.returncode == 0:
                import json
                gateway_data = json.loads(gateway_result.stdout)[0]
                gateway_info = {
                    "state": gateway_data["State"]["Status"],
                    "health": gateway_data["State"].get("Health", {}).get("Status", "N/A"),
                    "ports": gateway_data["NetworkSettings"]["Ports"],
                    "restart_count": gateway_data["RestartCount"]
                }
            
            return {
                "status": gateway_running,
                "containers_output": containers,
                "gateway_info": gateway_info,
                "error": None if gateway_running else "Gateway container not running"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_port_binding(self) -> Dict:
        """Aggressive port binding analysis"""
        try:
            # Check if port 8000 is bound
            result = subprocess.run(
                ["netstat", "-an"], capture_output=True, text=True
            )
            
            port_8000_lines = [line for line in result.stdout.split('\n') if ':8000' in line]
            
            # Check what's listening on port 8000
            listening_8000 = [line for line in port_8000_lines if 'LISTENING' in line or 'LISTEN' in line]
            
            # Try to connect to port 8000
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)
            port_connectable = sock.connect_ex(('localhost', 8000)) == 0
            sock.close()
            
            return {
                "status": len(listening_8000) > 0,
                "port_8000_lines": port_8000_lines,
                "listening_processes": listening_8000,
                "port_connectable": port_connectable,
                "error": None if len(listening_8000) > 0 else "Port 8000 not listening"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_network_connectivity(self) -> Dict:
        """Check network connectivity to port 8000"""
        try:
            connectivity_tests = {}
            
            # Test different connection methods
            test_urls = [
                "http://localhost:8000",
                "http://127.0.0.1:8000",
                "http://0.0.0.0:8000"
            ]
            
            for url in test_urls:
                try:
                    response = requests.get(f"{url}/health", timeout=5, 
                                          headers={"Authorization": "Bearer myverysecureapikey123"})
                    connectivity_tests[url] = {
                        "status": response.status_code,
                        "connectable": True,
                        "response_time": response.elapsed.total_seconds()
                    }
                except requests.exceptions.ConnectionError:
                    connectivity_tests[url] = {"connectable": False, "error": "Connection refused"}
                except requests.exceptions.Timeout:
                    connectivity_tests[url] = {"connectable": False, "error": "Timeout"}
                except Exception as e:
                    connectivity_tests[url] = {"connectable": False, "error": str(e)}
            
            any_connectable = any(test.get("connectable", False) for test in connectivity_tests.values())
            
            return {
                "status": any_connectable,
                "connectivity_tests": connectivity_tests,
                "error": None if any_connectable else "No connectivity to port 8000"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_service_health_internal(self) -> Dict:
        """Internal service health check"""
        try:
            # Check if we can exec into container
            health_result = subprocess.run(
                ["docker", "exec", "bhivhraiplatform-gateway-1", "curl", "-f", "http://localhost:8000/health"],
                capture_output=True, text=True, cwd="c:\\bhiv hr ai platform"
            )
            
            internal_healthy = health_result.returncode == 0
            
            # Check container processes
            ps_result = subprocess.run(
                ["docker", "exec", "bhivhraiplatform-gateway-1", "ps", "aux"],
                capture_output=True, text=True, cwd="c:\\bhiv hr ai platform"
            )
            
            processes = ps_result.stdout if ps_result.returncode == 0 else "Failed to get processes"
            uvicorn_running = "uvicorn" in processes
            
            return {
                "status": internal_healthy and uvicorn_running,
                "internal_health": internal_healthy,
                "health_response": health_result.stdout if internal_healthy else health_result.stderr,
                "uvicorn_running": uvicorn_running,
                "processes": processes,
                "error": None if internal_healthy else "Internal health check failed"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_process_analysis(self) -> Dict:
        """Analyze running processes"""
        try:
            # Check Docker processes
            docker_ps = subprocess.run(
                ["docker", "ps", "-a", "--format", "table {{.Names}}\\t{{.Status}}\\t{{.Ports}}\\t{{.Command}}"],
                capture_output=True, text=True, cwd="c:\\bhiv hr ai platform"
            )
            
            # Check system processes on port 8000
            tasklist_result = subprocess.run(
                ["tasklist", "/FI", "IMAGENAME eq python.exe"],
                capture_output=True, text=True
            )
            
            return {
                "status": True,
                "docker_processes": docker_ps.stdout,
                "python_processes": tasklist_result.stdout,
                "analysis": "Process analysis completed"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_container_logs(self) -> Dict:
        """Analyze container logs for errors"""
        try:
            # Get recent logs
            logs_result = subprocess.run(
                ["docker", "logs", "--tail", "50", "bhivhraiplatform-gateway-1"],
                capture_output=True, text=True, cwd="c:\\bhiv hr ai platform"
            )
            
            logs = logs_result.stdout + logs_result.stderr
            
            # Look for error patterns
            error_patterns = ["ERROR", "CRITICAL", "Exception", "Traceback", "Failed", "refused"]
            errors_found = []
            
            for line in logs.split('\n'):
                for pattern in error_patterns:
                    if pattern.lower() in line.lower():
                        errors_found.append(line.strip())
            
            return {
                "status": len(errors_found) == 0,
                "recent_logs": logs,
                "errors_found": errors_found,
                "warning": f"Found {len(errors_found)} potential errors" if errors_found else None
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_network_interfaces(self) -> Dict:
        """Check network interfaces and routing"""
        try:
            # Check network interfaces
            ipconfig_result = subprocess.run(
                ["ipconfig", "/all"], capture_output=True, text=True
            )
            
            # Check routing table
            route_result = subprocess.run(
                ["route", "print"], capture_output=True, text=True
            )
            
            return {
                "status": True,
                "network_interfaces": ipconfig_result.stdout,
                "routing_table": route_result.stdout,
                "analysis": "Network interface analysis completed"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_firewall_status(self) -> Dict:
        """Check Windows Firewall status"""
        try:
            firewall_result = subprocess.run(
                ["netsh", "advfirewall", "show", "allprofiles", "state"],
                capture_output=True, text=True
            )
            
            return {
                "status": True,
                "firewall_status": firewall_result.stdout,
                "analysis": "Firewall analysis completed"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_dns_resolution(self) -> Dict:
        """Check DNS resolution"""
        try:
            nslookup_result = subprocess.run(
                ["nslookup", "localhost"], capture_output=True, text=True
            )
            
            return {
                "status": True,
                "dns_resolution": nslookup_result.stdout,
                "analysis": "DNS resolution completed"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def check_external_connectivity(self) -> Dict:
        """Check external connectivity"""
        try:
            # Test external connectivity
            external_tests = {}
            
            test_sites = ["google.com", "github.com", "docker.com"]
            
            for site in test_sites:
                try:
                    response = requests.get(f"https://{site}", timeout=5)
                    external_tests[site] = {"status": response.status_code, "connectable": True}
                except Exception as e:
                    external_tests[site] = {"connectable": False, "error": str(e)}
            
            return {
                "status": True,
                "external_tests": external_tests,
                "analysis": "External connectivity tested"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def perform_load_testing(self) -> Dict:
        """Perform basic load testing"""
        try:
            # Try multiple concurrent connections
            def test_connection():
                try:
                    response = requests.get("http://localhost:8000/health", 
                                          headers={"Authorization": "Bearer myverysecureapikey123"},
                                          timeout=5)
                    return {"status": response.status_code, "success": True}
                except Exception as e:
                    return {"success": False, "error": str(e)}
            
            with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                futures = [executor.submit(test_connection) for _ in range(5)]
                results = [f.result() for f in concurrent.futures.as_completed(futures)]
            
            successful = sum(1 for r in results if r.get("success", False))
            
            return {
                "status": successful > 0,
                "successful_connections": successful,
                "total_attempts": len(results),
                "results": results,
                "error": None if successful > 0 else "All load test connections failed"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def perform_security_scan(self) -> Dict:
        """Perform basic security scan"""
        try:
            # Test different ports and protocols
            security_tests = {}
            
            ports_to_test = [8000, 8501, 8502, 9000, 5432]
            
            for port in ports_to_test:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex(('localhost', port))
                security_tests[f"port_{port}"] = {"open": result == 0}
                sock.close()
            
            return {
                "status": True,
                "port_scan": security_tests,
                "analysis": "Security scan completed"
            }
        except Exception as e:
            return {"status": False, "error": str(e)}
    
    def generate_report(self) -> Dict:
        """Generate comprehensive diagnostic report"""
        print("\n" + "=" * 80)
        print("DIAGNOSTIC REPORT SUMMARY")
        print("=" * 80)
        
        total_tests = len(self.results)
        passed_tests = sum(1 for r in self.results.values() if r.get("status", False))
        
        print(f"Total Tests: {passed_tests}/{total_tests}")
        print(f"Critical Issues: {len(self.critical_issues)}")
        print(f"Warnings: {len(self.warnings)}")
        
        if self.critical_issues:
            print("\nCRITICAL ISSUES:")
            for issue in self.critical_issues:
                print(f"  [FAIL] {issue}")
        
        if self.warnings:
            print("\nWARNINGS:")
            for warning in self.warnings:
                print(f"  [WARN] {warning}")
        
        # Determine root cause
        root_cause = self.determine_root_cause()
        print(f"\nROOT CAUSE ANALYSIS:")
        print(f"  {root_cause}")
        
        # Provide fix recommendations
        fixes = self.get_fix_recommendations()
        print(f"\nRECOMMENDED FIXES:")
        for i, fix in enumerate(fixes, 1):
            print(f"  {i}. {fix}")
        
        return {
            "summary": {
                "total_tests": total_tests,
                "passed_tests": passed_tests,
                "critical_issues": len(self.critical_issues),
                "warnings": len(self.warnings)
            },
            "critical_issues": self.critical_issues,
            "warnings": self.warnings,
            "root_cause": root_cause,
            "recommended_fixes": fixes,
            "detailed_results": self.results
        }
    
    def determine_root_cause(self) -> str:
        """Determine the root cause of port 8000 issues"""
        # Analyze results to determine root cause
        docker_status = self.results.get("Docker Container Status", {}).get("status", False)
        port_binding = self.results.get("Port Binding Analysis", {}).get("status", False)
        network_conn = self.results.get("Network Connectivity", {}).get("status", False)
        
        if not docker_status:
            return "Docker container is not running or not healthy"
        elif not port_binding:
            return "Port 8000 is not bound or listening"
        elif not network_conn:
            return "Network connectivity issues to port 8000"
        else:
            return "Service is running but may have configuration issues"
    
    def get_fix_recommendations(self) -> List[str]:
        """Get fix recommendations based on diagnostic results"""
        fixes = []
        
        docker_status = self.results.get("Docker Container Status", {}).get("status", False)
        if not docker_status:
            fixes.append("Restart Docker containers: docker-compose -f docker-compose.production.yml restart")
            fixes.append("Check Docker daemon is running: docker version")
        
        port_binding = self.results.get("Port Binding Analysis", {}).get("status", False)
        if not port_binding:
            fixes.append("Check port conflicts: netstat -an | findstr :8000")
            fixes.append("Restart gateway service specifically")
        
        container_logs = self.results.get("Container Logs Analysis", {})
        if container_logs.get("errors_found"):
            fixes.append("Check container logs for errors: docker logs bhivhraiplatform-gateway-1")
            fixes.append("Rebuild container: docker-compose build gateway")
        
        if not fixes:
            fixes.append("Perform full system restart")
            fixes.append("Check firewall and antivirus settings")
            fixes.append("Verify Docker Desktop is running")
        
        return fixes

if __name__ == "__main__":
    diagnostic = AggressiveDiagnostic()
    results = diagnostic.run_full_diagnostic()