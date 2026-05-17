from functools import lru_cache

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Typed application settings loaded from environment variables and .env."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = Field(default="langchain-property-appraiser", alias="APP_NAME")
    app_env: str = Field(default="local", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    database_url: str | None = Field(
        default="postgresql+psycopg://app:app@localhost:5432/langchain_property_appraiser",
        alias="DATABASE_URL",
    )

    llm_provider: str = Field(default="none", alias="LLM_PROVIDER")
    llm_api_key: str | None = Field(default=None, alias="LLM_API_KEY")

    embedding_provider: str = Field(default="none", alias="EMBEDDING_PROVIDER")
    embedding_api_key: str | None = Field(default=None, alias="EMBEDDING_API_KEY")

    langsmith_tracing: bool = Field(default=False, alias="LANGSMITH_TRACING")
    langsmith_api_key: str | None = Field(default=None, alias="LANGSMITH_API_KEY")
    langsmith_project: str | None = Field(default=None, alias="LANGSMITH_PROJECT")

    @computed_field
    @property
    def has_llm_api_key(self) -> bool:
        return bool(self.llm_api_key)

    @computed_field
    @property
    def has_embedding_api_key(self) -> bool:
        return bool(self.embedding_api_key)

    @computed_field
    @property
    def langsmith_tracing_enabled(self) -> bool:
        return self.langsmith_tracing and bool(self.langsmith_api_key)

    def public_summary(self) -> dict[str, str | bool | None]:
        """Return non-secret diagnostic settings safe for health/debug output."""
        return {
            "app_name": self.app_name,
            "app_env": self.app_env,
            "log_level": self.log_level,
            "database_configured": bool(self.database_url),
            "llm_provider": self.llm_provider,
            "has_llm_api_key": self.has_llm_api_key,
            "embedding_provider": self.embedding_provider,
            "has_embedding_api_key": self.has_embedding_api_key,
            "langsmith_tracing_enabled": self.langsmith_tracing_enabled,
            "langsmith_project": self.langsmith_project,
        }


@lru_cache
def get_settings() -> Settings:
    return Settings()
