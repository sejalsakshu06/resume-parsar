#!/usr/bin/env python3
"""
Test script to parse the provided resume text.
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from models.core import parse_resume_text
import json

# Resume text from user
RESUME_TEXT = """Rahul Kumar
​Full Stack Developer | Integrated Dual Degree (Btech+Mtech) | CSE IIT Kharagpur
rahulkumar2207@gmail.com | +918117244114 | India | linkedin.com/in/rahul-kumar
​WORK EXPERIENCE
​TechSolve Solutions
Software Development Intern | July 2024 - Dec 2024
​Developed a responsive web application using React.js and TailwindCSS, improving user engagement by 15%.
​Collaborated with a team of 4 to implement a RESTful API using Node.js and Express, ensuring seamless data flow between the frontend and backend.
​Optimized database queries in MongoDB, reducing query response time by 20%.
​Integrated JWT-based authentication, securing user access for 500+ accounts.
​Participated in code reviews and followed Agile methodologies, improving code quality and development efficiency.
​Deployed the application on AWS S3 and EC2, ensuring scalability and 99.9% uptime.
​EDUCATION
​IIT Kharagpur
Integrated Dual Degree (Btech+Mtech) - 9.2/10 | 2019 - 2024
​PROJECTS
​TaskManager Pro | 2019 - 2020
​Developed TaskManager Pro, a task management web application to streamline daily task organization and team collaboration.
​Implemented user authentication (signup, login, and password recovery) with secure JWT-based access, ensuring data protection for 1,000+ users.
​Designed an intuitive task management system with CRUD operations, improving task completion efficiency by 25%.
​Enabled team collaboration by allowing task sharing and assignments, boosting team productivity by 30%.
​Integrated email notifications for task updates and deadlines, reducing missed deadlines by 20%.
​Built using React.js, Node.js (Express), MongoDB, AWS S3/EC2, and JWT authentication, ensuring scalability and performance.
​Portfolio Builder | 2020 - 2021
​Developed a dynamic web application enabling users to create and customize professional portfolios with real-time previews.
​Integrated drag-and-drop features using React.js, enhancing user experience and reducing portfolio creation time by 40%.
​Built with React.js, Node.js, and MongoDB, and deployed on AWS S3/EC2, ensuring fast load times and scalability.
​SKILLS
​Languages: C/C++, Python, Javascript, Java, Scala
​Frameworks: React.js, Django, Vue.js, Springboot, Flink, Spark
​Cloud/Databases/Tech-Stack: Postgres, MS-SQL, Mysql, AWS Services, Azure Services, ELK Stack, Prometheus, Kubernetes, Docker, Aerospike, Airflow, Helm
​ACHIEVEMENT
​AIR 756 in JEE Advance 2019"""

def main():
    print("=" * 70)
    print("SIGMA-CV Resume Parser - Test Run")
    print("=" * 70)
    print("\n📄 Parsing resume for: Rahul Kumar\n")
    
    # Parse the resume
    result = parse_resume_text(RESUME_TEXT)
    
    # Print structured output
    print("=" * 70)
    print("PARSED RESULT")
    print("=" * 70)
    
    # Personal Info
    print("\n👤 PERSONAL INFORMATION")
    print("-" * 40)
    personal = result.get('personal_info', {})
    print(f"  Name:    {personal.get('name', 'N/A')}")
    print(f"  Email:   {personal.get('email', 'N/A')}")
    print(f"  Phone:   {personal.get('phone', 'N/A')}")
    
    # Education
    print("\n🎓 EDUCATION")
    print("-" * 40)
    education = result.get('education', [])
    if education:
        for i, edu in enumerate(education, 1):
            print(f"  {i}. {edu}")
    else:
        print("  Not detected")
    
    # Experience
    print("\n💼 WORK EXPERIENCE")
    print("-" * 40)
    experience = result.get('experience', [])
    if experience:
        for i, exp in enumerate(experience, 1):
            print(f"  {i}. {exp[:200]}..." if len(exp) > 200 else f"  {i}. {exp}")
    else:
        print("  Not detected")
    
    # Projects
    print("\n🚀 PROJECTS")
    print("-" * 40)
    projects = result.get('projects', [])
    if projects:
        for i, proj in enumerate(projects, 1):
            print(f"  {i}. {proj[:200]}..." if len(proj) > 200 else f"  {i}. {proj}")
    else:
        print("  Not detected")
    
    # Skills
    print("\n🛠 SKILLS")
    print("-" * 40)
    skills = result.get('skills', [])
    if skills:
        print(f"  {', '.join(skills)}")
    else:
        print("  Not detected")
    
    # Achievements
    print("\n🏆 ACHIEVEMENTS")
    print("-" * 40)
    achievements = result.get('achievements', [])
    if achievements:
        for i, ach in enumerate(achievements, 1):
            print(f"  {i}. {ach}")
    else:
        print("  Not detected")
    
    # JSON Output
    print("\n" + "=" * 70)
    print("JSON OUTPUT")
    print("=" * 70)
    print(json.dumps(result, indent=2))
    
    return result

if __name__ == "__main__":
    main()

