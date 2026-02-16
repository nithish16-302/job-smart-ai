from typing import Dict, List

KNOWN_SKILLS = [
    "python", "java", "javascript", "typescript", "react", "node", "aws", "azure", "gcp",
    "docker", "kubernetes", "sql", "postgres", "spark", "hadoop", "tensorflow", "pytorch",
    "devops", "data engineering", "machine learning", "network engineering", "business analysis",
    "product management"
]

KNOWN_ROLES = [
    "network engineer", "full stack developer", "data engineer", "data scientist",
    "ai engineer", "ml engineer", "devops engineer", "business analyst", "product manager"
]

def parse_resume_text(text: str) -> Dict[str, List[str]]:
    lower = text.lower()
    skills = [s for s in KNOWN_SKILLS if s in lower]
    roles = [r for r in KNOWN_ROLES if r in lower]
    return {"skills": sorted(set(skills)), "roles": sorted(set(roles))}
