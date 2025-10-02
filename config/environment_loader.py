"""
BHIV HR Platform - Environment Configuration Loader
Centralized configuration management with validation and environment detection
"""

import os
import sys
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging
from dataclasses import dataclass
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class ValidationResult:
    """Result of environment validation"""
    is_valid: bool
    errors: List[str]
    warnings: List[str]
    
    def __post_init__(self):
        if not hasattr(self, 'errors'):
            self.errors = []
        if not hasattr(self, 'warnings'):
            self.warnings = []

class EnvironmentValidator:
    """Validates environment configuration"""
    
    def __init__(self):
        self.result = ValidationResult(is_valid=True, errors=[], warnings=[])
    
    def validate_database_url(self, url: str) -> bool:
        """Validate database URL format"""
        if not url:
            self.result.errors.append("DATABASE_URL is required")
            return False
        
        # PostgreSQL URL pattern
        pattern = r'^postgresql://[\w\-\.]+:[\w\-\.@#$%^&*()+=]+@[\w\-\.]+:\d+/[\w\-]+(\?.*)?$'
        if not re.match(pattern, url):
            self.result.errors.append("Invalid DATABASE_URL format. Expected: postgresql://user:password@host:port/database")
            return False
        
        return True
    
    def validate_api_key(self, key: str, environment: str) -> bool:
        """Validate API key strength and appropriateness"""
        if not key:
            self.result.errors.append("API_KEY_SECRET is required")
            return False
        
        if len(key) < 32:
            self.result.errors.append("API_KEY_SECRET must be at least 32 characters long")
            return False
        
        # Check for development keys in production
        if environment == 'production':
            dev_indicators = ['dev_', 'test_', 'local_', 'demo_']
            if any(indicator in key.lower() for indicator in dev_indicators):
                self.result.errors.append("Development API key detected in production environment")
                return False
        
        return True
    
    def validate_jwt_secret(self, secret: str, environment: str) -> bool:
        """Validate JWT secret strength"""
        if not secret:
            self.result.errors.append("JWT_SECRET_KEY is required")
            return False
        
        if len(secret) < 32:
            self.result.errors.append("JWT_SECRET_KEY must be at least 32 characters long")
            return False
        
        # Check for development secrets in production
        if environment == 'production':
            dev_indicators = ['dev_', 'test_', 'local_', 'demo_']
            if any(indicator in secret.lower() for indicator in dev_indicators):
                self.result.errors.append("Development JWT secret detected in production environment")
                return False
        
        return True
    
    def validate_service_urls(self, config: Dict[str, str], environment: str) -> bool:
        """Validate service URL configuration"""
        required_urls = [
            'GATEWAY_SERVICE_URL',
            'AGENT_SERVICE_URL'
        ]
        
        for url_key in required_urls:
            url = config.get(url_key)
            if not url:
                self.result.errors.append(f"{url_key} is required")
                continue
            
            # Basic URL validation
            if not (url.startswith('http://') or url.startswith('https://')):
                self.result.errors.append(f"{url_key} must be a valid HTTP/HTTPS URL")
            
            # Production should use HTTPS
            if environment == 'production' and url.startswith('http://'):
                self.result.warnings.append(f"{url_key} should use HTTPS in production")
        
        return len([e for e in self.result.errors if any(url in e for url in required_urls)]) == 0
    
    def validate_environment_specific(self, config: Dict[str, str], environment: str) -> bool:
        """Validate environment-specific configuration"""
        if environment == 'production':
            # Production-specific validations
            if config.get('DEBUG', 'false').lower() == 'true':
                self.result.warnings.append("DEBUG mode is enabled in production")
            
            if config.get('LOG_LEVEL', 'INFO').upper() == 'DEBUG':
                self.result.warnings.append("DEBUG log level in production may impact performance")
            
            # Check for localhost URLs in production
            localhost_indicators = ['localhost', '127.0.0.1', '0.0.0.0']
            for key, value in config.items():
                if 'URL' in key and any(indicator in str(value) for indicator in localhost_indicators):
                    self.result.errors.append(f"{key} contains localhost reference in production: {value}")
        
        elif environment == 'local':
            # Local development validations
            if not config.get('DEBUG', 'false').lower() == 'true':
                self.result.warnings.append("DEBUG mode is disabled in local development")
        
        return True
    
    def validate_all(self, config: Dict[str, str]) -> ValidationResult:
        """Perform comprehensive validation"""
        self.result = ValidationResult(is_valid=True, errors=[], warnings=[])
        
        environment = config.get('ENVIRONMENT', 'local')
        
        # Core validations
        self.validate_database_url(config.get('DATABASE_URL', ''))
        self.validate_api_key(config.get('API_KEY_SECRET', ''), environment)
        self.validate_jwt_secret(config.get('JWT_SECRET_KEY', ''), environment)
        self.validate_service_urls(config, environment)
        self.validate_environment_specific(config, environment)
        
        # Set final validation status
        self.result.is_valid = len(self.result.errors) == 0
        
        return self.result

