"""
Debug script to analyze actual resume parsing issues.
"""
import sys
import os
from pathlib import Path

# Add parent directory to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.ingestion.pdf_reader import read_pdf
from models.ingestion.docx_reader import read_docx
from models.preprocessing.cleaner import clean_text
from models.segmentation.section_detector import detect_sections
from models.ner_engine.extractor import extract_name, extract_entities

def analyze_resume(file_path):
    """Analyze a resume file to debug parsing issues."""
    print(f"\n{'='*60}")
    print(f"ANALYZING: {file_path}")
    print(f"{'='*60}")
    
    # Read the file
    if file_path.endswith(".pdf"):
        text = read_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = read_docx(file_path)
    else:
        print(f"Unsupported file format")
        return
    
    print(f"\n--- RAW TEXT (first 2000 chars) ---")
    print(text[:2000])
    print(f"\n... (total length: {len(text)} chars)")
    
    # Clean the text
    cleaned_text = clean_text(text)
    print(f"\n--- CLEANED TEXT (first 2000 chars) ---")
    print(cleaned_text[:2000])
    print(f"\n... (total length: {len(cleaned_text)} chars)")
    
    # Show lines
    lines = cleaned_text.split('\n')
    print(f"\n--- CLEANED TEXT LINES (first 30 lines) ---")
    for i, line in enumerate(lines[:30]):
        print(f"{i:2d}: '{line}'")
    
    # Detect sections
    print(f"\n--- SECTION DETECTION ---")
    sections = detect_sections(cleaned_text)
    for section_name, content in sections.items():
        print(f"\n{section_name.upper()} SECTION ({len(content)} entries):")
        for i, item in enumerate(content[:10]):
            print(f"  {i}: {item}")
    
    # Extract name
    print(f"\n--- NAME EXTRACTION ---")
    name, confidence = extract_name(cleaned_text)
    print(f"Extracted name: '{name}' (confidence: {confidence})")
    
    # Extract all entities
    print(f"\n--- ALL ENTITIES ---")
    entities = extract_entities(cleaned_text)
    for key, value in entities.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    # Find and test all resume files using relative paths
    resume_files = []
    base_path = Path(__file__).parent.parent
    for ext in ['.pdf', '.docx']:
        resume_files.extend(base_path.rglob(f'*{ext}'))

    print("Found resume files:")
    for f in resume_files:
        print(f"  - {f}")

    if resume_files:
        for resume_file in resume_files:
            analyze_resume(str(resume_file))
    else:
        print("\nNo resume files found in the workspace.")
        print("Please place a resume file (PDF or DOCX) in the workspace to test.")

