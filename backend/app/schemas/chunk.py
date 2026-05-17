from dataclasses import dataclass, field


@dataclass(frozen=True)
class CanonicalChunk:
    document_source_id: str
    chunk_index: int
    text: str
    metadata: dict = field(default_factory=dict)
    lineage: dict = field(default_factory=dict)
    citation: dict = field(default_factory=dict)
    char_start: int | None = None
    char_end: int | None = None
