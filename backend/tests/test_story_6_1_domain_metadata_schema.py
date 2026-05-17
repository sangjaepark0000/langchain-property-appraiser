from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def test_domain_metadata_schema_defines_required_official_fields():
    schema = (DOCS / "domain-metadata-schema.md").read_text()

    required_fields = [
        "domain_metadata",
        "source_title",
        "law_name",
        "article_number",
        "revision_date",
        "effective_date",
        "collected_at",
        "source_url",
        "source_authority",
    ]
    for field in required_fields:
        assert field in schema


def test_domain_metadata_schema_distinguishes_date_meanings():
    schema = (DOCS / "domain-metadata-schema.md").read_text()

    for field in ["created_date", "collected_at", "revision_date", "effective_date", "appraisal_base_date"]:
        assert field in schema
    assert "작성일" in schema
    assert "수집일" in schema
    assert "개정일" in schema
    assert "시행일" in schema
    assert "평가기준일" in schema


def test_domain_metadata_schema_forbids_fabrication_and_allows_missing_values():
    schema = (DOCS / "domain-metadata-schema.md").read_text().lower()

    assert "unknown" in schema
    assert "null" in schema
    assert "do not fabricate" in schema
    assert "없는 공식 metadata" in schema
    assert "manual supplementation" in schema
    assert "agent limitation" in schema
    assert "prerequisite" in schema


def test_canonical_schema_links_domain_metadata_extension_without_requiring_db_columns():
    canonical = (DOCS / "canonical-document-schema.md").read_text()

    assert "domain_metadata" in canonical
    assert "docs/domain-metadata-schema.md" in canonical
    assert "DB column" in canonical
    assert "metadata" in canonical
