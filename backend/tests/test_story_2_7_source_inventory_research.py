from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOC = ROOT / "docs" / "source-inventory.md"


def test_official_sources_are_documented_but_not_ingested():
    text = DOC.read_text(encoding="utf-8")

    assert "official-law-open-api" in text
    assert "official-molit-appraisal-standards" in text
    assert "official-public-land-price-api" in text
    official_rows = [line for line in text.splitlines() if line.startswith("| `official-")]
    assert official_rows
    assert all("`ingested`" not in line for line in official_rows)


def test_source_inventory_records_access_format_auth_and_priority():
    text = DOC.read_text(encoding="utf-8")

    for expected in ["XML", "HTML", "JSON", "API key", "priority", "next_loader_work"]:
        assert expected in text


def test_unsupported_or_deferred_formats_are_explicit():
    text = DOC.read_text(encoding="utf-8")

    assert "PDF" in text
    assert "DOCX" in text
    assert "HWP" in text
    assert "OCR" in text
    assert "deferred" in text
    assert "unsupported" in text


def test_sample_and_official_data_modes_are_not_confused():
    text = DOC.read_text(encoding="utf-8")

    assert "sample-local-markdown" in text
    assert "data_mode` = `official`" in text
    assert "official source는 조사 완료 상태여도 ingestion 완료로 표시하지 않는다" in text
