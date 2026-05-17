from fastapi import FastAPI

from app.core.config import get_settings


SERVICE_NAME = "langchain-property-appraiser-backend"
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Local-first FastAPI backend foundation for RAG development.",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a minimal liveness response with no external dependencies."""
    return {"status": "ok", "service": SERVICE_NAME}
