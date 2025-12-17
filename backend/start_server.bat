@echo off
rem cd /d D:\s3\py\soutenance-manager\backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
