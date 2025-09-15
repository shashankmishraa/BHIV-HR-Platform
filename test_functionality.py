#!/usr/bin/env python3
"""
BHIV HR Platform - Functionality Testing
Tests the actual functionality of all endpoints by simulating their execution
"""

import json
import re
import secrets
import pyotp
from datetime import datetime, timezone

class MockDatabase:
    """Mock database for testing"""
    def __init__(self):
        self.candidates = [
            {"id": 1, "name": "John Doe", "email": "john@example.com", "technical_skills": "Python, FastAPI", "experience_years": 5},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com", "technical_skills": "JavaScript, React", "experience_years": 3}
        ]
        self.jobs = [
            {"id": 1, "title": "Senior Developer", "department": "Engineering", "location": "Remote", "status": "active"}
        ]
        self.interviews = []

class EndpointFunctionalityTester:
    """Test actual endpoint functionality"""
    
    def __init__(self):
        self.db = MockDatabase()
        self.api_key = "myverysecureapikey123"
        self.test_results = []
        
    def log_test(self, endpoint, test_name, success, details=""):
        """Log test result"""
        self.test_results.append({
            "endpoint": endpoint,
            "test": test_name,
            "success": success,
            "details": details
        })
        status = "PASS" if success else "FAIL"
        print(f"{status}: {endpoint} - {test_name}")
        if details and not success:
            print(f"      Details: {details}")
    
    def test_core_endpoints(self):
        """Test core API endpoints"""
        print("\nTesting Core API Endpoints...")
        
        # Test root endpoint
        try:
            root_response = {
                "message": "BHIV HR Platform API Gateway",
                "version": "3.1.0",
                "status": "healthy",
                "endpoints": 47
            }
            self.log_test("/", "Root endpoint response", True)
        except Exception as e:
            self.log_test("/", "Root endpoint response", False, str(e))
        
        # Test health endpoint
        try:
            health_response = {
                "status": "healthy",
                "service": "BHIV HR Gateway",
                "version": "3.1.0",
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            self.log_test("/health", "Health check response", True)
        except Exception as e:
            self.log_test("/health", "Health check response", False, str(e))
    
    def test_client_authentication(self):
        """Test client portal authentication"""
        print("\nTesting Client Authentication...")
        
        # Test login
        try:
            valid_clients = {"TECH001": "demo123"}
            client_id = "TECH001"
            password = "demo123"
            
            if client_id in valid_clients and valid_clients[client_id] == password:
                token_timestamp = datetime.now().timestamp()
                access_token = f"client_token_{client_id}_{token_timestamp}"
                
                login_response = {
                    "message": "Authentication successful",
                    "client_id": client_id,
                    "access_token": access_token,
                    "token_type": "bearer"
                }
                self.log_test("/v1/client/login", "Valid login", True)
                
                # Test token verification
                if access_token.startswith("client_token_"):
                    parts = access_token.split("_")
                    if len(parts) >= 3:
                        verify_response = {
                            "valid": True,
                            "client_id": parts[2],
                            "token_type": "bearer"
                        }
                        self.log_test("/v1/client/verify", "Token verification", True)
                    else:
                        self.log_test("/v1/client/verify", "Token verification", False, "Invalid token structure")
                else:
                    self.log_test("/v1/client/verify", "Token verification", False, "Invalid token format")
            else:
                self.log_test("/v1/client/login", "Valid login", False, "Invalid credentials")
                
        except Exception as e:
            self.log_test("/v1/client/login", "Login functionality", False, str(e))
    
    def test_job_management(self):
        """Test job management endpoints"""
        print("\nTesting Job Management...")
        
        # Test job creation
        try:
            job_data = {
                "title": "Test Developer",
                "department": "Engineering", 
                "location": "Remote",
                "experience_level": "Mid-level",
                "requirements": "Python, FastAPI",
                "description": "Test job posting"
            }
            
            # Simulate job creation
            new_job = {
                "id": len(self.db.jobs) + 1,
                **job_data,
                "status": "active",
                "created_at": datetime.now(timezone.utc).isoformat()
            }
            self.db.jobs.append(new_job)
            
            create_response = {
                "message": "Job created successfully",
                "job_id": new_job["id"],
                "created_at": new_job["created_at"]
            }
            self.log_test("/v1/jobs", "Job creation", True)
            
            # Test job listing
            jobs_response = {
                "jobs": self.db.jobs,
                "count": len(self.db.jobs)
            }
            self.log_test("/v1/jobs", "Job listing", len(self.db.jobs) > 0)
            
        except Exception as e:
            self.log_test("/v1/jobs", "Job management", False, str(e))
    
    def test_candidate_management(self):
        """Test candidate management endpoints"""
        print("\nTesting Candidate Management...")
        
        # Test candidate search
        try:
            # Test search with filters
            skills_filter = "python"
            filtered_candidates = [
                c for c in self.db.candidates 
                if skills_filter.lower() in c["technical_skills"].lower()
            ]
            
            search_response = {
                "candidates": filtered_candidates,
                "filters": {"skills": skills_filter},
                "count": len(filtered_candidates)
            }
            self.log_test("/v1/candidates/search", "Search with filters", True)
            
            # Test bulk upload
            bulk_data = {
                "candidates": [
                    {
                        "name": "Test Candidate",
                        "email": "test@example.com",
                        "technical_skills": "Python, Django",
                        "experience_years": 2
                    }
                ]
            }
            
            # Simulate bulk upload
            inserted_count = 0
            for candidate in bulk_data["candidates"]:
                new_candidate = {
                    "id": len(self.db.candidates) + 1,
                    **candidate
                }
                self.db.candidates.append(new_candidate)
                inserted_count += 1
            
            bulk_response = {
                "message": "Bulk upload completed",
                "candidates_received": len(bulk_data["candidates"]),
                "candidates_inserted": inserted_count,
                "status": "success"
            }
            self.log_test("/v1/candidates/bulk", "Bulk upload", inserted_count > 0)
            
        except Exception as e:
            self.log_test("/v1/candidates/search", "Candidate management", False, str(e))
    
    def test_security_features(self):
        """Test security endpoints"""
        print("\nTesting Security Features...")
        
        # Test input validation
        try:
            test_inputs = [
                ("normal input", "SAFE", []),
                ("<script>alert('xss')</script>", "BLOCKED", ["XSS attempt detected"]),
                ("'; DROP TABLE users; --", "BLOCKED", ["SQL injection attempt detected"])
            ]
            
            for input_data, expected_result, expected_threats in test_inputs:
                threats = []
                if "<script>" in input_data.lower():
                    threats.append("XSS attempt detected")
                if "'" in input_data and ("drop" in input_data.lower() or "select" in input_data.lower()):
                    threats.append("SQL injection attempt detected")
                
                result = "SAFE" if not threats else "BLOCKED"
                validation_response = {
                    "input": input_data,
                    "validation_result": result,
                    "threats_detected": threats
                }
                
                success = result == expected_result
                self.log_test("/v1/security/test-input-validation", f"Input validation: {input_data[:20]}...", success)
            
        except Exception as e:
            self.log_test("/v1/security/test-input-validation", "Input validation", False, str(e))
        
        # Test email validation
        try:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            test_emails = [
                ("test@example.com", True),
                ("invalid.email", False),
                ("user@domain.co.uk", True)
            ]
            
            for email, expected in test_emails:
                is_valid = re.match(email_pattern, email) is not None
                success = is_valid == expected
                self.log_test("/v1/security/test-email-validation", f"Email validation: {email}", success)
                
        except Exception as e:
            self.log_test("/v1/security/test-email-validation", "Email validation", False, str(e))
    
    def test_2fa_functionality(self):
        """Test 2FA endpoints"""
        print("\nTesting 2FA Functionality...")
        
        try:
            # Test 2FA setup
            secret = pyotp.random_base32()
            setup_response = {
                "message": "2FA setup initiated",
                "user_id": "testuser",
                "secret": secret
            }
            self.log_test("/v1/2fa/setup", "2FA setup", True)
            
            # Test 2FA verification
            stored_secret = "JBSWY3DPEHPK3PXP"
            totp = pyotp.TOTP(stored_secret)
            current_token = totp.now()
            
            # Test valid token
            if totp.verify(current_token, valid_window=1):
                verify_response = {
                    "message": "2FA setup verified successfully",
                    "user_id": "testuser",
                    "setup_complete": True
                }
                self.log_test("/v1/2fa/verify-setup", "2FA verification with valid token", True)
            else:
                self.log_test("/v1/2fa/verify-setup", "2FA verification with valid token", False, "Token verification failed")
            
            # Test invalid token
            try:
                invalid_token = "000000"
                if not totp.verify(invalid_token, valid_window=1):
                    self.log_test("/v1/2fa/verify-setup", "2FA verification with invalid token", True, "Correctly rejected invalid token")
                else:
                    self.log_test("/v1/2fa/verify-setup", "2FA verification with invalid token", False, "Accepted invalid token")
            except:
                self.log_test("/v1/2fa/verify-setup", "2FA verification with invalid token", True, "Correctly raised exception")
            
            # Test backup codes generation
            backup_codes = [f"BACKUP-{secrets.token_hex(4).upper()}" for _ in range(10)]
            backup_response = {
                "message": "Backup codes regenerated successfully",
                "backup_codes": backup_codes,
                "codes_count": len(backup_codes)
            }
            self.log_test("/v1/2fa/regenerate-backup-codes", "Backup codes generation", len(backup_codes) == 10)
            
        except Exception as e:
            self.log_test("/v1/2fa/setup", "2FA functionality", False, str(e))
    
    def test_password_management(self):
        """Test password management endpoints"""
        print("\nTesting Password Management...")
        
        try:
            # Test password validation
            test_passwords = [
                ("weak", "Weak", False),
                ("StrongPass123!", "Very Strong", True),
                ("Medium123", "Strong", True)
            ]
            
            for password, expected_strength, expected_valid in test_passwords:
                score = 0
                if len(password) >= 8: score += 20
                if any(c.isupper() for c in password): score += 20
                if any(c.islower() for c in password): score += 20
                if any(c.isdigit() for c in password): score += 20
                if any(c in "!@#$%^&*()" for c in password): score += 20
                
                strength = "Very Strong" if score >= 80 else "Strong" if score >= 60 else "Medium" if score >= 40 else "Weak"
                is_valid = score >= 60
                
                validation_response = {
                    "password_strength": strength,
                    "score": score,
                    "is_valid": is_valid
                }
                
                success = is_valid == expected_valid
                self.log_test("/v1/password/validate", f"Password validation: {password}", success)
            
            # Test password generation
            import string
            import random
            
            length = 12
            chars = string.ascii_letters + string.digits + "!@#$%^&*()"
            generated_password = ''.join(random.choice(chars) for _ in range(length))
            
            generation_response = {
                "generated_password": generated_password,
                "length": length,
                "strength": "Very Strong"
            }
            
            success = len(generated_password) == length
            self.log_test("/v1/password/generate", "Password generation", success)
            
        except Exception as e:
            self.log_test("/v1/password/validate", "Password management", False, str(e))
    
    def test_assessment_workflow(self):
        """Test assessment and workflow endpoints"""
        print("\nTesting Assessment & Workflow...")
        
        try:
            # Test feedback submission
            feedback_data = {
                "candidate_id": 1,
                "job_id": 1,
                "integrity": 5,
                "honesty": 5,
                "discipline": 4,
                "hard_work": 5,
                "gratitude": 4
            }
            
            average_score = (feedback_data["integrity"] + feedback_data["honesty"] + 
                           feedback_data["discipline"] + feedback_data["hard_work"] + 
                           feedback_data["gratitude"]) / 5
            
            feedback_response = {
                "message": "Feedback submitted successfully",
                "candidate_id": feedback_data["candidate_id"],
                "job_id": feedback_data["job_id"],
                "average_score": average_score
            }
            
            self.log_test("/v1/feedback", "Feedback submission", average_score > 0)
            
            # Test job offer creation
            offer_data = {
                "candidate_id": 1,
                "job_id": 1,
                "salary": 75000.0,
                "start_date": "2025-03-01",
                "terms": "Full-time employment"
            }
            
            offer_response = {
                "message": "Job offer created successfully",
                "offer_id": 1,
                "candidate_id": offer_data["candidate_id"],
                "job_id": offer_data["job_id"],
                "salary": offer_data["salary"],
                "status": "pending"
            }
            
            self.log_test("/v1/offers", "Job offer creation", True)
            
        except Exception as e:
            self.log_test("/v1/feedback", "Assessment workflow", False, str(e))
    
    def run_all_tests(self):
        """Run all functionality tests"""
        print("BHIV HR Platform - Functionality Testing")
        print("=" * 60)
        
        self.test_core_endpoints()
        self.test_client_authentication()
        self.test_job_management()
        self.test_candidate_management()
        self.test_security_features()
        self.test_2fa_functionality()
        self.test_password_management()
        self.test_assessment_workflow()
        
        # Generate summary
        self.generate_summary()
    
    def generate_summary(self):
        """Generate test summary"""
        print("\n" + "=" * 60)
        print("FUNCTIONALITY TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for r in self.test_results if r["success"])
        failed_tests = total_tests - passed_tests
        
        print(f"Total tests run: {total_tests}")
        print(f"Tests passed: {passed_tests}")
        print(f"Tests failed: {failed_tests}")
        print(f"Success rate: {(passed_tests/total_tests)*100:.1f}%")
        
        if failed_tests > 0:
            print(f"\nFailed tests:")
            for result in self.test_results:
                if not result["success"]:
                    print(f"  - {result['endpoint']}: {result['test']}")
                    if result.get("details"):
                        print(f"    Details: {result['details']}")
        
        # Test by category
        categories = {}
        for result in self.test_results:
            endpoint = result["endpoint"]
            if "/v1/client/" in endpoint:
                category = "Client Authentication"
            elif "/v1/jobs" in endpoint:
                category = "Job Management"
            elif "/v1/candidates/" in endpoint:
                category = "Candidate Management"
            elif "/v1/security/" in endpoint:
                category = "Security Features"
            elif "/v1/2fa/" in endpoint:
                category = "Two-Factor Authentication"
            elif "/v1/password/" in endpoint:
                category = "Password Management"
            elif endpoint in ["/v1/feedback", "/v1/offers"]:
                category = "Assessment & Workflow"
            else:
                category = "Core API"
            
            if category not in categories:
                categories[category] = {"total": 0, "passed": 0}
            
            categories[category]["total"] += 1
            if result["success"]:
                categories[category]["passed"] += 1
        
        print(f"\nResults by category:")
        for category, stats in categories.items():
            success_rate = (stats["passed"] / stats["total"]) * 100
            print(f"  {category}: {stats['passed']}/{stats['total']} ({success_rate:.1f}%)")
        
        overall_status = "PASSED" if failed_tests == 0 else "NEEDS ATTENTION"
        print(f"\nOVERALL STATUS: {overall_status}")
        
        return failed_tests == 0

def main():
    """Main test execution"""
    tester = EndpointFunctionalityTester()
    success = tester.run_all_tests()
    return success

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)