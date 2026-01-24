SKILLS_DB = ["python", "java", "sql", "machine learning", "nlp"]

def extract_skills(text):
    return list({s for s in SKILLS_DB if s in text.lower()})
