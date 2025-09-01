# BHIV HR Platform - Implementation Guide

## 🎯 How It Works - Complete Implementation Guide

### 🏗️ Architecture Overview

```
Resume Files → Processing → Database → API → Portals
     ↓            ↓          ↓        ↓      ↓
   PDF/DOCX   Extract Data  PostgreSQL FastAPI Streamlit
```

## 📋 Step-by-Step Implementation

### 1. **Resume Processing Engine**

```python
# tools/comprehensive_resume_extractor.py
import PyPDF2
from docx import Document
import pandas as pd
import re

def extract_from_pdf(file_path):
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
    return text

def extract_candidate_data(text):
    # Email extraction
    email = re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
    
    # Phone extraction
    phone = re.search(r'[\+]?[1-9]?[0-9]{7,15}', text)
    
    # Skills extraction
    skills = re.findall(r'\b(?:Python|Java|JavaScript|React|SQL|AWS)\b', text, re.IGNORECASE)
    
    return {
        'email': email.group() if email else '',
        'phone': phone.group() if phone else '',
        'skills': ', '.join(set(skills))
    }
```

### 2. **Database Schema**

```sql
-- services/db/init.sql
CREATE TABLE candidates (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    technical_skills TEXT,
    experience_years INTEGER,
    location VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE jobs (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    description TEXT,
    requirements TEXT,
    client_id INTEGER,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW()
);
```

### 3. **API Backend (FastAPI)**

```python
# services/gateway/app/main.py
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import os

app = FastAPI()

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:pass@db:5432/bhiv_hr")
engine = create_engine(DATABASE_URL)

@app.get("/v1/candidates/search")
async def search_candidates(q: str = "", skills: str = ""):
    with engine.connect() as connection:
        query = text("""
            SELECT id, name, email, phone, technical_skills, experience_years
            FROM candidates 
            WHERE name ILIKE :search OR technical_skills ILIKE :skills
            ORDER BY experience_years DESC
        """)
        
        result = connection.execute(query, {
            "search": f"%{q}%",
            "skills": f"%{skills}%"
        })
        
        candidates = []
        for row in result:
            candidates.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "phone": row[3],
                "technical_skills": row[4],
                "experience_years": row[5]
            })
        
        return {"candidates": candidates, "count": len(candidates)}

@app.post("/v1/jobs")
async def create_job(job_data: dict):
    with engine.connect() as connection:
        query = text("""
            INSERT INTO jobs (title, description, requirements, client_id)
            VALUES (:title, :description, :requirements, :client_id)
            RETURNING id
        """)
        
        result = connection.execute(query, job_data)
        job_id = result.fetchone()[0]
        connection.commit()
        
        return {"message": "Job created", "job_id": job_id}
```

### 4. **AI Matching Engine**

```python
# services/agent/app.py
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

class AIMatchingEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def calculate_match_score(self, candidate_skills, job_requirements):
        # Semantic similarity
        candidate_embedding = self.model.encode([candidate_skills])
        job_embedding = self.model.encode([job_requirements])
        
        semantic_score = cosine_similarity(candidate_embedding, job_embedding)[0][0]
        
        # Skills matching
        candidate_skills_list = candidate_skills.lower().split(',')
        job_skills = ['python', 'javascript', 'react', 'sql']
        
        skills_match = len([skill for skill in job_skills 
                           if any(skill in cs.strip() for cs in candidate_skills_list)])
        skills_score = skills_match / len(job_skills)
        
        # Final weighted score
        final_score = (semantic_score * 0.6) + (skills_score * 0.4)
        
        return {
            'total_score': int(final_score * 100),
            'semantic_similarity': int(semantic_score * 100),
            'skills_match': int(skills_score * 100),
            'explanation': f"Strong match based on {skills_match} matching skills"
        }

@app.post("/match")
async def match_candidates(request: dict):
    job_id = request['job_id']
    
    # Get job requirements and candidates from database
    # Apply AI matching logic
    # Return ranked candidates
    
    return {"top_candidates": ranked_candidates}
```

### 5. **Frontend Portals (Streamlit)**

```python
# services/portal/app.py
import streamlit as st
import requests

st.title("🎯 BHIV HR Portal")

# API configuration
API_BASE = "http://gateway:8000"
headers = {"Authorization": "Bearer myverysecureapikey123"}

# Sidebar navigation
menu = st.sidebar.selectbox("Menu", [
    "Dashboard", 
    "Search Candidates", 
    "Job Management", 
    "AI Matching"
])

if menu == "Search Candidates":
    st.header("Search Candidates")
    
    search_query = st.text_input("Search by name or skills")
    skills_filter = st.text_input("Filter by skills")
    
    if st.button("Search"):
        response = requests.get(f"{API_BASE}/v1/candidates/search", 
                              params={"q": search_query, "skills": skills_filter},
                              headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            candidates = data['candidates']
            
            for candidate in candidates:
                with st.expander(f"👤 {candidate['name']}"):
                    st.write(f"Email: {candidate['email']}")
                    st.write(f"Skills: {candidate['technical_skills']}")
                    st.write(f"Experience: {candidate['experience_years']} years")

elif menu == "AI Matching":
    st.header("AI-Powered Matching")
    
    job_id = st.number_input("Job ID", min_value=1)
    
    if st.button("Get AI Matches"):
        response = requests.get(f"{API_BASE}/v1/match/{job_id}/top", 
                              headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            candidates = data['top_candidates']
            
            for i, candidate in enumerate(candidates, 1):
                st.write(f"#{i} - {candidate['name']} (Score: {candidate['score']}/100)")
                st.write(f"Explanation: {candidate['explanation']}")
```

