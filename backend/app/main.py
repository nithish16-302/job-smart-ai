from fastapi import FastAPI
from app.api.routes import health, jobs, resume

app = FastAPI(title="Job Smart AI API", version="0.1.0")

app.include_router(health.router)
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
