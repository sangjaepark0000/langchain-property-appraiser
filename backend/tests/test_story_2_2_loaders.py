from pathlib import Path
import sys

import pytest


BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))


def test_markdown_loader_returns_canonical_document(tmp_path):
    source = tmp_path / "sample.md"
    source.write_text("# Sample\n\nHello markdown", encoding="utf-8")

    from app.ingestion.loaders import load_document

    doc = load_document(source, data_mode="sample", source_id="sample-local-markdown")

    assert doc.text == "# Sample\n\nHello markdown"
    assert doc.source_path == str(source)
    assert doc.source_name == "sample.md"
    assert doc.source_type == "markdown"
    assert doc.data_mode == "sample"
    assert doc.status == "loaded"
    assert doc.metadata["file_name"] == "sample.md"


def test_txt_loader_returns_canonical_document(tmp_path):
    source = tmp_path / "notes.txt"
    source.write_text("plain text", encoding="utf-8")

    from app.ingestion.loaders import load_document

    doc = load_document(source, data_mode="user_provided")

    assert doc.text == "plain text"
    assert doc.source_type == "txt"
    assert doc.data_mode == "user_provided"


def test_unsupported_file_type_raises_explicit_error(tmp_path):
    source = tmp_path / "document.pdf"
    source.write_bytes(b"not supported")

    from app.ingestion.loaders import UnsupportedFileTypeError, load_document

    with pytest.raises(UnsupportedFileTypeError) as exc:
        load_document(source)

    assert ".pdf" in str(exc.value)
    assert "unsupported" in str(exc.value).lower()


def test_loader_registry_can_be_extended_without_changing_existing_loaders(tmp_path):
    from app.ingestion.loaders import LoaderRegistry, register_default_loaders

    registry = LoaderRegistry()
    register_default_loaders(registry)

    assert registry.supports(".md")
    assert registry.supports(".markdown")
    assert registry.supports(".txt")
    assert not registry.supports(".pdf")
