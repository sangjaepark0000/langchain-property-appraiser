from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.session import SessionLocal
from app.services.ingest_service import ingest_paths


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest markdown/txt files into the local knowledge base.")
    parser.add_argument("paths", nargs="+", help="Files to ingest")
    parser.add_argument("--data-mode", default="sample")
    parser.add_argument("--no-persist", action="store_true", help="Run loader/chunker/embedding without DB writes")
    args = parser.parse_args()

    session = None if args.no_persist else SessionLocal()
    try:
        result = ingest_paths(args.paths, data_mode=args.data_mode, persist=not args.no_persist, session=session)
    finally:
        if session is not None:
            session.close()

    print(f"status={result.status}")
    print(f"documents_processed={result.documents_processed}")
    print(f"chunks_processed={result.chunks_processed}")
    print(f"embeddings_generated={result.embeddings_generated}")
    if result.unsupported_files:
        print("unsupported_files=" + ",".join(result.unsupported_files))
    if result.failed_files:
        print("failed_files=" + ",".join(result.failed_files))
    for summary in result.source_summaries.values():
        line = (
            f"source={summary.source_path} status={summary.status} "
            f"documents={summary.document_count} chunks={summary.chunk_count}"
        )
        if summary.failure_reason:
            line += f" reason={summary.failure_reason}"
        print(line)
    return 0 if result.items else 1


if __name__ == "__main__":
    raise SystemExit(main())
