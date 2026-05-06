# Soccho - Friend Money Tracker

## Overview
Soccho is a microservices app for tracking lent/borrowed money among friends with auth, social, transactions, notifications, admin, PWA/offline.

## Local Setup
1. Copy `.env.example` to `.env` and fill secrets/DB creds.
2. Create venvs per service: `python -m venv service_name/venv`
3. Install deps: `pip install -r service_name/requirements.txt`
4. DB: Enable pg_trgm: `psql -d $DATABASE_URL -c \"CREATE EXTENSION IF NOT EXISTS pg_trgm;\""
5. Per Django service: `python manage.py makemigrations && python manage.py migrate`
6. Redis: Ensure running.
7. Gateway: `uvicorn gateway.main:app --reload`
8. docker-compose up (dev stack).
9. Frontend: Open `frontend/index.html` or Vercel preview.

## Services
- Gateway: http://localhost:8000 (FastAPI, gRPC proxy)
- Auth: http://localhost:8001 (Django Ninja)
- Social: http://localhost:8002 (DRF+Graphene)
- Transaction: http://localhost:8003 (DRF+Graphene)
- Notification: http://localhost:8004/ws (Channels WS)
- Admin: http://localhost:8005/119115131318115/

## Deploy
- Git push to main: Render/Vercel auto-deploy via render.yaml.
- Render: Services/DB/Redis free tier.
- Vercel: `frontend/` dir.

## Tech
FastAPI/Django5/HTMX/Alpine/Postgres/Redis/gRPC/Celery/Graphene.

See prd-readable.txt for full spec.

