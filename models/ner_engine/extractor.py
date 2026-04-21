"""
This module provides functions for extracting named entities from resume text.
"""
import re
from collections import defaultdict
import spacy

# Import skills from the centralized skills module
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))
from models.skill_engine.skills import SKILLS_DB, extract_skills

def get_nlp():
    import spacy
    import os

    try:
        return spacy.load("en_core_web_sm")
    except:
        os.system("python -m spacy download en_core_web_sm")
        return spacy.load("en_core_web_sm")
EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
# Updated phone regex to handle formats like:
# +91-9812345678, +91 9812345678, 919812345678, 098123456789
PHONE_REGEX = r"(?:\+91[\s-]?|(0)?91[\s-]?)?[6-9]\d{9}"

# -----------------------------
# DOMAIN KNOWLEDGE
# -----------------------------
# SKILLS_DB is now imported from models.skill_engine.skills

TOOLS_DB = {
    "pycharm", "vscode", "visual", "studio", "github",
    "gitlab", "bitbucket", "notepad", "canva",
    "figma", "jira", "excel", "powerpoint", "word",
    "blackbox", "blackboxai"
}

ROLE_WORDS = {
    "engineer", "developer", "intern", "student",
    "freelance", "designer", "analyst", "manager",
    "consultant", "lead",
    # Role titles and descriptions
    "full stack", "fullstack", "frontend", "backend", "front-end", "back-end",
    "software", "web", "mobile", "data", "cloud",
    "devops", "ml", "ai", "machine learning", "deep learning",
    "python", "java", "javascript", "react", "angular", "node",
    "developer", "programmer", "architect", "administrator",
    "specialist", "coordinator", "supervisor", "head", "director",
    "ceo", "cto", "cfo", "cofounder", "founder",
    # Additional role indicators
    "integrated", "dual", "degree", "btech", "mtech", "cse",
    "stack", "developer"
}


# Common Indian name patterns (first names and last names)
INDIAN_NAMES = {
    # Common Indian first names
    "rahul", "raj", "amit", "amitabh", "ankit", "arjun", "ashish",
    "deepak", "dev", "gaurav", "harsh", "jai", "manish", "neeraj", "nitin",
    "prashant", "priya", "rani", "rajesh", "rakesh", "ravi", "rohit", "sachin",
    "sanjeev", "shankar", "suresh", "vikram", "vivek", "yash",
    # Common Indian surnames
    "kumar", "sharma", "singh", "gupta", "verma", "agrawal", "jain", "patel",
    "mehta", "shah", "desai", "iyer", "iyengar", "menon", "nair", "pillai",
    "reddy", "naidu", "babu", "chary", "rao", "devi", "kunwar"
}


def is_valid_candidate(cand):
    """
    Checks if a candidate name is valid.
    """
    words = cand.lower().split()

    is_valid = not any(w in TOOLS_DB for w in words) and \
               not any(w in SKILLS_DB for w in words) and \
               not any(w in ROLE_WORDS for w in words) and \
               not re.search(r"[0-9@#%$&+|()]", cand) and \
               1 <= len(words) <= 4 and \
               all(w.isalpha() for w in words)

    return is_valid


def is_likely_indian_name(cand):
    """
    Checks if the name is likely an Indian name based on common patterns.
    """
    words = cand.lower().split()
    
    # Check if any word is a common Indian name component
    if any(w in INDIAN_NAMES for w in words):
        return True
    
    # Indian names often have specific patterns
    # 2-word names like "Rahul Kumar"
    if len(words) == 2:
        # First name capitalized, last name capitalized
        if cand[0].isupper() and words[1][0].isupper():
            return True
    
    return False


