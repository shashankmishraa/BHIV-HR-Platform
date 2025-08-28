from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from .utils import generate_csv_report
from ..db.base import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/job/{job_id}/export.csv")
def export_job_report(job_id: int, db: Session = Depends(get_db)):
    csv_data = generate_csv_report(db, job_id)
    return Response(content=csv_data, media_type="text/csv")

