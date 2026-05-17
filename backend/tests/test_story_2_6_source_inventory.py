from pathlib import Path


def test_source_inventory_summary_marks_ingested_and_unsupported(tmp_path):
    supported = tmp_path / "ok.md"
    unsupported = tmp_path / "bad.pdf"
    supported.write_text("hello", encoding="utf-8")
    unsupported.write_bytes(b"pdf")

    from app.services.ingest_service import ingest_paths

    result = ingest_paths([supported, unsupported], persist=False)

    assert result.source_summaries[str(supported)].status == "ingested"
    assert result.source_summaries[str(supported)].document_count == 1
    assert result.source_summaries[str(supported)].chunk_count == 1
    assert result.source_summaries[str(unsupported)].status == "unsupported"
    assert result.source_summaries[str(unsupported)].document_count == 0


def test_failed_source_is_not_reported_as_success(tmp_path):
    empty = tmp_path / "empty.md"
    empty.write_text("   ", encoding="utf-8")

    from app.services.ingest_service import ingest_paths

    result = ingest_paths([empty], persist=False)

    summary = result.source_summaries[str(empty)]
    assert summary.status == "failed"
    assert summary.document_count == 0
    assert summary.chunk_count == 0
    assert "empty" in (summary.failure_reason or "").lower()
    assert result.status == "failed"


def test_source_summary_can_be_exported_as_dict(tmp_path):
    supported = tmp_path / "ok.txt"
    supported.write_text("hello", encoding="utf-8")

    from app.services.ingest_service import ingest_paths

    result = ingest_paths([supported], persist=False)
    exported = result.to_summary_dict()

    assert exported["status"] == "success"
    assert exported["sources"][str(supported)]["status"] == "ingested"
    assert exported["sources"][str(supported)]["document_count"] == 1
    assert exported["sources"][str(supported)]["chunk_count"] == 1


def test_cli_prints_source_level_summary(tmp_path):
    supported = tmp_path / "ok.md"
    unsupported = tmp_path / "bad.pdf"
    supported.write_text("hello", encoding="utf-8")
    unsupported.write_bytes(b"pdf")

    import subprocess
    import sys

    backend_root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        [
            sys.executable,
            str(backend_root / "scripts" / "ingest_file.py"),
            str(supported),
            str(unsupported),
            "--no-persist",
        ],
        cwd=backend_root,
        text=True,
        capture_output=True,
        timeout=15,
    )

    assert result.returncode == 0
    assert f"source={supported} status=ingested documents=1 chunks=1" in result.stdout
    assert f"source={unsupported} status=unsupported documents=0 chunks=0" in result.stdout
