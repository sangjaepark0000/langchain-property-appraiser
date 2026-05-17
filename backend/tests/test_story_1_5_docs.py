from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]


def test_source_inventory_doc_exists_and_defines_statuses():
    text = (REPO_ROOT / "docs" / "source-inventory.md").read_text()

    for term in ["supported", "unsupported", "deferred", "ingested", "failed"]:
        assert term in text
    assert "silent" in text.lower()
    assert "성공" in text or "success" in text.lower()


def test_canonical_document_schema_doc_exists_and_defines_data_modes():
    text = (REPO_ROOT / "docs" / "canonical-document-schema.md").read_text()

    for mode in ["sample", "official", "user_provided", "unknown"]:
        assert mode in text
    for concept in ["document", "chunk", "metadata", "citation", "lineage"]:
        assert concept in text.lower()


def test_docs_describe_expected_fields():
    source_text = (REPO_ROOT / "docs" / "source-inventory.md").read_text()
    schema_text = (REPO_ROOT / "docs" / "canonical-document-schema.md").read_text()

    for field in ["source_id", "name", "status", "data_mode", "source_url"]:
        assert field in source_text
    for field in ["document_id", "chunk_id", "source_path", "data_mode", "metadata"]:
        assert field in schema_text