class EnvironmentConfig:
    """Centralized environment configuration management"""
    
    def __init__(self, environment: Optional[str] = None):
        self.environment = environment or os.getenv('ENVIRONMENT', 'local')
        self.project_root = self._find_project_root()
        self.config: Dict[str, Any] = {}
        self.validator = EnvironmentValidator()
        
        # Load configuration
        self._load_base_config()
        self._load_environment_config()
        self._load_environment_variables()
        
        # Validate configuration
        self._validate_config()
    
    def _find_project_root(self) -> Path:
        """Find the project root directory"""
        current = Path(__file__).parent
        
        # Look for project indicators
        indicators = ['docker-compose.yml', 'docker-compose.production.yml', 'README.md']
        
        while current != current.parent:
            if any((current / indicator).exists() for indicator in indicators):
                return current
            current = current.parent
        
        # Fallback to current directory's parent
        return Path(__file__).parent.parent
    
    def _load_base_config(self):
        """Load shared base configuration"""
        base_config_path = self.project_root / 'environments' / 'shared' / 'base.env'
        
        if base_config_path.exists():
            self._load_env_file(base_config_path)
            logger.info(f"Loaded base configuration from {base_config_path}")
        else:
            logger.warning(f"Base configuration file not found: {base_config_path}")
    
    def _load_environment_config(self):
        """Load environment-specific configuration"""
        env_config_path = self.project_root / 'environments' / self.environment / '.env'
        
        # Try template if .env doesn't exist
        if not env_config_path.exists():
            env_config_path = self.project_root / 'environments' / self.environment / '.env.template'
        
        if env_config_path.exists():
            self._load_env_file(env_config_path)
            logger.info(f"Loaded {self.environment} configuration from {env_config_path}")
        else:
            logger.warning(f"Environment configuration file not found: {env_config_path}")
    
    def _load_env_file(self, file_path: Path):
        """Load environment variables from file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    
                    # Skip empty lines and comments
                    if not line or line.startswith('#'):
                        continue
                    
                    # Parse key=value pairs
                    if '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        
                        # Remove quotes if present
                        if value.startswith('"') and value.endswith('"'):
                            value = value[1:-1]
                        elif value.startswith("'") and value.endswith("'"):
                            value = value[1:-1]
                        
                        # Handle environment variable substitution
                        if value.startswith('${') and value.endswith('}'):
                            env_var = value[2:-1]
                            value = os.getenv(env_var, value)
                        
                        self.config[key] = value
                    else:
                        logger.warning(f"Invalid line format in {file_path}:{line_num}: {line}")
        
        except Exception as e:
            logger.error(f"Error loading environment file {file_path}: {e}")
    
    def _load_environment_variables(self):
        """Override with actual environment variables"""
        for key in self.config.keys():
            env_value = os.getenv(key)
            if env_value is not None:
                self.config[key] = env_value
                logger.debug(f"Override {key} from environment variable")
    
    def _validate_config(self):
        """Validate the loaded configuration"""
        validation_result = self.validator.validate_all(self.config)
        
        if validation_result.warnings:
            for warning in validation_result.warnings:
                logger.warning(f"Configuration warning: {warning}")
        
        if validation_result.errors:
            for error in validation_result.errors:
                logger.error(f"Configuration error: {error}")
            
            if self.environment == 'production':
                logger.critical("Configuration validation failed in production environment")
                sys.exit(1)
            else:
                logger.warning("Configuration validation failed - continuing in development mode")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value"""
        return self.config.get(key, default)
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get configuration value as integer"""
        value = self.get(key, default)
        try:
            return int(value)
        except (ValueError, TypeError):
            logger.warning(f"Invalid integer value for {key}: {value}, using default: {default}")
            return default
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get configuration value as boolean"""
        value = self.get(key, default)
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.lower() in ('true', '1', 'yes', 'on')
        return default
    
    def get_float(self, key: str, default: float = 0.0) -> float:
        """Get configuration value as float"""
        value = self.get(key, default)
        try:
            return float(value)
        except (ValueError, TypeError):
            logger.warning(f"Invalid float value for {key}: {value}, using default: {default}")
            return default
    
    def get_list(self, key: str, separator: str = ',', default: Optional[List[str]] = None) -> List[str]:
        """Get configuration value as list"""
        if default is None:
            default = []
        
        value = self.get(key)
        if not value:
            return default
        
        if isinstance(value, str):
            return [item.strip() for item in value.split(separator) if item.strip()]
        
        return default
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.environment == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.environment in ('local', 'development', 'dev')
    
    def is_staging(self) -> bool:
        """Check if running in staging environment"""
        return self.environment == 'staging'
    
    def get_database_config(self) -> Dict[str, Any]:
        """Get database configuration"""
        return {
            'url': self.get('DATABASE_URL'),
            'pool_size': self.get_int('DATABASE_POOL_SIZE', 10),
            'pool_timeout': self.get_int('DATABASE_POOL_TIMEOUT', 30),
            'max_overflow': self.get_int('DATABASE_MAX_OVERFLOW', 10),
            'pool_recycle': self.get_int('DATABASE_POOL_RECYCLE', 3600),
            'pool_pre_ping': self.get_bool('DATABASE_POOL_PRE_PING', True),
            'echo': self.get_bool('DATABASE_ECHO', False)
        }
    
    def get_security_config(self) -> Dict[str, Any]:
        """Get security configuration"""
        return {
            'api_key_secret': self.get('API_KEY_SECRET'),
            'jwt_secret_key': self.get('JWT_SECRET_KEY'),
            'jwt_algorithm': self.get('JWT_ALGORITHM', 'HS256'),
            'jwt_expiration_hours': self.get_int('JWT_EXPIRATION_HOURS', 24),
            'bcrypt_rounds': self.get_int('BCRYPT_ROUNDS', 12),
            'enable_2fa': self.get_bool('ENABLE_2FA', True),
            'enable_rate_limiting': self.get_bool('ENABLE_RATE_LIMITING', True)
        }
    
    def get_service_urls(self) -> Dict[str, str]:
        """Get service URL configuration"""
        return {
            'gateway': self.get('GATEWAY_SERVICE_URL'),
            'agent': self.get('AGENT_SERVICE_URL'),
            'portal': self.get('PORTAL_SERVICE_URL'),
            'client_portal': self.get('CLIENT_PORTAL_SERVICE_URL')
        }
    
    def export_for_docker(self) -> Dict[str, str]:
        """Export configuration for Docker Compose"""
        return {k: str(v) for k, v in self.config.items() if v is not None}
    
    def __repr__(self) -> str:
        """String representation of configuration"""
        return f"EnvironmentConfig(environment='{self.environment}', config_keys={len(self.config)})"

