# FastAPI Backend (Docker)

A modular FastAPI backend project structured for building REST APIs with routers, services, database models, and utilities.

---

## Project Structure

```
backend/
├── app
│   ├── api         # API routers
│   ├── core        # Core settings and configuration
│   ├── crud        # CRUD operations
│   ├── db          # Database connection and session
│   ├── models      # SQLAlchemy models
│   ├── schemas     # Pydantic schemas
│   ├── services    # Business logic
│   ├── utils       # Utility functions
│   └── __pycache__
```

---

## Requirements

- Docker Desktop
- Run via `docker compose` from the repo root

---

## Setup Instructions

From the repository root:

```
docker compose up -d --build
```

---

## Running the Server

The backend runs automatically via Docker Compose at:

- API: http://localhost:8000
- Docs: http://localhost:8000/docs

---

## Usage

- Add API routes in `app/api`
- Define models in `app/models`
- Create Pydantic schemas in `app/schemas`
- Implement business logic in `app/services`
- Utility functions in `app/utils`

---

## Notes

- For test data: `docker compose exec backend python scripts/create_test_data.py`

---

## License

This project is licensed under the MIT License.