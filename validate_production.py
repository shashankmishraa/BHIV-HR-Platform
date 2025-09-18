#!/usr/bin/env python3
"""Production Validation Script - Verify all upgrades are deployed"""

import requests
import json
from datetime import datetime

def test_production_upgrades():
    """Test all security and performance upgrades in production"""
    base_url = "https://bhiv-hr-agent.onrender.com"
    
    print("🔍 Validating Production Upgrades...")
    
    # Test 1: Real system metrics
    try:
        response = requests.get(f"{base_url}/metrics", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "performance_metrics" in data and "cpu_usage_percent" in data["performance_metrics"]:
                print("✅ Real system metrics (psutil) working")
            else:
                print("❌ System metrics not upgraded")
        else:
            print(f"❌ Metrics endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Metrics test failed: {e}")
    
    # Test 2: Timezone-aware timestamps
    try:
        response = requests.get(f"{base_url}/status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            timestamp = data.get("last_health_check", "")
            if "T" in timestamp and ("Z" in timestamp or "+" in timestamp):
                print("✅ Timezone-aware timestamps working")
            else:
                print("❌ Timestamps not upgraded")
    except Exception as e:
        print(f"❌ Status test failed: {e}")
    
    # Test 3: Enhanced error handling
    try:
        response = requests.get(f"{base_url}/analyze/99999", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "analysis_timestamp" in data:
                print("✅ Enhanced error handling working")
            else:
                print("❌ Error handling not upgraded")
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
    
    print(f"\n📊 Validation completed at {datetime.now()}")

if __name__ == "__main__":
    test_production_upgrades()