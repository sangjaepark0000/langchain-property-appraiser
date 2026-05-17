from __future__ import annotations

import argparse
import sys

import psycopg

from app.core.config import get_settings


def normalize_database_url(url: str) -> str:
    """Convert SQLAlchemy-style psycopg URLs to psycopg connection URLs."""
    return url.replace("postgresql+psycopg://", "postgresql://", 1)


def check_database(database_url: str) -> tuple[bool, str]:
    try:
        with psycopg.connect(normalize_database_url(database_url), connect_timeout=5) as conn:
            with conn.cursor() as cursor:
                cursor.execute("CREATE EXTENSION IF NOT EXISTS vector")
                cursor.execute("SELECT extversion FROM pg_extension WHERE extname = 'vector'")
                row = cursor.fetchone()
        if not row:
            return False, "Connected to PostgreSQL, but pgvector extension was not available."
        return True, f"Connected to PostgreSQL and pgvector is available (version: {row[0]})."
    except Exception as exc:  # pragma: no cover - exact driver errors vary by platform
        return (
            False,
            "Database connectivity check failed. "
            "Ensure Docker is running, start the local database with `docker compose up -d db`, "
            "and verify DATABASE_URL matches .env.example. "
            f"Original error: {exc}",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local PostgreSQL + pgvector connectivity.")
    parser.add_argument("--database-url", help="Override DATABASE_URL for this check.")
    args = parser.parse_args()

    database_url = args.database_url or get_settings().database_url
    if not database_url:
        print(
            "Database connectivity check failed. DATABASE_URL is not configured. "
            "Copy .env.example to .env or pass --database-url.",
            file=sys.stderr,
        )
        return 1

    ok, message = check_database(database_url)
    print(message, file=sys.stdout if ok else sys.stderr)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
