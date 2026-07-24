FROM python:3.11-slim AS base

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --no-cache-dir -r requirements.txt

FROM base AS tests

COPY app ./app
COPY tests ./tests
COPY scripts ./scripts

CMD ["pytest"]

FROM base AS app

COPY README.md .
COPY app ./app

CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
