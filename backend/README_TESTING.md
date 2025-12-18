# Testing & Seeding (PostgreSQL)

This guide explains how to seed a PostgreSQL database, run the backend locally, and test the API endpoints with Postman or curl.

Prerequisites
- PostgreSQL server accessible (local or remote)
- psql CLI installed
- Python 3.10+ (or appropriate for your project)

1) Configure `backend/.env`

Set `DATABASE_URL` in `backend/.env`. Example (Postgres):

```
DATABASE_URL=postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>
```

If you use a local Postgres with default port and a database named `aisoutenance`:

```
DATABASE_URL=postgresql://postgres:password@127.0.0.1:5432/aisoutenance
```

2) Create the database (if not exists)

```bash
# Replace with your credentials
createdb -h 127.0.0.1 -p 5432 -U postgres aisoutenance
# or using psql:
psql -h 127.0.0.1 -U postgres -c "CREATE DATABASE aisoutenance;"
```

3) Install Python deps and run the app

```powershell
cd backend
python -m venv venv
# PowerShell activate
venv\Scripts\Activate.ps1
pip install -r requirements.txt
# Ensure DATABASE_URL is exported or backend/.env is read by the project
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

When the app starts, `Base.metadata.create_all(bind=engine)` in `app/main.py` will create tables automatically.

4) Seed the DB

From `backend/` run:

```bash
# Using psql. It will prompt for the DB password.
psql "postgresql://<db_user>:<db_password>@<db_host>:<db_port>/<db_name>" -f seed.sql
```

Example:

```bash
psql "postgresql://postgres:password@127.0.0.1:5432/aisoutenance" -f seed.sql
```

Important: If you inserted explicit IDs in `seed.sql`, you may need to reset sequences:

```sql
SELECT setval(pg_get_serial_sequence('users','id'), (SELECT MAX(id) FROM users));
SELECT setval(pg_get_serial_sequence('reports','id'), (SELECT MAX(id) FROM reports));
SELECT setval(pg_get_serial_sequence('thesis_defenses','id'), (SELECT MAX(id) FROM thesis_defenses));
SELECT setval(pg_get_serial_sequence('notifications','id'), (SELECT MAX(id) FROM notifications));
```

Run those in `psql` after seeding.

5) Ensure sample report file exists

Place `sample_report.pdf` in `backend/storage/reports/` (a sample was created earlier). The `reports.file_name` in DB should match this filename.

6) Test endpoints with Postman / curl

Base URL: `http://127.0.0.1:8000/api/professors`

Required header to simulate auth: `X-Professor-Id: 1`

Examples (curl):

```bash
curl -H "X-Professor-Id: 1" http://127.0.0.1:8000/api/professors/assigned-soutenances

curl -H "X-Professor-Id: 1" http://127.0.0.1:8000/api/professors/soutenances/1

# Download PDF
curl -H "X-Professor-Id: 1" http://127.0.0.1:8000/api/professors/soutenances/1/report/download --output sample_report_downloaded.pdf

# Post evaluation
curl -X POST -H "X-Professor-Id: 1" -H "Content-Type: application/json" \
  -d '{"score":18.5,"comments":"Très bonne soutenance."}' \
  http://127.0.0.1:8000/api/professors/soutenances/1/evaluation

# Get notifications
curl -H "X-Professor-Id: 1" http://127.0.0.1:8000/api/professors/notifications

# Mark notification read
curl -X PATCH -H "X-Professor-Id: 1" http://127.0.0.1:8000/api/professors/notifications/1/read
```

7) Importing to Postman

- Create a new collection.
- Add requests with the paths above and set header `X-Professor-Id: 1` as a collection-level header.
- For PDF download, in Postman choose "Send and download" to save the file.

8) Troubleshooting

- If you see DB errors on startup, check `DATABASE_URL` and that Postgres user has privileges.
- If tables are missing, ensure `app/main.py` calls `Base.metadata.create_all(bind=engine)` (it does in this repo).
- For constraint errors, inspect the inserted data ordering; use sequences reset queries above.


---

If tu veux, je peux:
- Générer automatiquement une collection Postman JSON prête à importer.
- Exécuter les commandes `psql -f seed.sql` depuis ce environnement si tu veux que je fasse le seed (j'aurai besoin des credentials DB).
