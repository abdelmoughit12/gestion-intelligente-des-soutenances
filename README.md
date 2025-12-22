# 🎓 Soutenance Manager - AI-Powered Thesis Defense Management System

A smart thesis defense (soutenance) management platform built with FastAPI and Next.js, featuring AI-powered PDF analysis and automated scheduling.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124.0-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2-black.svg)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)

---

## 🚀 Features

- 📝 **Student Dashboard**: Submit thesis defense requests with PDF uploads
- 🆕 **Student Registration Workflow**: Students can register for an account, which remains inactive until approved by a manager.
- 🤖 **AI Integration**: Automated PDF analysis for summaries and domain detection
- 👨‍🏫 **Professor Management**: Jury assignment and availability tracking
- 🆕 **Manager Professor Management**: Managers can add new professor accounts directly.
- 📊 **Request Tracking**: Real-time status monitoring (pending/accepted/refused)
- 🆕 **Manager Student Approval**: Managers can view and approve/reject pending student registrations.
- 🗓️ **Smart Scheduling**: Automated defense scheduling
- 🔒 **Role-Based Access**: Student, Professor, Manager roles with strict route protection.

---

## 📋 Prerequisites

Before you begin, ensure you have installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Git](https://git-scm.com/)

---

## 🛠️ Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/IBIZZI-Khalid/soutenance-manager.git
cd soutenance-manager
```

### 2️⃣ Start the App

This project supports two ways to run locally.

#### Option A (Recommended): Run Everything with Docker

1.  **Build and Start Services:**

    ```bash
    # Build and start all services (PostgreSQL, Backend, Frontend) in detached mode
    docker compose up -d --build
    ```

2.  **Prepare Backend Environment:**
    Ensure a `.env` file exists in the `backend/` directory. If not, copy from `.env.example`:
    ```bash
    cp backend/.env.example backend/.env # For Linux/macOS
    # For Windows PowerShell:
    # Copy-Item backend\.env.example backend\.env
    ```
    Make sure the `.env` file contains the `DATABASE_URL` and `GEMINI_API_KEY` as specified in the project requirements.

3.  **Seed Initial Data:**
    This step populates the database with essential users (manager, student, professor).
    ```bash
    docker compose exec backend python seed_data.py
    ```

4.  **Access Applications:**

    - Frontend: **http://localhost:3000**
    - Backend API: **http://localhost:8000**
    - Swagger docs: **http://localhost:8000/docs**

#### Option B (Manual Dev): Frontend Local, DB+Backend in Docker

1) Start only Postgres + Backend via Docker:

```bash
docker compose up -d --build postgres backend
```

2) Start the frontend locally:

```bash
cd frontend
npm install
npm run dev
```

Frontend will run at **http://localhost:3000** and call the backend at **http://localhost:8000**.

### 3️⃣ (Optional) Seed Test Data

```bash
docker compose exec backend python scripts/create_test_data.py
```

If you want to override the default Postgres credentials without editing Compose, copy `.env.example` to `.env` at the repo root.

---

## 📁 Project Structure

```
soutenance-manager/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── student.py    # Student endpoints
│   │   │   ├── professor.py  # Professor endpoints
│   │   │   ├── thesis_defense.py
│   │   │   ├── manager.py    # NEW: Manager-specific endpoints
│   │   │   └── auth.py       # UPDATED: Added student registration endpoint
│   │   ├── crud/             # Database operations
│   │   │   ├── crud_student.py # NEW: Student-specific CRUD operations
│   │   │   └── crud_professor.py # UPDATED: Professor CRUD operations
│   │   ├── db/               # Database configuration
│   │   ├── models/           # SQLAlchemy models (UPDATED: User model)
│   │   └── schemas/          # Pydantic schemas (UPDATED: User, Professor schemas)
│   ├── scripts/              # Utility scripts
│   ├── uploads/              # PDF file storage
│   ├── seed_data.py          # UPDATED: Seed script for initial data
│   └── requirements.txt
├── frontend/
│   ├── app/                  # Next.js app directory
│   │   ├── register/page.tsx # UPDATED: Student registration page
│   │   ├── dashboard/manager/requests/page.tsx # NEW: Manager student approval page
│   │   ├── dashboard/manager/professors/page.tsx # NEW: Manager add professor page
│   │   └── unauthorized/page.tsx # UPDATED: Redirection logic
│   ├── components/           # React components
│   │   ├── StudentDashboard.tsx
│   │   ├── SoutenanceRequestForm.tsx
│   │   ├── RequestHistory.tsx
│   │   ├── unified-sidebar.tsx # UPDATED: Manager navigation links
│   │   ├── MultiPageDashboard.tsx # UPDATED: Student navigation links
│   │   └── withAuth.tsx      # UPDATED: Role-based access control logic
│   ├── services/             # API integration
│   │   ├── api.ts            # UPDATED: Exported api instance
│   │   ├── auth.ts           # UPDATED: Added registerStudent function
│   │   └── manager.ts        # NEW: Manager-specific API services
│   └── types/                # TypeScript types (UPDATED: UserRole enum)
└── docker-compose.yml        # PostgreSQL setup
```

---

## 🏛️ Architecture and Development Guide

This section provides a high-level overview of the project's architecture and a guide for adding new features.

### High-Level Architecture

The application is a monorepo composed of three main services orchestrated by Docker Compose:

1.  **Frontend**: A **Next.js (React)** application responsible for the user interface. It communicates with the backend via a REST API.
2.  **Backend**: A **FastAPI (Python)** application that serves the API, handles business logic, and interacts with the database.
3.  **Database**: A **PostgreSQL** database that stores all the application data.

### Authentication Flow

Authentication is handled using JWT (JSON Web Tokens).

1.  **Login**: The user enters their credentials on the frontend, which sends a request to the `/api/v1/auth/login` endpoint on the backend.
2.  **Token Generation**: The backend authenticates the user. If successful, it generates a JWT access token containing the user's ID, email, and role.
3.  **Token Storage**: The frontend receives the token and stores it in the browser's `localStorage`.
4.  **Authenticated Requests**: For subsequent requests to protected endpoints, the frontend attaches the JWT to the `Authorization` header as a `Bearer` token.
5.  **Token Verification**: The backend uses a dependency (`get_current_user`) to verify the token on protected routes. If the token is valid, the user's information is retrieved from the database and made available to the endpoint. Role-based access is controlled by `require_role` dependencies. Unauthorized users are now redirected to their respective home dashboards.

### Backend Development Guide: Adding a New Feature

Here’s a step-by-step guide to adding a new feature (e.g., a "Projects" feature).

#### 1. Create the Model

Define the database table structure in a new file, `backend/app/models/project.py`. This uses SQLAlchemy's ORM.

```python
# backend/app/models/project.py
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..db.session import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")
```

Remember to import the new model in `backend/app/models/__init__.py`.

#### 2. Create the Schemas

Define the Pydantic schemas for data validation and serialization in `backend/app/schemas/project.py`.

```python
# backend/app/schemas/project.py
from pydantic import BaseModel

class ProjectBase(BaseModel):
    title: str
    description: str | None = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True
```

Import the new schemas in `backend/app/schemas/__init__.py`.

#### 3. Create CRUD Operations

Create a file for database operations in `backend/app/crud/crud_project.py`.

```python
# backend/app/crud/crud_project.py
from sqlalchemy.orm import Session
from .base import CRUDBase
from ..models.project import Project
from ..schemas.project import ProjectCreate, ProjectUpdate

class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    pass

project = CRUDProject(Project) # IMPORTANT: The instance name must match the import in __init__.py
```

Import the new CRUD object in `backend/app/crud/__init__.py`.

#### 4. Create the API Router

Create the API endpoints in `backend/app/api/project.py`. Ensure routes are protected with the appropriate dependencies.

```python
# backend/app/api/project.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ... import crud, schemas
from ...dependencies import get_current_user, get_db

router = APIRouter()

@router.post("/", response_model=schemas.Project)
def create_project(
    *,
    db: Session = Depends(get_db),
    project_in: schemas.ProjectCreate,
    current_user = Depends(get_current_user)
):
    project = crud.project.create_with_owner(db=db, obj_in=project_in, owner_id=current_user.id)
    return project
```

#### 5. Include the Router in the Main App

Finally, add the new router to `backend/app/main.py`.

```python
# backend/app/main.py
from app.api import project # 1. Import the new router

# ... (inside the main app)

# 2. Include the router
app.include_router(project.router, prefix="/api/v1/projects", tags=["projects"])
```

### Frontend Development Guide

1.  **API Service**: Add a function in `frontend/services/api.ts` (or a new dedicated service like `frontend/services/manager.ts` for role-specific actions) to call the new backend endpoints.
2.  **Component**: Create new React components (e.g., `frontend/components/ProjectForm.tsx`) to interact with the API.
3.  **Page**: Create new pages in `frontend/app/projects/page.tsx` to display the components. Ensure pages are protected using the `withAuth` HOC with the correct `UserRole`.

---

## 🔧 Configuration

### Backend Environment Variables

The `.env` file in the `backend` folder should now contain:

```env
DATABASE_URL="postgresql://postgres:admin1234@localhost:5432/Ai_Soutenance"
GEMINI_API_KEY="AIzaSyA4DzC34gyFWPHIZXudOtDh688K0-blCoQ"
# ... other existing variables
```

When using Docker Compose, `DATABASE_URL` is injected automatically and should use the service name `postgres`.

### Frontend Environment Variables

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 📊 Database Schema

The system uses PostgreSQL with the following main tables:

- **users**: User authentication and roles (UPDATED: Added `phone` and `is_active` columns).
- **students**: Student-specific information
- **professors**: Professor details and availability
- **thesis_defenses**: Defense requests and schedules
- **reports**: Uploaded PDF reports with AI analysis
- **jury_members**: Jury assignments for defenses
- **notifications**: System notifications
- **managers**: Manager-specific information (NEW: Added as a separate model)

---

## 🧪 Testing

### Test Users

You can use the following credentials to log in and test the application with different roles. The password for all users is `password`.

| Role      | Email                  | Password   |
|-----------|------------------------|------------|
| Student   | student1@example.com   | `password` |
| Professor | prof1@example.com      | `password` |
| Manager   | manager@example.com    | `password` |
| Admin     | admin@example.com      | `password` |

### API Testing

Visit **http://localhost:8000/docs** for interactive API documentation (Swagger UI).

---

## 🐳 Docker Commands

```bash
# Start everything (builds if necessary, runs in foreground)
docker compose up --build

# Start everything in detached mode
docker compose up -d --build

# Stop everything
docker compose down

# View logs
docker compose logs -f

# Reset database (⚠️ deletes all data)
docker compose down
docker volume rm ai_soutenance_postgres_data
docker compose up -d --build
docker compose exec backend python seed_data.py
```

## 🧯 Docker Troubleshooting

If you get a container name conflict (example: `postgres-soutenance is already in use`), it usually means you previously started a container manually.

```bash
docker rm -f postgres-soutenance
docker compose up -d --build
```

If you get a port conflict on `5432`, stop/remove the other Postgres container using that port, then rerun Compose.

---

## 👥 Team Workflow (Dev Branch)

Teammates should work from `dev` and run the app with Docker.

1) Pull latest `dev`:

```bash
git checkout dev
git pull
```

2) Run the stack:

```bash
docker compose up -d --build
```

3) (Optional) Seed test data:

```bash
docker compose exec backend python seed_data.py
```

4) Create a feature branch, push, and open a PR into `dev`:

```bash
git checkout -b feature/<your-feature>
git add .
git commit -m "Your message"
git push -u origin feature/<your-feature>
```

---

## 📝 API Endpoints

### Authentication Endpoints
- `POST /api/v1/auth/register/student` - NEW: Register a new student account (initially inactive).
- `POST /api/v1/auth/login` - Authenticate user and receive JWT token.

### Student Endpoints
- `POST /api/students/soutenance-requests` - Submit defense request
- `GET /api/students/soutenance-requests` - Get student's requests
- `GET /api/students/dashboard` - Get dashboard statistics
- `GET /api/students/requests/{id}` - Get specific request

### Professor Endpoints
- `GET /api/v1/professors` - List all professors
- `GET /api/v1/professors/{professor_id}` - Retrieve a specific professor
- `GET /api/v1/professors/assigned-soutenances` - Get assigned thesis defenses
- `GET /api/v1/professors/soutenances/{defense_id}` - Get details of a specific assigned defense
- `GET /api/v1/professors/soutenances/{defense_id}/report/download` - Download report for an assigned defense
- `POST /api/v1/professors/soutenances/{defense_id}/evaluation` - Submit evaluation for a defense
- `GET /api/v1/professors/notifications` - List professor's notifications
- `PATCH /api/v1/professors/notifications/{notification_id}/read` - Mark notification as read

### Manager Endpoints (NEW)
- `GET /api/v1/manager/pending-students` - List all pending student registration requests.
- `PATCH /api/v1/manager/pending-students/{user_id}/approve` - Approve a student registration request.
- `DELETE /api/v1/manager/pending-students/{user_id}/reject` - Reject and delete a student registration request.
- `POST /api/v1/manager/professors` - Add a new professor.

### Thesis Defense Endpoints
- `GET /api/v1/thesis-defenses/` - List all thesis defenses
- `PATCH /api/v1/thesis-defenses/{defense_id}` - Update a thesis defense (e.g., status, schedule)
- `GET /api/v1/thesis-defenses/{defense_id}/jury` - Retrieve jury members for a defense
- `POST /api/v1/thesis-defenses/{defense_id}/jury` - Assign a professor to a jury
- `PUT /api/v1/thesis-defenses/{defense_id}/jury/{professor_id}` - Update a jury member's role
- `GET /api/v1/thesis-defenses/{defense_id}/jury-suggestions` - Get AI-powered jury suggestions

### User Endpoints
- `GET /api/v1/users/me` - Get current authenticated user's profile.

### Statistics Endpoints
- `GET /api/v1/stats/` - Retrieve overall application statistics.

---

## 📄 License

This project is part of an academic project for [Your University Name].

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📧 Contact

For questions or support, contact the team:
- **Repository**: https://github.com/IBIZZI-Khalid/soutenance-manager
- **Upstream**: https://github.com/AbdelkbirNA/Ai_Soutenance

---

Made with ❤️ by the Soutenance Manager Team
