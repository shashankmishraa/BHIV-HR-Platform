#!/usr/bin/env python3
"""
Enhanced Authentication System
Standardized authentication with proper fallback mechanisms and consistent validation
"""

import os
import jwt
import secrets
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass
from fastapi import HTTPException, Depends, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# Configure logging
logger = logging.getLogger(__name__)

class AuthenticationMethod(Enum):
    API_KEY = "api_key"
    JWT_TOKEN = "jwt_token"
    SESSION_COOKIE = "session_cookie"
    FALLBACK = "fallback"

class AuthenticationLevel(Enum):
    NONE = 0
    BASIC = 1
    STANDARD = 2
    ENHANCED = 3
    ENTERPRISE = 4

@dataclass
class AuthenticationResult:
    """Standardized authentication result"""
    success: bool
    method: AuthenticationMethod
    level: AuthenticationLevel
    user_id: Optional[str] = None
    permissions: List[str] = None
    metadata: Dict[str, Any] = None
    error_message: Optional[str] = None
    
    def __post_init__(self):
        if self.permissions is None:
            self.permissions = []
        if self.metadata is None:
            self.metadata = {}

class EnhancedAuthenticationSystem:
    """
    Centralized authentication system with standardized validation
    and proper fallback mechanisms
    """
    
    def __init__(self):
        self.security_bearer = HTTPBearer(auto_error=False)
        self.environment = os.getenv("ENVIRONMENT", "development").lower()
        
        # Initialize authentication components
        self._init_api_keys()
        self._init_jwt_config()
        self._init_session_config()
        self._init_fallback_config()
        
        logger.info(f"Enhanced authentication system initialized for {self.environment}")
    
    def _init_api_keys(self):
        """Initialize API key configuration"""
        # Production API keys - Load from environment
        self.production_keys = {}
        prod_key = os.getenv("PROD_API_KEY")
        if prod_key:
            self.production_keys[prod_key] = {
                "client_id": "production_client",
                "permissions": ["read", "write", "admin"],
                "level": AuthenticationLevel.ENTERPRISE,
                "environment": "production"
            }
        
        # Development/Demo API keys - Load from environment or use secure defaults
        self.development_keys = {}
        dev_key = os.getenv("DEV_API_KEY", secrets.token_urlsafe(32))
        demo_key = os.getenv("DEMO_API_KEY", secrets.token_urlsafe(24))
        
        self.development_keys[dev_key] = {
            "client_id": "demo_client",
            "permissions": ["read", "write"],
            "level": AuthenticationLevel.STANDARD,
            "environment": "development"
        }
        self.development_keys[demo_key] = {
            "client_id": "demo_user",
            "permissions": ["read"],
            "level": AuthenticationLevel.BASIC,
            "environment": "development"
        }
        
        # Environment-specific API key from environment variable
        env_api_key = os.getenv("API_KEY_SECRET")
        if env_api_key:
            self.production_keys[env_api_key] = {
                "client_id": "env_client",
                "permissions": ["read", "write", "admin"],
                "level": AuthenticationLevel.ENTERPRISE,
                "environment": self.environment
            }
    
    def _init_jwt_config(self):
        """Initialize JWT configuration"""
        self.jwt_secret = os.getenv("JWT_SECRET", "dev_jwt_" + secrets.token_urlsafe(32))
        self.jwt_algorithm = "HS256"
        self.jwt_expiry_hours = 24
        
        # Validate JWT secret strength
        if self.environment == "production" and len(self.jwt_secret) < 32:
            logger.warning("JWT secret is too short for production environment")
    
    def _init_session_config(self):
        """Initialize session configuration"""
        self.session_timeout_hours = 24
        self.session_secret = secrets.token_urlsafe(32)
        self.active_sessions = {}
    
    def _init_fallback_config(self):
        """Initialize fallback authentication configuration"""
        self.fallback_enabled = True
        self.fallback_permissions = ["read"]
        self.fallback_client_id = "fallback_client"
    
    def validate_api_key(self, api_key: str) -> AuthenticationResult:
        """
        Standardized API key validation with proper fallback
        """
        if not api_key:
            return AuthenticationResult(
                success=False,
                method=AuthenticationMethod.API_KEY,
                level=AuthenticationLevel.NONE,
                error_message="API key is required"
            )
        
        # Clean the API key (remove Bearer prefix if present)
        clean_key = api_key.replace("Bearer ", "").strip()
        
        # Check production keys first
        if clean_key in self.production_keys:
            key_data = self.production_keys[clean_key]
            return AuthenticationResult(
                success=True,
                method=AuthenticationMethod.API_KEY,
                level=key_data["level"],
                user_id=key_data["client_id"],
                permissions=key_data["permissions"],
                metadata={
                    "environment": key_data["environment"],
                    "key_type": "production"
                }
            )
        
        # Check development keys
        if clean_key in self.development_keys:
            key_data = self.development_keys[clean_key]
            return AuthenticationResult(
                success=True,
                method=AuthenticationMethod.API_KEY,
                level=key_data["level"],
                user_id=key_data["client_id"],
                permissions=key_data["permissions"],
                metadata={
                    "environment": key_data["environment"],
                    "key_type": "development"
                }
            )
        
        # Fallback authentication if enabled
        if self.fallback_enabled and self.environment != "production":
            logger.warning(f"Using fallback authentication for key: {clean_key[:8]}...")
            return AuthenticationResult(
                success=True,
                method=AuthenticationMethod.FALLBACK,
                level=AuthenticationLevel.BASIC,
                user_id=self.fallback_client_id,
                permissions=self.fallback_permissions,
                metadata={
                    "environment": "fallback",
                    "key_type": "fallback",
                    "original_key": clean_key[:8] + "..."
                }
            )
        
        # Authentication failed
        logger.warning(f"Invalid API key attempt: {clean_key[:8]}...")
        return AuthenticationResult(
            success=False,
            method=AuthenticationMethod.API_KEY,
            level=AuthenticationLevel.NONE,
            error_message="Invalid API key"
        )
    
    def validate_jwt_token(self, token: str) -> AuthenticationResult:
        """
        Standardized JWT token validation
        """
        if not token:
            return AuthenticationResult(
                success=False,
                method=AuthenticationMethod.JWT_TOKEN,
                level=AuthenticationLevel.NONE,
                error_message="JWT token is required"
            )
        
        try:
            # Clean the token (remove Bearer prefix if present)
            clean_token = token.replace("Bearer ", "").strip()
            
            # Decode and validate JWT
            payload = jwt.decode(clean_token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            # JWT library handles expiration automatically via ExpiredSignatureError
            
            return AuthenticationResult(
                success=True,
                method=AuthenticationMethod.JWT_TOKEN,
                level=AuthenticationLevel.STANDARD,
                user_id=payload.get("user_id"),
                permissions=payload.get("permissions", []),
                metadata={
                    "issued_at": payload.get("iat"),
                    "expires_at": payload.get("exp"),
                    "algorithm": self.jwt_algorithm
                }
            )
            
        except jwt.ExpiredSignatureError:
            return AuthenticationResult(
                success=False,
                method=AuthenticationMethod.JWT_TOKEN,
                level=AuthenticationLevel.NONE,
                error_message="JWT token has expired"
            )
        except jwt.InvalidTokenError as e:
            return AuthenticationResult(
                success=False,
                method=AuthenticationMethod.JWT_TOKEN,
                level=AuthenticationLevel.NONE,
                error_message=f"Invalid JWT token: {str(e)}"
            )
        except Exception as e:
            logger.error(f"JWT validation error: {str(e)}")
            return AuthenticationResult(
                success=False,
                method=AuthenticationMethod.JWT_TOKEN,
                level=AuthenticationLevel.NONE,
                error_message="JWT validation failed"
            )
    
    def validate_session(self, request: Request) -> AuthenticationResult:
        """
        Standardized session validation
        """
        try:
            # Extract session ID from cookies
            session_id = request.cookies.get("session_id")
            
            if not session_id:
                return AuthenticationResult(
                    success=False,
                    method=AuthenticationMethod.SESSION_COOKIE,
                    level=AuthenticationLevel.NONE,
                    error_message="No session found"
                )
            
            # Validate session
            session_data = self.active_sessions.get(session_id)
            if not session_data:
                return AuthenticationResult(
                    success=False,
                    method=AuthenticationMethod.SESSION_COOKIE,
                    level=AuthenticationLevel.NONE,
                    error_message="Invalid session"
                )
            
            # Check session expiration
            expires_at = session_data.get("expires_at")
            if expires_at and datetime.fromisoformat(expires_at) < datetime.now(timezone.utc):
                # Clean up expired session
                del self.active_sessions[session_id]
                return AuthenticationResult(
                    success=False,
                    method=AuthenticationMethod.SESSION_COOKIE,
                    level=AuthenticationLevel.NONE,
                    error_message="Session has expired"
                )
            
            return AuthenticationResult(
                success=True,
                method=AuthenticationMethod.SESSION_COOKIE,
                level=AuthenticationLevel.STANDARD,
                user_id=session_data.get("user_id"),
                permissions=session_data.get("permissions", []),
                metadata={
                    "session_id": session_id[:8] + "...",
                    "created_at": session_data.get("created_at"),
                    "expires_at": expires_at
                }
            )
            
        except Exception as e:
            logger.error(f"Session validation error: {str(e)}")
            return AuthenticationResult(
                success=False,
                method=AuthenticationMethod.SESSION_COOKIE,
                level=AuthenticationLevel.NONE,
                error_message="Session validation failed"
            )
    
    def authenticate_request(self, request: Request, credentials: Optional[HTTPAuthorizationCredentials] = None) -> AuthenticationResult:
        """
        Comprehensive request authentication with multiple methods and fallback
        """
        authentication_attempts = []
        
        # Method 1: Try API Key authentication (Bearer token)
        if credentials and credentials.credentials:
            api_result = self.validate_api_key(credentials.credentials)
            authentication_attempts.append(api_result)
            if api_result.success:
                return api_result
        
        # Method 2: Try JWT token authentication
        auth_header = request.headers.get("Authorization", "")
        if auth_header.startswith("Bearer "):
            jwt_token = auth_header[7:]  # Remove "Bearer " prefix
            jwt_result = self.validate_jwt_token(jwt_token)
            authentication_attempts.append(jwt_result)
            if jwt_result.success:
                return jwt_result
        
        # Method 3: Try session authentication
        session_result = self.validate_session(request)
        authentication_attempts.append(session_result)
        if session_result.success:
            return session_result
        
        # Method 4: Fallback authentication (development only)
        if self.fallback_enabled and self.environment != "production":
            logger.warning("Using fallback authentication - no valid credentials provided")
            return AuthenticationResult(
                success=True,
                method=AuthenticationMethod.FALLBACK,
                level=AuthenticationLevel.BASIC,
                user_id=self.fallback_client_id,
                permissions=self.fallback_permissions,
                metadata={
                    "environment": "fallback",
                    "attempts": len(authentication_attempts),
                    "fallback_reason": "No valid credentials provided"
                }
            )
        
        # All authentication methods failed
        error_messages = [attempt.error_message for attempt in authentication_attempts if attempt.error_message]
        return AuthenticationResult(
            success=False,
            method=AuthenticationMethod.API_KEY,  # Default method for error reporting
            level=AuthenticationLevel.NONE,
            error_message=f"Authentication failed: {'; '.join(error_messages)}" if error_messages else "Authentication required"
        )
    
    def generate_jwt_token(self, user_id: str, permissions: List[str], expires_hours: int = None) -> str:
        """
        Generate a standardized JWT token
        """
        if expires_hours is None:
            expires_hours = self.jwt_expiry_hours
        
        now = datetime.now(timezone.utc)
        payload = {
            "user_id": user_id,
            "permissions": permissions,
            "iat": now,
            "exp": now + timedelta(hours=expires_hours),
            "iss": "bhiv-hr-platform",
            "aud": "bhiv-hr-api"
        }
        
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def create_session(self, user_id: str, permissions: List[str], request: Request) -> str:
        """
        Create a standardized session
        """
        session_id = secrets.token_urlsafe(32)
        now = datetime.now(timezone.utc)
        
        session_data = {
            "user_id": user_id,
            "permissions": permissions,
            "created_at": now.isoformat(),
            "expires_at": (now + timedelta(hours=self.session_timeout_hours)).isoformat(),
            "ip_address": request.client.host if request.client else "unknown",
            "user_agent": request.headers.get("user-agent", "unknown")
        }
        
        self.active_sessions[session_id] = session_data
        return session_id
    
    def invalidate_session(self, session_id: str) -> bool:
        """
        Invalidate a session
        """
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            return True
        return False
    
    def cleanup_expired_sessions(self) -> int:
        """
        Clean up expired sessions
        """
        now = datetime.now(timezone.utc)
        expired_sessions = []
        
        for session_id, session_data in self.active_sessions.items():
            expires_at = session_data.get("expires_at")
            if expires_at and datetime.fromisoformat(expires_at) < now:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            del self.active_sessions[session_id]
        
        return len(expired_sessions)
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get authentication system status
        """
        return {
            "environment": self.environment,
            "fallback_enabled": self.fallback_enabled,
            "active_sessions": len(self.active_sessions),
            "production_keys_count": len(self.production_keys),
            "development_keys_count": len(self.development_keys),
            "jwt_algorithm": self.jwt_algorithm,
            "session_timeout_hours": self.session_timeout_hours,
            "system_health": "operational"
        }

# Global authentication system instance
enhanced_auth_system = EnhancedAuthenticationSystem()

# Standardized authentication dependency
def get_enhanced_authentication(
    request: Request,
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(enhanced_auth_system.security_bearer)
) -> AuthenticationResult:
    """
    Enhanced authentication dependency with comprehensive validation and fallback
    """
    return enhanced_auth_system.authenticate_request(request, credentials)

def require_authentication(
    auth_result: AuthenticationResult = Depends(get_enhanced_authentication)
) -> AuthenticationResult:
    """
    Require successful authentication
    """
    if not auth_result.success:
        raise HTTPException(
            status_code=401,
            detail=auth_result.error_message or "Authentication required",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return auth_result

def require_permissions(required_permissions: List[str]):
    """
    Require specific permissions
    """
    def permission_checker(auth_result: AuthenticationResult = Depends(require_authentication)) -> AuthenticationResult:
        if not auth_result.permissions:
            raise HTTPException(
                status_code=403,
                detail="No permissions granted"
            )
        
        missing_permissions = [perm for perm in required_permissions if perm not in auth_result.permissions]
        if missing_permissions:
            raise HTTPException(
                status_code=403,
                detail=f"Missing required permissions: {', '.join(missing_permissions)}"
            )
        
        return auth_result
    
    return permission_checker

def require_authentication_level(min_level: AuthenticationLevel):
    """
    Require minimum authentication level
    """
    def level_checker(auth_result: AuthenticationResult = Depends(require_authentication)) -> AuthenticationResult:
        if auth_result.level.value < min_level.value:
            raise HTTPException(
                status_code=403,
                detail=f"Insufficient authentication level. Required: {min_level.name}, Current: {auth_result.level.name}"
            )
        
        return auth_result
    
    return level_checker

# Backward compatibility functions
def get_api_key(auth_result: AuthenticationResult = Depends(require_authentication)) -> str:
    """
    Backward compatibility function for existing endpoints
    """
    return auth_result.user_id or "authenticated_user"

def validate_api_key(api_key: str) -> Optional[Dict]:
    """
    Backward compatibility function for direct API key validation
    """
    result = enhanced_auth_system.validate_api_key(api_key)
    if result.success:
        return {
            "client_id": result.user_id,
            "permissions": result.permissions,
            "key_type": result.metadata.get("key_type", "unknown"),
            "environment": result.metadata.get("environment", "unknown")
        }
    return None