# -------------------------------------------------
# NAME EXTRACTION (ENTERPRISE-GRADE)
# -------------------------------------------------
def extract_name(text):
    """
    Extracts the name from the resume text using a rule-based approach.
    """
    # Get all non-empty lines
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    
    if not lines:
        return None, 0.0
    
    # Strategy 0: Handle pipe-separated header (like "Name | Title | Info")
    first_line = lines[0]
    if '|' in first_line:
        name_part = first_line.split('|')[0].strip()
        name_words = name_part.split()
        if 1 <= len(name_words) <= 4 and is_valid_candidate(name_part):
            confidence = 0.95 if is_likely_indian_name(name_part) else 0.85
            return name_part, confidence
    
    # Strategy 1: First line is usually the name
    # But we need to check if it's valid (not a role title)
    first_line_words = first_line.split()
    
    # Check if first line is a valid name candidate
    if 1 <= len(first_line_words) <= 4 and is_valid_candidate(first_line):
        # Additional check: first line shouldn't contain pipe or special chars
        if '|' not in first_line and '•' not in first_line:
            # This is likely the name
            confidence = 0.95 if is_likely_indian_name(first_line) else 0.85
            return first_line, confidence
    
    # Strategy 2: If first line has pipe (like "Name | Title"), extract just the name
    if '|' in first_line:
        name_part = first_line.split('|')[0].strip()
        name_words = name_part.split()
        if 1 <= len(name_words) <= 4 and is_valid_candidate(name_part):
            confidence = 0.95 if is_likely_indian_name(name_part) else 0.85
            return name_part, confidence
    
    # Strategy 3: Use NER to find PERSON entities in the first few lines
    doc = nlp(text[:1500])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name_text = ent.text.strip()
            words = name_text.split()
            # Only consider valid name candidates
            if 1 <= len(words) <= 4 and is_valid_candidate(name_text):
                return name_text, 0.90
    
    # Strategy 4: Fall back to scoring approach for remaining candidates
    scores = defaultdict(float)

    # Early position (header dominance) - but only single lines, not multi-line
    for i, line in enumerate(lines[:20]):
        # Only consider lines that look like names (1-4 words)
        words = line.split()
        if 1 <= len(words) <= 4:
            scores[line] += max(0, 2.0 - i * 0.1)

    # Proximity to contact info
    for i, line in enumerate(lines):
        if re.search(EMAIL_REGEX, line) or re.search(PHONE_REGEX, line):
            for j in range(max(0, i - 3), i):  # Reduced to 3 lines before contact info
                words = lines[j].split()
                if 1 <= len(words) <= 4:  # Only single lines
                    scores[lines[j]] += 2.0
            break

    # NER signal (stronger) - Use spaCy NER for name extraction
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            name_text = ent.text.strip()
            words = name_text.split()
            # Only consider valid name candidates
            if 1 <= len(words) <= 4 and all(w.isalpha() for w in words):
                scores[name_text] += 4.0  # Higher weight for NER

    # Filter out invalid candidates (multi-word titles, tools, etc.)
    candidates = {
        cand: score
        for cand, score in scores.items()
        if is_valid_candidate(cand)
    }

    if not candidates:
        return None, 0.0

    # Indian name boost - give extra points to likely Indian names
    indian_name_boost = {}
    for cand, score in candidates.items():
        boost = 0
        if is_likely_indian_name(cand):
            boost = 2.0  # Significant boost for Indian names
        indian_name_boost[cand] = score + boost

    # Find the best candidate with the boost
    best = max(indian_name_boost, key=indian_name_boost.get)
    boosted_score = indian_name_boost[best]
    
    # Calculate confidence based on boosted score
    confidence = min(0.99, boosted_score / 8.0)

    return best, round(confidence, 2)


# -------------------------------------------------
# EMAIL
# -------------------------------------------------
def extract_email(text):
    """
    Extracts the email address from the text.
    """
    m = re.search(EMAIL_REGEX, text)
    return m.group() if m else None


# -------------------------------------------------
# PHONE
# -------------------------------------------------
def extract_phone(text):
    """
    Extracts the phone number from the text.
    """
    m = re.search(PHONE_REGEX, text)
    return m.group() if m else None


# -------------------------------------------------
# SKILLS
# -------------------------------------------------
# extract_skills is now imported from models.skill_engine.skills


# -------------------------------------------------
# MAIN
# -------------------------------------------------
def extract_entities(text):
    """
    Extracts all entities (name, email, phone, skills) from the text.
    """
    name, confidence = extract_name(text)

    return {
        "name": name,
        "name_confidence": confidence,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }

