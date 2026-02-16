from pydantic import BaseModel

class LocationPreferenceRequest(BaseModel):
    preferred_location: str

class MeResponse(BaseModel):
    id: int
    email: str
    full_name: str
    preferred_location: str | None = None
