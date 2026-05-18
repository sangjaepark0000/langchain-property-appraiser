from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


def test_status_panel_displays_loading_error_and_insufficient_states():
    panel = (FRONTEND / "src" / "lib" / "components" / "StatusPanel.svelte").read_text()

    assert 'data-testid="status-panel"' in panel
    assert "loading" in panel
    assert "error" in panel
    assert "insufficient_evidence" in panel
    assert "질문을 처리하는 중입니다" in panel
    assert "근거가 충분하지 않습니다" in panel
    assert "다시 시도하세요" in panel


def test_page_sets_loading_then_insufficient_or_ready_or_error_status():
    page = (FRONTEND / "src" / "routes" / "+page.svelte").read_text()

    assert "type ChatStatus" in page
    assert "statusKind = 'loading'" in page
    assert "statusKind = response.insufficient_evidence ? 'insufficient_evidence' : 'ready'" in page
    assert "statusKind = 'error'" in page
    assert "isSubmitting = false" in page


def test_chat_input_remains_retryable_after_error():
    page = (FRONTEND / "src" / "routes" / "+page.svelte").read_text()
    input_component = (FRONTEND / "src" / "lib" / "components" / "ChatInput.svelte").read_text()

    assert "finally" in page
    assert "isSubmitting = false" in page
    assert "disabled={isSubmitting}" in page
    assert "disabled={disabled || !question.trim()}" in input_component
