from __future__ import annotations

import argparse
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.ingestion.chunker import chunk_document
from app.ingestion.official_sources import load_normalized_official_source
from app.rag.embeddings import embed_texts
from app.services.ingest_service import IngestedItem, persist_ingested_item


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest normalized official appraisal law sources.")
    parser.add_argument(
        "--source-root",
        default=str(PROJECT_ROOT / "official_sources" / "normalized"),
        help="Folder containing */extracted.txt and */source-notes.md",
    )
    parser.add_argument("--no-persist", action="store_true")
    args = parser.parse_args()

    source_root = Path(args.source_root)
    source_dirs = sorted(path for path in source_root.iterdir() if path.is_dir() and (path / "extracted.txt").exists())
    if not source_dirs:
        print(f"status=failed reason=no_normalized_sources source_root={source_root}")
        return 1

    if not args.no_persist:
        Base.metadata.create_all(engine)
    session = None if args.no_persist else SessionLocal()
    documents = 0
    chunks_count = 0
    try:
        for source_dir in source_dirs:
            document = load_normalized_official_source(source_dir)
            chunks = chunk_document(document)
            embeddings = embed_texts([chunk.text for chunk in chunks])
            item = IngestedItem(document=document, chunks=chunks, embeddings=embeddings)
            if session is not None:
                persist_ingested_item(item, session)
            documents += 1
            chunks_count += len(chunks)
            print(
                f"source={source_dir.name} status=ingested data_mode={document.data_mode} "
                f"chunks={len(chunks)} document_kind={document.metadata.get('document_kind')}"
            )
        if session is not None:
            session.commit()
    finally:
        if session is not None:
            session.close()

    print("status=success")
    print(f"documents_processed={documents}")
    print(f"chunks_processed={chunks_count}")
    print("data_mode=official")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
