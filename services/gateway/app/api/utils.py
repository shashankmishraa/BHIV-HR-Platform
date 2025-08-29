import csv
from io import StringIO
from ..db import models

def generate_csv_report(db, job_id: int) -> str:
    # Input validation to prevent SQL injection
    if not isinstance(job_id, int) or job_id <= 0:
        raise ValueError("Invalid job_id parameter")
    
    # Use parameterized query (SQLAlchemy ORM handles this safely)
    candidates = db.query(models.Candidate).filter(models.Candidate.job_id == job_id).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Candidate ID", "Name", "Status", "CV URL"])
    
    for c in candidates:
        # Sanitize output to prevent CSV injection
        safe_name = str(c.name).replace('=', '').replace('+', '').replace('-', '').replace('@', '') if c.name else ''
        safe_status = str(c.status).replace('=', '').replace('+', '').replace('-', '').replace('@', '') if c.status else ''
        safe_cv_url = str(c.cv_url).replace('=', '').replace('+', '').replace('-', '').replace('@', '') if c.cv_url else ''
        writer.writerow([c.id, safe_name, safe_status, safe_cv_url])
    
    return output.getvalue()
