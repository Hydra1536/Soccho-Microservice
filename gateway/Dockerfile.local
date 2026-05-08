# Multi-stage build for FastAPI gateway
FROM python:3.12-slim as builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY gateway/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Final stage
FROM python:3.12-slim

WORKDIR /app

RUN useradd -m -u 1000 soccho && chown -R soccho:soccho /app

COPY --from=builder --chown=soccho:soccho /root/.local /home/soccho/.local
COPY --chown=soccho:soccho gateway/ /app/gateway/
COPY --chown=soccho:soccho shared/ /app/shared/

ENV PATH=/home/soccho/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER soccho

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import httpx; httpx.get('http://localhost:8000/health', timeout=2)" || exit 1

EXPOSE 8000

CMD ["uvicorn", "gateway.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]
