#!/usr/bin/env python3
import json
from datetime import datetime
from pathlib import Path
from urllib.request import Request, urlopen

TARGET_ROLES = {
    "software_engineering": ["software engineer", "full stack", "backend", "frontend", "developer"],
    "devops": ["devops", "sre", "platform engineer", "site reliability"],
    "network_engineering": ["network engineer", "network administrator", "nocc", "noc"],
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


def fetch_remotive(limit=200):
    req = Request(
        "https://remotive.com/api/remote-jobs",
        headers={"User-Agent": "Mozilla/5.0 TeamSoftLeadBot/1.0"}
    )
    with urlopen(req, timeout=30) as r:
        payload = json.loads(r.read().decode("utf-8"))
    return payload.get("jobs", [])[:limit]


def classify(job_text):
    text = job_text.lower()
    matched = []
    for tech, kws in TARGET_ROLES.items():
        if any(k in text for k in kws):
            matched.append(tech)
    return matched


def location_score(location):
    loc = (location or "").lower()
    if any(t1 in loc for t1 in EXCLUDED_TIER1):
        return 0
    if any(city in loc for city in TIER2_3_CITIES):
        return 2
    if "remote" in loc:
        return 1
    return 0


def lead_score(job, matched_tech):
    score = 0
    score += 3 if matched_tech else 0
    score += location_score(job.get("candidate_required_location", ""))
    score += 2 if "contract" in (job.get("title", "") + " " + job.get("description", "")).lower() else 0
    score += 1 if any(k in (job.get("description", "")).lower() for k in ["urgent", "immediate", "asap"]) else 0
    return score


def main():
    jobs = fetch_remotive()
    leads = []

    for j in jobs:
        text = f"{j.get('title','')} {j.get('description','')} {j.get('category','')}"
        matched = classify(text)
        if not matched:
            continue

        score = lead_score(j, matched)
        if score < 4:
            continue

        leads.append({
            "source": "remotive",
            "title": j.get("title"),
            "company": j.get("company_name"),
            "location": j.get("candidate_required_location"),
            "url": j.get("url"),
            "technologies": matched,
            "lead_score": score,
            "contract_signal": "contract" in text.lower(),
            "posted_at": j.get("publication_date"),
        })

    leads.sort(key=lambda x: x["lead_score"], reverse=True)

    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    ts = now.strftime("%Y-%m-%d_%H-%M")

    out_dir = Path(__file__).resolve().parents[1] / "data" / "lead_sourcing"
    out_dir.mkdir(parents=True, exist_ok=True)

    latest_path = out_dir / "latest.json"
    dated_path = out_dir / f"leads_{ts}.json"
    summary_path = out_dir / "summary.txt"

    payload = {
        "generated_at": now.isoformat(),
        "total_leads": len(leads),
        "top_leads": leads[:100]
    }

    latest_path.write_text(json.dumps(payload, indent=2))
    dated_path.write_text(json.dumps(payload, indent=2))

    by_tech = {k: 0 for k in TARGET_ROLES.keys()}
    for l in leads:
        for t in l["technologies"]:
            by_tech[t] += 1

    summary_lines = [
        f"Generated at: {now.isoformat()}",
        f"Total qualified leads: {len(leads)}",
        "By technology:"
    ] + [f"- {k}: {v}" for k, v in by_tech.items()]

    summary_path.write_text("\n".join(summary_lines) + "\n")
    print(json.dumps({
        "total_leads": len(leads),
        "latest": str(latest_path),
        "snapshot": str(dated_path),
        "summary": str(summary_path)
    }))


if __name__ == "__main__":
    main()
