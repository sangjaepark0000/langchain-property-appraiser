from __future__ import annotations

import logging
import sys
from pathlib import Path

from fastapi.testclient import TestClient

# Allow `python scripts/smoke.py` from backend/ without package installation edge cases.
BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import get_settings
from app.core.logging import configure_logging, log_startup_summary, safe_settings_summary
from app.main import app


def main() -> int:
    settings = get_settings()
    configure_logging(settings)
    logger = logging.getLogger("app.smoke")

    logger.info("FastAPI app import: ok")
    log_startup_summary(settings)

    response = TestClient(app).get("/health")
    if response.status_code != 200:
        logger.error("health endpoint failed: status=%s body=%s", response.status_code, response.text)
        return 1

    summary = safe_settings_summary(settings)
    logger.info("health endpoint: ok")
    logger.info("configuration summary: %s", summary)
    logger.info("database_configured: %s", summary["database_configured"])
    logger.info("langsmith_tracing_enabled: %s", summary["langsmith_tracing_enabled"])
    logger.info("optional provider keys are not required for this smoke check")
    print("Smoke check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
