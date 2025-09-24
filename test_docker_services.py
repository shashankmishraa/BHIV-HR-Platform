#!/usr/bin/env python3
"""
BHIV HR Platform - Docker Services Test
Quick test to verify Docker services are running correctly
"""

import requests
import time
import json
from datetime import datetime

def test_service_health(service_name, url, timeout=10):
    """Test individual service health"""
    try:
        print(f"Testing {service_name}...")
        response = requests.get(url, timeout=timeout)
        
        if response.status_code == 200:
            print(f"✅ {service_name}: HEALTHY")
            try:
                data = response.json()
                if 'status' in data:
                    print(f"   Status: {data['status']}")
                if 'timestamp' in data:
                    print(f"   Timestamp: {data['timestamp']}")
            except:
                pass
            return True
        else:
            print(f"❌ {service_name}: UNHEALTHY (Status: {response.status_code})")
            return False
            
    except requests.exceptions.ConnectionError:
        print(f"❌ {service_name}: CONNECTION REFUSED")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ {service_name}: TIMEOUT")
        return False
    except Exception as e:
        print(f"❌ {service_name}: ERROR - {str(e)}")
        return False

def test_database_endpoints():
    """Test database-specific endpoints"""
    print("\n🗄️ Testing Database Endpoints...")
    
    endpoints = [
        ("Database Health", "http://localhost:8000/database/health"),
        ("Database Stats", "http://localhost:8000/database/stats"),
        ("Jobs Count", "http://localhost:8000/database/jobs/count"),
        ("Candidates Count", "http://localhost:8000/database/candidates/count")
    ]
    
    results = []
    for name, url in endpoints:
        try:
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {name}: OK")
                try:
                    data = response.json()
                    if 'count' in data:
                        print(f"   Count: {data['count']}")
                    elif 'database_status' in data:
                        print(f"   DB Status: {data['database_status']}")
                except:
                    pass
                results.append(True)
            else:
                print(f"❌ {name}: Status {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            results.append(False)
    
    return results

def test_ai_endpoints():
    """Test AI agent endpoints"""
    print("\n🤖 Testing AI Agent Endpoints...")
    
    endpoints = [
        ("AI Health", "http://localhost:9000/health"),
        ("AI Status", "http://localhost:9000/"),
        ("Match Candidates", "http://localhost:9000/match-candidates")
    ]
    
    results = []
    for name, url in endpoints:
        try:
            if "match-candidates" in url:
                # POST request with sample data
                payload = {
                    "job_id": 1,
                    "requirements": ["Python", "SQL"],
                    "limit": 5
                }
                response = requests.post(url, json=payload, timeout=5)
            else:
                response = requests.get(url, timeout=5)
                
            if response.status_code == 200:
                print(f"✅ {name}: OK")
                results.append(True)
            else:
                print(f"❌ {name}: Status {response.status_code}")
                results.append(False)
        except Exception as e:
            print(f"❌ {name}: {str(e)}")
            results.append(False)
    
    return results

def main():
    print("🐳 BHIV HR Platform - Docker Services Test")
    print("=" * 50)
    print(f"Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Test core services
    services = [
        ("Gateway Service", "http://localhost:8000/health"),
        ("AI Agent Service", "http://localhost:9000/health"),
        ("HR Portal", "http://localhost:8501"),
        ("Client Portal", "http://localhost:8502")
    ]
    
    print("🔍 Testing Core Services...")
    service_results = []
    for name, url in services:
        result = test_service_health(name, url)
        service_results.append(result)
        time.sleep(1)  # Brief pause between tests
    
    # Test database endpoints if gateway is up
    db_results = []
    if service_results[0]:  # Gateway is up
        db_results = test_database_endpoints()
    
    # Test AI endpoints if agent is up
    ai_results = []
    if len(service_results) > 1 and service_results[1]:  # AI Agent is up
        ai_results = test_ai_endpoints()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    total_tests = len(service_results) + len(db_results) + len(ai_results)
    passed_tests = sum(service_results) + sum(db_results) + sum(ai_results)
    
    print(f"✅ Passed: {passed_tests}/{total_tests}")
    print(f"❌ Failed: {total_tests - passed_tests}/{total_tests}")
    
    if total_tests > 0:
        success_rate = (passed_tests / total_tests) * 100
        print(f"📈 Success Rate: {success_rate:.1f}%")
        
        if success_rate >= 80:
            print("\n🎉 DOCKER SERVICES RUNNING WELL!")
        elif success_rate >= 60:
            print("\n⚠️ SOME SERVICES NEED ATTENTION")
        else:
            print("\n🚨 MULTIPLE SERVICE ISSUES DETECTED")
    
    # Quick fix suggestions
    if not service_results[0]:  # Gateway down
        print("\n💡 Quick Fix: Try 'docker-compose restart gateway'")
    if len(service_results) > 1 and not service_results[1]:  # Agent down
        print("💡 Quick Fix: Try 'docker-compose restart agent'")
    if len(db_results) > 0 and not any(db_results):
        print("💡 Database Issue: Check PostgreSQL container status")

if __name__ == "__main__":
    main()