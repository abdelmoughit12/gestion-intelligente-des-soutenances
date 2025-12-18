# Soutenance Manager (Docker Edition)

## 🚀 Quick Start (for New Teammates)

This guide will get you running the full stack (backend, frontend, database, AI) **with Docker only**—no Python, Node, or venv setup needed!

---

## 1. Prerequisites
- **Docker Desktop**: [Download & Install](https://www.docker.com/products/docker-desktop)
- (Recommended) **Git**: [Download Git](https://git-scm.com/downloads)

---

## 2. Clone the Repository

```bash
git clone https://github.com/AbdelkbirNA/Ai_Soutenance.git
cd Ai_Soutenance
git checkout dev
git pull
```
*Or use your fork’s URL if you’re working from there.*

---

## 3. Configure Environment Variables

- Copy the example env file:
  ```bash
  cp .env.example .env
  ```
- **Edit `.env`** (in the project root) and add your Gemini API key:
  ```
  GEMINI_API_KEY=your_actual_gemini_api_key_here
  ```
  *(Get a Gemini API key from [Google AI Studio](https://aistudio.google.com/) > "Get API key")*

---

## 4. Build and Start All Services

```bash
docker compose up -d --build
```
This will:
- Build and start the **PostgreSQL database**
- Build and start the **FastAPI backend**
- Build and start the **Next.js frontend**

---

## 5. (Optional) Seed Test Data

```bash
docker compose exec backend python scripts/create_test_data.py
```

---

## 6. Access the Application
- **Frontend:** [http://localhost:3000](http://localhost:3000)
- **Backend API docs:** [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 7. Stopping and Restarting
- **Stop everything:**
  ```bash
  docker compose down
  ```
- **Restart:**
  ```bash
  docker compose up -d
  ```

---

## 8. Troubleshooting
- **Check logs:**
  ```bash
  docker compose logs -f backend
  docker compose logs -f frontend
  docker compose logs -f postgres
  ```
- **Rebuild if you pull new changes:**
  ```bash
  docker compose up -d --build
  ```

---

## 9. Features
- Student dashboard (multi-page: Home, Upload, History)
- PDF upload with AI-powered summary, domain verification, and similarity check
- Gemini AI integration (auto fallback to Flash-Lite if rate-limited)
- All code, dependencies, and data run in Docker containers

---

## 10. Need Help?
If you get stuck, copy the error and send it to the team!
