from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import health, jobs, resume, auth, profile, dashboard, applications, alerts, admin
from app.db.init_db import init_db

app = FastAPI(title="Job Smart AI API", version="0.2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    init_db()

app.include_router(health.router)
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(jobs.router, prefix="/jobs", tags=["jobs"])
app.include_router(applications.router, prefix="/applications", tags=["applications"])
app.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(admin.router, prefix="/admin", tags=["admin"])
