from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = BACKEND_ROOT.parent
OFFICIAL_FIXTURE = BACKEND_ROOT / "tests" / "fixtures" / "official_law" / "sample_law.xml"
INVALID_FIXTURE = BACKEND_ROOT / "tests" / "fixtures" / "official_law" / "invalid_shape.xml"
SAMPLE_FIXTURE = PROJECT_ROOT / "sample_data" / "sample-property-alpha.md"


def run(command: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=BACKEND_ROOT, env=env, text=True, capture_output=True, timeout=45)


def require(condition: bool, name: str, detail: str = "") -> None:
    if not condition:
        raise AssertionError(f"{name} failed: {detail}")
    print(f"{name}=pass")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run official ingestion smoke using a local official XML fixture; live API is not required.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--database-url", default="sqlite+pysqlite:///./official-ingestion-smoke.db")
    args = parser.parse_args()
    env = {**os.environ, "DATABASE_URL": args.database_url, "LANGSMITH_TRACING": "false"}

    smoke_code = f'''
from app.db.base import Base
from app.db.session import SessionLocal, engine
from app.models.chunk import Chunk
from app.models.document import Document
from app.services.ingest_service import ingest_paths

Base.metadata.create_all(bind=engine)
with SessionLocal() as session:
    official = ingest_paths([{str(OFFICIAL_FIXTURE)!r}], data_mode='official', persist=True, session=session)
    assert official.status == 'success', official.to_summary_dict()
    invalid = ingest_paths([{str(INVALID_FIXTURE)!r}], data_mode='official', persist=True, session=session)
    assert invalid.status == 'failed', invalid.to_summary_dict()
    sample = ingest_paths([{str(SAMPLE_FIXTURE)!r}], data_mode='sample', persist=True, session=session)
    assert sample.status == 'success', sample.to_summary_dict()
    official_doc = session.query(Document).filter(Document.data_mode == 'official').one()
    sample_doc = session.query(Document).filter(Document.data_mode == 'sample').one()
    assert official_doc.ingestion_status == 'ingested'
    assert official_doc.metadata_['domain_metadata']['source_authority'] == '국가법령정보센터'
    assert official_doc.metadata_['domain_metadata']['source_url'] == 'https://open.law.go.kr/sample/law'
    assert sample_doc.metadata_.get('domain_metadata') is None
    official_chunk = session.query(Chunk).filter(Chunk.document_id == official_doc.id).first()
    assert official_chunk is not None
    assert official_chunk.metadata_['data_mode'] == 'official'
    assert official_chunk.metadata_['domain_metadata']['article_number'] == '제1조'
    assert official_chunk.source_lineage['source_id'] == 'official-law-open-api'
    assert session.query(Document).count() == 2
print('official_document=pass')
print('domain_metadata=pass')
print('official_data_mode=pass')
print('failed_source_not_ingested=pass')
print('sample_official_separation=pass')
print('source_lineage=pass')
print('live_api=not_required')
'''
    smoke = run([sys.executable, "-c", smoke_code], env)
    if smoke.returncode != 0:
        raise AssertionError(smoke.stderr)
    print(smoke.stdout, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
