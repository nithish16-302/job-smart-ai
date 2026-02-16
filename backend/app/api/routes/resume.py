from fastapi import APIRouter, UploadFile, File, Form

router = APIRouter()

@router.post('/upload')
async def upload_resume(
    file: UploadFile = File(...),
    location: str = Form(...)
):
    # TODO: parse resume and store structured profile
    return {
        "filename": file.filename,
        "location": location,
        "message": "Resume received. Parsing pipeline to be implemented in next milestone."
    }
