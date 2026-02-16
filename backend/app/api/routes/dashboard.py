from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.application import Application
from app.models.job import Job
from app.models.user import User

router = APIRouter()


@router.get('/stages')
def dashboard_stages(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    total_jobs = db.query(func.count(Job.id)).scalar() or 0
    total_apps = db.query(func.count(Application.id)).filter(Application.user_id == current_user.id).scalar() or 0

    stage_rows = (
        db.query(Application.stage, func.count(Application.id))
        .filter(Application.user_id == current_user.id)
        .group_by(Application.stage)
        .all()
    )
    stage_counts = {stage: count for stage, count in stage_rows}

    return {
        "sourced": total_jobs,
        "matched": total_jobs,
        "applied": total_apps,
        "stages": {
            "saved": stage_counts.get("saved", 0),
            "applied": stage_counts.get("applied", 0),
            "interview": stage_counts.get("interview", 0),
            "offer": stage_counts.get("offer", 0),
            "rejected": stage_counts.get("rejected", 0),
        },
    }
