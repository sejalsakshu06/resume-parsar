"""
Defines the schema for the resume output.
"""


def build_schema(personal, sections, skills):
    """Builds the resume schema from the extracted information."""
    # Filter out empty entries
    education = [e for e in sections.get("education", []) if e.strip()]
    experience = [e for e in sections.get("experience", []) if e.strip()]
    projects = [e for e in sections.get("projects", []) if e.strip()]
    achievements = [e for e in sections.get("achievement", []) if e.strip()]

    return {
        "personal_info": personal,
        "education": education,
        "experience": experience,
        "projects": projects,
        "achievements": achievements,
        "skills": skills
    }

