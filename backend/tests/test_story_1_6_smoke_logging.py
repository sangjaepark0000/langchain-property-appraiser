from pathlib import Path
import subprocess
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_logging_module_redacts_secret_values():
    from app.core.logging import redact_secret

    assert redact_secret("sentinel-secret-value") == "[redacted]"
    assert redact_secret("") == "[empty]"
    assert redact_secret(None) == "[not-set]"


def test_smoke_command_succeeds_without_provider_keys():
    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "smoke.py")],
        cwd=BACKEND_ROOT,
        env={
            "APP_ENV": "test",
            "LOG_LEVEL": "INFO",
            "LLM_API_KEY": "sentinel-llm-secret",
            "EMBEDDING_API_KEY": "sentinel-embedding-secret",
            "LANGSMITH_API_KEY": "sentinel-langsmith-secret",
        },
        text=True,
        capture_output=True,
        timeout=15,
    )

    output = result.stdout + result.stderr

    assert result.returncode == 0
    assert "Smoke check passed" in output
    assert "FastAPI app import" in output
    assert "health endpoint" in output
    assert "langsmith_tracing_enabled" in output
    assert "sentinel-llm-secret" not in output
    assert "sentinel-embedding-secret" not in output
    assert "sentinel-langsmith-secret" not in output


def test_backend_readme_documents_smoke_command():
    readme = (BACKEND_ROOT / "README.md").read_text()

    assert "Smoke Check" in readme
    assert "python scripts/smoke.py" in readme
    assert "LLM" in readme
    assert "embedding" in readme
