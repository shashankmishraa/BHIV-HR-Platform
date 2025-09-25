"""Jobs workflow router"""

from fastapi import APIRouter, Query, BackgroundTasks, HTTPException
from typing import Optional
from datetime import datetime
import hashlib
from pydantic import ValidationError

from ..shared.models import JobCreate  # pyright: ignore[reportMissingImports]
from ..shared.validation import ValidationUtils, StandardJobCreate  # pyright: ignore[reportMissingImports]
from ..workflow_engine import workflow_engine, create_job_posting_workflow  # pyright: ignore[reportMissingImports]

router = APIRouter(prefix="/v1/jobs", tags=["Jobs"])

@router.get("")
async def list_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    department: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    status: Optional[str] = Query(None)
):
    """List job postings with filtering"""
    return {
        "jobs": [],
        "total": 7,
        "page": page,
        "per_page": per_page,
        "pages": 1,
        "filters": {
            "department": department,
            "experience_level": experience_level,
            "status": status
        }
    }

@router.post("")
async def create_job(job: JobCreate, background_tasks: BackgroundTasks):
    """Create new job posting with enhanced validation and trigger job workflow"""
    try:
        # Validate and normalize job data
        job_data = job.model_dump()
        validated_data = ValidationUtils.validate_job_data(job_data)
        
        # Generate job ID
        job_id = f"job_{hash(job.title + job.department) % 100000}"
        
        # Create and trigger job posting workflow
        workflow_id = create_job_posting_workflow({**validated_data, "job_id": job_id})
        workflow_engine.start_workflow(workflow_id)
        background_tasks.add_task(monitor_workflow_completion, workflow_id)
        
        return {
            "job_id": job_id,
            "id": job_id,  # For backward compatibility
            "message": "Job created successfully with enhanced validation",
            "status": "active",
            "workflow_triggered": True,
            "workflow_id": workflow_id,
            "created_at": datetime.now().isoformat(),
            "validation_applied": True,
            **validated_data
        }
    except ValidationError as e:
        # Return detailed validation errors
        error_details = []
        for error in e.errors():
            field = '.'.join(str(loc) for loc in error['loc'])
            error_details.append({
                "field": field,
                "message": error['msg'],
                "invalid_value": error.get('input')
            })
        
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Job validation failed",
                "errors": error_details,
                "help": {
                    "requirements": "Provide as list ['Python', 'FastAPI'] or string 'Python, FastAPI'",
                    "experience_level": "Use: Entry, Mid, Senior, Lead, or Executive",
                    "salary_fields": "Both salary_min and salary_max are required (integers)"
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": "Internal server error during job creation", "error": str(e)}
        )

@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get specific job details"""
    return {
        "id": job_id,
        "title": "Software Engineer",
        "department": "Engineering",
        "experience_level": "Mid-level",
        "salary_min": 80000,
        "salary_max": 120000,
        "status": "active"
    }

@router.put("/{job_id}")
async def update_job(job_id: str, job: JobCreate):
    """Update job posting with enhanced validation"""
    try:
        # Validate and normalize job data
        job_data = job.model_dump()
        validated_data = ValidationUtils.validate_job_data(job_data)
        
        return {
            "job_id": job_id,
            "id": job_id,  # For backward compatibility
            "message": "Job updated successfully with enhanced validation",
            "updated_at": datetime.now().isoformat(),
            "validation_applied": True,
            **validated_data
        }
    except ValidationError as e:
        # Return detailed validation errors
        error_details = []
        for error in e.errors():
            field = '.'.join(str(loc) for loc in error['loc'])
            error_details.append({
                "field": field,
                "message": error['msg'],
                "invalid_value": error.get('input')
            })
        
        raise HTTPException(
            status_code=422,
            detail={
                "message": "Job validation failed",
                "errors": error_details,
                "help": {
                    "requirements": "Provide as list ['Python', 'FastAPI'] or string 'Python, FastAPI'",
                    "experience_level": "Use: Entry, Mid, Senior, Lead, or Executive",
                    "salary_fields": "Both salary_min and salary_max are required (integers)"
                }
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={"message": "Internal server error during job update", "error": str(e)}
        )

@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete job posting"""
    return {"message": f"Job {job_id} deleted successfully"}

@router.get("/search")
async def search_jobs(
    q: str = Query(..., min_length=2),
    department: Optional[str] = Query(None),
    salary_min: Optional[int] = Query(None)
):
    """Search job postings"""
    return {
        "query": q,
        "results": [],
        "total": 0,
        "filters": {"department": department, "salary_min": salary_min}
    }

@router.get("/{job_id}/applications")
async def get_job_applications(job_id: str):
    """Get applications for specific job"""
    return {
        "job_id": job_id,
        "applications": [],
        "total": 0
    }

@router.get("/analytics")
async def get_job_analytics():
    """Get job analytics and metrics"""
    return {
        "total_jobs": 7,
        "active_jobs": 5,
        "by_department": {"engineering": 4, "marketing": 2, "sales": 1},
        "avg_salary": 95000
    }

# AI Matching endpoints for jobs
@router.post("/{job_id}/match-candidates")
async def match_candidates_to_job(job_id: str, background_tasks: BackgroundTasks):
    """Find matching candidates for job and trigger matching workflow"""
    background_tasks.add_task(trigger_matching_workflow, job_id, "candidates")
    
    return {
        "job_id": job_id,
        "matches": [],
        "total_matches": 0,
        "algorithm": "semantic_v3.2",
        "workflow_triggered": True
    }

@router.get("/{job_id}/match-score/{candidate_id}")
async def get_job_candidate_match_score(job_id: str, candidate_id: str):
    """Get compatibility score between job and candidate"""
    return {
        "job_id": job_id,
        "candidate_id": candidate_id,
        "score": 85.5,
        "factors": {"skills": 90, "experience": 80, "location": 85}
    }

# Workflow integration functions
async def monitor_workflow_completion(workflow_id: str):
    """Monitor workflow completion and handle results"""
    import asyncio
    
    # Wait for workflow completion
    max_wait = 300  # 5 minutes timeout
    wait_time = 0
    
    while wait_time < max_wait:
        workflow = workflow_engine.get_workflow(workflow_id)
        if workflow and workflow.status.value in ["completed", "failed", "cancelled"]:
            # Handle workflow completion
            if workflow.status.value == "completed":
                print(f"Job workflow {workflow_id} completed successfully")
            else:
                print(f"Job workflow {workflow_id} failed with status: {workflow.status.value}")
            break
        
        await asyncio.sleep(5)
        wait_time += 5

async def trigger_matching_workflow(job_id: str, match_type: str):
    """Trigger AI matching workflow"""
    # Create matching workflow
    workflow_id = workflow_engine.create_workflow(
        "ai_matching", 
        {"job_id": job_id, "match_type": match_type}
    )
    workflow_engine.start_workflow(workflow_id)
    return workflow_id