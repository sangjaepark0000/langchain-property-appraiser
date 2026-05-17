from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DOCS = ROOT / "docs"


def test_source_priority_rubric_exists_with_required_criteria():
    inventory = (DOCS / "source-inventory.md").read_text()

    assert "## Official Source Prioritization Rubric" in inventory
    for criterion in ["official authority", "access stability", "machine readability", "metadata completeness", "implementation complexity"]:
        assert criterion in inventory.lower()
    assert "first_loader_target" in inventory


def test_official_sources_have_loader_status_and_manual_notes():
    inventory = (DOCS / "source-inventory.md").read_text()

    for source_id in [
        "official-law-open-api",
        "official-molit-appraisal-standards",
        "official-public-land-price-api",
    ]:
        assert source_id in inventory
    for field in ["expected_loader_type", "manual_supplementation", "agent_limitation", "prerequisite_work"]:
        assert field in inventory


def test_first_ingestion_candidate_is_selected_but_not_marked_ingested():
    inventory = (DOCS / "source-inventory.md").read_text()

    assert "official-law-open-api" in inventory
    assert "first_loader_target=true" in inventory
    law_row = next(line for line in inventory.splitlines() if line.startswith("| `official-law-open-api`"))
    assert "deferred" in law_row
    assert "ingested" not in law_row
    assert "xml_api_loader" in law_row


def test_priority_decision_notes_explain_unsupported_and_deferred_sources():
    inventory = (DOCS / "source-inventory.md").read_text().lower()

    assert "unsupported/deferred rationale" in inventory
    assert "hwp" in inventory
    assert "api key" in inventory
    assert "do not display as official knowledge base" in inventory
