import os
import pandas as pd
import numpy as np
import json
import re
from pathlib import Path
import PyPDF2
import docx

class SemanticResumeProcessor:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """Initialize with lightweight sentence transformer model"""
        try:
            from sentence_transformers import SentenceTransformer
            from sklearn.metrics.pairwise import cosine_similarity
            self.model = SentenceTransformer(model_name)
            self.cosine_similarity = cosine_similarity
            print(f"Loaded semantic model: {model_name}")
        except Exception as e:
            print(f"Failed to load model: {e}")
            self.model = None
    
    def extract_text_from_file(self, file_path):
        """Extract text from PDF or DOCX files"""
        try:
            if file_path.suffix.lower() == '.pdf':
                with open(file_path, 'rb') as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        text += page.extract_text() + "\n"
                    return text
            elif file_path.suffix.lower() in ['.docx', '.doc']:
                doc = docx.Document(file_path)
                return "\n".join([p.text for p in doc.paragraphs])
        except Exception as e:
            print(f"Error extracting text from {file_path}: {e}")
            return ""
        return ""
    
    def semantic_skill_extraction(self, text):
        """Extract skills using semantic similarity"""
        skill_categories = {
            "programming": ["Python programming", "Java development", "JavaScript coding", "C++ programming", "React development"],
            "data_science": ["Machine Learning", "Data Analysis", "Statistical modeling", "Deep Learning", "AI development"],
            "web_development": ["Frontend development", "Backend development", "Full stack development", "Web design", "API development"],
            "cloud": ["Cloud computing", "AWS services", "Azure platform", "DevOps practices", "Container orchestration"],
            "databases": ["Database management", "SQL queries", "NoSQL databases", "Data modeling", "Database optimization"]
        }
        
        if not self.model:
            return self._fallback_skill_extraction(text)
        
        text_embedding = self.model.encode([text])
        extracted_skills = []
        
        for category, skills in skill_categories.items():
            skill_embeddings = self.model.encode(skills)
            similarities = self.cosine_similarity(text_embedding, skill_embeddings)[0]
            
            for i, similarity in enumerate(similarities):
                if similarity > 0.3:
                    extracted_skills.append({
                        "skill": skills[i],
                        "category": category,
                        "confidence": float(similarity)
                    })
        
        extracted_skills.sort(key=lambda x: x['confidence'], reverse=True)
        return extracted_skills[:10]
    
    def _fallback_skill_extraction(self, text):
        """Fallback skill extraction without semantic model"""
        basic_skills = ['Python', 'Java', 'JavaScript', 'React', 'SQL', 'AWS', 'Machine Learning', 'Data Science']
        found_skills = []
        text_lower = text.lower()
        
        for skill in basic_skills:
            if skill.lower() in text_lower:
                found_skills.append({
                    "skill": skill,
                    "category": "general",
                    "confidence": 0.8
                })
        return found_skills
    
    def semantic_role_extraction(self, text):
        """Extract roles using semantic understanding"""
        role_patterns = [
            "Software Engineer", "Data Scientist", "Product Manager", "DevOps Engineer",
            "Full Stack Developer", "Machine Learning Engineer", "Frontend Developer",
            "Backend Developer", "Data Analyst", "Cloud Architect"
        ]
        
        if not self.model:
            return self._fallback_role_extraction(text)
        
        text_embedding = self.model.encode([text])
        role_embeddings = self.model.encode(role_patterns)
        similarities = self.cosine_similarity(text_embedding, role_embeddings)[0]
        
        roles = []
        for i, similarity in enumerate(similarities):
            if similarity > 0.25:
                roles.append({
                    "role": role_patterns[i],
                    "confidence": float(similarity)
                })
        
        roles.sort(key=lambda x: x['confidence'], reverse=True)
        return roles[:3]
    
    def _fallback_role_extraction(self, text):
        """Fallback role extraction"""
        text_lower = text.lower()
        if 'engineer' in text_lower:
            return [{"role": "Software Engineer", "confidence": 0.7}]
        elif 'developer' in text_lower:
            return [{"role": "Developer", "confidence": 0.7}]
        return [{"role": "Professional", "confidence": 0.5}]
    
    def calculate_job_similarity(self, resume_text, job_description):
        """Calculate similarity between resume and job description"""
        if not self.model:
            return 0.5
        
        try:
            resume_embedding = self.model.encode([resume_text])
            job_embedding = self.model.encode([job_description])
            similarity = self.cosine_similarity(resume_embedding, job_embedding)[0][0]
            return float(similarity)
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.5
    
    def process_resume(self, file_path, job_description=""):
        """Process single resume with semantic enrichment"""
        text = self.extract_text_from_file(file_path)
        if not text:
            return None
        
        name = self._extract_name(text, file_path.name)
        email = self._extract_email(text)
        phone = self._extract_phone(text)
        
        skills = self.semantic_skill_extraction(text)
        roles = self.semantic_role_extraction(text)
        
        job_similarity = 0.0
        if job_description:
            job_similarity = self.calculate_job_similarity(text, job_description)
        
        return {
            "name": name,
            "email": email,
            "phone": phone,
            "semantic_skills": skills,
            "semantic_roles": roles,
            "job_similarity": job_similarity,
            "resume_file": file_path.name,
            "text_length": len(text)
        }
    
    def _extract_name(self, text, filename):
        """Basic name extraction"""
        name = Path(filename).stem
        name = re.sub(r'[_-]', ' ', name)
        name = re.sub(r'(?i)(resume|cv)', '', name).strip()
        return name.title() if name else "Unknown"
    
    def _extract_email(self, text):
        """Basic email extraction"""
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(pattern, text)
        return emails[0] if emails else ""
    
    def _extract_phone(self, text):
        """Basic phone extraction"""
        pattern = r'\+?\d{1,3}[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phones = re.findall(pattern, text)
        return phones[0] if phones else ""

def main():
    """Test semantic processor"""
    processor = SemanticResumeProcessor()
    
    job_desc = "We are looking for a Python developer with machine learning experience and AWS knowledge."
    
    resume_folder = Path("resume")
    if resume_folder.exists():
        pdf_files = list(resume_folder.glob("*.pdf"))[:3]
        
        results = []
        for pdf_file in pdf_files:
            print(f"Processing: {pdf_file.name}")
            result = processor.process_resume(pdf_file, job_desc)
            if result:
                results.append(result)
                skills_list = [s['skill'] for s in result['semantic_skills'][:3]]
                roles_list = [r['role'] for r in result['semantic_roles'][:2]]
                print(f"  Skills: {skills_list}")
                print(f"  Roles: {roles_list}")
                print(f"  Job Similarity: {result['job_similarity']:.3f}")
        
        if results:
            df = pd.DataFrame(results)
            df.to_csv("data/semantic_candidates.csv", index=False)
            print(f"\nProcessed {len(results)} resumes with semantic enrichment")

if __name__ == "__main__":
    main()