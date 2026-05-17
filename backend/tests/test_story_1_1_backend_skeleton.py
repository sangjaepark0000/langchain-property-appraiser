from pathlib import Path
import sys

import pytest


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_required_backend_project_files_and_directories_exist():
    required_paths = [
        BACKEND_ROOT / "pyproject.toml",
        BACKEND_ROOT / "app" / "main.py",
        BACKEND_ROOT / "app" / "api",
        BACKEND_ROOT / "app" / "core",
        BACKEND_ROOT / "app" / "db",
        BACKEND_ROOT / "app" / "models",
        BACKEND_ROOT / "app" / "schemas",
        BACKEND_ROOT / "app" / "ingestion",
        BACKEND_ROOT / "app" / "rag",
        BACKEND_ROOT / "app" / "graph",
        BACKEND_ROOT / "app" / "services",
        BACKEND_ROOT / "tests",
    ]

    missing = [str(path.relative_to(REPO_ROOT)) for path in required_paths if not path.exists()]

    assert missing == []


def test_pyproject_declares_required_runtime_and_dependencies():
    pyproject = (BACKEND_ROOT / "pyproject.toml").read_text()

    assert 'requires-python = ">=3.12"' in pyproject
    for dependency in ["fastapi==0.136.1", "uvicorn[standard]==0.47.0", "langchain==1.3.1", "langgraph==1.2.0"]:
        assert dependency in pyproject


def test_backend_readme_documents_setup_and_no_credential_startup():
    readme = (BACKEND_ROOT / "README.md").read_text()

    for expected_text in ["Python 3.12", "Python 3.13", "uvicorn app.main:app", "pytest", "Credentials Are Not Required"]:
        assert expected_text in readme


def test_fastapi_app_imports_without_external_credentials(monkeypatch):
    for key in [
        "DATABASE_URL",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "LANGSMITH_API_KEY",
        "LANGCHAIN_API_KEY",
    ]:
        monkeypatch.delenv(key, raising=False)

    from app.main import app

    assert app.title


def test_health_endpoint_succeeds_without_external_credentials(monkeypatch):
    for key in [
        "DATABASE_URL",
        "OPENAI_API_KEY",
        "ANTHROPIC_API_KEY",
        "LANGSMITH_API_KEY",
        "LANGCHAIN_API_KEY",
    ]:
        monkeypatch.delenv(key, raising=False)

    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient
    from app.main import app

    response = TestClient(app).get("/health")

    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "ok"
    assert payload["service"] == "langchain-property-appraiser-backend"
