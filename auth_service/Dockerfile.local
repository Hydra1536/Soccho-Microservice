# Multi-stage build for auth service
FROM python:3.12-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY auth_service/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies only (no build tools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN useradd -m -u 1000 soccho && chown -R soccho:soccho /app

# Copy Python dependencies from builder
COPY --from=builder --chown=soccho:soccho /root/.local /home/soccho/.local

# Copy application code
COPY --chown=soccho:soccho auth_service/ /app/auth_service/
COPY --chown=soccho:soccho shared/ /app/shared/

# Set environment
ENV PATH=/home/soccho/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER soccho

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" || exit 1

EXPOSE 8000

# Run migrations and start server
CMD ["sh", "-c", "python manage.py migrate && gunicorn auth_service.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2 --worker-class sync --timeout 60"]
