from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.resume_profile import ResumeProfile

router = APIRouter()

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

    return {
        "location": current_user.preferred_location or "Remote",
        "skills": latest_profile.parsed_skills.split(", ") if latest_profile and latest_profile.parsed_skills else [],
        "roles": latest_profile.parsed_roles.split(", ") if latest_profile and latest_profile.parsed_roles else [],
        "jobs": [],
        "message": "Personalized context ready. Job source aggregation is next."
    }
