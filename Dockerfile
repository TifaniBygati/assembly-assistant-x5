FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

FROM base AS tests

COPY app ./app
COPY tests ./tests
COPY scripts ./scripts
COPY alembic ./alembic
COPY alembic.ini .

CMD ["pytest"]

FROM base AS app

COPY README.md .
COPY app ./app
COPY alembic ./alembic
COPY alembic.ini .

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

FROM app AS prod

COPY scripts ./scripts
COPY seed ./seed
