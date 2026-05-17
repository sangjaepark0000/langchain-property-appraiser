from pathlib import Path
import sys


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_ingestion_service_processes_supported_and_unsupported_files(tmp_path):
    (tmp_path / "a.md").write_text("# A\nhello", encoding="utf-8")
    (tmp_path / "b.txt").write_text("plain", encoding="utf-8")
    (tmp_path / "c.pdf").write_bytes(b"pdf")

    from app.services.ingest_service import ingest_paths

    result = ingest_paths([tmp_path / "a.md", tmp_path / "b.txt", tmp_path / "c.pdf"], persist=False)

    assert result.documents_processed == 2
    assert result.chunks_processed == 2
    assert result.embeddings_generated == 2
    assert len(result.unsupported_files) == 1
    assert result.unsupported_files[0].endswith("c.pdf")
    assert result.status == "partial_success"


def test_ingestion_result_contains_lineage_and_data_mode(tmp_path):
    source = tmp_path / "sample.md"
    source.write_text("hello", encoding="utf-8")

    from app.services.ingest_service import ingest_paths

    result = ingest_paths([source], data_mode="sample", persist=False)

    chunk = result.items[0].chunks[0]
    assert chunk.metadata["data_mode"] == "sample"
    assert chunk.lineage["source_path"] == str(source)
    assert result.items[0].document.data_mode == "sample"


def test_cli_smoke_outputs_summary_without_db_requirement(tmp_path):
    source = tmp_path / "sample.md"
    source.write_text("hello", encoding="utf-8")

    import subprocess

    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "ingest_file.py"), str(source), "--no-persist"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=15,
    )

    assert result.returncode == 0
    assert "documents_processed=1" in result.stdout
    assert "chunks_processed=1" in result.stdout
    assert "embeddings_generated=1" in result.stdout


def test_debug_list_command_runs_without_db_when_no_persist_mode():
    import subprocess

    result = subprocess.run(
        [sys.executable, str(BACKEND_ROOT / "scripts" / "list_ingested.py"), "--no-db"],
        cwd=BACKEND_ROOT,
        text=True,
        capture_output=True,
        timeout=15,
    )

    assert result.returncode == 0
    assert "DB inspection skipped" in result.stdout
