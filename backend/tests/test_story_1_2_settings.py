from pathlib import Path
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_settings_load_with_minimal_environment(monkeypatch):
    for key in [
        "APP_NAME",
        "APP_ENV",
        "DATABASE_URL",
        "LLM_PROVIDER",
        "LLM_API_KEY",
        "EMBEDDING_PROVIDER",
        "EMBEDDING_API_KEY",
        "LANGSMITH_TRACING",
        "LANGSMITH_API_KEY",
        "LANGSMITH_PROJECT",
    ]:
        monkeypatch.delenv(key, raising=False)

    from app.core.config import Settings

    settings = Settings()

    assert settings.app_name == "langchain-property-appraiser"
    assert settings.langsmith_tracing_enabled is False
    assert settings.has_llm_api_key is False
    assert settings.has_embedding_api_key is False


def test_settings_support_environment_overrides(monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("LLM_PROVIDER", "openai")

    from app.core.config import Settings

    settings = Settings()

    assert settings.app_env == "test"
    assert settings.log_level == "DEBUG"
    assert settings.llm_provider == "openai"


def test_langsmith_tracing_requires_api_key(monkeypatch):
    monkeypatch.setenv("LANGSMITH_TRACING", "true")
    monkeypatch.delenv("LANGSMITH_API_KEY", raising=False)

    from app.core.config import Settings

    settings = Settings()

    assert settings.langsmith_tracing is True
    assert settings.langsmith_tracing_enabled is False


def test_env_example_documents_required_settings_without_real_secrets():
    env_example = (REPO_ROOT / ".env.example").read_text()

    required_keys = [
        "APP_NAME=",
        "APP_ENV=",
        "DATABASE_URL=",
        "LLM_PROVIDER=",
        "LLM_API_KEY=",
        "EMBEDDING_PROVIDER=",
        "EMBEDDING_API_KEY=",
        "LANGSMITH_TRACING=",
        "LANGSMITH_API_KEY=",
        "LANGSMITH_PROJECT=",
        "LOG_LEVEL=",
    ]
    for key in required_keys:
        assert key in env_example

    forbidden_secret_fragments = ["sk-", "ghp_", "gho_", "xoxb-", "BEGIN PRIVATE KEY"]
    for fragment in forbidden_secret_fragments:
        assert fragment not in env_example
