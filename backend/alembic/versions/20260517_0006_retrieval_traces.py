"""create retrieval traces

Revision ID: 20260517_0006
Revises: 20260517_0005
Create Date: 2026-05-17
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "20260517_0006"
down_revision: str | None = "20260517_0005"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "retrieval_traces",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("conversation_id", sa.Integer(), nullable=True),
        sa.Column("message_id", sa.Integer(), nullable=True),
        sa.Column("query_preview", sa.Text(), nullable=False),
        sa.Column("query_hash", sa.String(length=64), nullable=False),
        sa.Column("rewritten_query_preview", sa.Text(), nullable=True),
        sa.Column("rewritten_query_hash", sa.String(length=64), nullable=True),
        sa.Column("retrieved_chunk_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("rewritten_retrieved_chunk_ids", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("relevance_result", sa.String(length=100), nullable=False),
        sa.Column("insufficient_evidence_reason", sa.Text(), nullable=True),
        sa.Column("summary", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["message_id"], ["messages.id"], ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_retrieval_traces_conversation_id_created_at",
        "retrieval_traces",
        ["conversation_id", "created_at"],
        unique=False,
    )
    op.create_index("ix_retrieval_traces_message_id", "retrieval_traces", ["message_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_retrieval_traces_message_id", table_name="retrieval_traces")
    op.drop_index("ix_retrieval_traces_conversation_id_created_at", table_name="retrieval_traces")
    op.drop_table("retrieval_traces")
