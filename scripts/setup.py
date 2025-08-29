#!/usr/bin/env python3
"""
BHIV HR Platform - Complete Setup & Deployment
Minimal script for full platform deployment
"""
import os
import sys
import subprocess
import time
import requests
import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def run_command(cmd, cwd=None):
    """Execute command and return success status"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ {cmd}")
            return True
        else:
            logger.error(f"❌ {cmd}: {result.stderr}")
            return False
    except Exception as e:
        logger.error(f"❌ {cmd}: {str(e)}")
        return False

def check_service(url, name):
    """Check if service is healthy"""
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            logger.info(f"✅ {name} service healthy")
            return True
    except:
        pass
    logger.warning(f"⚠️ {name} service not ready")
    return False

def main():
    """Complete platform setup"""
    logger.info("🚀 BHIV HR Platform Setup Starting...")
    
    # Check prerequisites
    if not run_command("docker --version"):
        logger.error("Docker not found. Please install Docker.")
        return False
    
    if not run_command("docker-compose --version"):
        logger.error("Docker Compose not found. Please install Docker Compose.")
        return False
    
    # Setup environment
    env_content = """DATABASE_URL=postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr
API_KEY_SECRET=myverysecureapikey123
POSTGRES_USER=bhiv_user
POSTGRES_PASSWORD=bhiv_pass
POSTGRES_DB=bhiv_hr"""
    
    with open('.env', 'w') as f:
        f.write(env_content)
    logger.info("✅ Environment configured")
    
    # Build and start services
    logger.info("🔨 Building services...")
    if not run_command("docker-compose build"):
        return False
    
    logger.info("🚀 Starting services...")
    if not run_command("docker-compose up -d"):
        return False
    
    # Wait for services
    logger.info("⏳ Waiting for services...")
    for i in range(30):
        if (check_service("http://localhost:8000/health", "Gateway") and
            check_service("http://localhost:9000/health", "AI Agent")):
            break
        time.sleep(2)
    
    # Process sample data if available
    if os.path.exists("resume"):
        logger.info("📄 Processing sample resumes...")
        run_command("python scripts/simple_enhanced_processor.py")
        run_command("python scripts/final_upload_test.py")
    
    # Success message
    logger.info("🎉 BHIV HR Platform Ready!")
    logger.info("🎯 Portal: http://localhost:8501")
    logger.info("📚 API: http://localhost:8000/docs")
    logger.info("🤖 AI Agent: http://localhost:9000/docs")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)