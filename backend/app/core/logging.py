import logging
import sys
from typing import Any

from app.core.config import Settings


def redact_secret(value: str | None) -> str:
    if value is None:
        return "[not-set]"
    if value == "":
        return "[empty]"
    return "[redacted]"


def configure_logging(settings: Settings) -> None:
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper(), logging.INFO),
        format="%(levelname)s [%(name)s] %(message)s",
        stream=sys.stdout,
        force=True,
    )


def safe_settings_summary(settings: Settings) -> dict[str, Any]:
    return settings.public_summary()


def log_startup_summary(settings: Settings) -> None:
    logger = logging.getLogger("app.startup")
    summary = safe_settings_summary(settings)
    logger.info("startup configuration summary: %s", summary)
