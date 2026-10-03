# Samify

React + Vite + Tailwind frontend, FastAPI + SQLAlchemy + Alembic backend, MySQL database.
Stage 1 (foundation) only. See each stage's report for status.

## Requirements
Node 20+, Python 3.11+, MySQL 8+

## Database
```sql
CREATE DATABASE samify CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'samify_user'@'localhost' IDENTIFIED BY 'change_me';
GRANT ALL ON samify.* TO 'samify_user'@'localhost';
```

## Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env        # then edit DATABASE_URL and SECRET_KEY
pytest                      # unit tests (use in-memory SQLite, no MySQL needed)
uvicorn app.main:app --reload --port 8000
```
Docs: http://localhost:8000/docs

## Frontend
```bash
cd frontend
cp .env.example .env
npm install
npm run dev     # http://localhost:5173
```

## Stage 1 live check (needs MySQL + both servers running)
```bash
cd backend && python scripts/check_stage1.py
```
Alembic: `alembic current` should run without error (no migrations until Stage 2).
