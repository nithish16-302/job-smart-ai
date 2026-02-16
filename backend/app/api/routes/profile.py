from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.profile import LocationPreferenceRequest, MeResponse

router = APIRouter()

@router.get('/me', response_model=MeResponse)
def me(current_user: User = Depends(get_current_user)):
    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        preferred_location=current_user.preferred_location,
    )

@router.post('/preferences/location', response_model=MeResponse)
def set_location_preference(
    payload: LocationPreferenceRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.preferred_location = payload.preferred_location
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return MeResponse(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        preferred_location=current_user.preferred_location,
    )