# Global configuration instance
config: Optional[EnvironmentConfig] = None

def get_config(environment: Optional[str] = None) -> EnvironmentConfig:
    """Get global configuration instance"""
    global config
    if config is None or (environment and config.environment != environment):
        config = EnvironmentConfig(environment)
    return config

def reload_config(environment: Optional[str] = None) -> EnvironmentConfig:
    """Reload configuration"""
    global config
    config = EnvironmentConfig(environment)
    return config

# Convenience functions
def get_database_url() -> str:
    """Get database URL"""
    return get_config().get('DATABASE_URL', '')

def get_api_key() -> str:
    """Get API key"""
    return get_config().get('API_KEY_SECRET', '')

def is_production() -> bool:
    """Check if running in production"""
    return get_config().is_production()

def is_development() -> bool:
    """Check if running in development"""
    return get_config().is_development()

if __name__ == '__main__':
    # Test configuration loading
    config = get_config()
    print(f"Environment: {config.environment}")
    print(f"Database URL: {config.get('DATABASE_URL', 'Not configured')}")
    print(f"API Key configured: {'Yes' if config.get('API_KEY_SECRET') else 'No'}")
    print(f"Debug mode: {config.get_bool('DEBUG')}")
    print(f"Configuration valid: {config.validator.validate_all(config.config).is_valid}")