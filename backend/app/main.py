from fastapi import FastAPI


SERVICE_NAME = "langchain-property-appraiser-backend"

app = FastAPI(
    title="LangChain Property Appraiser Backend",
    version="0.1.0",
    description="Local-first FastAPI backend foundation for RAG development.",
)


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a minimal liveness response with no external dependencies."""
    return {"status": "ok", "service": SERVICE_NAME}
