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

- [Python 3.11+](https://www.python.org/downloads/)
- [Node.js 18+](https://nodejs.org/)
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (for PostgreSQL)
- [Git](https://git-scm.com/)

---

## 🛠️ Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/IBIZZI-Khalid/soutenance-manager.git
cd soutenance-manager
```

### 2️⃣ Start PostgreSQL Database

```bash
# Start PostgreSQL using Docker Compose
docker-compose up -d

# Verify it's running
docker ps
```

### 3️⃣ Setup Backend (FastAPI)

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create .env file from example
copy .env.example .env  # Windows
# cp .env.example .env  # Mac/Linux

# Create test student data
python scripts/create_test_data.py

# Start backend server
uvicorn app.main:app --reload
# Or use: start_server.bat (Windows)
```

Backend will run at: **http://localhost:8000**
API Documentation: **http://localhost:8000/docs**

### 4️⃣ Setup Frontend (Next.js)

```bash
cd ../frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will run at: **http://localhost:3000**

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

Edit `backend/.env`:

```env
DATABASE_URL=postgresql://postgres:admin1234@localhost:5432/Ai_Soutenance
API_HOST=0.0.0.0
API_PORT=8000
```

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

### Test Student Account

```
Email: test.student@example.com
User ID: 1
Major: Computer Science
```

### API Testing

Visit **http://localhost:8000/docs** for interactive API documentation (Swagger UI).

---

## 🐳 Docker Commands

```bash
# Start PostgreSQL
docker-compose up -d

# Stop PostgreSQL
docker-compose down

# View logs
docker-compose logs -f

# Reset database (⚠️ deletes all data)
docker-compose down -v
docker-compose up -d
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
