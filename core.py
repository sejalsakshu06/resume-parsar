from ingestion.pdf_reader import read_pdf
from ingestion.docx_reader import read_docx
from preprocessing.cleaner import clean_text
from segmentation.section_detector import detect_sections
from ner_engine.extractor import extract_entities
from skill_engine.skills import extract_skills
from schema.resume_schema import build_schema
def remove_contact_info(text):
    import re
    # Simple regex patterns for email and phone numbers
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    phone_pattern = r'\+?\d[\d -]{8,}\d'
    text = re.sub(email_pattern, '', text)
    text = re.sub(phone_pattern, '', text)
    return text.strip()

def parse_resume(file_path):
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
     # Clean and filter education (skips the 'Education' header line)
    sections['education'] = [remove_contact_info(line) for line in sections['education'] 
                             if line.strip().lower() != "education" and line.strip() != '']
     # Clean contact info from education and experience
    sections['education'] = [remove_contact_info(line) for line in sections['education']]
    sections['experience'] = [remove_contact_info(line) for line in sections['experience']]

    return build_schema(personal, sections, skills)
