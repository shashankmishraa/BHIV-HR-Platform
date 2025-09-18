"""
Enterprise Security Manager
Comprehensive security configuration and management system
"""

import os
import secrets
import hashlib
import jwt
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
from enum import Enum
import logging
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityLevel(Enum):
    """Security levels for different environments"""
    DEVELOPMENT = "development"
    STAGING = "staging"
    PRODUCTION = "production"

@dataclass
class SecurityConfig:
    """Security configuration data class"""
    api_key: str
    jwt_secret: str
    environment: SecurityLevel
    cors_origins: List[str]
    session_timeout: int = 3600  # 1 hour
    max_login_attempts: int = 5
    lockout_duration: int = 1800  # 30 minutes
    password_min_length: int = 8
    require_2fa: bool = False

class SecurityManager:
    """Centralized security management"""
    
    def __init__(self):
        self.config = self._load_security_config()
        self._validate_security_config()
        logger.info(f"Security Manager initialized for {self.config.environment.value} environment")
    
    def _load_security_config(self) -> SecurityConfig:
        """Load security configuration from environment variables"""
        
        # Determine environment
        env_name = os.getenv("ENVIRONMENT", "development").lower()
        try:
            environment = SecurityLevel(env_name)
        except ValueError:
            logger.warning(f"Unknown environment '{env_name}', defaulting to development")
            environment = SecurityLevel.DEVELOPMENT
        
        # Load API key with validation
        api_key = self._get_secure_api_key(environment)
        
        # Load JWT secret with validation
        jwt_secret = self._get_jwt_secret(environment)
        
        # Load CORS origins
        cors_origins_str = os.getenv("CORS_ORIGINS", "http://localhost:8501,http://localhost:8502")
        cors_origins = [origin.strip() for origin in cors_origins_str.split(",")]
        
        # Load other security settings
        session_timeout = int(os.getenv("SESSION_TIMEOUT", "3600"))
        max_login_attempts = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
        lockout_duration = int(os.getenv("LOCKOUT_DURATION", "1800"))
        password_min_length = int(os.getenv("PASSWORD_MIN_LENGTH", "8"))
        require_2fa = os.getenv("REQUIRE_2FA", "false").lower() == "true"
        
        return SecurityConfig(
            api_key=api_key,
            jwt_secret=jwt_secret,
            environment=environment,
            cors_origins=cors_origins,
            session_timeout=session_timeout,
            max_login_attempts=max_login_attempts,
            lockout_duration=lockout_duration,
            password_min_length=password_min_length,
            require_2fa=require_2fa
        )
    
    def _get_secure_api_key(self, environment: SecurityLevel) -> str:
        """Get secure API key from environment with validation"""
        api_key = os.getenv("API_KEY_SECRET")
        
        # For production, require secure API key
        if environment == SecurityLevel.PRODUCTION:
            if not api_key:
                raise ValueError(
                    "API_KEY_SECRET environment variable is required for production. "
                    "Generate a secure key using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
            
            # Validate API key is not a demo key
            demo_keys = ["myverysecureapikey123", "demo", "test", "sample"]
            if api_key.lower() in demo_keys or len(api_key) < 16:
                raise ValueError(
                    "Demo or weak API key detected. Use a secure, unique API key in production. "
                    "Generate one using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
        
        # For development, provide fallback with warning
        if not api_key:
            if environment == SecurityLevel.PRODUCTION:
                raise ValueError("API_KEY_SECRET is required for production")
            
            logger.warning("Using fallback API key for development. Set API_KEY_SECRET for production.")
            api_key = "dev_fallback_key_" + secrets.token_urlsafe(16)
        
        return api_key
    
    def _get_jwt_secret(self, environment: SecurityLevel) -> str:
        """Get JWT secret from environment with validation"""
        jwt_secret = os.getenv("JWT_SECRET")
        
        # For production, require JWT secret
        if environment == SecurityLevel.PRODUCTION:
            if not jwt_secret:
                raise ValueError(
                    "JWT_SECRET environment variable is required for production. "
                    "Generate a secure secret using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
            
            if len(jwt_secret) < 32:
                raise ValueError(
                    "JWT_SECRET must be at least 32 characters for production security. "
                    "Generate a secure secret using: python -c \"import secrets; print(secrets.token_urlsafe(32))\""
                )
        
        # For development, provide fallback with warning
        if not jwt_secret:
            if environment == SecurityLevel.PRODUCTION:
                raise ValueError("JWT_SECRET is required for production")
            
            logger.warning("Using fallback JWT secret for development. Set JWT_SECRET for production.")
            jwt_secret = "dev_jwt_secret_" + secrets.token_urlsafe(32)
        
        return jwt_secret
    
    def _validate_security_config(self):
        """Validate security configuration"""
        if self.config.environment == SecurityLevel.PRODUCTION:
            # Production security checks
            if len(self.config.api_key) < 16:
                raise ValueError("API key too short for production")
            
            if len(self.config.jwt_secret) < 32:
                raise ValueError("JWT secret too short for production")
            
            if "localhost" in str(self.config.cors_origins):
                logger.warning("Localhost CORS origins detected in production")
        
        logger.info("Security configuration validated successfully")
    
    def get_api_headers(self) -> Dict[str, str]:
        """Get secure API headers"""
        return {"Authorization": f"Bearer {self.config.api_key}"}
    
    def generate_jwt_token(self, payload: Dict[str, Any], expires_hours: int = None) -> str:
        """Generate JWT token with secure configuration"""
        if expires_hours is None:
            expires_hours = self.config.session_timeout // 3600
        
        token_payload = {
            **payload,
            'exp': datetime.utcnow() + timedelta(hours=expires_hours),
            'iat': datetime.utcnow(),
            'iss': 'bhiv_hr_platform'
        }
        
        return jwt.encode(token_payload, self.config.jwt_secret, algorithm='HS256')
    
    def verify_jwt_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token"""
        try:
            payload = jwt.decode(token, self.config.jwt_secret, algorithms=['HS256'])
            return {'success': True, 'payload': payload}
        except jwt.ExpiredSignatureError:
            return {'success': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'success': False, 'error': 'Invalid token'}
    
    def hash_password(self, password: str) -> str:
        """Hash password securely"""
        import bcrypt
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        import bcrypt
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))
    
    def validate_password_strength(self, password: str) -> Dict[str, Any]:
        """Validate password strength"""
        score = 0
        feedback = []
        
        if len(password) >= self.config.password_min_length:
            score += 20
        else:
            feedback.append(f"Password must be at least {self.config.password_min_length} characters")
        
        if any(c.isupper() for c in password):
            score += 20
        else:
            feedback.append("Password must contain uppercase letters")
        
        if any(c.islower() for c in password):
            score += 20
        else:
            feedback.append("Password must contain lowercase letters")
        
        if any(c.isdigit() for c in password):
            score += 20
        else:
            feedback.append("Password must contain numbers")
        
        if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
            score += 20
        else:
            feedback.append("Password must contain special characters")
        
        return {
            'score': score,
            'is_valid': score >= 60,
            'feedback': feedback,
            'strength': self._get_strength_label(score)
        }
    
    def _get_strength_label(self, score: int) -> str:
        """Get password strength label"""
        if score >= 80:
            return "Very Strong"
        elif score >= 60:
            return "Strong"
        elif score >= 40:
            return "Medium"
        elif score >= 20:
            return "Weak"
        else:
            return "Very Weak"
    
    @staticmethod
    def generate_secure_key(length: int = 32) -> str:
        """Generate cryptographically secure key"""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_secure_password(length: int = 16) -> str:
        """Generate secure password"""
        import string
        import random
        
        chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-="
        password = ''.join(random.choice(chars) for _ in range(length))
        return password

class APIKeyManager:
    """API Key management with database storage"""
    
    def __init__(self, security_manager: SecurityManager):
        self.security_manager = security_manager
        self.database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
    
    def validate_api_key(self, api_key: str) -> Optional[Dict[str, Any]]:
        """Validate API key and return metadata"""
        # For demo purposes, validate against configured key
        if api_key == self.security_manager.config.api_key:
            return {
                'client_id': 'system',
                'permissions': ['read', 'write'],
                'key_type': 'system'
            }
        
        # In production, this would check database
        return None
    
    def generate_api_key(self, client_id: str, permissions: List[str] = None) -> Dict[str, Any]:
        """Generate new API key for client"""
        api_key = self.security_manager.generate_secure_key(32)
        key_id = f"key_{secrets.token_hex(8)}"
        
        # In production, store in database
        return {
            'key_id': key_id,
            'api_key': api_key,
            'client_id': client_id,
            'permissions': permissions or ['read'],
            'created_at': datetime.utcnow().isoformat()
        }
    
    def revoke_api_key(self, key_id: str) -> bool:
        """Revoke API key"""
        # In production, update database
        logger.info(f"API key revoked: {key_id}")
        return True