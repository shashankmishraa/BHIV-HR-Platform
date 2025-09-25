"""Workflow orchestration router"""

from fastapi import APIRouter, BackgroundTasks, HTTPException
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from enum import Enum
import uuid
import asyncio

from app.shared.models import WorkflowStatus, WorkflowStep

router = APIRouter(prefix="/v1/workflows", tags=["Workflows"])

class WorkflowType(str, Enum):
    CANDIDATE_ONBOARDING = "candidate_onboarding"
    JOB_POSTING = "job_posting"
    INTERVIEW_PROCESS = "interview_process"
    HIRING_PIPELINE = "hiring_pipeline"
    BULK_OPERATIONS = "bulk_operations"

# In-memory workflow storage
workflows_store: Dict[str, dict] = {}

WORKFLOW_DEFINITIONS = {
    WorkflowType.CANDIDATE_ONBOARDING: [
        {"step_id": "validate_data", "name": "Validate Candidate Data"},
        {"step_id": "create_profile", "name": "Create Candidate Profile"},
        {"step_id": "extract_resume", "name": "Extract Resume Information"},
        {"step_id": "skill_analysis", "name": "Analyze Skills & Experience"},
        {"step_id": "ai_matching", "name": "Generate AI Matches"},
        {"step_id": "send_welcome", "name": "Send Welcome Email"}
    ],
    WorkflowType.JOB_POSTING: [
        {"step_id": "validate_job", "name": "Validate Job Requirements"},
        {"step_id": "create_job", "name": "Create Job Posting"},
        {"step_id": "setup_matching", "name": "Setup AI Matching Criteria"},
        {"step_id": "publish_job", "name": "Publish Job Posting"},
        {"step_id": "notify_team", "name": "Notify Hiring Team"}
    ],
    WorkflowType.INTERVIEW_PROCESS: [
        {"step_id": "schedule_interview", "name": "Schedule Interview"},
        {"step_id": "send_invites", "name": "Send Calendar Invites"},
        {"step_id": "prepare_materials", "name": "Prepare Interview Materials"},
        {"step_id": "conduct_interview", "name": "Conduct Interview"},
        {"step_id": "collect_feedback", "name": "Collect Feedback"},
        {"step_id": "update_status", "name": "Update Candidate Status"}
    ]
}

@router.post("")
async def create_workflow(
    workflow_type: WorkflowType,
    metadata: Optional[Dict[str, Any]] = None,
    background_tasks: BackgroundTasks = None
):
    """Create new workflow instance"""
    workflow_id = f"wf_{uuid.uuid4().hex[:8]}"
    
    # Create workflow steps
    steps = [
        WorkflowStep(**step_def).dict()
        for step_def in WORKFLOW_DEFINITIONS.get(workflow_type, [])
    ]
    
    workflow = {
        "workflow_id": workflow_id,
        "workflow_type": workflow_type,
        "status": WorkflowStatus.PENDING,
        "steps": steps,
        "created_at": datetime.now(timezone.utc),
        "metadata": metadata or {}
    }
    
    workflows_store[workflow_id] = workflow
    
    # Start workflow execution in background
    if background_tasks:
        background_tasks.add_task(execute_workflow, workflow_id)
    
    return workflow

@router.get("")
async def list_workflows(
    status: Optional[WorkflowStatus] = None,
    workflow_type: Optional[WorkflowType] = None,
    limit: int = 50
):
    """List workflows with filtering"""
    workflows = list(workflows_store.values())
    
    if status:
        workflows = [w for w in workflows if w["status"] == status]
    if workflow_type:
        workflows = [w for w in workflows if w["workflow_type"] == workflow_type]
    
    workflows.sort(key=lambda w: w["created_at"], reverse=True)
    return {"workflows": workflows[:limit], "total": len(workflows)}

