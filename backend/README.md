# Backend Setup

This backend is the FastAPI-first foundation for `langchain-property-appraiser`.

## Python Version

Use Python 3.12 or 3.13 for day-to-day development. The architecture notes that these versions are safer for current FastAPI, LangChain, and LangGraph package compatibility than a bleeding-edge local interpreter.

The package metadata allows Python `>=3.12` so local tooling can still inspect and run tests where dependencies support the interpreter.

## Create Environment

```bash
cd backend
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
```

If your machine does not have `python3.12`, use Python 3.13.

## Environment Configuration

Copy the committed example file before local customization:

```bash
cp ../.env.example .env
```

`.env` is for local values only and must not be committed. Provider keys are optional for local startup. If LangSmith variables are absent, tracing remains disabled and local logging remains the baseline observability path.

## Run the API Locally

```bash
cd backend
source .venv/bin/activate
uvicorn app.main:app --reload
```

Health check:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok","service":"langchain-property-appraiser-backend"}
```

## Local PostgreSQL + pgvector

Start the local database from the repository root:

```bash
docker compose up -d db
```

Check status and logs:

```bash
docker compose ps
docker compose logs db
```

Verify backend connectivity and pgvector support:

```bash
cd backend
source .venv/bin/activate
python scripts/check_db.py
```

Stop the database while keeping local data:

```bash
docker compose stop db
```

Reset local database state, including the persistent volume:

```bash
docker compose down -v
docker compose up -d db
```

The local compose defaults match `../.env.example`:

```text
DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/langchain_property_appraiser
```

## Database Migrations

After starting the local database, run the baseline migration from `backend/`:

```bash
cd backend
source .venv/bin/activate
python -m alembic -c alembic.ini upgrade head
```

The initial baseline migration intentionally creates no domain tables. It only establishes Alembic version tracking so later stories can add controlled migrations.

After resetting local database state:

```bash
docker compose down -v
docker compose up -d db
cd backend
python -m alembic -c alembic.ini upgrade head
```

## Run Tests

```bash
cd backend
source .venv/bin/activate
pytest
```

## Credentials Are Not Required for Local Startup

The app and health endpoint start without database credentials, LLM provider keys, embedding provider keys, or LangSmith configuration. Optional secrets belong only in local `.env` or environment variables, never in committed files.
