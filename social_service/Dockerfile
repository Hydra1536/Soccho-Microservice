# Multi-stage build for social service
FROM python:3.12-slim as builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY social_service/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 soccho && chown -R soccho:soccho /app

COPY --from=builder --chown=soccho:soccho /root/.local /home/soccho/.local
COPY --chown=soccho:soccho social_service/ /app/social_service/
COPY --chown=soccho:soccho shared/ /app/shared/

ENV PATH=/home/soccho/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER soccho

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import django; django.setup(); from django.db import connection; connection.ensure_connection()" || exit 1

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && gunicorn social_service.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 2 --worker-class sync --timeout 60"]
