#!/usr/bin/env python3
"""
BHIV HR Platform - Check All Services Deployment Status
Verifies all 5 services are operational after deployment
"""

import requests
import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Service URLs
SERVICES = {
    "Gateway API": "https://bhiv-hr-gateway-46pz.onrender.com",
    "AI Agent": "https://bhiv-hr-agent-m1me.onrender.com", 
    "HR Portal": "https://bhiv-hr-portal-cead.onrender.com",
    "Client Portal": "https://bhiv-hr-client-portal-5g33.onrender.com",
    "Candidate Portal": "https://bhiv-hr-candidate-portal.onrender.com"
}

API_KEY = "prod_api_key_XUqM2msdCa4CYIaRywRNXRVc477nlI3AQ-lr6cgTB2o"

def check_service_health(name, url):
    """Check individual service health"""
    try:
        # Try health endpoint
        health_url = f"{url}/health"
        response = requests.get(health_url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            logger.info(f"✅ {name}: {data.get('status', 'healthy')} - {data.get('version', 'N/A')}")
            return True
        else:
            logger.warning(f"⚠️ {name}: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"❌ {name}: Connection failed - {e}")
        return False

def check_api_endpoints():
    """Check key API endpoints"""
    headers = {"Authorization": f"Bearer {API_KEY}"}
    
    endpoints = [
        ("Database Schema", "/v1/database/schema"),
        ("Jobs List", "/v1/jobs"),
        ("Candidates List", "/v1/candidates"),
        ("Health Detailed", "/health/detailed")
    ]
    
    base_url = SERVICES["Gateway API"]
    
    for name, endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if endpoint == "/v1/database/schema":
                    logger.info(f"✅ {name}: Schema v{data.get('schema_version')} - {data.get('total_tables')} tables")
                elif endpoint == "/v1/jobs":
                    logger.info(f"✅ {name}: {len(data)} jobs available")
                elif endpoint == "/v1/candidates":
                    logger.info(f"✅ {name}: {len(data)} candidates")
                else:
                    logger.info(f"✅ {name}: OK")
            else:
                logger.warning(f"⚠️ {name}: HTTP {response.status_code}")
        except Exception as e:
            logger.error(f"❌ {name}: {e}")

def main():
    """Main deployment check"""
    logger.info("🔍 Checking BHIV HR Platform deployment status...")
    logger.info(f"Time: {datetime.now()}")
    
    # Check all services
    healthy_services = 0
    for name, url in SERVICES.items():
        if check_service_health(name, url):
            healthy_services += 1
    
    logger.info(f"\n📊 Service Status: {healthy_services}/{len(SERVICES)} services healthy")
    
    # Check API endpoints
    logger.info("\n🔧 Checking API endpoints...")
    check_api_endpoints()
    
    # Final status
    if healthy_services == len(SERVICES):
        logger.info("\n🎉 All services are operational!")
        logger.info("✅ Deployment verification SUCCESSFUL")
    else:
        logger.warning(f"\n⚠️ {len(SERVICES) - healthy_services} services need attention")

if __name__ == "__main__":
    main()