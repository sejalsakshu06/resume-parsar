"""
This module provides functions for extracting skills from resume text.
"""

SKILLS_DB = [
    # Programming Languages
    "python", "java", "c", "c++", "c/c++", "c#", "javascript", "typescript",
    "go", "golang", "rust", "ruby", "php", "swift", "kotlin", "scala",
    "perl", "r", "matlab", "bash", "shell",
    
    # Web Technologies
    "html", "html5", "css", "css3", "sass", "less",
    "react", "reactjs", "react native", "vue", "vuejs", "angular",
    "node", "nodejs", "express", "expressjs", "nextjs", "nuxt",
    "jquery", "bootstrap", "tailwind", "tailwindcss", "material ui", "ant design",
    
    # Backend & Databases
    "django", "flask", "fastapi", "spring", "spring boot",
    "sql", "mysql", "postgresql", "postgres", "mongodb", "redis", "sqlite",
    "oracle", "nosql", "firebase", "supabase", "ms-sql", "mssql",
    
    # Data Science & ML
    "machine learning", "ml", "deep learning", "nlp", "nlu",
    "tensorflow", "pytorch", "keras", "scikit-learn", "sklearn",
    "pandas", "numpy", "matplotlib", "seaborn", "plotly",
    "computer vision", "opencv", "yolo", "data science", "flink", "spark",
    
    # DevOps & Cloud
    "docker", "kubernetes", "k8s", "jenkins", "git", "github", "gitlab",
    "aws", "aws services", "azure", "azure services", "gcp", "google cloud", "cloud", "terraform",
    "ansible", "puppet", "chef", "ci/cd", "devops",
    
    # Tools & Other
    "jira", "confluence", "figma", "sketch", "adobe xd",
    "postman", "insomnia", "swagger", "rest api", "graphql",
    "microservices", "agile", "scrum", "kanban",
    
    # Soft Skills
    "communication", "leadership", "teamwork", "problem solving",
    "project management", "time management", "analytical",
]


def extract_skills(text):
    """
    Extracts skills from the text based on a predefined list.
    """
    return list({s for s in SKILLS_DB if s in text.lower()})

