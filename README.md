# Job Smart AI

Resume-aware job discovery platform.

## MVP Goals
- User login
- Resume upload + parsing
- Location preferences
- Personalized job search across multiple sources
- Apply tracking

## Current Status
### Milestone 1 ✅
- Monorepo scaffold complete

### Milestone 2 ✅
- Email/password auth (register/login)
- JWT-based protected endpoints
- Resume upload + keyword parser (skills/roles extraction)
- User location preference persistence

### Milestone 3 ✅
- Multi-source job ingestion (`/jobs/ingest`)
- Job normalization + persistence
- Personalized ranking (`/jobs/personalized`)
- Pipeline stage dashboard (`/dashboard/stages`)

### Milestone 4 ✅
- Routing-based UX (`/login`, `/dashboard`, `/jobs`, `/applications`, `/admin`)
- Client-side auth guards + persistent token session
- Apply tracking UI with stage updates
- Alerts API + dashboard integration
- Admin source health UI

## Monorepo Structure
- `frontend/` - Next.js app
- `backend/` - FastAPI API
- `infra/` - infrastructure and docker files
- `docs/` - product and architecture docs

## Quick Start
### 1) Start infra
```bash
docker compose up -d db
```

### 2) Backend
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
# If you're on Python 3.14, use this env var for pydantic-core build compatibility:
PYO3_USE_ABI3_FORWARD_COMPATIBILITY=1 pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### 3) Frontend
```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:3000  
Backend health: http://localhost:8000/health

> Recommended backend Python: **3.12 or 3.13** for smooth dependency install.
