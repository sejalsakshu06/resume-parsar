SECTIONS = {
    "education": ["education", "academic"],
    "experience": ["experience", "work history"],
    "skills": ["skills", "technical skills"],
}

def detect_sections(text):
    sections = {}
    current = None

    for line in text.split("\n"):
        lower = line.lower()
        for key, words in SECTIONS.items():
            if any(w in lower for w in words):
                current = key
                sections[current] = []
        if current:
            sections[current].append(line)

    return sections
