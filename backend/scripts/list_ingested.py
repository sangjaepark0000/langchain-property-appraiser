from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.session import SessionLocal
from app.models.chunk import Chunk
from app.models.document import Document


def main() -> int:
    parser = argparse.ArgumentParser(description="List ingested documents/chunks for local debugging.")
    parser.add_argument("--no-db", action="store_true", help="Skip DB inspection")
    args = parser.parse_args()
    if args.no_db:
        print("DB inspection skipped")
        return 0

    with SessionLocal() as session:
        documents = session.query(Document).all()
        print(f"documents={len(documents)}")
        for document in documents:
            chunk_count = session.query(Chunk).filter(Chunk.document_id == document.id).count()
            print(
                f"document id={document.id} source_name={document.source_name} "
                f"data_mode={document.data_mode} chunks={chunk_count}"
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
