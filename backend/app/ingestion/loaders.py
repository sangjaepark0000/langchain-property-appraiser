from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from app.schemas.document import CanonicalDocument


class UnsupportedFileTypeError(ValueError):
    pass


Loader = Callable[[Path, str, str | None], CanonicalDocument]


class LoaderRegistry:
    def __init__(self) -> None:
        self._loaders: dict[str, Loader] = {}

    def register(self, suffix: str, loader: Loader) -> None:
        normalized = suffix.lower()
        if not normalized.startswith("."):
            normalized = f".{normalized}"
        self._loaders[normalized] = loader

    def supports(self, suffix: str) -> bool:
        normalized = suffix.lower()
        if not normalized.startswith("."):
            normalized = f".{normalized}"
        return normalized in self._loaders

    def load(self, path: str | Path, data_mode: str = "unknown", source_id: str | None = None) -> CanonicalDocument:
        source_path = Path(path)
        suffix = source_path.suffix.lower()
        loader = self._loaders.get(suffix)
        if loader is None:
            raise UnsupportedFileTypeError(f"Unsupported file type '{suffix}' for {source_path}")
        return loader(source_path, data_mode, source_id)


def _load_text_file(path: Path, data_mode: str, source_id: str | None, source_type: str) -> CanonicalDocument:
    text = path.read_text(encoding="utf-8")
    resolved_source_id = source_id or f"local-{source_type}"
    metadata = {
        "source_id": resolved_source_id,
        "source_name": path.name,
        "source_path": str(path),
        "source_url": None,
        "source_type": source_type,
        "data_mode": data_mode,
        "file_name": path.name,
        "file_suffix": path.suffix.lower(),
    }
    return CanonicalDocument(
        source_id=resolved_source_id,
        source_path=str(path),
        source_url=None,
        source_name=path.name,
        source_type=source_type,
        data_mode=data_mode,
        text=text,
        metadata=metadata,
        title=path.stem,
        status="loaded",
    )


def load_markdown(path: Path, data_mode: str = "unknown", source_id: str | None = None) -> CanonicalDocument:
    return _load_text_file(path, data_mode, source_id, "markdown")


def load_txt(path: Path, data_mode: str = "unknown", source_id: str | None = None) -> CanonicalDocument:
    return _load_text_file(path, data_mode, source_id, "txt")


def register_default_loaders(registry: LoaderRegistry) -> None:
    registry.register(".md", load_markdown)
    registry.register(".markdown", load_markdown)
    registry.register(".txt", load_txt)


def default_loader_registry() -> LoaderRegistry:
    registry = LoaderRegistry()
    register_default_loaders(registry)
    return registry


def load_document(path: str | Path, data_mode: str = "unknown", source_id: str | None = None) -> CanonicalDocument:
    return default_loader_registry().load(path, data_mode=data_mode, source_id=source_id)
