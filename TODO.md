# Soccho Project TODO
Tracking progress based on approved plan to complete Soccho per PRD.

## Phase 1: Root/Setup (5 files)
- [x] Create .gitignore
- [x] Create .env.example (generate secrets: AES_KEY, DJANGO_SECRET_KEYs per service)
- [ ] Create .env.example (generate secrets: AES_KEY, DJANGO_SECRET_KEYs per service)
- [ ] Create render.yaml (adapt with provided DB/Redis/Google creds)
- [ ] Create README.md (setup/deploy instructions)
- [ ] Create requirements-dev.txt (local dev deps)

## Phase 2: Shared (4 files)
- [x] shared/proto/soccho.proto (gRPC defs)
- [x] shared/encryption.py (AES helpers)
- [x] shared/pagination.py (cursor paginator)
- [x] shared/exceptions.py

**Progress: Phase 2 complete. Starting Phase 3: Frontend.**

## Phase 3: Frontend (~20 files)
- [x] frontend/vercel.json
- [x] frontend HTML pages: index.html (login), register.html, otp.html, forgot-password.html, home.html, profile.html, friendship.html, find-friends.html, 404.html (core pages complete, placeholders ready)
- [x] frontend/static/css: main.css, mobile.css, animations.css (design tokens, 3D cards, mobile-first)
- [x] frontend/static/js: app.js, charts.js (Chart.js), sw.js (Service Worker), offline.js (IndexedDB)
- [x] frontend/manifest.json (PWA)

**Progress: Phase 3 complete. Starting Phase 4: Gateway (FastAPI).**

## Phase 4: Gateway (FastAPI, 15 files)
- [ ] gateway/main.py, routers/auth/social/transaction/notification.py
- [ ] gateway/grpc_clients/auth/social/notification_client.py
- [ ] gateway/middleware/jwt.py, rate_limit.py, cors.py
- [ ] gateway/requirements.txt

## Phase 5: Django Services (~60 files)
### 5.1 Auth Service (Django Ninja)
- [ ] auth_service/manage.py, auth_service/settings.py/urls.py
- [ ] auth_service/users/models.py/api.py/grpc_server.py/schemas.py/utils.py/tasks.py
- [ ] auth_service/requirements.txt

### 5.2 Social Service (DRF + Graphene)
- [ ] social_service/manage.py, social_service/settings.py/urls.py
- [ ] social_service/friends/models.py/serializers.py/viewsets.py/routers.py/pagination.py/search.py/loyalty.py/search_history.py
- [ ] social_service/graphql/schema.py/types.py/resolvers.py
- [ ] social_service/requirements.txt

### 5.3 Transaction Service (DRF + Graphene + Celery)
- [ ] transaction_service/manage.py, transaction_service/settings.py/urls.py/celery.py
- [ ] transaction_service/transactions/models.py/serializers.py/viewsets.py/routers.py/idempotency.py/balance.py/pagination.py/tasks.py
- [ ] transaction_service/graphql/schema.py/types.py/resolvers.py
- [ ] transaction_service/requirements.txt

### 5.4 Notification Service (Channels)
- [ ] notification_service/manage.py, notification_service/settings.py/urls.py/asgi.py
- [ ] notification_service/notifications/models.py/serializers.py/consumers.py/routing.py/grpc_server.py/viewsets.py/tasks.py
- [ ] notification_service/requirements.txt

### 5.5 Admin Service
- [ ] admin_service/manage.py, admin_service/settings.py/urls.py
- [ ] admin_service/portal/models.py/admin.py (hidden /119115131318115/)
- [ ] admin_service/requirements.txt

## Phase 6: Local Dev & docker-compose.yml
- [ ] docker-compose.yml (Postgres/Redis/services for local)

## Phase 7: Testing & Deploy
- [ ] Local setup: venvs, pip install, migrations, docker-compose up, test endpoints
- [ ] Git init/add/commit/push to https://github.com/Hydra1536/Soccho-Microservice
- [ ] Render/Vercel deploy (auto via render.yaml/git), verify

**Progress: Starting Phase 1**

Last updated: Initial creation

