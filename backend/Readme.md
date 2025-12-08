# FastAPI Backend Project

[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

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
└── venv            # Virtual environment
```

---

## Requirements

- Python 3.10+
- FastAPI
- Uvicorn
- Other dependencies in `requirements.txt`

---

## Setup Instructions

1. Clone the repository:

```
git clone <your-repo-url>
cd backend
```

2. Create and activate virtual environment:

```
python -m venv venv
.\venv\Scripts\Activate    # Windows
# source venv/bin/activate  # macOS/Linux
```

3. Upgrade pip (optional but recommended):

```
python -m pip install --upgrade pip
```

4. Install dependencies:

```
pip install -r requirements.txt
```

---

## Running the Server

```
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Access API docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Usage

- Add API routes in `app/api`
- Define models in `app/models`
- Create Pydantic schemas in `app/schemas`
- Implement business logic in `app/services`
- Utility functions in `app/utils`

---

## Notes

- Always activate the virtual environment before running the server.
- Use `--reload` during development for automatic server restart.

---

## License

This project is licensed under the MIT License.