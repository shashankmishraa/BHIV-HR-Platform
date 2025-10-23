"""
Enterprise Client Authentication Service
Secure, scalable authentication with JWT tokens and bcrypt hashing
"""

import bcrypt
import jwt
import os
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ClientAuthService:
    """Production-grade client authentication service"""
    
    def __init__(self):
        self.database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu")
        self.jwt_secret = os.getenv("JWT_SECRET", "fallback_jwt_secret_key_for_client_auth_2025")
        
        if not self.database_url or not self.jwt_secret:
            logger.error("Missing required environment variables: DATABASE_URL, JWT_SECRET")
            raise ValueError("Missing required environment variables")
        self.jwt_algorithm = "HS256"
        self.token_expiry_hours = 24
        self.engine = create_engine(self.database_url, pool_pre_ping=True, pool_recycle=300)
        self._initialize_database()
    
    def _initialize_database(self):
        """Initialize client authentication tables"""
        try:
            with self.engine.begin() as connection:
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS client_auth (
                        id SERIAL PRIMARY KEY,
                        client_id VARCHAR(100) UNIQUE NOT NULL,
                        company_name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        password_hash VARCHAR(255) NOT NULL,
                        is_active BOOLEAN DEFAULT TRUE,
                        created_at TIMESTAMP DEFAULT NOW(),
                        updated_at TIMESTAMP DEFAULT NOW(),
                        last_login TIMESTAMP,
                        login_attempts INTEGER DEFAULT 0,
                        locked_until TIMESTAMP
                    )
                """))
                
                connection.execute(text("""
                    CREATE TABLE IF NOT EXISTS client_sessions (
                        id SERIAL PRIMARY KEY,
                        client_id VARCHAR(100) NOT NULL,
                        token_hash VARCHAR(255) NOT NULL,
                        expires_at TIMESTAMP NOT NULL,
                        created_at TIMESTAMP DEFAULT NOW(),
                        is_revoked BOOLEAN DEFAULT FALSE,
                        FOREIGN KEY (client_id) REFERENCES client_auth(client_id) ON DELETE CASCADE
                    )
                """))
                
                self._create_default_clients(connection)
                logger.info("Client authentication database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def _create_default_clients(self, connection):
        """Create default clients with secure passwords"""
        default_clients = [
            {
                'client_id': 'TECH001',
                'company_name': 'TechCorp Solutions',
                'email': 'admin@techcorp.com',
                'password': 'demo123'
            },
            {
                'client_id': 'STARTUP01',
                'company_name': 'InnovateLab',
                'email': 'hello@innovatelab.com',
                'password': 'demo123'
            }
        ]
        
        for client in default_clients:
            try:
                password_hash = self._hash_password(client['password'])
                connection.execute(text("""
                    INSERT INTO client_auth (client_id, company_name, email, password_hash)
                    VALUES (:client_id, :company_name, :email, :password_hash)
                    ON CONFLICT (client_id) DO NOTHING
                """), {
                    'client_id': client['client_id'],
                    'company_name': client['company_name'],
                    'email': client['email'],
                    'password_hash': password_hash
                })
            except Exception as e:
                logger.warning(f"Could not create default client {client['client_id']}: {e}")
    
    def _hash_password(self, password: str) -> str:
        """Hash password using bcrypt"""
        # Truncate password to 72 bytes for bcrypt compatibility
        password_bytes = password.encode('utf-8')[:72]
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password_bytes, salt).decode('utf-8')
    
    def _verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        # Truncate password to 72 bytes for bcrypt compatibility
        password_bytes = password.encode('utf-8')[:72]
        return bcrypt.checkpw(password_bytes, password_hash.encode('utf-8'))
    
    def _generate_jwt_token(self, client_id: str, company_name: str) -> str:
        """Generate JWT token for authenticated client"""
        now = datetime.utcnow()
        payload = {
            'client_id': client_id,
            'company_name': company_name,
            'exp': now + timedelta(hours=self.token_expiry_hours),
            'iat': now,
            'iss': 'bhiv_hr_platform'
        }
        return jwt.encode(payload, self.jwt_secret, algorithm=self.jwt_algorithm)
    
    def authenticate_client(self, client_id: str, password: str) -> Dict[str, Any]:
        """Authenticate client and return JWT token"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT client_id, company_name, password_hash, login_attempts, locked_until, is_active
                    FROM client_auth 
                    WHERE client_id = :client_id
                """), {'client_id': client_id})
                
                client_data = result.fetchone()
                
                if not client_data:
                    return {'success': False, 'error': 'Invalid credentials'}
                
                if not client_data[5]:  # is_active
                    return {'success': False, 'error': 'Account is deactivated'}
                
                if client_data[4] and client_data[4] > datetime.utcnow():  # locked_until
                    return {'success': False, 'error': 'Account is temporarily locked'}
                
                if not self._verify_password(password, client_data[2]):  # password_hash
                    new_attempts = client_data[3] + 1  # login_attempts
                    locked_until = None
                    
                    if new_attempts >= 5:
                        locked_until = datetime.utcnow() + timedelta(minutes=30)
                    
                    with self.engine.begin() as conn:
                        conn.execute(text("""
                            UPDATE client_auth 
                            SET login_attempts = :attempts, locked_until = :locked_until
                            WHERE client_id = :client_id
                        """), {
                            'attempts': new_attempts,
                            'locked_until': locked_until,
                            'client_id': client_id
                        })
                    
                    return {'success': False, 'error': 'Invalid credentials'}
                
                token = self._generate_jwt_token(client_data[0], client_data[1])
                
                with self.engine.begin() as conn:
                    conn.execute(text("""
                        UPDATE client_auth 
                        SET login_attempts = 0, locked_until = NULL, last_login = NOW()
                        WHERE client_id = :client_id
                    """), {'client_id': client_id})
                    
                    token_hash = self._hash_password(token)
                    conn.execute(text("""
                        INSERT INTO client_sessions (client_id, token_hash, expires_at)
                        VALUES (:client_id, :token_hash, :expires_at)
                    """), {
                        'client_id': client_id,
                        'token_hash': token_hash,
                        'expires_at': datetime.utcnow() + timedelta(hours=self.token_expiry_hours)
                    })
                
                logger.info(f"Client authenticated successfully: {client_id}")
                return {
                    'success': True,
                    'token': token,
                    'client_id': client_data[0],
                    'company_name': client_data[1]
                }
                
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return {'success': False, 'error': 'Authentication failed'}
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify JWT token and return client data"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            with self.engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT is_revoked FROM client_sessions 
                    WHERE client_id = :client_id AND expires_at > NOW()
                    ORDER BY created_at DESC LIMIT 1
                """), {'client_id': payload['client_id']})
                
                session = result.fetchone()
                if session and session[0]:  # is_revoked
                    return {'success': False, 'error': 'Token revoked'}
            
            return {
                'success': True,
                'client_id': payload['client_id'],
                'company_name': payload['company_name']
            }
            
        except jwt.ExpiredSignatureError:
            return {'success': False, 'error': 'Token expired'}
        except jwt.InvalidTokenError:
            return {'success': False, 'error': 'Invalid token'}
        except Exception as e:
            logger.error(f"Token verification error: {e}")
            return {'success': False, 'error': 'Token verification failed'}
    
    def register_client(self, client_id: str, company_name: str, email: str, password: str) -> Dict[str, Any]:
        """Register new client with validation"""
        try:
            if not all([client_id, company_name, email, password]):
                return {'success': False, 'error': 'All fields are required'}
            
            if len(password) < 8:
                return {'success': False, 'error': 'Password must be at least 8 characters'}
            
            if '@' not in email:
                return {'success': False, 'error': 'Invalid email format'}
            
            password_hash = self._hash_password(password)
            
            with self.engine.begin() as connection:
                connection.execute(text("""
                    INSERT INTO client_auth (client_id, company_name, email, password_hash)
                    VALUES (:client_id, :company_name, :email, :password_hash)
                """), {
                    'client_id': client_id,
                    'company_name': company_name,
                    'email': email,
                    'password_hash': password_hash
                })
            
            logger.info(f"Client registered successfully: {client_id}")
            return {'success': True, 'message': 'Client registered successfully'}
            
        except IntegrityError as e:
            if 'client_id' in str(e):
                return {'success': False, 'error': 'Client ID already exists'}
            elif 'email' in str(e):
                return {'success': False, 'error': 'Email already registered'}
            else:
                return {'success': False, 'error': 'Registration failed'}
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return {'success': False, 'error': 'Registration failed'}
    
    def logout_client(self, token: str) -> bool:
        """Revoke client session token"""
        try:
            payload = jwt.decode(token, self.jwt_secret, algorithms=[self.jwt_algorithm])
            
            with self.engine.begin() as connection:
                connection.execute(text("""
                    UPDATE client_sessions 
                    SET is_revoked = TRUE 
                    WHERE client_id = :client_id AND expires_at > NOW()
                """), {'client_id': payload['client_id']})
            
            return True
        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False
    
    def get_client_info(self, client_id: str) -> Optional[Dict[str, Any]]:
        """Get client information"""
        try:
            with self.engine.connect() as connection:
                result = connection.execute(text("""
                    SELECT client_id, company_name, email, created_at, last_login
                    FROM client_auth 
                    WHERE client_id = :client_id AND is_active = TRUE
                """), {'client_id': client_id})
                
                client_data = result.fetchone()
                if client_data:
                    return {
                        'client_id': client_data[0],
                        'company_name': client_data[1],
                        'email': client_data[2],
                        'created_at': client_data[3],
                        'last_login': client_data[4]
                    }
                return None
        except Exception as e:
            logger.error(f"Get client info error: {e}")
            return None