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

## Run Tests

```bash
cd backend
source .venv/bin/activate
pytest
```

## Credentials Are Not Required for Local Startup

The app and health endpoint start without database credentials, LLM provider keys, embedding provider keys, or LangSmith configuration. Optional secrets belong only in local `.env` or environment variables, never in committed files.
