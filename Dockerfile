# -----------------------------
# Stage 1: Dependency Builder
# -----------------------------
FROM python:3.12-slim AS builder

WORKDIR /app

COPY requirements-docker.txt .

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --prefix=/install -r requirements-docker.txt


# -----------------------------
# Stage 2: Runtime
# -----------------------------
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

COPY --from=builder /install /usr/local

COPY api/ api/
COPY rag/ rag/
COPY crew_ai/ crew_ai/
COPY data/ data/

EXPOSE 8000

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]

