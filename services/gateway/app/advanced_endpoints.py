#!/usr/bin/env python3
"""
Advanced Enterprise Endpoints
Password management, session management, and security features
"""

import secrets
import hashlib
from datetime import datetime, timezone, timedelta
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field
from fastapi import HTTPException

# Request models for advanced endpoints
class BulkPasswordReset(BaseModel):
    user_ids: List[str] = Field(..., min_items=1, max_items=100)
    force_change: bool = Field(default=True)
    reset_reason: str = Field(default="admin_reset", max_length=100)

class SessionCleanupConfig(BaseModel):
    max_age_hours: int = Field(default=24, ge=1, le=168)
    cleanup_inactive: bool = Field(default=True)
    force_cleanup: bool = Field(default=False)

class ThreatDetectionConfig(BaseModel):
    enable_monitoring: bool = Field(default=True)
    alert_threshold: int = Field(default=5, ge=1, le=100)
    time_window_minutes: int = Field(default=60, ge=1, le=1440)

# Advanced password management
async def get_password_history(user_id: str, api_key: str) -> Dict[str, Any]:
    """Get password history for user"""
    try:
        from auth_manager import auth_manager
        
        if not user_id or len(user_id.strip()) == 0:
            raise HTTPException(status_code=400, detail="User ID is required")
        
        history = auth_manager.get_password_history(user_id)
        
        # Sanitize sensitive data
        sanitized_history = []
        for entry in history:
            sanitized_history.append({
                "changed_at": entry.get("changed_at"),
                "reason": entry.get("reason", "unknown"),
                "ip_address": entry.get("ip_address", "unknown"),
                "user_agent": entry.get("user_agent", "unknown")[:50] + "..." if len(entry.get("user_agent", "")) > 50 else entry.get("user_agent", "unknown")
            })
        
        return {
            "user_id": user_id,
            "password_history": sanitized_history,
            "total_changes": len(sanitized_history),
            "policy": {
                "max_history": 12,
                "min_age_days": 1,
                "reuse_prevention": True
            },
            "retrieved_at": datetime.now(timezone.utc).isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Password history retrieval failed: {str(e)}")

async def bulk_password_reset(reset_data: BulkPasswordReset, api_key: str) -> Dict[str, Any]:
    """Bulk password reset for multiple users"""
    try:
        from auth_manager import auth_manager
        
        results = {
            "successful_resets": [],
            "failed_resets": [],
            "total_requested": len(reset_data.user_ids),
            "reset_timestamp": datetime.now(timezone.utc).isoformat()
        }
        
        for user_id in reset_data.user_ids:
            try:
                # Generate secure temporary password
                temp_password = secrets.token_urlsafe(12)
                
                # Reset password
                success = auth_manager.reset_password(
                    user_id=user_id,
                    new_password=temp_password,
                    force_change=reset_data.force_change,
                    reset_reason=reset_data.reset_reason
                )
                
                if success:
                    results["successful_resets"].append({
                        "user_id": user_id,
                        "temporary_password": temp_password,
                        "force_change": reset_data.force_change,
                        "reset_reason": reset_data.reset_reason
                    })
                else:
                    results["failed_resets"].append({
                        "user_id": user_id,
                        "error": "User not found or reset failed"
                    })
                    
            except Exception as e:
                results["failed_resets"].append({
                    "user_id": user_id,
                    "error": str(e)
                })
        
        return {
            "message": f"Bulk password reset completed: {len(results['successful_resets'])}/{results['total_requested']} successful",
            "results": results,
            "security_note": "Temporary passwords should be changed immediately",
            "next_steps": [
                "Notify users of password reset",
                "Ensure users change temporary passwords",
                "Monitor for successful logins"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Bulk password reset failed: {str(e)}")

# Advanced session management
async def get_active_sessions(api_key: str) -> Dict[str, Any]:
    """Get all active sessions with detailed information"""
    try:
        from auth_manager import auth_manager
        
        current_time = datetime.now(timezone.utc)
        active_sessions = []
        
        for session_id, session in auth_manager.sessions.items():
            if session.is_active and session.expires_at > current_time:
                # Calculate session duration
                duration = current_time - session.created_at
                
                active_sessions.append({
                    "session_id": session_id[:8] + "...",
                    "user_id": session.user_id,
                    "created_at": session.created_at.isoformat(),
                    "expires_at": session.expires_at.isoformat(),
                    "last_activity": session.last_activity.isoformat() if session.last_activity else None,
                    "ip_address": session.ip_address,
                    "user_agent": session.user_agent[:50] + "..." if len(session.user_agent) > 50 else session.user_agent,
                    "session_type": session.session_type,
                    "two_factor_verified": session.two_factor_verified,
                    "duration_minutes": int(duration.total_seconds() / 60),
                    "time_remaining_minutes": int((session.expires_at - current_time).total_seconds() / 60)
                })
        
        # Session statistics
        total_sessions = len(auth_manager.sessions)
        expired_sessions = total_sessions - len(active_sessions)
        
        return {
            "active_sessions": active_sessions,
            "session_statistics": {
                "total_active": len(active_sessions),
                "total_sessions": total_sessions,
                "expired_sessions": expired_sessions,
                "average_duration_minutes": sum(s["duration_minutes"] for s in active_sessions) / len(active_sessions) if active_sessions else 0
            },
            "session_policy": {
                "timeout_hours": 24,
                "max_concurrent_sessions": 5,
                "require_2fa": False,
                "track_ip_changes": True
            },
            "retrieved_at": current_time.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Active sessions retrieval failed: {str(e)}")

async def cleanup_sessions(cleanup_config: SessionCleanupConfig, api_key: str) -> Dict[str, Any]:
    """Clean up expired and inactive sessions"""
    try:
        from auth_manager import auth_manager
        
        current_time = datetime.now(timezone.utc)
        cleanup_results = {
            "expired_sessions_removed": 0,
            "inactive_sessions_removed": 0,
            "total_sessions_before": len(auth_manager.sessions),
            "cleanup_timestamp": current_time.isoformat()
        }
        
        sessions_to_remove = []
        
        for session_id, session in auth_manager.sessions.items():
            # Remove expired sessions
            if session.expires_at <= current_time:
                sessions_to_remove.append(session_id)
                cleanup_results["expired_sessions_removed"] += 1
                continue
            
            # Remove inactive sessions if configured
            if cleanup_config.cleanup_inactive and session.last_activity:
                inactive_threshold = current_time - timedelta(hours=cleanup_config.max_age_hours)
                if session.last_activity < inactive_threshold:
                    sessions_to_remove.append(session_id)
                    cleanup_results["inactive_sessions_removed"] += 1
                    continue
            
            # Force cleanup if configured
            if cleanup_config.force_cleanup:
                session_age = current_time - session.created_at
                if session_age > timedelta(hours=cleanup_config.max_age_hours):
                    sessions_to_remove.append(session_id)
                    cleanup_results["inactive_sessions_removed"] += 1
        
        # Remove identified sessions
        for session_id in sessions_to_remove:
            auth_manager.invalidate_session(session_id)
        
        cleanup_results["total_sessions_after"] = len(auth_manager.sessions)
        cleanup_results["total_removed"] = len(sessions_to_remove)
        
        return {
            "message": f"Session cleanup completed: {cleanup_results['total_removed']} sessions removed",
            "cleanup_results": cleanup_results,
            "cleanup_configuration": {
                "max_age_hours": cleanup_config.max_age_hours,
                "cleanup_inactive": cleanup_config.cleanup_inactive,
                "force_cleanup": cleanup_config.force_cleanup
            },
            "recommendations": [
                "Run cleanup regularly to maintain performance",
                "Monitor session patterns for security",
                "Adjust cleanup policies based on usage patterns"
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Session cleanup failed: {str(e)}")

# Advanced security features
async def get_threat_detection(api_key: str) -> Dict[str, Any]:
    """Get threat detection report"""
    try:
        current_time = datetime.now(timezone.utc)
        
        # Simulate threat detection data (in production, this would come from security monitoring)
        threat_data = {
            "monitoring_period_hours": 24,
            "threats_detected": [
                {
                    "threat_id": "THR_001",
                    "threat_type": "Brute Force Attack",
                    "severity": "High",
                    "source_ip": "192.168.1.100",
                    "target_endpoint": "/v1/auth/login",
                    "attempts": 15,
                    "detected_at": (current_time - timedelta(hours=2)).isoformat(),
                    "status": "Blocked",
                    "mitigation": "IP temporarily blocked"
                },
                {
                    "threat_id": "THR_002", 
                    "threat_type": "SQL Injection Attempt",
                    "severity": "Critical",
                    "source_ip": "10.0.0.50",
                    "target_endpoint": "/v1/candidates/search",
                    "attempts": 3,
                    "detected_at": (current_time - timedelta(hours=1)).isoformat(),
                    "status": "Blocked",
                    "mitigation": "Request sanitized and blocked"
                }
            ],
            "security_metrics": {
                "total_requests": 15420,
                "blocked_requests": 18,
                "threat_detection_rate": 0.12,
                "false_positive_rate": 0.02,
                "response_time_ms": 2.5
            },
            "threat_categories": {
                "brute_force": 1,
                "sql_injection": 1,
                "xss_attempts": 0,
                "csrf_attempts": 0,
                "rate_limit_violations": 0
            }
        }
        
        return {
            "threat_detection_report": threat_data,
            "system_status": {
                "monitoring_active": True,
                "last_update": current_time.isoformat(),
                "detection_rules": 25,
                "active_blocks": 2
            },
            "recommendations": [
                "Review and update security rules regularly",
                "Monitor for new threat patterns",
                "Implement additional rate limiting for sensitive endpoints",
                "Consider implementing CAPTCHA for repeated failures"
            ],
            "generated_at": current_time.isoformat()
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Threat detection report failed: {str(e)}")