from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.ingest_run import IngestRun
from app.models.job import Job
from app.models.user import User

router = APIRouter()


@router.get("/source-health")
def source_health(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # For MVP, authenticated users can view admin health stats.
    source_counts = db.query(Job.source, func.count(Job.id)).group_by(Job.source).all()
    source_map = {source: count for source, count in source_counts}

    latest_runs = (
        db.query(IngestRun)
        .order_by(IngestRun.id.desc())
        .limit(10)
        .all()
    )

    return {
        "source_counts": source_map,
        "recent_ingest_runs": [
            {
                "id": r.id,
                "source": r.source,
                "fetched": r.fetched,
                "inserted": r.inserted,
                "status": r.status,
                "created_at": str(r.created_at),
            }
            for r in latest_runs
        ],
    }