@router.get("/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get specific workflow details"""
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflows_store[workflow_id]

@router.post("/{workflow_id}/start")
async def start_workflow(workflow_id: str, background_tasks: BackgroundTasks):
    """Start workflow execution"""
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_store[workflow_id]
    
    if workflow["status"] != WorkflowStatus.PENDING:
        raise HTTPException(status_code=400, detail="Workflow already started or completed")
    
    workflow["status"] = WorkflowStatus.IN_PROGRESS
    workflow["started_at"] = datetime.now(timezone.utc)
    
    background_tasks.add_task(execute_workflow, workflow_id)
    
    return {"message": "Workflow started", "workflow_id": workflow_id}

@router.post("/{workflow_id}/cancel")
async def cancel_workflow(workflow_id: str):
    """Cancel workflow execution"""
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_store[workflow_id]
    
    if workflow["status"] in [WorkflowStatus.COMPLETED, WorkflowStatus.FAILED]:
        raise HTTPException(status_code=400, detail="Cannot cancel completed workflow")
    
    workflow["status"] = WorkflowStatus.CANCELLED
    workflow["completed_at"] = datetime.now(timezone.utc)
    
    return {"message": "Workflow cancelled", "workflow_id": workflow_id}

@router.get("/{workflow_id}/steps")
async def get_workflow_steps(workflow_id: str):
    """Get workflow step details"""
    if workflow_id not in workflows_store:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_store[workflow_id]
    
    return {
        "workflow_id": workflow_id,
        "total_steps": len(workflow["steps"]),
        "completed_steps": len([s for s in workflow["steps"] if s["status"] == WorkflowStatus.COMPLETED]),
        "failed_steps": len([s for s in workflow["steps"] if s["status"] == WorkflowStatus.FAILED]),
        "steps": workflow["steps"]
    }

@router.get("/analytics")
async def get_workflow_analytics():
    """Get workflow execution analytics"""
    workflows = list(workflows_store.values())
    
    if not workflows:
        return {"message": "No workflows found"}
    
    total_workflows = len(workflows)
    completed_workflows = len([w for w in workflows if w["status"] == WorkflowStatus.COMPLETED])
    failed_workflows = len([w for w in workflows if w["status"] == WorkflowStatus.FAILED])
    
    return {
        "total_workflows": total_workflows,
        "success_rate": (completed_workflows / total_workflows * 100) if total_workflows > 0 else 0,
        "failure_rate": (failed_workflows / total_workflows * 100) if total_workflows > 0 else 0,
        "workflow_distribution": {
            wf_type.value: len([w for w in workflows if w["workflow_type"] == wf_type])
            for wf_type in WorkflowType
        }
    }

@router.get("/health")
async def get_workflow_system_health():
    """Get workflow system health status"""
    active_workflows = len([w for w in workflows_store.values() if w["status"] == WorkflowStatus.IN_PROGRESS])
    failed_workflows = len([w for w in workflows_store.values() if w["status"] == WorkflowStatus.FAILED])
    
    health_status = "healthy"
    if failed_workflows > 5:
        health_status = "degraded"
    if active_workflows > 20:
        health_status = "overloaded"
    
    return {
        "status": health_status,
        "active_workflows": active_workflows,
        "failed_workflows": failed_workflows,
        "system_capacity": "normal",
        "last_check": datetime.now(timezone.utc).isoformat()
    }

# Pipeline endpoints
@router.get("/pipelines/templates")
async def list_pipeline_templates():
    """List available pipeline templates"""
    templates = [
        {
            "template_id": "complete_candidate_flow",
            "name": "Complete Candidate Management Flow",
            "description": "End-to-end candidate processing pipeline",
            "steps_count": 4
        },
        {
            "template_id": "job_posting_workflow",
            "name": "Job Posting Workflow",
            "description": "Complete job creation and matching pipeline",
            "steps_count": 4
        },
        {
            "template_id": "interview_management_flow",
            "name": "Interview Management Flow",
            "description": "Complete interview scheduling and management",
            "steps_count": 4
        }
    ]
    
    return {
        "templates": templates,
        "total_templates": len(templates)
    }

@router.post("/pipelines/execute/{template_id}")
async def execute_pipeline_template(
    template_id: str,
    parameters: Optional[Dict[str, Any]] = None,
    background_tasks: BackgroundTasks = None
):
    """Execute pipeline template"""
    execution_id = f"exec_{uuid.uuid4().hex[:8]}"
    
    if background_tasks:
        background_tasks.add_task(execute_pipeline, execution_id, template_id, parameters or {})
    
    return {
        "execution_id": execution_id,
        "template_id": template_id,
        "status": "started",
        "started_at": datetime.now(timezone.utc).isoformat()
    }

# Workflow execution engine
async def execute_workflow(workflow_id: str):
    """Execute workflow steps sequentially"""
    if workflow_id not in workflows_store:
        return
    
    workflow = workflows_store[workflow_id]
    
    try:
        workflow["status"] = WorkflowStatus.IN_PROGRESS
        workflow["started_at"] = datetime.now(timezone.utc)
        
        for step in workflow["steps"]:
            if step["status"] == WorkflowStatus.COMPLETED:
                continue
            
            # Execute step
            step["status"] = WorkflowStatus.IN_PROGRESS
            step["started_at"] = datetime.now(timezone.utc)
            
            # Simulate step execution
            await asyncio.sleep(1)
            
            step["status"] = WorkflowStatus.COMPLETED
            step["completed_at"] = datetime.now(timezone.utc)
            step["output"] = {"status": "completed", "timestamp": datetime.now(timezone.utc).isoformat()}
        
        workflow["status"] = WorkflowStatus.COMPLETED
        workflow["completed_at"] = datetime.now(timezone.utc)
        
    except Exception as e:
        workflow["status"] = WorkflowStatus.FAILED
        workflow["completed_at"] = datetime.now(timezone.utc)

async def execute_pipeline(execution_id: str, template_id: str, parameters: dict):
    """Execute pipeline template"""
    # Pipeline execution implementation would go here
    await asyncio.sleep(2)  # Simulate pipeline execution