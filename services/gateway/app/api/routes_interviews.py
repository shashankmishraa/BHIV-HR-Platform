from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import schemas
from ..db.base import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/")
def schedule_interview(interview: schemas.InterviewCreate, db: Session = Depends(get_db)):
    # Stub: Implement interview creation logic here
    return {"message": "Interview scheduled (stub)"}
