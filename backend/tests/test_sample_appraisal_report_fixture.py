from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "sample_data" / "sample-appraisal-report.md"


def test_sample_appraisal_report_fixture_is_clearly_marked_sample():
    text = SAMPLE.read_text(encoding="utf-8")

    assert "SAMPLE 감정평가서 요약서" in text
    assert "합성 샘플" in text
    assert "현업 감정평가사가 작성한 문서가 아니라" in text
    assert "data_mode: sample" in text
    assert "감정평가 방법" in text
    assert "가치형성요인" in text
    assert "현실의 거래, 담보, 과세, 보상 또는 회계 목적의 감정평가액이 아니다" in text


def test_sample_data_readme_lists_appraisal_report_fixture():
    readme = (ROOT / "sample_data" / "README.md").read_text(encoding="utf-8")

    assert "sample-appraisal-report.md" in readme
    assert "not an actual appraisal report" in readme
