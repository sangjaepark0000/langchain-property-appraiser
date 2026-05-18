from __future__ import annotations

import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.core.config import get_settings


def main() -> int:
    settings = get_settings()
    if not settings.langsmith_tracing_enabled:
        print("status=skipped reason=LANGSMITH_TRACING is false or LANGSMITH_API_KEY is missing")
        return 1

    from langsmith import Client, traceable

    @traceable(name="LangSmith Connectivity Smoke", run_type="chain")
    def smoke_trace() -> dict[str, str]:
        return {"status": "ok", "project": settings.langsmith_project or "unknown"}

    result = smoke_trace()
    client = Client()
    client.flush()
    print("status=success")
    print(f"project={settings.langsmith_project}")
    print(f"result={result['status']}")
    print("Check LangSmith for run: LangSmith Connectivity Smoke")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
