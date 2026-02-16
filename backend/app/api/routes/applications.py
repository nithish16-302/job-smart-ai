from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.application import Application
from app.models.job import Job
from app.models.user import User

router = APIRouter()


@router.get('/mine')
def list_my_applications(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    apps = (
        db.query(Application, Job)
        .join(Job, Application.job_id == Job.id)
        .filter(Application.user_id == current_user.id)
        .order_by(Application.id.desc())
        .all()
    )
    return {
        "applications": [
            {
                "application_id": a.id,
                "stage": a.stage,
                "created_at": str(a.created_at),
                "job": {
                    "id": j.id,
                    "title": j.title,
                    "company": j.company,
                    "location": j.location,
                    "apply_url": j.apply_url,
                    "source": j.source,
                },
            }
            for a, j in apps
        ]
    }


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
