"""create workflow tables

Revision ID: 007
Revises: 006
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "007"
down_revision: Union[str, None] = "006"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "offer_workflow",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "candidate_detail_id",
            sa.BigInteger(),
            sa.ForeignKey("candidate_detail.candidate_detail_id"),
            nullable=False,
        ),
        sa.Column("current_level", sa.String(100), nullable=False, server_default="TowerLead"),
        sa.Column("status", sa.String(50), nullable=False, server_default="Pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_offer_workflow_candidate_id", "offer_workflow", ["candidate_detail_id"])
    op.create_index("ix_offer_workflow_status", "offer_workflow", ["status"])

    op.create_table(
        "workflow_comments",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("workflow_id", sa.BigInteger(), sa.ForeignKey("offer_workflow.id"), nullable=False),
        sa.Column("commenter_email", sa.String(255), nullable=False),
        sa.Column("comment_text", sa.Text()),
        sa.Column(
            "action",
            sa.String(20),
            sa.CheckConstraint("action IN ('Approved','Rejected','Comment')"),
            nullable=False,
        ),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_workflow_comments_workflow_id", "workflow_comments", ["workflow_id"])

    op.create_table(
        "ctc_history",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "candidate_detail_id",
            sa.BigInteger(),
            sa.ForeignKey("candidate_detail.candidate_detail_id"),
            nullable=False,
        ),
        sa.Column("ctc_value", sa.String(50), nullable=False),
        sa.Column("changed_by", sa.String(255)),
        sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_ctc_history_candidate_id", "ctc_history", ["candidate_detail_id"])

    op.create_table(
        "joining_bonus",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "candidate_detail_id",
            sa.BigInteger(),
            sa.ForeignKey("candidate_detail.candidate_detail_id"),
            nullable=False,
        ),
        sa.Column("bonus_amount", sa.Numeric(12, 2)),
        sa.Column("status", sa.String(50), nullable=False, server_default="Pending"),
        sa.Column("dl_email", sa.String(255)),
        sa.Column("updated_by", sa.String(255)),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_joining_bonus_candidate_id", "joining_bonus", ["candidate_detail_id"])


def downgrade() -> None:
    op.drop_table("joining_bonus")
    op.drop_table("ctc_history")
    op.drop_table("workflow_comments")
    op.drop_table("offer_workflow")
