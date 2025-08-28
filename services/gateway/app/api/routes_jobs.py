from fastapi import APIRouter

router = APIRouter()

@router.post("/")
def create_job():
    return {"message": "Job creation endpoint - ready for implementation"}

@router.get("/")
def list_jobs():
    return {"message": "Job listing endpoint - ready for implementation"}
