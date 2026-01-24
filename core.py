from ingestion.pdf_reader import read_pdf
from ingestion.docx_reader import read_docx
from preprocessing.cleaner import clean_text
from segmentation.section_detector import detect_sections
from ner_engine.extractor import extract_entities
from skill_engine.skills import extract_skills
from schema.resume_schema import build_schema

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

    return build_schema(personal, sections, skills)
