from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.resume_profile import ResumeProfile
from app.models.job import Job
from app.services.job_sources import fetch_all_sources
from app.services.matching import rank_jobs

router = APIRouter()


@router.post('/ingest')
def ingest_jobs(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    fetched = fetch_all_sources(limit=25)
    inserted = 0
    for item in fetched:
        exists = (
            db.query(Job)
            .filter(Job.source == item["source"], Job.external_id == item["external_id"])
            .first()
        )
        if exists:
            continue
        row = Job(**item)
        db.add(row)
        inserted += 1
    db.commit()
    return {"fetched": len(fetched), "inserted": inserted}


@router.get('/personalized')
def get_personalized_jobs(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    latest_profile = (
        db.query(ResumeProfile)
        .filter(ResumeProfile.user_id == current_user.id)
        .order_by(ResumeProfile.id.desc())
        .first()
    )

    skills = latest_profile.parsed_skills.split(", ") if latest_profile and latest_profile.parsed_skills else []
    roles = latest_profile.parsed_roles.split(", ") if latest_profile and latest_profile.parsed_roles else []

    jobs = db.query(Job).order_by(Job.id.desc()).limit(100).all()
    normalized = [
        {
            "id": j.id,
            "source": j.source,
            "title": j.title,
            "company": j.company,
            "location": j.location,
            "apply_url": j.apply_url,
            "description": j.description or "",
            "tags": j.tags or "",
            "posted_at": j.posted_at,
        }
        for j in jobs
    ]

    ranked = rank_jobs(normalized, skills, roles, current_user.preferred_location or "Remote")

    return {
        "location": current_user.preferred_location or "Remote",
        "skills": skills,
        "roles": roles,
        "jobs": ranked[:25],
        "message": "Personalized jobs ranked successfully."
    }
