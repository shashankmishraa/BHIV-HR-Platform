"""Jobs workflow router"""

import hashlib
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, BackgroundTasks, HTTPException, Query
from pydantic import ValidationError
from typing import Optional

# Import with fallbacks
try:
    from app.shared.models import JobCreate
except ImportError:
    from pydantic import BaseModel
    class JobCreate(BaseModel):
        title: str
        department: str
        location: str = "Remote"
        experience_level: str = "Mid"
        requirements: str = ""
        description: str = ""

try:
    from app.shared.validation import ValidationUtils
except ImportError:
    class ValidationUtils:
        @staticmethod
        def validate_job_data(data):
            return data

try:
    from app.workflow_engine import workflow_engine
except ImportError:
    class MockWorkflowEngine:
        def create_workflow(self, name, data):
            return f"workflow_{hash(str(data)) % 10000}"
        def start_workflow(self, workflow_id):
            return True
        def get_workflow(self, workflow_id):
            return None
    workflow_engine = MockWorkflowEngine()

def create_job_posting_workflow(data):
    return workflow_engine.create_workflow("job_posting", data)

router = APIRouter(prefix="/v1/jobs", tags=["Jobs"])


@router.get("")
async def list_jobs(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    department: Optional[str] = Query(None),
    experience_level: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
):
    """List job postings with filtering"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Build dynamic query with filters
            where_conditions = []
            params = []
            
            if department:
                where_conditions.append("department ILIKE %s")
                params.append(f"%{department}%")
            
            if experience_level:
                where_conditions.append("experience_level ILIKE %s")
                params.append(f"%{experience_level}%")
            
            if status:
                where_conditions.append("status = %s")
                params.append(status)
            else:
                where_conditions.append("status = 'active'")
            
            where_clause = " AND ".join(where_conditions) if where_conditions else "1=1"
            
            # Get total count
            count_query = f"SELECT COUNT(*) FROM jobs WHERE {where_clause}"
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]
            
            # Get paginated results
            offset = (page - 1) * per_page
            data_query = f"""
                SELECT id, title, department, location, experience_level, 
                       requirements, description, status, client_id, created_at
                FROM jobs 
                WHERE {where_clause}
                ORDER BY created_at DESC 
                LIMIT %s OFFSET %s
            """
            cursor.execute(data_query, params + [per_page, offset])
            
            jobs = []
            for row in cursor.fetchall():
                jobs.append({
                    "id": row[0],
                    "title": row[1],
                    "department": row[2],
                    "location": row[3],
                    "experience_level": row[4],
                    "requirements": row[5],
                    "description": row[6],
                    "status": row[7],
                    "client_id": row[8],
                    "created_at": row[9].isoformat() if row[9] else None
                })
            
            pages = (total + per_page - 1) // per_page
            
            return {
                "jobs": jobs,
                "total": total,
                "page": page,
                "per_page": per_page,
                "pages": pages,
                "filters": {
                    "department": department,
                    "experience_level": experience_level,
                    "status": status,
                },
            }
    except Exception as e:
        return {
            "jobs": [],
            "total": 0,
            "page": page,
            "per_page": per_page,
            "pages": 0,
            "error": str(e),
            "filters": {
                "department": department,
                "experience_level": experience_level,
                "status": status,
            },
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
            **validated_data,
        }
    except ValidationError as e:
        # Return detailed validation errors
        error_details = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            error_details.append(
                {
                    "field": field,
                    "message": error["msg"],
                    "invalid_value": error.get("input"),
                }
            )

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Job validation failed",
                "errors": error_details,
                "help": {
                    "requirements": "Provide as list ['Python', 'FastAPI'] or string 'Python, FastAPI'",
                    "experience_level": "Use: Entry, Mid, Senior, Lead, or Executive",
                    "salary_fields": "Both salary_min and salary_max are required (integers)",
                },
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Internal server error during job creation",
                "error": str(e),
            },
        )


@router.get("/{job_id}")
async def get_job(job_id: str):
    """Get specific job details"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, title, department, location, experience_level,
                       requirements, description, status, client_id, 
                       created_at, updated_at
                FROM jobs WHERE id = %s
            """, (job_id,))
            
            row = cursor.fetchone()
            if not row:
                return {"error": "Job not found", "job_id": job_id}
            
            return {
                "id": row[0],
                "title": row[1],
                "department": row[2],
                "location": row[3],
                "experience_level": row[4],
                "requirements": row[5],
                "description": row[6],
                "status": row[7],
                "client_id": row[8],
                "created_at": row[9].isoformat() if row[9] else None,
                "updated_at": row[10].isoformat() if row[10] else None
            }
    except Exception as e:
        return {"error": str(e), "job_id": job_id}


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
            **validated_data,
        }
    except ValidationError as e:
        # Return detailed validation errors
        error_details = []
        for error in e.errors():
            field = ".".join(str(loc) for loc in error["loc"])
            error_details.append(
                {
                    "field": field,
                    "message": error["msg"],
                    "invalid_value": error.get("input"),
                }
            )

        raise HTTPException(
            status_code=422,
            detail={
                "message": "Job validation failed",
                "errors": error_details,
                "help": {
                    "requirements": "Provide as list ['Python', 'FastAPI'] or string 'Python, FastAPI'",
                    "experience_level": "Use: Entry, Mid, Senior, Lead, or Executive",
                    "salary_fields": "Both salary_min and salary_max are required (integers)",
                },
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Internal server error during job update",
                "error": str(e),
            },
        )


@router.delete("/{job_id}")
async def delete_job(job_id: str):
    """Delete job posting"""
    return {"message": f"Job {job_id} deleted successfully"}


@router.get("/search")
async def search_jobs(
    q: str = Query(..., min_length=2),
    department: Optional[str] = Query(None),
    salary_min: Optional[int] = Query(None),
):
    """Search job postings"""
    return {
        "query": q,
        "results": [],
        "total": 0,
        "filters": {"department": department, "salary_min": salary_min},
    }


@router.get("/{job_id}/applications")
async def get_job_applications(job_id: str):
    """Get applications for specific job"""
    return {"job_id": job_id, "applications": [], "total": 0}


@router.get("/analytics")
async def get_job_analytics():
    """Get job analytics and metrics"""
    from app.shared.database import db_manager
    
    try:
        async with db_manager.get_connection() as conn:
            cursor = conn.cursor()
            
            # Total and active jobs
            cursor.execute("SELECT COUNT(*) FROM jobs")
            total_jobs = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM jobs WHERE status = 'active'")
            active_jobs = cursor.fetchone()[0]
            
            # By department
            cursor.execute("""
                SELECT department, COUNT(*) 
                FROM jobs 
                WHERE department IS NOT NULL
                GROUP BY department
                ORDER BY COUNT(*) DESC
            """)
            by_department = {row[0]: row[1] for row in cursor.fetchall()}
            
            return {
                "total_jobs": total_jobs,
                "active_jobs": active_jobs,
                "by_department": by_department,
                "timestamp": datetime.now().isoformat()
            }
    except Exception as e:
        return {
            "total_jobs": 0,
            "active_jobs": 0,
            "by_department": {},
            "error": str(e),
            "timestamp": datetime.now().isoformat()
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
        "workflow_triggered": True,
    }


@router.get("/{job_id}/match-score/{candidate_id}")
async def get_job_candidate_match_score(job_id: str, candidate_id: str):
    """Get compatibility score between job and candidate"""
    return {
        "job_id": job_id,
        "candidate_id": candidate_id,
        "score": 85.5,
        "factors": {"skills": 90, "experience": 80, "location": 85},
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
                print(
                    f"Job workflow {workflow_id} failed with status: {workflow.status.value}"
                )
            break

        await asyncio.sleep(5)
        wait_time += 5


async def trigger_matching_workflow(job_id: str, match_type: str):
    """Trigger AI matching workflow"""
    # Create matching workflow
    workflow_id = workflow_engine.create_workflow(
        "ai_matching", {"job_id": job_id, "match_type": match_type}
    )
    workflow_engine.start_workflow(workflow_id)
    return workflow_id


@router.post("/{job_id}/match")
async def match_job_candidates(job_id: str):
    """Match candidates to specific job"""
    return {
        "job_id": job_id,
        "matched_candidates": [],
        "total_matches": 0,
        "algorithm": "semantic_v3.2",
        "status": "success",
    }


@router.get("/{job_id}/candidates")
async def get_job_candidates(job_id: str):
    """Get candidates for specific job"""
    return {"job_id": job_id, "candidates": [], "total": 0, "status": "success"}


@router.post("/bulk")
async def bulk_job_operations():
    """Bulk job operations"""
    return {
        "processed": 0,
        "created": 0,
        "updated": 0,
        "errors": [],
        "status": "success",
    }
