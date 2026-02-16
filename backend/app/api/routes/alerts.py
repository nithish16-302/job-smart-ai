from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.application import Application
from app.models.resume_profile import ResumeProfile
from app.models.user import User

router = APIRouter()


@router.get("")
def get_alerts(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    alerts: list[dict] = []

    profile = (
        db.query(ResumeProfile)
        .filter(ResumeProfile.user_id == current_user.id)
        .order_by(ResumeProfile.id.desc())
        .first()
    )
    if not profile:
        alerts.append({"level": "warning", "message": "Upload your resume to get personalized matching."})

    saved_count = (
        db.query(Application)
        .filter(Application.user_id == current_user.id, Application.stage == "saved")
        .count()
    )
    if saved_count > 0:
        alerts.append({
            "level": "info",
            "message": f"You have {saved_count} saved jobs pending application."
        })

    interview_count = (
        db.query(Application)
        .filter(Application.user_id == current_user.id, Application.stage == "interview")
        .count()
    )
    if interview_count > 0:
        alerts.append({
            "level": "success",
            "message": f"Great news: {interview_count} applications are in interview stage."
        })

    if not alerts:
        alerts.append({"level": "info", "message": "No critical alerts. Keep applying to improve your pipeline."})

    return {"alerts": alerts}
