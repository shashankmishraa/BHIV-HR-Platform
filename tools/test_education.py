import PyPDF2
from pathlib import Path

def test_education_extraction():
    """Test education extraction on a few PDFs"""
    
    resume_folder = Path("resume")
    test_files = ["AdarshYadavResume.pdf", "Anurag_CV.pdf", "ASMA_RESUME.pdf"]
    
    for filename in test_files:
        file_path = resume_folder / filename
        if not file_path.exists():
            continue
            
        print(f"\n=== {filename} ===")
        
        # Extract text
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
        except:
            print("Could not read PDF")
            continue
        
        # Show relevant text snippets
        text_lower = text.lower()
        
        # Look for education keywords
        education_keywords = ['bachelor', 'master', 'phd', 'diploma', 'b.tech', 'm.tech', 'mba', 'be', 'me']
        
        print("Education keywords found:")
        for keyword in education_keywords:
            if keyword in text_lower:
                # Find context around the keyword
                start = max(0, text_lower.find(keyword) - 30)
                end = min(len(text), text_lower.find(keyword) + 50)
                context = text[start:end].replace('\n', ' ')
                print(f"  - {keyword}: ...{context}...")
        
        # Check what our logic would return
        if any(word in text_lower for word in ['phd', 'ph.d', 'doctorate', 'doctoral']):
            result = 'PhD'
        elif any(word in text_lower for word in ['master', 'masters', 'mba', 'm.tech', 'mtech', 'm.s', 'ms', 'm.a', 'ma', 'post graduate', 'pg']):
            result = 'Masters'
        elif any(word in text_lower for word in ['bachelor', 'bachelors', 'b.tech', 'btech', 'be', 'b.e', 'b.s', 'bs', 'b.a', 'ba', 'b.com', 'bcom', 'graduate', 'ug']):
            result = 'Bachelors'
        elif any(word in text_lower for word in ['diploma', 'associate', 'polytechnic']):
            result = 'Diploma'
        elif any(word in text_lower for word in ['12th', '12', 'higher secondary', 'intermediate', 'hsc', '+2']):
            result = '12th'
        elif any(word in text_lower for word in ['10th', '10', 'matriculation', 'ssc']):
            result = '10th'
        elif any(word in text_lower for word in ['engineer', 'developer', 'analyst', 'manager', 'consultant']):
            result = 'Bachelors'
        else:
            result = 'Not Specified'
        
        print(f"Detected education: {result}")

if __name__ == "__main__":
    test_education_extraction()