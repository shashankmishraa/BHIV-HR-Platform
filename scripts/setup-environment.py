#!/usr/bin/env python3
"""
BHIV HR Platform - Environment Setup Script
Automated setup and validation of development environment
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Dict, List, Optional
import argparse
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class EnvironmentSetup:
    """Handles environment setup and validation"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.environments_dir = project_root / 'environments'
        
    def check_prerequisites(self) -> bool:
        """Check if all prerequisites are installed"""
        logger.info("🔍 Checking prerequisites...")
        
        prerequisites = {
            'docker': 'Docker',
            'docker-compose': 'Docker Compose',
            'python': 'Python 3.8+',
            'git': 'Git'
        }
        
        missing = []
        
        for cmd, name in prerequisites.items():
            if not self._command_exists(cmd):
                missing.append(name)
                logger.error(f"❌ {name} not found")
            else:
                logger.info(f"✅ {name} found")
        
        if missing:
            logger.error(f"Missing prerequisites: {', '.join(missing)}")
            return False
        
        # Check Docker daemon
        try:
            subprocess.run(['docker', 'info'], 
                         capture_output=True, check=True, timeout=10)
            logger.info("✅ Docker daemon is running")
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
            logger.error("❌ Docker daemon is not running")
            return False
        
        return True
    
    def _command_exists(self, command: str) -> bool:
        """Check if a command exists in PATH"""
        return shutil.which(command) is not None
    
    def setup_local_environment(self) -> bool:
        """Setup local development environment"""
        logger.info("🚀 Setting up local development environment...")
        
        # Create local .env file from template
        local_env_path = self.environments_dir / 'local' / '.env'
        local_template_path = self.environments_dir / 'local' / '.env.template'
        
        if not local_env_path.exists() and local_template_path.exists():
            logger.info("📝 Creating local .env file from template...")
            shutil.copy2(local_template_path, local_env_path)
            logger.info(f"✅ Created {local_env_path}")
            logger.warning("⚠️  Please review and update the .env file with your local settings")
        elif local_env_path.exists():
            logger.info("✅ Local .env file already exists")
        else:
            logger.error("❌ Local .env template not found")
            return False
        
        return True
    
    def validate_environment_files(self, environment: str) -> bool:
        """Validate environment configuration files"""
        logger.info(f"🔍 Validating {environment} environment files...")
        
        env_dir = self.environments_dir / environment
        
        if not env_dir.exists():
            logger.error(f"❌ Environment directory not found: {env_dir}")
            return False
        
        # Check for required files
        required_files = ['.env.template']
        if environment == 'local':
            required_files.extend(['docker-compose.yml'])
        
        missing_files = []
        for file_name in required_files:
            file_path = env_dir / file_name
            if not file_path.exists():
                missing_files.append(file_name)
            else:
                logger.info(f"✅ Found {file_name}")
        
        if missing_files:
            logger.error(f"❌ Missing files in {environment}: {', '.join(missing_files)}")
            return False
        
        return True
    
    def test_docker_compose(self) -> bool:
        """Test Docker Compose configuration"""
        logger.info("🐳 Testing Docker Compose configuration...")
        
        compose_file = self.environments_dir / 'local' / 'docker-compose.yml'
        env_file = self.environments_dir / 'local' / '.env'
        
        if not compose_file.exists():
            logger.error(f"❌ Docker Compose file not found: {compose_file}")
            return False
        
        if not env_file.exists():
            logger.error(f"❌ Environment file not found: {env_file}")
            return False
        
        try:
            # Test configuration syntax
            cmd = [
                'docker-compose',
                '-f', str(compose_file),
                '--env-file', str(env_file),
                'config'
            ]
            
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                logger.info("✅ Docker Compose configuration is valid")
                return True
            else:
                logger.error(f"❌ Docker Compose configuration error: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error("❌ Docker Compose validation timed out")
            return False
        except Exception as e:
            logger.error(f"❌ Error testing Docker Compose: {e}")
            return False
    
    def start_services(self, detached: bool = True) -> bool:
        """Start Docker services"""
        logger.info("🚀 Starting Docker services...")
        
        compose_file = self.environments_dir / 'local' / 'docker-compose.yml'
        env_file = self.environments_dir / 'local' / '.env'
        
        cmd = [
            'docker-compose',
            '-f', str(compose_file),
            '--env-file', str(env_file),
            'up'
        ]
        
        if detached:
            cmd.append('-d')
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                timeout=300  # 5 minutes timeout
            )
            
            if result.returncode == 0:
                logger.info("✅ Services started successfully")
                return True
            else:
                logger.error("❌ Failed to start services")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error("❌ Service startup timed out")
            return False
        except KeyboardInterrupt:
            logger.info("🛑 Service startup interrupted by user")
            return False
        except Exception as e:
            logger.error(f"❌ Error starting services: {e}")
            return False
    
    def check_service_health(self) -> Dict[str, bool]:
        """Check health of all services"""
        logger.info("🔍 Checking service health...")
        
        services = {
            'Gateway': 'http://localhost:8000/health',
            'AI Agent': 'http://localhost:9000/health',
            'HR Portal': 'http://localhost:8501/_stcore/health',
            'Client Portal': 'http://localhost:8502/_stcore/health'
        }
        
        health_status = {}
        
        for service_name, health_url in services.items():
            try:
                import urllib.request
                import urllib.error
                
                request = urllib.request.Request(health_url)
                with urllib.request.urlopen(request, timeout=10) as response:
                    if response.status == 200:
                        logger.info(f"✅ {service_name}: Healthy")
                        health_status[service_name] = True
                    else:
                        logger.warning(f"⚠️  {service_name}: Unhealthy (status: {response.status})")
                        health_status[service_name] = False
            
            except urllib.error.URLError as e:
                logger.warning(f"⚠️  {service_name}: Not accessible ({e})")
                health_status[service_name] = False
            except Exception as e:
                logger.warning(f"⚠️  {service_name}: Health check failed ({e})")
                health_status[service_name] = False
        
        return health_status
    
    def stop_services(self) -> bool:
        """Stop Docker services"""
        logger.info("🛑 Stopping Docker services...")
        
        compose_file = self.environments_dir / 'local' / 'docker-compose.yml'
        env_file = self.environments_dir / 'local' / '.env'
        
        cmd = [
            'docker-compose',
            '-f', str(compose_file),
            '--env-file', str(env_file),
            'down'
        ]
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.project_root,
                timeout=60
            )
            
            if result.returncode == 0:
                logger.info("✅ Services stopped successfully")
                return True
            else:
                logger.error("❌ Failed to stop services")
                return False
        
        except Exception as e:
            logger.error(f"❌ Error stopping services: {e}")
            return False
    
    def clean_environment(self) -> bool:
        """Clean up Docker environment"""
        logger.info("🧹 Cleaning up Docker environment...")
        
        try:
            # Stop and remove containers
            self.stop_services()
            
            # Remove volumes
            subprocess.run([
                'docker', 'volume', 'prune', '-f'
            ], timeout=30)
            
            # Remove unused networks
            subprocess.run([
                'docker', 'network', 'prune', '-f'
            ], timeout=30)
            
            logger.info("✅ Environment cleaned successfully")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error cleaning environment: {e}")
            return False
    
    def generate_secrets(self) -> Dict[str, str]:
        """Generate secure secrets for development"""
        import secrets
        import string
        
        def generate_secret(length: int = 64) -> str:
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            return ''.join(secrets.choice(alphabet) for _ in range(length))
        
        return {
            'API_KEY_SECRET': f"dev_api_key_{generate_secret(32)}",
            'JWT_SECRET_KEY': f"dev_jwt_secret_{generate_secret(32)}"
        }
    
    def update_env_file_with_secrets(self, env_file: Path, secrets: Dict[str, str]) -> bool:
        """Update environment file with generated secrets"""
        try:
            # Read current content
            content = []
            if env_file.exists():
                with open(env_file, 'r') as f:
                    content = f.readlines()
            
            # Update or add secrets
            updated_keys = set()
            for i, line in enumerate(content):
                for key, value in secrets.items():
                    if line.startswith(f"{key}="):
                        content[i] = f"{key}={value}\n"
                        updated_keys.add(key)
                        break
            
            # Add missing secrets
            for key, value in secrets.items():
                if key not in updated_keys:
                    content.append(f"{key}={value}\n")
            
            # Write updated content
            with open(env_file, 'w') as f:
                f.writelines(content)
            
            logger.info(f"✅ Updated secrets in {env_file}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Error updating secrets: {e}")
            return False

