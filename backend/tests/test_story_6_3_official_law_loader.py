from pathlib import Path

import pytest

from app.ingestion.loaders import load_document
from app.ingestion.official_law import OfficialLawParseError, load_official_law_xml


FIXTURES = Path(__file__).parent / "fixtures" / "official_law"


def test_official_law_xml_loader_creates_canonical_document_with_domain_metadata():
    document = load_official_law_xml(FIXTURES / "sample_law.xml", data_mode="official", source_id="official-law-open-api")

    assert document.source_id == "official-law-open-api"
    assert document.source_type == "official_law_xml"
    assert document.data_mode == "official"
    assert document.source_url == "https://open.law.go.kr/sample/law"
    assert document.source_name == "감정평가 및 감정평가사에 관한 법률"
    assert "감정평가" in document.text
    domain = document.metadata["domain_metadata"]
    assert domain["source_authority"] == "국가법령정보센터"
    assert domain["source_url"] == "https://open.law.go.kr/sample/law"
    assert domain["law_name"] == "감정평가 및 감정평가사에 관한 법률"
    assert domain["article_number"] == "제1조"
    assert domain["revision_date"] == "2024-01-01"
    assert domain["effective_date"] == "2024-02-01"
    assert domain["collected_at"]
    assert domain["manual_supplementation_status"] == "not_reviewed"


def test_xml_loader_registered_for_official_xml_files():
    document = load_document(FIXTURES / "sample_law.xml", data_mode="official", source_id="official-law-open-api")

    assert document.source_type == "official_law_xml"
    assert document.metadata["domain_metadata"]["source_authority"] == "국가법령정보센터"


def test_official_law_loader_uses_unknown_or_null_for_missing_metadata_without_fabrication():
    document = load_official_law_xml(FIXTURES / "missing_metadata.xml", data_mode="official", source_id="official-law-open-api")
    domain = document.metadata["domain_metadata"]

    assert domain["source_title"] == "unknown"
    assert domain["law_name"] is None
    assert domain["article_number"] is None
    assert domain["revision_date"] is None
    assert domain["effective_date"] is None
    assert domain["source_url"] == "unknown"
    assert domain["source_authority"] == "unknown"
    assert "open.law.go.kr" not in document.source_url if document.source_url else True


def test_official_law_loader_rejects_unexpected_shape_instead_of_partial_success():
    with pytest.raises(OfficialLawParseError) as exc:
        load_official_law_xml(FIXTURES / "invalid_shape.xml", data_mode="official", source_id="official-law-open-api")

    assert "LawDocument" in str(exc.value)
