from fastapi import APIRouter, Depends
from app.api.deps import get_current_user
from app.models.user import User
from app.services.lead_sourcing import run_lead_sourcing

router = APIRouter()

_last_result = {"total_leads": 0, "by_technology": {}, "leads": []}


@router.post('/run-now')
def run_now(current_user: User = Depends(get_current_user)):
    global _last_result
    _last_result = run_lead_sourcing(limit=150)
    return _last_result


@router.get('/latest')
def latest(current_user: User = Depends(get_current_user)):
    return _last_result
