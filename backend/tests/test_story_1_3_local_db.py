from pathlib import Path
import subprocess
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_docker_compose_defines_postgres_pgvector_service():
    compose = (REPO_ROOT / "docker-compose.yml").read_text()

    assert "pgvector/pgvector" in compose
    assert "POSTGRES_DB: langchain_property_appraiser" in compose
    assert "POSTGRES_USER: app" in compose
    assert "POSTGRES_PASSWORD: app" in compose
    assert '"5432:5432"' in compose or "5432:5432" in compose
    assert "postgres_data:" in compose
    assert "docker/postgres/init" in compose


def test_pgvector_init_sql_creates_vector_extension():
    init_sql = (REPO_ROOT / "docker" / "postgres" / "init" / "01-create-vector-extension.sql").read_text()

    assert "CREATE EXTENSION IF NOT EXISTS vector" in init_sql


def test_env_example_database_url_matches_compose_defaults():
    env_example = (REPO_ROOT / ".env.example").read_text()

    assert "DATABASE_URL=postgresql+psycopg://app:app@localhost:5432/langchain_property_appraiser" in env_example


def test_database_check_reports_clear_error_for_unavailable_database():
    result = subprocess.run(
        [
            sys.executable,
            str(BACKEND_ROOT / "scripts" / "check_db.py"),
            "--database-url",
            "postgresql+psycopg://app:app@127.0.0.1:1/langchain_property_appraiser",
        ],
        text=True,
        capture_output=True,
        timeout=10,
    )

    assert result.returncode != 0
    combined_output = result.stdout + result.stderr
    assert "Database connectivity check failed" in combined_output
    assert "docker compose up -d db" in combined_output
