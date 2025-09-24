"""Workflow Engine Implementation for BHIV HR Platform"""

import asyncio
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import logging

logger = logging.getLogger("workflow_engine")

class WorkflowStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowStep:
    def __init__(self, step_id: str, name: str, handler: Callable):
        self.step_id = step_id
        self.name = name
        self.handler = handler
        self.status = WorkflowStatus.PENDING
        self.started_at = None
        self.completed_at = None
        self.error = None
        self.output = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "step_id": self.step_id,
            "name": self.name,
            "status": self.status.value,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "error": self.error,
            "output": self.output
        }

class Workflow:
    def __init__(self, workflow_id: str, workflow_type: str):
        self.workflow_id = workflow_id
        self.workflow_type = workflow_type
        self.status = WorkflowStatus.PENDING
        self.steps: List[WorkflowStep] = []
        self.created_at = datetime.now()
        self.started_at = None
        self.completed_at = None
        self.metadata = {}

    def add_step(self, step_id: str, name: str, handler: Callable) -> WorkflowStep:
        step = WorkflowStep(step_id, name, handler)
        self.steps.append(step)
        return step

    def to_dict(self) -> Dict[str, Any]:
        return {
            "workflow_id": self.workflow_id,
            "workflow_type": self.workflow_type,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "steps": [step.to_dict() for step in self.steps],
            "metadata": self.metadata
        }

class WorkflowEngine:
    def __init__(self):
        self.workflows: Dict[str, Workflow] = {}
        self.running_workflows: Dict[str, asyncio.Task] = {}

    def create_workflow(self, workflow_type: str, metadata: Dict = None) -> str:
        workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
        workflow = Workflow(workflow_id, workflow_type)
        workflow.metadata = metadata or {}
        self.workflows[workflow_id] = workflow
        logger.info(f"Created workflow {workflow_id} of type {workflow_type}")
        return workflow_id

    def get_workflow(self, workflow_id: str) -> Optional[Workflow]:
        return self.workflows.get(workflow_id)

    def list_workflows(self, workflow_type: str = None, status: str = None) -> List[Workflow]:
        workflows = list(self.workflows.values())
        
        if workflow_type:
            workflows = [w for w in workflows if w.workflow_type == workflow_type]
        
        if status:
            workflows = [w for w in workflows if w.status.value == status]
        
        return workflows

    async def execute_workflow(self, workflow_id: str):
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            logger.error(f"Workflow {workflow_id} not found")
            return

        workflow.status = WorkflowStatus.RUNNING
        workflow.started_at = datetime.now()
        logger.info(f"Starting workflow {workflow_id}")

        try:
            for step in workflow.steps:
                step.status = WorkflowStatus.RUNNING
                step.started_at = datetime.now()
                logger.info(f"Executing step {step.step_id} in workflow {workflow_id}")
                
                try:
                    step.output = await step.handler(workflow.metadata)
                    step.status = WorkflowStatus.COMPLETED
                    step.completed_at = datetime.now()
                    logger.info(f"Step {step.step_id} completed successfully")
                except Exception as e:
                    step.status = WorkflowStatus.FAILED
                    step.error = str(e)
                    workflow.status = WorkflowStatus.FAILED
                    logger.error(f"Workflow {workflow_id} step {step.step_id} failed: {e}")
                    return

            workflow.status = WorkflowStatus.COMPLETED
            workflow.completed_at = datetime.now()
            logger.info(f"Workflow {workflow_id} completed successfully")

        except Exception as e:
            workflow.status = WorkflowStatus.FAILED
            logger.error(f"Workflow {workflow_id} failed: {e}")
        finally:
            # Clean up running workflow reference
            if workflow_id in self.running_workflows:
                del self.running_workflows[workflow_id]

    def start_workflow(self, workflow_id: str) -> bool:
        if workflow_id in self.running_workflows:
            logger.warning(f"Workflow {workflow_id} is already running")
            return False
        
        workflow = self.workflows.get(workflow_id)
        if not workflow:
            logger.error(f"Workflow {workflow_id} not found")
            return False
        
        task = asyncio.create_task(self.execute_workflow(workflow_id))
        self.running_workflows[workflow_id] = task
        logger.info(f"Started workflow {workflow_id}")
        return True

    def cancel_workflow(self, workflow_id: str) -> bool:
        if workflow_id in self.running_workflows:
            task = self.running_workflows[workflow_id]
            task.cancel()
            del self.running_workflows[workflow_id]
            
            workflow = self.workflows.get(workflow_id)
            if workflow:
                workflow.status = WorkflowStatus.CANCELLED
            
            logger.info(f"Cancelled workflow {workflow_id}")
            return True
        return False

# Global workflow engine instance
workflow_engine = WorkflowEngine()

