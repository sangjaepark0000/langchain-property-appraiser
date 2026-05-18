from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


def test_citation_panel_displays_legal_source_fields_from_api_only():
    panel = (FRONTEND / "src" / "lib" / "components" / "CitationPanel.svelte").read_text()

    assert 'data-testid="citation-panel"' in panel
    assert "citation.source_name" in panel
    assert "citation.source_path" in panel
    assert "citation.source_authority" in panel
    assert "citation.law_name" in panel
    assert "citation.article_number" in panel
    assert "citation.article_title" in panel
    assert "citation.effective_date" in panel
    assert "citation.revision_date" in panel
    assert "citation.document_kind" in panel
    assert "citation.chunk_type" in panel
    assert "citation.chunk_index" in panel
    assert "citation.data_mode" in panel
    assert "unknown" in panel.lower()
    assert "law.go.kr" not in panel


def test_message_list_separates_answer_body_from_citation_list():
    component = (FRONTEND / "src" / "lib" / "components" / "MessageList.svelte").read_text()

    assert "import CitationPanel" in component
    assert "message.citations" in component
    assert "<CitationPanel citations={message.citations}" in component
    assert 'class="answer-body"' in component


def test_page_attaches_api_citations_to_assistant_messages():
    page = (FRONTEND / "src" / "routes" / "+page.svelte").read_text()

    assert "citations: response.citations" in page
    assert "citations?: Citation[]" in page or "type Citation" in page
