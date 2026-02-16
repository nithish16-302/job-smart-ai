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
    if "remote" in loc or "world" in loc or "usa" in loc:
        return 1
    return 0


def enrich_contact(company_name: str) -> Dict:
    domain = None
    try:
        r = requests.get(
            "https://autocomplete.clearbit.com/v1/companies/suggest",
            params={"query": company_name},
            timeout=10,
            headers={"User-Agent": "TeamSoftLeadBot/1.0"},
        )
        items = r.json() if r.ok else []
        if items:
            domain = items[0].get("domain")
    except Exception:
        domain = None

    emails = []
    if domain:
        emails = [
            f"recruiting@{domain}",
            f"talent@{domain}",
            f"hr@{domain}",
            f"vendors@{domain}",
            f"partnerships@{domain}",
        ]

    return {
        "company_domain": domain,
        "target_contact_titles": [
            "Talent Acquisition Manager",
            "Technical Recruiter",
            "Delivery Manager",
            "Engineering Manager",
            "Vendor Manager",
        ],
        "suggested_emails": emails,
        "note": "Generated role inbox suggestions; verify before outreach.",
    }


def run_lead_sourcing(limit: int = 120) -> Dict:
    try:
        data = requests.get("https://remotive.com/api/remote-jobs", timeout=20, headers={"User-Agent": "TeamSoftLeadBot/1.0"}).json()
        jobs = data.get("jobs", [])[:limit]
    except Exception as e:
        return {
            "total_leads": 0,
            "leads_with_contact": 0,
            "by_technology": {k: 0 for k in TARGET_ROLES.keys()},
            "leads": [],
            "warning": f"source fetch failed: {e}",
        }

    leads = []

    for j in jobs:
        text = f"{j.get('title','')} {j.get('description','')} {j.get('category','')}"
        tech = classify(text)
        if not tech:
            continue
        score = 3 + loc_score(j.get("candidate_required_location", ""))
        if any(k in text.lower() for k in ["contract", "c2c", "1099"]):
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
            "contact": enrich_contact(j.get("company_name", "")),
        })

    leads.sort(key=lambda x: x["lead_score"], reverse=True)

    by_tech = {k: 0 for k in TARGET_ROLES.keys()}
    with_contact = 0
    for lead in leads:
        for t in lead["technologies"]:
            by_tech[t] += 1
        if lead.get("contact", {}).get("company_domain"):
            with_contact += 1

    return {
        "total_leads": len(leads),
        "leads_with_contact": with_contact,
        "by_technology": by_tech,
        "leads": leads[:50],
    }
