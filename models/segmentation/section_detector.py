"""
This module provides functions for detecting sections in resume text.
"""
import re
from collections import defaultdict

SECTIONS = {
    "education": [
        "education",
        "academic",
        "educational qualification",
        "qualification",
        "academic background",
        "edu",
        "educational details",
        "studies",
        "college",
        "university",
        "school",
        "iit",
        "engineering"
    ],
    "experience": [
        "experience",
        "work experience",
        "work history",
        "professional experience",
        "employment history",
        "employment",
        "internship",
        "internships",
        "work history",
        "professional background",
        "career history"
    ],
    "projects": [
        "projects",
        "project",
        "key projects",
        "academic projects",
        "personal projects",
        "portfolio"
    ],
    "skills": [
        "skills",
        "technical skills",
        "technical",
        "technologies",
        "skill set",
        "core competencies",
        "competencies",
        "areas of expertise",
        "expertise",
        "tech stack",
        "technologies"
    ],
    "achievement": [
        "achievement",
        "achievements",
        "awards",
        "honors",
        "recognition",
        "accomplishments"
    ],
}


def detect_sections(text):
    """
    Detects sections in the text based on predefined keywords.
    This function is case-insensitive and excludes the header from the content.
    """
    sections = defaultdict(list)
    current_section = None

    lines = text.split('\n')

    for line in lines:
        line_stripped = line.strip()
        
        # Remove special characters and zero-width spaces for matching
        line_clean = re.sub(r'[\U0001F300-\U0001F9FF\u200b\u200c\u200d\ufeff\r]', '', line_stripped)
        line_clean_lower = line_clean.lower()
        
        if not line_clean_lower:
            continue

        new_section = None
        
        # Check if this line is a section header
        for section_name, keywords in SECTIONS.items():
            for keyword in keywords:
                # Try different matching strategies
                
                # Strategy 1: Exact match on cleaned line (most reliable)
                if line_clean_lower == keyword:
                    new_section = section_name
                    break
                
                # Strategy 2: Match with colon or dash
                if re.fullmatch(rf'{re.escape(keyword)}\s*[:|-]?\s*', line_clean_lower):
                    new_section = section_name
                    break
                
                # Strategy 3: Line contains the keyword and is short (likely a header)
                if keyword in line_clean_lower and len(line_clean_lower) <= len(keyword) + 10:
                    new_section = section_name
                    break
                
                # Strategy 4: All-caps section headers (like "WORK EXPERIENCE")
                if line_clean_lower.isupper() and keyword in line_clean_lower.split():
                    # Check if the line is just the keyword(s)
                    words_in_line = line_clean_lower.split()
                    if len(words_in_line) <= len(keyword.split()) + 2:  # Allow some flexibility
                        new_section = section_name
                        break
                
                # Strategy 5: Keyword at the beginning of line
                if line_clean_lower.startswith(keyword):
                    new_section = section_name
                    break
            
            if new_section:
                break

        if new_section:
            current_section = new_section
            # Don't add the section header itself to the content
            continue

        if current_section:
            # Only add non-empty lines to the section
            if line_stripped:
                sections[current_section].append(line_stripped)

    return sections

