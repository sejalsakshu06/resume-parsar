def build_schema(personal, sections, skills):
    # Filter out empty entries
    education = [e for e in sections.get("education", []) if e.strip()]
    experience = [e for e in sections.get("experience", []) if e.strip()]
    
    return {
        "personal_info": personal,
        "education": sections.get("education", []),
        "experience": sections.get("experience", []),
        "skills": skills
    }
