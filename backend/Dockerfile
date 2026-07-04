# ---- Build Stage ----
FROM python:3.11-slim AS builder

WORKDIR /app

# Install system deps for psycopg2-binary
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ---- Runtime Stage ----
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy app code
COPY . .

# Render provides PORT env var
ENV PORT=8000
EXPOSE ${PORT}

# Start uvicorn — bind to 0.0.0.0 so Render can route traffic
CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT}
