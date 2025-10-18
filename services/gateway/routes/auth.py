from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
import pyotp
import qrcode
import io
import base64
import jwt
from datetime import datetime, timezone, timedelta
import os
import sys
sys.path.append('..')
from dependencies import auth_dependency

router = APIRouter(prefix="/auth", tags=["Authentication"])

class TwoFASetup(BaseModel):
    user_id: str

class TwoFAVerify(BaseModel):
    user_id: str
    totp_code: str

class LoginRequest(BaseModel):
    username: str
    password: str
    totp_code: str = None

@router.post("/2fa/setup")
async def setup_2fa(setup_data: TwoFASetup, auth = Depends(auth_dependency)):
    """Setup 2FA TOTP for user"""
    secret = pyotp.random_base32()
    totp_uri = pyotp.totp.TOTP(secret).provisioning_uri(
        name=setup_data.user_id,
        issuer_name="BHIV HR Platform"
    )
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(totp_uri)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img_buffer = io.BytesIO()
    img.save(img_buffer, format='PNG')
    img_str = base64.b64encode(img_buffer.getvalue()).decode()
    
    return {
        "user_id": setup_data.user_id,
        "secret": secret,
        "qr_code": f"data:image/png;base64,{img_str}",
        "manual_entry_key": secret,
        "instructions": "Scan QR code with Google Authenticator, Microsoft Authenticator, or Authy"
    }

@router.post("/2fa/verify")
async def verify_2fa(verify_data: TwoFAVerify, auth = Depends(auth_dependency)):
    """Verify 2FA TOTP code"""
    # In production, get secret from database
    stored_secret = "JBSWY3DPEHPK3PXP"  # Demo secret
    totp = pyotp.TOTP(stored_secret)
    
    if totp.verify(verify_data.totp_code, valid_window=1):
        return {
            "success": True,
            "user_id": verify_data.user_id,
            "verified_at": datetime.now(timezone.utc).isoformat()
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid 2FA code")

@router.post("/login")
async def login_with_2fa(login_data: LoginRequest):
    """Login with optional 2FA"""
    # Basic authentication (in production, verify against database)
    if login_data.username == "admin" and login_data.password == "admin123":
        # If 2FA is enabled for user, verify TOTP
        if login_data.totp_code:
            stored_secret = "JBSWY3DPEHPK3PXP"
            totp = pyotp.TOTP(stored_secret)
            
            if not totp.verify(login_data.totp_code, valid_window=1):
                raise HTTPException(status_code=401, detail="Invalid 2FA code")
        
        # Generate JWT token
        jwt_secret = os.getenv("JWT_SECRET", "fallback_jwt_secret_key_for_client_auth_2025")
        payload = {
            "user_id": login_data.username,
            "exp": datetime.utcnow() + timedelta(hours=24),
            "iat": datetime.utcnow(),
            "type": "user_token"
        }
        
        token = jwt.encode(payload, jwt_secret, algorithm="HS256")
        
        return {
            "success": True,
            "access_token": token,
            "token_type": "bearer",
            "expires_in": 86400,
            "user_id": login_data.username,
            "2fa_verified": bool(login_data.totp_code)
        }
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/2fa/status/{user_id}")
async def get_2fa_status(user_id: str, auth = Depends(auth_dependency)):
    """Get 2FA status for user"""
    return {
        "user_id": user_id,
        "2fa_enabled": True,  # In production, check database
        "setup_date": "2025-01-01T12:00:00Z",
        "last_used": "2025-01-02T08:30:00Z",
        "backup_codes_remaining": 8
    }