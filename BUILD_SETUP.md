# Build Configuration

## Render Deployment (Production)

Render uses `render.yaml` with native Python runtime. **No Dockerfiles used.**

- Build command: `pip install -r requirements.txt`
- Start command: `gunicorn` or `daphne`
- Environment: Managed by Render

## Local Development (Docker Compose)

For local development, use `docker-compose.yml` with Docker:

```bash
docker-compose up -d
```

**Note**: Service Dockerfiles are named `Dockerfile.local` to prevent Render from auto-detecting them. This ensures:
- ✅ Render uses native Python build (render.yaml)
- ✅ Local Docker Compose uses Dockerfile.local
- ✅ No conflicts between build strategies

## Files

| File | Purpose | Used By |
|------|---------|---------|
| `render.yaml` | Service definitions | Render (production) |
| `**/Dockerfile.local` | Container definitions | Docker Compose (local) |
| `docker-compose.yml` | Local stack orchestration | Local development |

## Why This Approach?

- **Render**: Simpler deployment, native Python runtime, fewer moving parts
- **Local**: Full Docker containers for production-like environment
- **No conflict**: Render ignores Dockerfile.local, uses render.yaml instead
