from typing import List, Dict


def score_job(job: Dict, skills: List[str], roles: List[str], preferred_location: str) -> Dict:
    text = f"{job.get('title', '')} {job.get('description', '')} {job.get('tags', '')}".lower()
    title = str(job.get("title", "")).lower()
    location = str(job.get("location", "")).lower()

    skills_hits = sum(1 for s in skills if s and s.lower() in text)
    roles_hits = sum(1 for r in roles if r and r.lower() in title)

    skill_score = min(skills_hits * 8, 40)
    role_score = min(roles_hits * 20, 20)

    preferred = (preferred_location or "").lower()
    if not preferred or preferred == "remote":
        location_score = 15 if ("remote" in location or location) else 8
    else:
        location_score = 15 if preferred in location else 5

    recency_score = 10
    total = skill_score + role_score + location_score + recency_score

    return {
        **job,
        "score": min(total, 100),
        "score_breakdown": {
            "skills": skill_score,
            "role": role_score,
            "location": location_score,
            "recency": recency_score,
        },
    }


def rank_jobs(jobs: List[Dict], skills: List[str], roles: List[str], preferred_location: str) -> List[Dict]:
    scored = [score_job(j, skills, roles, preferred_location) for j in jobs]
    return sorted(scored, key=lambda x: x["score"], reverse=True)
