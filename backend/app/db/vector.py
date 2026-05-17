from __future__ import annotations

from sqlalchemy import JSON, TypeDecorator


class EmbeddingVector(TypeDecorator):
    """Portable embedding vector column.

    PostgreSQL uses pgvector's `vector(N)` type. Non-PostgreSQL dialects use JSON so
    sqlite smoke tests can run without the extension.
    """

    impl = JSON
    cache_ok = True

    def __init__(self, dimensions: int = 16, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.dimensions = dimensions

    def load_dialect_impl(self, dialect):
        if dialect.name == "postgresql":
            from pgvector.sqlalchemy import Vector

            return dialect.type_descriptor(Vector(self.dimensions))
        return dialect.type_descriptor(JSON())
