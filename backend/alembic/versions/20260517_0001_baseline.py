"""baseline

Revision ID: 20260517_0001
Revises:
Create Date: 2026-05-17
"""

from collections.abc import Sequence

revision: str = "20260517_0001"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Baseline migration: creates no domain tables yet."""
    pass


def downgrade() -> None:
    """Baseline migration rollback: no domain tables to drop."""
    pass
