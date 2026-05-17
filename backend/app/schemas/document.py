from dataclasses import dataclass, field


VALID_DATA_MODES = {"sample", "official", "user_provided", "unknown"}


@dataclass(frozen=True)
class CanonicalDocument:
    source_id: str
    source_path: str | None
    source_url: str | None
    source_name: str
    source_type: str
    data_mode: str
    text: str
    metadata: dict = field(default_factory=dict)
    title: str | None = None
    status: str = "loaded"

    def __post_init__(self) -> None:
        if self.data_mode not in VALID_DATA_MODES:
            raise ValueError(f"Unsupported data_mode: {self.data_mode}")