def main():
    """Main setup function"""
    parser = argparse.ArgumentParser(description='BHIV HR Platform Environment Setup')
    parser.add_argument('action', choices=[
        'setup', 'start', 'stop', 'status', 'clean', 'validate'
    ], help='Action to perform')
    parser.add_argument('--environment', '-e', default='local',
                       choices=['local', 'staging', 'production'],
                       help='Environment to setup')
    parser.add_argument('--generate-secrets', action='store_true',
                       help='Generate new secrets for development')
    parser.add_argument('--no-start', action='store_true',
                       help='Setup without starting services')
    
    args = parser.parse_args()
    
    # Find project root
    project_root = Path(__file__).parent.parent
    setup = EnvironmentSetup(project_root)
    
    logger.info(f"🎯 BHIV HR Platform Environment Setup")
    logger.info(f"📁 Project root: {project_root}")
    logger.info(f"🌍 Environment: {args.environment}")
    
    success = True
    
    if args.action == 'setup':
        logger.info("🚀 Starting environment setup...")
        
        # Check prerequisites
        if not setup.check_prerequisites():
            logger.error("❌ Prerequisites check failed")
            sys.exit(1)
        
        # Validate environment files
        if not setup.validate_environment_files(args.environment):
            logger.error("❌ Environment validation failed")
            sys.exit(1)
        
        # Setup local environment
        if args.environment == 'local':
            if not setup.setup_local_environment():
                logger.error("❌ Local environment setup failed")
                sys.exit(1)
            
            # Generate secrets if requested
            if args.generate_secrets:
                secrets = setup.generate_secrets()
                env_file = project_root / 'environments' / 'local' / '.env'
                setup.update_env_file_with_secrets(env_file, secrets)
            
            # Test Docker Compose
            if not setup.test_docker_compose():
                logger.error("❌ Docker Compose validation failed")
                sys.exit(1)
            
            # Start services unless --no-start
            if not args.no_start:
                if not setup.start_services():
                    logger.error("❌ Failed to start services")
                    sys.exit(1)
                
                # Wait a bit for services to start
                import time
                logger.info("⏳ Waiting for services to initialize...")
                time.sleep(30)
                
                # Check service health
                health_status = setup.check_service_health()
                healthy_services = sum(health_status.values())
                total_services = len(health_status)
                
                if healthy_services == total_services:
                    logger.info(f"🎉 All {total_services} services are healthy!")
                else:
                    logger.warning(f"⚠️  {healthy_services}/{total_services} services are healthy")
        
        logger.info("✅ Environment setup completed!")
    
    elif args.action == 'start':
        if not setup.start_services():
            sys.exit(1)
    
    elif args.action == 'stop':
        if not setup.stop_services():
            sys.exit(1)
    
    elif args.action == 'status':
        health_status = setup.check_service_health()
        for service, healthy in health_status.items():
            status = "✅ Healthy" if healthy else "❌ Unhealthy"
            print(f"{service}: {status}")
    
    elif args.action == 'clean':
        if not setup.clean_environment():
            sys.exit(1)
    
    elif args.action == 'validate':
        if not setup.validate_environment_files(args.environment):
            sys.exit(1)
        if args.environment == 'local':
            if not setup.test_docker_compose():
                sys.exit(1)
        logger.info("✅ Validation completed successfully!")
    
    if success:
        logger.info("🎉 Operation completed successfully!")
        
        if args.action in ['setup', 'start'] and args.environment == 'local':
            logger.info("\n📊 Access Points:")
            logger.info("   - API Gateway: http://localhost:8000/docs")
            logger.info("   - AI Agent: http://localhost:9000/docs")
            logger.info("   - HR Portal: http://localhost:8501")
            logger.info("   - Client Portal: http://localhost:8502")
            logger.info("\n🔑 Default Credentials:")
            logger.info("   - Client Portal: TECH001 / demo123")

if __name__ == '__main__':
    main()