from typing import List, Dict
import requests


def _normalize(source: str, payload: Dict) -> Dict:
    return {
        "source": source,
        "external_id": str(payload.get("id") or payload.get("url") or payload.get("title")),
        "title": payload.get("title", "Untitled"),
        "company": payload.get("company", "Unknown"),
        "location": payload.get("location", "Remote"),
        "apply_url": payload.get("url", ""),
        "description": payload.get("description", ""),
        "tags": ", ".join(payload.get("tags", [])) if isinstance(payload.get("tags"), list) else str(payload.get("tags", "")),
        "posted_at": payload.get("publication_date") or payload.get("posted_at") or "",
    }


def fetch_remotive(limit: int = 30) -> List[Dict]:
    url = "https://remotive.com/api/remote-jobs"
    try:
        data = requests.get(url, timeout=20).json()
        jobs = data.get("jobs", [])[:limit]
        mapped = []
        for j in jobs:
            mapped.append(_normalize("remotive", {
                "id": j.get("id"),
                "title": j.get("title"),
                "company": j.get("company_name"),
                "location": j.get("candidate_required_location"),
                "url": j.get("url"),
                "description": j.get("description", ""),
                "tags": j.get("tags", []),
                "publication_date": j.get("publication_date", ""),
            }))
        return mapped
    except Exception:
        return []


def fetch_mock_jobs() -> List[Dict]:
    sample = [
        {
            "id": "mk-1",
            "title": "Senior Data Engineer",
            "company": "Midwest Analytics Co",
            "location": "Austin, TX",
            "url": "https://example.com/jobs/mk-1",
            "description": "Build ETL pipelines, Python, SQL, Spark.",
            "tags": ["python", "sql", "spark", "data engineering"],
            "posted_at": "2026-02-16",
        },
        {
            "id": "mk-2",
            "title": "DevOps Engineer",
            "company": "CloudForge Systems",
            "location": "Remote",
            "url": "https://example.com/jobs/mk-2",
            "description": "AWS, Kubernetes, Docker, CI/CD.",
            "tags": ["aws", "kubernetes", "docker", "devops"],
            "posted_at": "2026-02-16",
        },
        {
            "id": "mk-3",
            "title": "AI/ML Engineer",
            "company": "ProductNova",
            "location": "Raleigh, NC",
            "url": "https://example.com/jobs/mk-3",
            "description": "Train and deploy ML models. Python, PyTorch.",
            "tags": ["python", "machine learning", "pytorch", "ai"],
            "posted_at": "2026-02-15",
        },
    ]
    return [_normalize("mock", j) for j in sample]


def fetch_all_sources(limit: int = 30) -> List[Dict]:
    jobs = fetch_mock_jobs()
    jobs.extend(fetch_remotive(limit=limit))
    return jobs
