# SIGMA-CV - Resume Parsing Engine

SIGMA-CV is a production-grade Resume Parsing Engine with a Streamlit UI.
It converts unstructured resumes into structured JSON using hybrid NLP techniques.

## Project Structure

```
SIC-25-26-TeamXXX/
├── notebook/
│   └── resume_analysis.ipynb          # Jupyter notebook for analysis
├── data/
│   └── sample_resume.json             # Sample parsed resume data
├── submission_templates/
│   ├── Idea_Submission_Form.doc       # Idea submission form placeholder
│   └── Final_Presentation.pptx        # Final presentation placeholder
├── models/
│   ├── app.py                         # Streamlit web application
│   ├── core.py                        # Main parsing logic
│   ├── debug_resume.py                # Debug script for analysis
│   ├── ingestion/
│   │   ├── docx_reader.py             # DOCX text extraction
│   │   └── pdf_reader.py              # PDF text extraction
│   ├── ner_engine/
│   │   └── extractor.py               # Named entity extraction
│   ├── preprocessing/
│   │   └── cleaner.py                 # Text cleaning
│   ├── schema/
│   │   └── resume_schema.py           # Output schema definition
│   ├── segmentation/
│   │   └── section_detector.py        # Section detection
│   └── skill_engine/
│       └── skills.py                  # Skills extraction
├── README.md
└── requirements.txt
```

## Features

- **Resume Parsing**: Extract structured information from PDF and DOCX resumes
- **Section Detection**: Automatically identifies Education, Experience, Projects, Skills, Achievements
- **Named Entity Recognition**: Extracts Name, Email, Phone, Skills
- **Streamlit UI**: User-friendly web interface for uploading and parsing resumes

## Setup Instructions

```bash
# Install dependencies
pip install -r requirements.txt

# Download spaCy model
python -m spacy download en_core_web_sm

# Run the application
python -m streamlit run models/app.py
```

## Usage

1. Upload a resume (PDF or DOCX format)
2. Click "Parse Resume"
3. View extracted information:
   - Personal Information (Name, Email, Phone)
   - Education Details
   - Work Experience
   - Skills

## API Usage

```python
from models.core import parse_resume, parse_resume_text

# Parse a file
result = parse_resume("resume.pdf")

# Parse text directly
result = parse_resume_text(resume_text)

# Result format
{
    "personal_info": {"name": "...", "email": "...", "phone": "..."},
    "education": [...],
    "experience": [...],
    "projects": [...],
    "achievements": [...],
    "skills": [...]
}
```

## Technologies Used

- Python 3.x
- Streamlit (Web UI)
- spaCy (NLP)
- pdfminer.six (PDF extraction)
- python-docx (DOCX extraction)
