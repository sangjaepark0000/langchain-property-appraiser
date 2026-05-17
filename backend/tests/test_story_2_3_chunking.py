import pytest

from app.schemas.document import CanonicalDocument


def make_doc(text: str) -> CanonicalDocument:
    return CanonicalDocument(
        source_id="sample-local-markdown",
        source_path="sample_data/example.md",
        source_url=None,
        source_name="example.md",
        source_type="markdown",
        data_mode="sample",
        text=text,
        metadata={"source_id": "sample-local-markdown", "source_path": "sample_data/example.md", "data_mode": "sample"},
    )


def test_short_document_becomes_single_chunk():
    from app.ingestion.chunker import chunk_document

    chunks = chunk_document(make_doc("short text"), chunk_size=100, chunk_overlap=10)

    assert len(chunks) == 1
    assert chunks[0].chunk_index == 0
    assert chunks[0].text == "short text"
    assert chunks[0].document_source_id == "sample-local-markdown"


def test_long_document_splits_with_configurable_size_and_overlap():
    from app.ingestion.chunker import chunk_document

    chunks = chunk_document(make_doc("abcdefghijklmnopqrstuvwxyz"), chunk_size=10, chunk_overlap=2)

    assert [chunk.text for chunk in chunks] == ["abcdefghij", "ijklmnopqr", "qrstuvwxyz"]
    assert [chunk.char_start for chunk in chunks] == [0, 8, 16]
    assert [chunk.char_end for chunk in chunks] == [10, 18, 26]


def test_chunk_metadata_preserves_lineage_and_citation_fields():
    from app.ingestion.chunker import chunk_document

    chunk = chunk_document(make_doc("hello"))[0]

    assert chunk.metadata["source_path"] == "sample_data/example.md"
    assert chunk.metadata["source_type"] == "markdown"
    assert chunk.metadata["data_mode"] == "sample"
    assert chunk.lineage["source_id"] == "sample-local-markdown"
    assert chunk.lineage["chunk_index"] == 0
    assert chunk.citation["source_name"] == "example.md"


def test_empty_document_raises_clear_error():
    from app.ingestion.chunker import EmptyDocumentError, chunk_document

    with pytest.raises(EmptyDocumentError):
        chunk_document(make_doc("   \n\t"))
