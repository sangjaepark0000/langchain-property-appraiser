from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.chunk import Chunk  # noqa: F401 - ensure table registration for CLI create_all
from app.models.document import Document  # noqa: F401 - ensure table registration for CLI create_all
from app.rag.query import answer_question


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a single local RAG question against ingested chunks.")
    parser.add_argument("question")
    parser.add_argument("--limit", type=int, default=5)
    parser.add_argument("--debug", "--verbose", action="store_true", dest="debug")
    args = parser.parse_args()

    Base.metadata.create_all(engine)
    with SessionLocal() as session:
        result = answer_question(session, args.question, limit=args.limit)

    print(f"status={result.answer.status}")
    print(f"answer={result.answer.answer}")
    print(f"citations={len(result.answer.citations)}")
    for citation in result.answer.citations:
        print(
            "citation="
            + f"source_path={citation.get('source_path', 'unknown')} "
            + f"chunk_index={citation.get('chunk_index', 'unknown')} "
            + f"data_mode={citation.get('data_mode', 'unknown')}"
        )
    if args.debug:
        print(f"query={result.question}")
        print(f"retrieved_count={result.retrieved_count}")
        print(f"fallback={result.answer.fallback}")
        print(f"provider={result.answer.provider}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
