#!/usr/bin/env python3
"""
Quick script to run PDF to CSV conversion
Usage: python tools/run_pdf_conversion.py
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.pdf_to_csv import PDFToCSVConverter

def main():
    print("Starting PDF to CSV Conversion")
    print("=" * 50)
    
    # Check if resume folder exists
    resume_folder = project_root / "resume"
    if not resume_folder.exists():
        print(f"ERROR: Resume folder not found: {resume_folder}")
        print("Please ensure PDF files are in the 'resume' folder")
        return
    
    # Count PDF files
    pdf_files = list(resume_folder.glob("*.pdf"))
    print(f"Found {len(pdf_files)} PDF files in resume folder")
    
    if len(pdf_files) == 0:
        print("ERROR: No PDF files found in resume folder")
        return
    
    # Run conversion
    converter = PDFToCSVConverter(
        pdf_folder=str(resume_folder),
        output_csv="data/candidates.csv"
    )
    
    result = converter.convert_pdfs_to_csv()
    
    if result is not None:
        print(f"\nSUCCESS! Converted {len(result)} resumes")
        print(f"Output saved to: data/candidates.csv")
        
        # Show summary stats
        print(f"\nSummary Statistics:")
        print(f"   - Candidates with email: {result['email'].notna().sum()}")
        print(f"   - Candidates with phone: {result['phone'].notna().sum()}")
        print(f"   - Candidates with location: {result['location'].notna().sum()}")
        print(f"   - Average experience: {result['experience_years'].mean():.1f} years")
        
        # Show education distribution
        education_counts = result['education_level'].value_counts()
        print(f"\nEducation Levels:")
        for edu, count in education_counts.items():
            if edu:  # Skip empty values
                print(f"   - {edu}: {count}")
    else:
        print("ERROR: Conversion failed")

if __name__ == "__main__":
    main()