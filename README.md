# 🎓 Soutenance Manager - AI-Powered Thesis Defense Management System

A smart thesis defense (soutenance) management platform built with FastAPI and Next.js, featuring AI-powered PDF analysis and automated scheduling.

[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.124.0-green.svg)](https://fastapi.tiangolo.com/)
[![Next.js](https://img.shields.io/badge/Next.js-14.2-black.svg)](https://nextjs.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)

---

## 🚀 Features

- 📝 **Student Dashboard**: Submit thesis defense requests with PDF uploads
- 🤖 **AI Integration**: Automated PDF analysis for summaries and domain detection
- 👨‍🏫 **Professor Management**: Jury assignment and availability tracking
- 📊 **Request Tracking**: Real-time status monitoring (pending/accepted/refused)
- 🗓️ **Smart Scheduling**: Automated defense scheduling
- 🔒 **Role-Based Access**: Student, Professor, Manager roles

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
    docker compose up --build -d
    ```

2.  **Prepare Backend Environment (for data seeding):**
    Ensure a `.env` file exists in the `backend/` directory. If not, copy from `.env.example`:
    ```bash
    cp backend/.env.example backend/.env # For Linux/macOS
    # For Windows PowerShell:
    # Copy-Item backend\.env.example backend\.env
    ```
    (Note: The `SECRET_KEY` in `backend/.env` should be a strong, random 32-character key for production, but can be left as default for development.)

3.  **Seed Initial Data:**
    This step populates the database with essential users (admin, student, professor, manager).
    ```bash
    docker compose run --rm backend python scripts/create_initial_data.py
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
│   │   │   └── thesis_defense.py
│   │   ├── crud/             # Database operations
│   │   ├── db/               # Database configuration
│   │   ├── models/           # SQLAlchemy models
│   │   └── schemas/          # Pydantic schemas
│   ├── scripts/              # Utility scripts
│   ├── uploads/              # PDF file storage
│   └── requirements.txt
├── frontend/
│   ├── app/                  # Next.js app directory
│   ├── components/           # React components
│   │   ├── StudentDashboard.tsx
│   │   ├── SoutenanceRequestForm.tsx
│   │   └── RequestHistory.tsx
│   ├── services/             # API integration
│   └── types/                # TypeScript types
└── docker-compose.yml        # PostgreSQL setup
```

---

## 🔧 Configuration

### Backend Environment Variables

If you run the backend outside Docker, edit `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:admin1234@localhost:5432/Ai_Soutenance
API_HOST=0.0.0.0
API_PORT=8000
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

- **users**: User authentication and roles
- **students**: Student-specific information
- **professors**: Professor details and availability
- **thesis_defenses**: Defense requests and schedules
- **reports**: Uploaded PDF reports with AI analysis
- **jury_members**: Jury assignments for defenses
- **notifications**: System notifications

---

## 🧪 Testing

### Test Users

You can use the following credentials to log in and test the application with different roles. The password for all users is `password`.

| Role      | Email                  | Password   |
|-----------|------------------------|------------|
| Student   | student@example.com    | `password` |
| Professor | professor@example.com  | `password` |
| Manager   | manager@example.com    | `password` |
| Admin     | admin@example.com      | `password` |

### API Testing

Visit **http://localhost:8000/docs** for interactive API documentation (Swagger UI).

---

## 🐳 Docker Commands

```bash
# Start everything
docker compose up --build

# Start in background
docker compose up -d --build

# Stop everything
docker compose down

# View logs
docker compose logs -f

# Reset database (⚠️ deletes all data)
docker compose down -v
docker compose up -d --build
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
docker compose exec backend python scripts/create_test_data.py
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

### Student Endpoints

- `POST /api/students/soutenance-requests` - Submit defense request
- `GET /api/students/soutenance-requests` - Get student's requests
- `GET /api/students/dashboard` - Get dashboard statistics
- `GET /api/students/requests/{id}` - Get specific request

### Professor Endpoints

- `GET /api/v1/professors` - List all professors
- `POST /api/v1/professors` - Create professor

### Thesis Defense Endpoints

- `GET /api/v1/defenses/` - List all defenses
- `PATCH /api/v1/defenses/{id}` - Update defense status
- `GET /api/v1/defenses/{id}/jury` - Get jury members
- `POST /api/v1/defenses/{id}/jury` - Assign jury member

---

## 👥 Team Contributions

- **Khalid**: Student Dashboard & Frontend Integration
- **Abdelmoughit**: Professor Space
- **Abdelkbir**: Database & Backend Architecture
- **Achraf**: [Your role]

---

## 🔜 Upcoming Features

- [ ] AI-powered PDF analysis integration
- [ ] Email notifications
- [ ] Calendar integration
- [ ] Multi-language support
- [ ] Advanced search and filtering
- [ ] Export reports (PDF/Excel)

---

## 🐛 Troubleshooting

### Database Connection Error

```bash
# Ensure PostgreSQL is running
docker ps

# Restart PostgreSQL
docker-compose restart
```

### Backend Module Not Found

```bash
# Ensure you're in the backend directory
cd backend

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Build Errors

```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Login and Authentication Troubleshooting

If you encounter issues during login, refer to these common problems and their solutions:

-   **`401 Unauthorized` errors in backend logs (`INFO: ... 401 Unauthorized`)**:
    This indicates that the provided username (email) or password is incorrect. Ensure you are using the default credentials created by the `create_initial_data.py` script.
    *   **Default Credentials (password for all):**
        *   `student@example.com`
        *   `professor@example.com`
        *   `manager@example.com`
        *   `admin@example.com`
    *   **Solution:** Verify the backend database has been seeded. Follow step 3 in "Quick Start -> Option A" to run `docker compose run --rm backend python scripts/create_initial_data.py`.

-   **`Failed to load resource: net::ERR_NAME_NOT_RESOLVED` or `AxiosError` in browser console**:
    This means your frontend application cannot reach the backend API.
    *   **Common Causes:**
        *   The backend service is not running.
        *   The frontend's `NEXT_PUBLIC_API_URL` environment variable is misconfigured for client-side access.
    *   **Solution:**
        1.  Ensure all Docker services are running: `docker compose ps`. If any service is down, run `docker compose up -d`.
        2.  Verify the `NEXT_PUBLIC_API_URL` in `docker-compose.yml` for the frontend service is set to `http://localhost:8000`. If you changed it, revert it and rebuild the frontend:
            ```bash
            docker compose build frontend
            docker compose up -d --force-recreate frontend
            ```
            Then access the frontend at `http://localhost:3000`.

-   **`AttributeError: module 'app.crud' has no attribute 'user'` in backend logs**:
    This is an internal backend issue related to how database operations for users are exposed.
    *   **Solution:** This was addressed by ensuring `app/crud/crud_user.py` is correctly imported in `app/crud/__init__.py`. If you encounter this, ensure your codebase is up-to-date with the latest changes.

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
