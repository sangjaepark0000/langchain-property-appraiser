from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FRONTEND = ROOT / "frontend"


def test_data_mode_notice_distinguishes_sample_unknown_from_official():
    notice = (FRONTEND / "src" / "lib" / "components" / "DataModeNotice.svelte").read_text()

    assert 'data-testid="data-mode-notice"' in notice
    assert "dataMode" in notice
    assert "샘플" in notice
    assert "출처 불명" in notice
    assert "공식 판단이 아닙니다" in notice
    assert "official review result" not in notice.lower()


def test_message_list_renders_data_mode_and_safety_notice_for_assistant_messages():
    component = (FRONTEND / "src" / "lib" / "components" / "MessageList.svelte").read_text()

    assert "import DataModeNotice" in component
    assert "message.dataMode" in component
    assert "message.insufficientEvidenceReason" in component
    assert "<DataModeNotice" in component
    assert "message.dataMode !== 'none'" in component
    assert "참고용 답변" in component


def test_page_preserves_backend_insufficient_evidence_reason_and_data_mode():
    page = (FRONTEND / "src" / "routes" / "+page.svelte").read_text()

    assert "dataMode: response.data_mode" in page
    assert "insufficientEvidenceReason: response.insufficient_evidence_reason" in page
    assert "status = response.insufficient_evidence" in page
    assert "근거 부족:" in page
