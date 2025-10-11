"""
Phase 3 Gateway Integration
Integrates consolidated semantic engine with gateway API endpoints
"""

import os
import sys
import asyncio
import httpx
from typing import Optional, Dict, Any

# Add semantic engine to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

# Add absolute paths for deployment
sys.path.insert(0, "/app/services")
sys.path.insert(0, "/app/services/semantic_engine")
sys.path.insert(0, "/app")

try:
    from semantic_engine.phase3_engine import Phase3SemanticEngine
    PHASE3_AVAILABLE = True
except ImportError:
    try:
        from phase3_engine import Phase3SemanticEngine
        PHASE3_AVAILABLE = True
    except ImportError:
        try:
            import sys
            import os
            # Try to import from semantic_engine directory
            semantic_path = os.path.join(os.path.dirname(__file__), '..', '..', 'semantic_engine')
            sys.path.insert(0, semantic_path)
            from phase3_engine import Phase3SemanticEngine
            PHASE3_AVAILABLE = True
        except ImportError:
            PHASE3_AVAILABLE = False
            Phase3SemanticEngine = None

class Phase3GatewayIntegration:
    """Integration layer for Phase 3 features in gateway"""
    
    def __init__(self):
        self.phase3_engine = None
        self.agent_url = os.getenv("AGENT_SERVICE_URL", "https://bhiv-hr-agent-m1me.onrender.com")
        
        if PHASE3_AVAILABLE:
            try:
                self.phase3_engine = Phase3SemanticEngine()
                print("INFO: Phase 3 gateway integration initialized")
            except Exception as e:
                print(f"WARNING: Phase 3 gateway integration failed: {e}")
    
    async def enhanced_ai_matching(self, job_id: int, limit: int = 10) -> Dict[str, Any]:
        """Enhanced AI matching with Phase 3 features"""
        try:
            # Try agent service first
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    f"{self.agent_url}/match",
                    json={"job_id": job_id},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    agent_result = response.json()
                    
                    # Check if Phase 3 algorithm is being used
                    algorithm_version = agent_result.get("algorithm_version", "")
                    if "3.0.0" in algorithm_version:
                        agent_result["phase3_enabled"] = True
                        agent_result["features"] = [
                            "Adaptive Scoring",
                            "Cultural Fit Analysis", 
                            "Company Preferences",
                            "Learning Engine"
                        ]
                    else:
                        agent_result["phase3_enabled"] = False
                        agent_result["features"] = ["Basic Semantic Matching"]
                    
                    return self._format_gateway_response(agent_result, job_id, limit)
                else:
                    return await self._fallback_matching(job_id, limit)
                    
        except Exception as e:
            print(f"ERROR: Enhanced AI matching failed: {e}")
            return await self._fallback_matching(job_id, limit)
    
    async def enhanced_batch_matching(self, job_ids: list) -> Dict[str, Any]:
        """Enhanced batch matching with Phase 3 features"""
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    f"{self.agent_url}/batch-match",
                    json={"job_ids": job_ids},
                    headers={"Content-Type": "application/json"}
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    # Add Phase 3 metadata
                    algorithm_version = result.get("algorithm_version", "")
                    if "3.0.0" in algorithm_version:
                        result["phase3_features"] = {
                            "async_processing": True,
                            "smart_caching": True,
                            "chunk_optimization": True,
                            "learning_integration": True
                        }
                    
                    return result
                else:
                    raise Exception(f"Agent service returned {response.status_code}")
                    
        except Exception as e:
            print(f"ERROR: Enhanced batch matching failed: {e}")
            return {
                "batch_results": {},
                "total_jobs_processed": 0,
                "error": str(e),
                "status": "failed"
            }
    
    def _format_gateway_response(self, agent_result: Dict[str, Any], job_id: int, limit: int) -> Dict[str, Any]:
        """Format agent response for gateway API"""
        matches = []
        for candidate in agent_result.get("top_candidates", [])[:limit]:
            matches.append({
                "candidate_id": candidate.get("candidate_id"),
                "name": candidate.get("name"),
                "email": candidate.get("email"),
                "score": candidate.get("score"),
                "skills_match": ", ".join(candidate.get("skills_match", [])),
                "experience_match": candidate.get("experience_match"),
                "location_match": candidate.get("location_match"),
                "reasoning": candidate.get("reasoning"),
                "recommendation_strength": "Strong Match" if candidate.get("score", 0) > 80 else "Good Match"
            })
        
        return {
            "matches": matches,
            "top_candidates": matches,
            "job_id": job_id,
            "limit": limit,
            "total_candidates": agent_result.get("total_candidates", 0),
            "algorithm_version": agent_result.get("algorithm_version", "unknown"),
            "processing_time": f"{agent_result.get('processing_time', 0)}s",
            "ai_analysis": "Phase 3 Enhanced AI Matching" if agent_result.get("phase3_enabled") else "Basic AI Matching",
            "agent_status": "connected",
            "phase3_enabled": agent_result.get("phase3_enabled", False),
            "features": agent_result.get("features", [])
        }
    
    async def _fallback_matching(self, job_id: int, limit: int) -> Dict[str, Any]:
        """Fallback matching when agent service is unavailable"""
        try:
            from sqlalchemy import create_engine, text
            
            database_url = os.getenv("DATABASE_URL", 
                "postgresql://bhiv_user:3CvUtwqULlIcQujUzJ3SNzhStTGbRbU2@dpg-d3bfmj8dl3ps739blqt0-a.oregon-postgres.render.com/bhiv_hr_jcuu")
            engine = create_engine(database_url)
            
            with engine.connect() as connection:
                query = text("SELECT id, name, email, technical_skills FROM candidates LIMIT :limit")
                result = connection.execute(query, {"limit": limit})
                matches = [{
                    "candidate_id": row[0],
                    "name": row[1],
                    "email": row[2],
                    "score": 75.0 + (row[0] % 20),
                    "skills_match": row[3] or "",
                    "experience_match": "Gateway fallback",
                    "location_match": True,
                    "reasoning": "Gateway fallback matching",
                    "recommendation_strength": "Fallback Match"
                } for row in result]
            
            return {
                "matches": matches,
                "top_candidates": matches,
                "job_id": job_id,
                "limit": limit,
                "algorithm_version": "3.0.0-gateway-fallback",
                "processing_time": "0.05s",
                "ai_analysis": "Gateway fallback - Agent service unavailable",
                "agent_status": "disconnected",
                "phase3_enabled": False,
                "features": ["Database Fallback"]
            }
        except Exception as e:
            return {
                "matches": [], 
                "job_id": job_id, 
                "limit": limit, 
                "error": str(e), 
                "agent_status": "error",
                "phase3_enabled": False
            }

# Global instance for gateway use
phase3_integration = Phase3GatewayIntegration()