# Workflow step handlers
async def job_validation_handler(metadata: Dict) -> Dict:
    """Validate job data"""
    await asyncio.sleep(0.1)  # Simulate processing time
    job_id = metadata.get("job_id", "unknown")
    
    # Simulate validation logic
    validation_result = {
        "validation_status": "passed",
        "job_id": job_id,
        "checks_performed": ["title_length", "description_content", "salary_range"],
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"Job validation completed for {job_id}")
    return validation_result

async def ai_processing_handler(metadata: Dict) -> Dict:
    """Process job with AI matching algorithms"""
    await asyncio.sleep(0.5)  # Simulate AI processing time
    job_id = metadata.get("job_id", "unknown")
    
    # Simulate AI processing
    ai_result = {
        "ai_processing_status": "completed",
        "job_id": job_id,
        "match_score": 85.5,
        "keywords_extracted": ["python", "fastapi", "postgresql"],
        "difficulty_level": "intermediate",
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"AI processing completed for {job_id}")
    return ai_result

async def notification_handler(metadata: Dict) -> Dict:
    """Send notifications for job posting"""
    await asyncio.sleep(0.2)  # Simulate notification time
    job_id = metadata.get("job_id", "unknown")
    
    # Simulate notification sending
    notification_result = {
        "notification_status": "sent",
        "job_id": job_id,
        "notifications_sent": 3,
        "channels": ["email", "webhook", "dashboard"],
        "recipients": ["hr_team", "hiring_manager", "system_admin"],
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"Notifications sent for {job_id}")
    return notification_result

async def candidate_verification_handler(metadata: Dict) -> Dict:
    """Verify candidate information"""
    await asyncio.sleep(0.3)
    candidate_id = metadata.get("candidate_id", "unknown")
    
    verification_result = {
        "verification_status": "completed",
        "candidate_id": candidate_id,
        "email_verified": True,
        "phone_verified": True,
        "document_verified": False,
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"Candidate verification completed for {candidate_id}")
    return verification_result

async def profile_setup_handler(metadata: Dict) -> Dict:
    """Setup candidate profile"""
    await asyncio.sleep(0.2)
    candidate_id = metadata.get("candidate_id", "unknown")
    
    profile_result = {
        "profile_status": "created",
        "candidate_id": candidate_id,
        "profile_completeness": 85,
        "skills_extracted": True,
        "preferences_set": True,
        "timestamp": datetime.now().isoformat()
    }
    
    logger.info(f"Profile setup completed for {candidate_id}")
    return profile_result

# Workflow template functions
def create_job_posting_workflow(job_data: Dict) -> str:
    """Create job posting workflow with validation, AI processing, and notifications"""
    workflow_id = workflow_engine.create_workflow("job_posting", job_data)
    workflow = workflow_engine.get_workflow(workflow_id)
    
    workflow.add_step("validate", "Job Validation", job_validation_handler)
    workflow.add_step("ai_process", "AI Processing", ai_processing_handler)
    workflow.add_step("notify", "Send Notifications", notification_handler)
    
    logger.info(f"Created job posting workflow {workflow_id}")
    return workflow_id

def create_candidate_onboarding_workflow(candidate_data: Dict) -> str:
    """Create candidate onboarding workflow"""
    workflow_id = workflow_engine.create_workflow("candidate_onboarding", candidate_data)
    workflow = workflow_engine.get_workflow(workflow_id)
    
    workflow.add_step("verify", "Candidate Verification", candidate_verification_handler)
    workflow.add_step("profile", "Profile Setup", profile_setup_handler)
    workflow.add_step("notify", "Welcome Notifications", notification_handler)
    
    logger.info(f"Created candidate onboarding workflow {workflow_id}")
    return workflow_id

def create_interview_scheduling_workflow(interview_data: Dict) -> str:
    """Create interview scheduling workflow"""
    workflow_id = workflow_engine.create_workflow("interview_scheduling", interview_data)
    workflow = workflow_engine.get_workflow(workflow_id)
    
    # Add interview-specific steps here
    workflow.add_step("schedule", "Schedule Interview", notification_handler)  # Placeholder
    workflow.add_step("remind", "Send Reminders", notification_handler)
    
    logger.info(f"Created interview scheduling workflow {workflow_id}")
    return workflow_id

# Utility functions
def get_workflow_engine() -> WorkflowEngine:
    """Get the global workflow engine instance"""
    return workflow_engine

def get_workflow_stats() -> Dict[str, Any]:
    """Get workflow engine statistics"""
    workflows = list(workflow_engine.workflows.values())
    
    stats = {
        "total_workflows": len(workflows),
        "running_workflows": len(workflow_engine.running_workflows),
        "completed_workflows": len([w for w in workflows if w.status == WorkflowStatus.COMPLETED]),
        "failed_workflows": len([w for w in workflows if w.status == WorkflowStatus.FAILED]),
        "workflow_types": {}
    }
    
    # Count by type
    for workflow in workflows:
        workflow_type = workflow.workflow_type
        if workflow_type not in stats["workflow_types"]:
            stats["workflow_types"][workflow_type] = 0
        stats["workflow_types"][workflow_type] += 1
    
    return stats