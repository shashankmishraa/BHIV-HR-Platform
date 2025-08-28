from sqlalchemy.orm import Session
from . import models, schemas

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job


def create_candidates_bulk(db: Session, candidates: list[schemas.CandidateCreate]):
    db_objs = [models.Candidate(**candidate.dict()) for candidate in candidates]
    db.add_all(db_objs)
    db.commit()
    return db_objs

def get_candidate_by_id(db: Session, candidate_id: int):
    return db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()

def create_feedback(db: Session, feedback: schemas.FeedbackCreate):
    db_feedback = models.Feedback(**feedback.dict())
    db.add(db_feedback)
    db.commit()
    db.refresh(db_feedback)
    return db_feedback
