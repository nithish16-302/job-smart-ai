from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.application import Application
from app.models.job import Job
from app.models.user import User

router = APIRouter()


@router.post('/save/{job_id}')
def save_job(job_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    existing = (
        db.query(Application)
        .filter(Application.user_id == current_user.id, Application.job_id == job_id)
        .first()
    )
    if existing:
        return {"message": "Already saved", "application_id": existing.id, "stage": existing.stage}

    app = Application(user_id=current_user.id, job_id=job_id, stage="saved")
    db.add(app)
    db.commit()
    db.refresh(app)
    return {"application_id": app.id, "stage": app.stage}


@router.post('/stage/{application_id}')
def update_stage(application_id: int, stage: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    app = (
        db.query(Application)
        .filter(Application.id == application_id, Application.user_id == current_user.id)
        .first()
    )
    if not app:
        raise HTTPException(status_code=404, detail="Application not found")

    app.stage = stage
    db.add(app)
    db.commit()
    db.refresh(app)
    return {"application_id": app.id, "stage": app.stage}
