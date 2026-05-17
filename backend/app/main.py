from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.core.config import get_settings


SERVICE_NAME = "langchain-property-appraiser-backend"
settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Local-first FastAPI backend foundation for RAG development.",
)
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Request validation failed.",
                "details": exc.errors(),
            }
        },
    )


@app.get("/health", tags=["health"])
def health_check() -> dict[str, str]:
    """Return a minimal liveness response with no external dependencies."""
    return {"status": "ok", "service": SERVICE_NAME}
