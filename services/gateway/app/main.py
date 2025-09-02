from fastapi import FastAPI, HTTPException, Header, Depends
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import os
from sqlalchemy import create_engine, text
from typing import Optional

app = FastAPI(title="BHIV HR Platform API Gateway", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

def get_db_engine():
    database_url = os.getenv("DATABASE_URL", "postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr")
    return create_engine(database_url, pool_pre_ping=True)

def validate_api_key(api_key: str) -> bool:
    expected_key = os.getenv("API_KEY_SECRET", "myverysecureapikey123")
    return api_key == expected_key

def get_api_key(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid API key")
    api_key = authorization[7:]
    if not validate_api_key(api_key):
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

@app.get("/")
def read_root():
    return {
        "message": "🎯 BHIV HR Platform API Gateway",
        "version": "3.0.0",
        "status": "healthy"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "BHIV HR Gateway",
        "version": "3.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

@app.get("/v1/jobs")
async def list_jobs(api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("SELECT id, title, description FROM jobs WHERE status = 'active' ORDER BY id")
            result = connection.execute(query)
            jobs = [{"id": row[0], "title": row[1], "description": row[2]} for row in result]
        return {"jobs": jobs, "count": len(jobs)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/v1/candidates/job/{job_id}")
async def get_candidates_by_job(job_id: int, api_key: str = Depends(get_api_key)):
    try:
        engine = get_db_engine()
        with engine.connect() as connection:
            query = text("SELECT id, name, email FROM candidates LIMIT 50")
            result = connection.execute(query)
            candidates = [{"id": row[0], "name": row[1], "email": row[2]} for row in result]
        return {"job_id": job_id, "candidates": candidates, "count": len(candidates)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))