"""
Core resume parsing logic.
"""
import re
import sys
from pathlib import Path

# For running from root directory
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.ingestion.pdf_reader import read_pdf
from models.ingestion.docx_reader import read_docx
from models.preprocessing.cleaner import clean_text, remove_contact_info
from models.segmentation.section_detector import detect_sections
from models.ner_engine.extractor import extract_entities
from models.skill_engine.skills import extract_skills
from models.schema.resume_schema import build_schema


def parse_resume(file_path):
    """
    Parses a resume file (PDF or DOCX) and extracts structured information.
    """
    if file_path.endswith(".pdf"):
        text = read_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = read_docx(file_path)
    else:
        raise ValueError("Unsupported file format")

    text = clean_text(text)
    sections = detect_sections(text)
    personal = extract_entities(text)
    skills = extract_skills(text)

    # Clean and group experience entries
    raw_exp = []
    for line in sections.get('experience', []):
        clean_line = line.strip()
        if "key projects" in clean_line.lower():
            continue
        if "projects" in clean_line.lower() and clean_line.lower() in ["projects", "project"]:
            continue
        if clean_line:
            raw_exp.append(remove_contact_info(line))
    sections['experience'] = group_entries(raw_exp)

    # Clean and group projects entries
    raw_projects = []
    for line in sections.get('projects', []):
        clean_line = line.strip()
        if clean_line:
            raw_projects.append(remove_contact_info(line))
    sections['projects'] = group_entries(raw_projects)

    # Clean education entries
    raw_edu = []
    for line in sections.get('education', []):
        clean_line = line.strip()
        if clean_line:
            raw_edu.append(remove_contact_info(line))
    sections['education'] = group_entries(raw_edu)

    return build_schema(personal, sections, skills)


def group_entries(lines):
    """
    Groups related lines together into cohesive entries.
    For experience: company + role + date + bullet points
    For education: institution + degree + details
    """
    if not lines:
        return []
    
    grouped = []
    current_entry = []
    
    for line in lines:
        line = line.strip()
        if not line:
            if current_entry:
                grouped.append('\n'.join(current_entry))
                current_entry = []
            continue
        
        # Date patterns
        date_patterns = [
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\s*-\s*(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}',
            r'\b\d{4}\s*-\s*\d{4}',
            r'\b\d{4}\s*-\s*Present',
            r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\s*-\s*Present',
        ]
        
        is_new_entry = False
        
        # Check if line is a project title (has date and no verb at start)
        if re.search(r'\|\s*\d{4}', line) and not any(verb in line.lower() for verb in ['developed', 'created', 'designed', 'implemented', 'built', 'managed', 'led', 'achieved', 'improved', 'increased']):
            is_new_entry = True
        
        # Check if line has date pattern (likely a role/date line)
        for pattern in date_patterns:
            if re.search(pattern, line):
                # If current entry is not empty and this looks like continuation
                if current_entry:
                    # Check if previous line was a header (company/institution)
                    prev_line = current_entry[0]
                    if not any(verb in prev_line.lower() for verb in ['developed', 'created', 'designed', 'implemented', 'built', 'managed', 'led', 'achieved', 'improved', 'increased']):
                        # This is continuation of previous entry
                        is_new_entry = False
                    else:
                        is_new_entry = True
                break
        
        # Check if line starts with a verb (likely a bullet point, not a new entry)
        verbs = ['developed', 'created', 'designed', 'implemented', 'built', 'managed', 'led', 'achieved', 'improved', 'increased', 'collaborated', 'optimized', 'integrated', 'participated', 'deployed', 'enabled']
        if any(line.lower().startswith(verb) for verb in verbs):
            is_new_entry = False
        
        if is_new_entry and current_entry:
            grouped.append('\n'.join(current_entry))
            current_entry = []
        
        current_entry.append(line)
    
    # Don't forget the last entry
    if current_entry:
        grouped.append('\n'.join(current_entry))
    
    return grouped


def parse_resume_text(text):
    """
    Parses resume text directly (useful for testing).
    """
    text = clean_text(text)
    sections = detect_sections(text)
    personal = extract_entities(text)
    skills = extract_skills(text)

    # Clean and group experience entries
    raw_exp = []
    for line in sections.get('experience', []):
        clean_line = line.strip()
        if "key projects" in clean_line.lower():
            continue
        if "projects" in clean_line.lower() and clean_line.lower() in ["projects", "project"]:
            continue
        if clean_line:
            raw_exp.append(remove_contact_info(line))
    sections['experience'] = group_entries(raw_exp)

    # Clean and group projects entries
    raw_projects = []
    for line in sections.get('projects', []):
        clean_line = line.strip()
        if clean_line:
            raw_projects.append(remove_contact_info(line))
    sections['projects'] = group_entries(raw_projects)
    
    # Clean education entries
    raw_edu = []
    for line in sections.get('education', []):
        clean_line = line.strip()
        if clean_line:
            raw_edu.append(remove_contact_info(line))
    sections['education'] = group_entries(raw_edu)

    return build_schema(personal, sections, skills)


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        result = parse_resume(sys.argv[1])
        print(f"Parsed: {result['personal_info'].get('name', 'N/A')}")
    else:
        print("Usage: python core.py <resume_file_path>")

