import re
import spacy
from collections import defaultdict

nlp = spacy.load("en_core_web_sm")

EMAIL_REGEX = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
PHONE_REGEX = r"(\+91[\s-]?)?[6-9]\d{9}"

# -----------------------------
# DOMAIN KNOWLEDGE
# -----------------------------
SKILLS_DB = {
    "python", "java", "c", "c++", "sql", "html", "css",
    "javascript", "machine learning", "ml", "nlp",
    "deep learning", "django", "flask", "react",
    "node", "git", "docker", "aws"
}

TOOLS_DB = {
    "pycharm", "vscode", "visual", "studio", "github",
    "gitlab", "bitbucket", "notepad", "canva",
    "figma", "jira", "excel", "powerpoint", "word"
}

ROLE_WORDS = {
    "engineer", "developer", "intern", "student",
    "freelance", "designer", "analyst", "manager",
    "consultant", "lead"
}

# -------------------------------------------------
# NAME EXTRACTION (ENTERPRISE-GRADE)
# -------------------------------------------------
def extract_name(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    scores = defaultdict(float)

    # 1️⃣ Early position (header dominance)
    for i, line in enumerate(lines[:20]):
        scores[line] += max(0, 2.0 - i * 0.1)

    # 2️⃣ Proximity to contact info
    for i, line in enumerate(lines):
        if re.search(EMAIL_REGEX, line) or re.search(PHONE_REGEX, line):
            for j in range(max(0, i - 5), i):
                scores[lines[j]] += 2.0
            break

    # 3️⃣ NER signal (soft)
    doc = nlp(text[:1200])
    for ent in doc.ents:
        if ent.label_ == "PERSON":
            scores[ent.text.strip()] += 3.0

    candidates = {}

    for cand, score in scores.items():
        words = cand.lower().split()

        # HARD BLOCKERS (this is what fixes PyCharm)
        if any(w in TOOLS_DB for w in words):
            continue
        if any(w in SKILLS_DB for w in words):
            continue
        if any(w in ROLE_WORDS for w in words):
            continue
        if re.search(r"[0-9@#%$&+]", cand):
            continue
        if not (1 <= len(words) <= 4):
            continue
        if not all(w.isalpha() for w in words):
            continue

        candidates[cand] = score

    if not candidates:
        return None, 0.0

    best = max(candidates, key=candidates.get)
    confidence = min(0.99, candidates[best] / 7.0)

    return best, round(confidence, 2)

# -------------------------------------------------
# EMAIL
# -------------------------------------------------
def extract_email(text):
    m = re.search(EMAIL_REGEX, text)
    return m.group() if m else None

# -------------------------------------------------
# PHONE
# -------------------------------------------------
def extract_phone(text):
    m = re.search(PHONE_REGEX, text)
    return m.group() if m else None

# -------------------------------------------------
# SKILLS
# -------------------------------------------------
def extract_skills(text):
    text_lower = text.lower()
    return sorted({s for s in SKILLS_DB if s in text_lower})

# -------------------------------------------------
# MAIN
# -------------------------------------------------
def extract_entities(text):
    name, confidence = extract_name(text)

    return {
        "name": name,
        "name_confidence": confidence,
        "email": extract_email(text),
        "phone": extract_phone(text),
        "skills": extract_skills(text)
    }
