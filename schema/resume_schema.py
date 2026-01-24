def build_schema(personal, sections, skills):
    return {
        "personal_info": personal,
        "education": sections.get("education", []),
        "experience": sections.get("experience", []),
        "skills": skills
    }
