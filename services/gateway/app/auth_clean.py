# Authentication Router
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest):
    """User login endpoint"""
    # Basic validation
    if request.username == "admin" and request.password == "admin123":
        return TokenResponse(access_token="mock_token_123")
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/logout")
async def logout():
    """User logout endpoint"""
    return {"message": "Logged out successfully"}

@router.get("/profile")
async def get_profile():
    """Get user profile"""
    return {
        "user_id": "user_123",
        "username": "admin",
        "role": "administrator"
    }

@router.post("/register")
async def register(request: LoginRequest):
    """User registration endpoint"""
    return {"message": "User registered successfully", "user_id": "user_new"}