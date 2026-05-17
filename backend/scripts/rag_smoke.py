from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent


def run_command(command: list[str], *, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=BACKEND_ROOT, env=env, text=True, capture_output=True, timeout=30)


def assert_pass(condition: bool, name: str, detail: str = "") -> None:
    if not condition:
        raise AssertionError(f"{name} failed: {detail}")
    print(f"{name}=pass")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run local RAG API/CLI smoke checks without external keys using sqlite and fallback providers."
    )
    parser.add_argument("--database-url", default="sqlite+pysqlite:///./rag-smoke.db")
    args = parser.parse_args()

    env = {**os.environ, "DATABASE_URL": args.database_url}
    sample_alpha = PROJECT_ROOT / "sample_data" / "sample-property-alpha.md"

    ingest = run_command([sys.executable, "scripts/ingest_file.py", str(sample_alpha)], env=env)
    assert_pass(ingest.returncode == 0 and "documents_processed=1" in ingest.stdout, "sample_ingestion", ingest.stderr)

    cli_query = run_command([sys.executable, "scripts/rag_query.py", "Fictional Parcel Alpha", "--debug"], env=env)
    assert_pass(
        cli_query.returncode == 0
        and "answer=" in cli_query.stdout
        and "citations=" in cli_query.stdout
        and "retrieved_count=" in cli_query.stdout,
        "cli_query",
        cli_query.stderr,
    )

    api_check = run_command(
        [
            sys.executable,
            "-c",
            "from fastapi.testclient import TestClient; from app.main import app; "
            "c=TestClient(app); r=c.post('/query', json={'question':'Fictional Parcel Alpha'}); "
            "b=r.json(); assert r.status_code==200; "
            "assert 'answer' in b and 'citations' in b and 'data_mode' in b and 'insufficient_evidence' in b; "
            "print('api_contract_fields=ok')",
        ],
        env=env,
    )
    assert_pass(api_check.returncode == 0 and "api_contract_fields=ok" in api_check.stdout, "api_contract", api_check.stderr)

    no_evidence = run_command([sys.executable, "scripts/rag_query.py", "What official law article applies to Gamma?"], env=env)
    assert_pass(
        no_evidence.returncode == 0 and "official data is not available" in no_evidence.stdout.lower(),
        "no_evidence",
        no_evidence.stderr,
    )
    assert_pass("law.go.kr" not in no_evidence.stdout.lower() and "article 1" not in no_evidence.stdout.lower(), "official_hallucination")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
