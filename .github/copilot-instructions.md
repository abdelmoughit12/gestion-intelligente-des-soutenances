<!-- Copilot instructions tailored for the Ai_Soutenance workspace -->
# Copilot / AI coding instructions — Ai_Soutenance

Purpose
- Help an AI agent become productive quickly in this repo by summarizing architecture, key files, conventions, and exact dev commands.

Big picture
- Monorepo with two apps: a FastAPI backend under `backend/app` and a Next.js frontend under `frontend`.
- Backend: FastAPI + SQLAlchemy. Models live in `backend/app/models`; DB session is configured in `backend/app/db/session.py`. Tables are currently created at startup in `backend/app/main.py` via `Base.metadata.create_all(bind=engine)` (no migrations present).
- Frontend: Next.js (app directory), Tailwind CSS, client-side React components. HTTP client is `frontend/services/api.ts` (axios) which targets `NEXT_PUBLIC_API_URL`.

Quick dev commands
- Backend (from `backend/`):
  - Create venv and install: `python -m venv venv && venv\\Scripts\\activate && pip install -r requirements.txt` (Windows example)
  - Run dev server: `uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`
  - Set `DATABASE_URL` in `backend/.env`
- Frontend (from `frontend/`):
  - Install + dev: `npm install && npm run dev`
  - Build: `npm run build`
  - Uses `NEXT_PUBLIC_API_URL` to point to backend (defaults to `http://localhost:8000`). See `frontend/services/api.ts`.

Important integration points & patterns
- Backend DB: See `backend/app/db/session.py` for `SessionLocal`, `Base`. Models import `Base` from that module. Example models: `backend/app/models/user.py`, `professor.py`, `thesis_defense.py`.
- API routers: `backend/app/api/*.py`. Example: `professor.py` contains professor-facing endpoints (many are TODO placeholders and return dummy data). Frontend expects endpoints such as `/api/professors/assigned-soutenances`, `/api/professors/soutenances/{id}/report/download`.
- Frontend service: `frontend/services/api.ts` centralizes API calls (axios). It sets `Content-Type` and handles blobs for PDF downloads. Note: currently this file has duplicated function blocks—deduplicate when changing.
- File upload: Frontend uses `FormData` and sets `multipart/form-data` for uploads (see `submitSoutenanceRequest`). Backend endpoints must accept multipart on student request routes.
- Authentication: There are many placeholder auth dependencies (e.g., `get_current_professor`) in backend routes; authentication is not implemented — treat auth checks as TODOs unless you implement an auth layer. Search for `get_current_professor` or placeholder comments.

Project-specific conventions
- Models use `user`, `professor`, `student` split: `User` holds auth/profile fields, specialized tables (Professor/Student/Manager) reference `users.id` via ForeignKey.
- Status strings for soutenances are used directly in components and services: `pending`, `scheduled`, `in_progress`, `evaluated`. Keep responses consistent with these values.
- Frontend components are React client components (many start with `'use client'`) and rely on the service functions from `frontend/services/api.ts`.
- No DB migrations: current approach uses `Base.metadata.create_all(...)`. If adding schema changes, prefer adding Alembic and not relying on runtime table creation for production.

When editing or adding endpoints
- Match the shapes used by the frontend types: check `frontend/types/soutenance.ts` for expected fields like `id`, `title`, `studentName`, `domain`, `status`.
- Return JSON arrays/objects matching what `frontend/services/api.ts` expects (see `getProfessorAssignedSoutenances` and `getSoutenanceDetail`).
- For file downloads, return a proper `FileResponse` with `media_type='application/pdf'` so frontend `axios` can download as blob.

Files to inspect when changing behavior
- Backend: [backend/app/main.py](backend/app/main.py#L1), [backend/app/db/session.py](backend/app/db/session.py#L1), [backend/app/models/user.py](backend/app/models/user.py#L1), [backend/app/models/thesis_defense.py](backend/app/models/thesis_defense.py#L1), [backend/app/api/professor.py](backend/app/api/professor.py#L1)
- Frontend: [frontend/services/api.ts](frontend/services/api.ts#L1), [frontend/components/professor/ProfessorDashboard.tsx](frontend/components/professor/ProfessorDashboard.tsx#L1), [frontend/components/professor/AssignedSoutenanceCard.tsx](frontend/components/professor/AssignedSoutenanceCard.tsx#L1), [frontend/types/soutenance.ts](frontend/types/soutenance.ts#L1)

Common pitfalls & TODOs found
- `backend/app/api/professor.py` contains placeholder logic and dummy responses — implement DB queries and auth before marking features complete.
- `frontend/services/api.ts` contains duplicate function blocks; deduplicate to avoid maintenance issues.
- No auth or migrations — plan these before production rollout.

If you need clarification
- Ask for the desired auth approach (JWT/session) and how you want to store uploaded PDFs (filesystem path vs external storage).

End of file
