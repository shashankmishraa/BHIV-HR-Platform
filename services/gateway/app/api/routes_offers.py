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
def log_offer(offer: schemas.OfferCreate, db: Session = Depends(get_db)):
    # Stub: Implement offer logging here
    return {"message": "Offer logged (stub)"}
