import csv
from io import StringIO
from ..db import models

def generate_csv_report(db, job_id: int) -> str:
    candidates = db.query(models.Candidate).filter(models.Candidate.job_id == job_id).all()
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["Candidate ID", "Name", "Status", "CV URL"])
    for c in candidates:
        writer.writerow([c.id, c.name, c.status, c.cv_url])
    return output.getvalue()
