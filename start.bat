@echo off
setlocal

echo Starting Soutenance Manager (Docker)...
docker compose up -d --build
if errorlevel 1 (
  echo.
  echo Failed to start Docker Compose. Make sure Docker Desktop is running.
  exit /b 1
)

echo.
echo Services are starting.
echo - Frontend: http://localhost:3000
echo - Backend : http://localhost:8000
echo - Docs    : http://localhost:8000/docs

echo.
echo Optional: seed test data
echo   docker compose exec backend python scripts/create_test_data.py

endlocal
