"""Workflow Engine Module for BHIV HR Platform"""

from typing import Dict, Any, List, Optional
import logging

logger = logging.getLogger(__name__)

class WorkflowEngine:
    """Simple workflow engine for HR processes"""
    
    def __init__(self):
        self.workflows = {}
        logger.info("Workflow engine initialized")
    
    def register_workflow(self, name: str, steps: List[str]) -> bool:
        """Register a new workflow"""
        try:
            self.workflows[name] = steps
            return True
        except Exception as e:
            logger.error(f"Failed to register workflow {name}: {e}")
            return False
    
    def execute_workflow(self, name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a workflow"""
        try:
            if name not in self.workflows:
                return {"status": "error", "message": f"Workflow {name} not found"}
            
            return {
                "status": "success",
                "workflow": name,
                "steps": self.workflows[name],
                "data": data
            }
        except Exception as e:
            logger.error(f"Workflow execution failed: {e}")
            return {"status": "error", "message": str(e)}

# Global workflow engine instance
workflow_engine = WorkflowEngine()

# Register default workflows
workflow_engine.register_workflow("candidate_onboarding", [
    "application_received",
    "initial_screening", 
    "interview_scheduled",
    "interview_completed",
    "decision_made"
])

workflow_engine.register_workflow("job_posting", [
    "job_created",
    "approval_pending",
    "job_published",
    "applications_received",
    "job_closed"
])