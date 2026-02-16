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
pip install -r requirements.txt
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
