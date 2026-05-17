from pathlib import Path
import re
import subprocess
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_sqlalchemy_and_alembic_dependencies_declared():
    pyproject = (BACKEND_ROOT / "pyproject.toml").read_text()

    assert "sqlalchemy" in pyproject.lower()
    assert "alembic" in pyproject.lower()


def test_db_foundation_modules_exist_and_use_settings():
    base = (BACKEND_ROOT / "app" / "db" / "base.py").read_text()
    session = (BACKEND_ROOT / "app" / "db" / "session.py").read_text()

    assert "DeclarativeBase" in base
    assert "create_engine" in session
    assert "get_settings" in session
    assert "database_url" in session


def test_alembic_configuration_uses_app_metadata_and_settings():
    alembic_ini = (BACKEND_ROOT / "alembic.ini").read_text()
    env_py = (BACKEND_ROOT / "alembic" / "env.py").read_text()

    assert "script_location = alembic" in alembic_ini
    assert "Base.metadata" in env_py
    assert "get_settings" in env_py
    assert "target_metadata" in env_py


def test_baseline_migration_does_not_create_domain_tables():
    versions = list((BACKEND_ROOT / "alembic" / "versions").glob("*.py"))
    assert versions, "Expected a baseline Alembic revision"

    migration_text = next(path.read_text() for path in versions if "baseline" in path.name)
    assert "create_table" not in migration_text
    assert "documents" not in migration_text
    assert "chunks" not in migration_text
    assert "conversations" not in migration_text
    assert "messages" not in migration_text
    assert "retrieval_traces" not in migration_text
    assert "source_inventory" not in migration_text


def test_alembic_upgrade_head_can_run_against_unavailable_db_with_clear_failure():
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "alembic",
            "-c",
            str(BACKEND_ROOT / "alembic.ini"),
            "upgrade",
            "head",
        ],
        cwd=BACKEND_ROOT,
        env={"DATABASE_URL": "postgresql+psycopg://app:app@127.0.0.1:1/langchain_property_appraiser"},
        text=True,
        capture_output=True,
        timeout=10,
    )

    assert result.returncode != 0
    assert re.search("connection|connect|refused|failed", result.stderr + result.stdout, re.IGNORECASE)