### 6. **Docker Containerization**

```yaml
# docker-compose.production.yml
version: '3.8'
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: bhiv_hr
      POSTGRES_USER: bhiv_user
      POSTGRES_PASSWORD: bhiv_pass
    volumes:
      - ./services/db/init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"

  gateway:
    build: ./services/gateway
    ports:
      - "8000:8000"
    depends_on:
      - db
    environment:
      DATABASE_URL: postgresql://bhiv_user:bhiv_pass@db:5432/bhiv_hr

  agent:
    build: ./services/agent
    ports:
      - "9000:9000"

  portal:
    build: ./services/portal
    ports:
      - "8501:8501"
    environment:
      GATEWAY_URL: http://gateway:8000

  client_portal:
    build: ./services/client_portal
    ports:
      - "8502:8502"
    environment:
      GATEWAY_URL: http://gateway:8000
```

### 7. **Data Synchronization**

```python
# tools/database_sync_manager.py
import pandas as pd
from sqlalchemy import create_engine

def sync_csv_to_database():
    # Read processed CSV
    df = pd.read_csv('data/candidates.csv')
    
    # Connect to database
    engine = create_engine('postgresql://bhiv_user:bhiv_pass@localhost:5432/bhiv_hr')
    
    # Upload to database
    df.to_sql('candidates', engine, if_exists='append', index=False)
    
    print(f"Synced {len(df)} candidates to database")

def auto_sync_watcher():
    # Monitor resume folder for changes
    from watchdog.observers import Observer
    from watchdog.events import FileSystemEventHandler
    
    class ResumeHandler(FileSystemEventHandler):
        def on_created(self, event):
            if event.src_path.endswith(('.pdf', '.docx')):
                print(f"New resume: {event.src_path}")
                # Trigger processing
                process_new_resume(event.src_path)
    
    observer = Observer()
    observer.schedule(ResumeHandler(), 'resume/', recursive=False)
    observer.start()
```

## 🚀 Implementation Steps

### Phase 1: Basic Setup
1. **Create project structure** with services folders
2. **Set up PostgreSQL** database with tables
3. **Build FastAPI backend** with basic endpoints
4. **Create Streamlit frontend** with search functionality

### Phase 2: Resume Processing
1. **Implement PDF/DOCX extraction** using PyPDF2/python-docx
2. **Add regex patterns** for email, phone, skills extraction
3. **Create CSV export** functionality
4. **Build database sync** mechanism

### Phase 3: AI Enhancement
1. **Install sentence-transformers** for semantic matching
2. **Implement cosine similarity** scoring
3. **Add weighted scoring** (semantic + skills + experience)
4. **Create explanation generation**

### Phase 4: Production Ready
1. **Dockerize all services** with docker-compose
2. **Add health checks** and monitoring
3. **Implement authentication** with API keys
4. **Create deployment scripts**

## 🔧 Key Technologies

### Backend Stack
- **FastAPI**: Modern Python web framework
- **PostgreSQL**: Robust relational database
- **SQLAlchemy**: Python SQL toolkit
- **Pydantic**: Data validation

### Frontend Stack
- **Streamlit**: Rapid web app development
- **Pandas**: Data manipulation
- **Requests**: HTTP client library

### AI/ML Stack
- **Sentence Transformers**: Semantic embeddings
- **Scikit-learn**: Machine learning utilities
- **PyPDF2**: PDF text extraction
- **python-docx**: Word document processing

### DevOps Stack
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **PostgreSQL**: Database persistence

## 📊 Data Flow

1. **Resume Upload** → PDF/DOCX files in resume/ folder
2. **Text Extraction** → PyPDF2/python-docx extract raw text
3. **Data Processing** → Regex patterns extract structured data
4. **CSV Storage** → Processed data saved to data/candidates.csv
5. **Database Sync** → CSV data uploaded to PostgreSQL
6. **API Access** → FastAPI serves data via REST endpoints
7. **Frontend Display** → Streamlit portals consume API data
8. **AI Matching** → Semantic models rank candidates for jobs

## 🎯 Core Features Implementation

### Resume Processing
```python
def process_resume(file_path):
    text = extract_text(file_path)
    data = extract_structured_data(text)
    save_to_csv(data)
    sync_to_database(data)
```

### AI Matching
```python
def match_candidates(job_requirements):
    candidates = get_candidates_from_db()
    scores = []
    for candidate in candidates:
        score = calculate_semantic_similarity(candidate.skills, job_requirements)
        scores.append((candidate, score))
    return sorted(scores, key=lambda x: x[1], reverse=True)
```

### API Endpoints
```python
@app.get("/candidates/search")  # Search and filter
@app.post("/jobs")              # Create jobs
@app.get("/match/{job_id}/top") # AI matching
@app.post("/candidates/bulk")   # Bulk upload
```

This implementation guide provides the complete blueprint for building your own BHIV HR Platform with semantic AI matching, dual portals, and production-ready deployment.