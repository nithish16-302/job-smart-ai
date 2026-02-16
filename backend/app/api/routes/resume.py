from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.models.resume_profile import ResumeProfile
from app.services.resume_parser import parse_resume_text

router = APIRouter()

@router.post('/upload')
async def upload_resume(
    file: UploadFile = File(...),
    location: str = Form(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    raw = await file.read()
    text = raw.decode("utf-8", errors="ignore")
    parsed = parse_resume_text(text)

    profile = ResumeProfile(
        user_id=current_user.id,
        file_name=file.filename,
        extracted_text=text[:5000],
        parsed_skills=", ".join(parsed["skills"]),
        parsed_roles=", ".join(parsed["roles"]),
    )
    db.add(profile)

    current_user.preferred_location = location
    db.add(current_user)

    db.commit()
    db.refresh(profile)

    return {
        "resume_profile_id": profile.id,
        "filename": file.filename,
        "location": location,
        "skills": parsed["skills"],
        "roles": parsed["roles"],
        "message": "Resume parsed and profile saved."
    }
