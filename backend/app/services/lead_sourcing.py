from typing import Dict, List
import requests

TARGET_ROLES = {
    "software_engineering": ["software engineer", "full stack", "backend", "frontend", "developer"],
    "devops": ["devops", "sre", "platform engineer", "site reliability"],
    "network_engineering": ["network engineer", "network administrator", "noc"],
    "qa_testing": ["qa", "quality assurance", "test automation", "sdet"],
    "ba_product": ["business analyst", "product manager", "product owner"],
    "data_science": ["data scientist", "data analyst", "analytics engineer"],
    "ai_ml": ["ml engineer", "machine learning", "ai engineer", "llm", "genai"],
}

TIER2_3_CITIES = [
    "raleigh", "charlotte", "nashville", "tampa", "orlando", "columbus", "indianapolis",
    "st. louis", "kansas city", "salt lake city", "phoenix", "pittsburgh", "cincinnati", "richmond",
    "boise", "oklahoma city", "omaha", "milwaukee", "cleveland", "jacksonville"
]
EXCLUDED_TIER1 = ["new york", "san francisco", "seattle", "los angeles", "boston", "chicago", "austin"]


def classify(text: str) -> List[str]:
    t = text.lower()
    found = []
    for tech, kws in TARGET_ROLES.items():
        if any(k in t for k in kws):
            found.append(tech)
    return found


def loc_score(location: str) -> int:
    loc = (location or "").lower()
    if any(x in loc for x in EXCLUDED_TIER1):
        return 0
    if any(x in loc for x in TIER2_3_CITIES):
        return 2
    if "remote" in loc:
        return 1
    return 0


def run_lead_sourcing(limit: int = 120) -> Dict:
    data = requests.get("https://remotive.com/api/remote-jobs", timeout=20).json()
    jobs = data.get("jobs", [])[:limit]
    leads = []

    for j in jobs:
        text = f"{j.get('title','')} {j.get('description','')} {j.get('category','')}"
        tech = classify(text)
        if not tech:
            continue
        score = 3 + loc_score(j.get("candidate_required_location", ""))
        if "contract" in text.lower():
            score += 2
        if score < 4:
            continue
        leads.append({
            "title": j.get("title"),
            "company": j.get("company_name"),
            "location": j.get("candidate_required_location"),
            "url": j.get("url"),
            "technologies": tech,
            "lead_score": score,
        })

    leads.sort(key=lambda x: x["lead_score"], reverse=True)

    by_tech = {k: 0 for k in TARGET_ROLES.keys()}
    for lead in leads:
        for t in lead["technologies"]:
            by_tech[t] += 1

    return {
        "total_leads": len(leads),
        "by_technology": by_tech,
        "leads": leads[:50],
    }
