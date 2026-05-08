# Soccho - Friend Money Ledger Application

A privacy-first microservices application for tracking money lent and borrowed among friends. Built with FastAPI, Django, PostgreSQL, Redis, and WebSockets.

## 🎯 Features

### Authentication
- Email + password registration with OTP verification
- Google OAuth2 integration
- Forgot password with OTP reset flow
- JWT-based authentication (1hr access, 12hr refresh)
- Rate limiting: 100 login attempts/hour per IP
- Throttling: 1-hour cooldown after limit

### Social
- Friend search with fuzzy matching
- Friend suggestions based on loyalty score
- Friend requests: send, pending, accept, reject
- Cursor-based pagination (keyset)
- Loyalty score: `(total_given - total_lent) / total_transactions`
- Loyalty visible only to user (private)

### Transactions
- Ledger-based: every give/lend is a transaction entry
- Net balance per friendship: auto-calculated
- Optional due dates per transaction
- Confirmation flow: lender → borrower → confirm/deny
- Idempotency keys: prevent duplicate submissions
- Soft deletes: 30-day retention, then purged
- GraphQL queries for complex searches

### Notifications
- Real-time WebSocket notifications via Django Channels
- 3 notification types:
  1. Pending lend confirmation (with Agree/Disagree)
  2. Payment received acknowledgment
  3. Due date reminders (on every login until cleared)
- Offline support: Service Worker + IndexedDB
- Background sync when reconnected

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.12+

### Local Development

1. **Clone and setup**
```bash
git clone https://github.com/Hydra1536/Soccho-Microservice.git
cd Soccho-Microservice
cp .env.example .env
```

2. **Generate secrets**
```bash
python -c "import secrets; print('AES_SECRET_KEY=' + secrets.token_bytes(32).hex())"
```

3. **Start all services**
```bash
docker-compose up -d
```

4. **Run migrations**
```bash
docker-compose exec auth python manage.py migrate
docker-compose exec social python manage.py migrate
docker-compose exec transaction python manage.py migrate
docker-compose exec notification python manage.py migrate
docker-compose exec admin python manage.py migrate
```

5. **Access services**
- Frontend: Open `frontend/index.html`
- API Docs: http://localhost:8000/api/docs
- Admin Panel: http://localhost:8005/119115131318115/

## 📦 Tech Stack

| Component | Tech | Port |
|-----------|------|------|
| API Gateway | FastAPI | 8000 |
| Auth Service | Django Ninja | 8001 |
| Social Service | Django REST | 8002 |
| Transaction Service | Django REST | 8003 |
| Notification Service | Django Channels | 8004 |
| Admin Service | Django Admin | 8005 |
| Frontend | HTMX + Alpine.js | Vercel |
| Database | PostgreSQL 16 | Render |
| Cache/Queue | Redis 7 | Render |

## 🔒 Security Features

- **Encryption**: AES-256 for financial data
- **Authentication**: JWT (1hr access, 12hr refresh)
- **OTP**: 6-digit, 10-minute expiry (FormSubmit.co)
- **Rate Limiting**: 100 attempts/hour per IP
- **CORS**: Whitelisted to soccho.vercel.app
- **Security Headers**: CSP, HSTS, X-Frame-Options, etc.
- **Admin**: Non-guessable path `/119115131318115/`

## 🏗️ Architecture

- **Microservices**: Independent services per domain
- **gRPC**: Inter-service communication
- **GraphQL**: Complex queries on Social & Transaction
- **WebSocket**: Real-time notifications
- **Async**: Celery tasks for background jobs
- **Caching**: Redis for performance
- **Database**: PostgreSQL with full-text search

## 📚 Documentation

- [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) - Deploy to Render + Vercel
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Pre-deployment checks
- [prd-readable.txt](prd-readable.txt) - Complete requirements spec

## 🚢 Deployment

### Backend (Render)
```bash
# Push to GitHub - Render auto-deploys via render.yaml
git push origin main
```

### Frontend (Vercel)
```bash
# Connect GitHub → Vercel, select `frontend/` folder
# Auto-deploys on push
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed setup.

## 📝 Environment Variables

```bash
# Generate strong secrets
python -c "import secrets; print('AES_SECRET_KEY=' + secrets.token_bytes(32).hex()); print('JWT_SECRET=' + secrets.token_urlsafe(50))"

# Copy to .env
AES_SECRET_KEY=<your_key>
DATABASE_URL=postgresql://user:pass@host/db
REDIS_URL=redis://host:6379
```

## 🧪 Testing

```bash
# Run tests (unit + integration)
pytest auth_service/
pytest social_service/
pytest transaction_service/
```

## 📈 Performance

- Cursor-based pagination (no OFFSET)
- Redis caching: friends (5min), loyalty (15min)
- Query optimization: select_related/prefetch_related
- O(log n) time complexity
- Circuit breaker on gRPC calls

## 🐛 Troubleshooting

**OTP not sending**: Check Render logs, verify FormSubmit.co is accessible
**WebSocket failed**: Verify Redis running, check Notification service logs
**DB connection error**: Check DATABASE_URL format, verify database exists

## 📄 License

MIT License

## 👥 Support

Issues & Questions: [GitHub Issues](https://github.com/Hydra1536/Soccho-Microservice/issues)

---

Built with ❤️ for tracking friendships and money

