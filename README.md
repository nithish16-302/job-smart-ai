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

### Milestone 5 (Lead Sourcing Stage 1) ✅
- Lead sourcing service + API (`/lead-sourcing/run-now`, `/lead-sourcing/latest`)
- Pipeline UI route (`/pipeline`) for manual run + summary view
- Local lead sourcing script writes outputs to `data/lead_sourcing/`

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

## Deploy Backend on Render
This repo includes a Render Blueprint file: `render.yaml`.

### Option A (recommended)
1. In Render dashboard, click **New +** → **Blueprint**
2. Connect this GitHub repo: `nithish16-302/job-smart-ai`
3. Render will create:
   - `jobsmart-db` (Postgres)
   - `jobsmart-api` (FastAPI web service)
4. After deploy, copy backend URL (example: `https://jobsmart-api.onrender.com`)

### Option B (manual service)
- Root directory: `backend`
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`
- Env vars:
  - `DATABASE_URL` (from Render Postgres)
  - `JWT_SECRET` (random strong value)
  - `GOOGLE_CLIENT_ID` (Google OAuth Web Client ID)

## Connect Frontend to Render Backend
In Vercel project env vars, set:
- `NEXT_PUBLIC_API_BASE=https://<your-render-backend-url>`
- `NEXT_PUBLIC_GOOGLE_CLIENT_ID=<same-google-client-id>`

Then redeploy frontend.
