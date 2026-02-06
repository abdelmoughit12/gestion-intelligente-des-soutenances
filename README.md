# Soutenance Manager — Intelligent Thesis Defense Management

A smart thesis defense (soutenance) management platform built with FastAPI (backend) and Next.js (frontend). This repository contains the full-stack project for submitting, managing, scheduling, and evaluating thesis defenses with optional AI-assisted PDF analysis.

## Features

- Student dashboard to submit defense requests with PDF uploads
- Student registration workflow (pending approval by a manager)
- AI-powered PDF analysis (summaries, domain detection)
- Professor management: jury assignment and availability tracking
- Manager area for approving students and adding professors
- Request tracking with statuses (pending / scheduled / in_progress / evaluated)
- Smart scheduling and jury suggestions
- Role-based access control (Student, Professor, Manager)

## Quick Start (Docker - recommended)

1. Build and start services:

```bash
docker compose up -d --build
```

2. Ensure backend environment file exists at `backend/.env` (copy from `.env.example` if needed) and contains `DATABASE_URL` and any API keys the app expects.

3. Seed initial data (creates sample manager, professor, student):

```bash
docker compose exec backend python seed_data.py
```

4. Open the apps:

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

## Quick Start (Manual frontend, Docker backend)

1. Start Postgres + Backend with Docker:

```bash
docker compose up -d --build postgres backend
```

2. Start frontend locally:

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at http://localhost:3000 and call the backend at http://localhost:8000 by default.

## Project Layout (important folders)

- `backend/` — FastAPI application (models, CRUD, API routers, storage)
- `frontend/` — Next.js app (app directory, components, services)
- `docker-compose.yml` — orchestrates Postgres, backend, frontend

Key backend files to inspect:
- `backend/app/main.py` — app startup and router inclusion
- `backend/app/db/session.py` — database session and `Base`
- `backend/app/models/` — SQLAlchemy models
- `backend/app/api/` — API routers (student, professor, manager, auth)

Key frontend files:
- `frontend/services/api.ts` — central axios instance and API functions
- `frontend/app/` and `frontend/components/` — pages and UI components

## Environment variables

Backend `.env` should include at least:

```
DATABASE_URL="postgresql://postgres:password@postgres:5432/Ai_Soutenance"
GEMINI_API_KEY="your_api_key_here"
```

Frontend: create `frontend/.env.local` with:

```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## API (high-level)

- `POST /api/v1/auth/register/student` — register a student (pending)
- `POST /api/v1/auth/login` — obtain JWT token
- Student endpoints under `/api/students` for submitting and listing requests
- Professor endpoints under `/api/v1/professors` for assigned defenses and report downloads
- Manager endpoints under `/api/v1/manager` for pending student approvals and adding professors

Refer to `backend/app/api/` for exact route definitions and request/response shapes.

## Seeding & Test Data

To populate the database with test users and sample data:

```bash
docker compose exec backend python seed_data.py
```

Additional test scripts are available under `backend/scripts/`.

## Contributing

1. Fork the repo and create a feature branch
2. Commit and push your changes
3. Open a PR into the main/dev branch

## Pushing this file to your GitHub

Run the following from the repository root to commit and push the new English README:

```bash
git add README-LAST-en.md
git commit -m "Add English README (last version)"
git push origin YOUR_BRANCH
```

If you want me to create a branch and open a PR, tell me the target remote/branch and I can provide the exact commands.

## License & Contact

This project is an academic project. See the original repository for authorship details and license notes.

---

