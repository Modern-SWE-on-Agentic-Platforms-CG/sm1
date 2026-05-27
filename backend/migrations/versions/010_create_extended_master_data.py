"""create extended master data tables

Revision ID: 010
Revises: 009
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "010"
down_revision: Union[str, None] = "009"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "source_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("source_name", sa.String(100), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "vendor_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("vendor_name", sa.String(100), nullable=False),
        sa.Column("source_id", sa.Integer(), sa.ForeignKey("source_master.id")),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("vendor_name", "source_id"),
    )

    op.create_table(
        "approver_dl_mapping",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tower_id", sa.Integer(), sa.ForeignKey("tower_master.id")),
        sa.Column("dl_email", sa.String(255), nullable=False),
        sa.Column("dl_title", sa.String(200)),
        sa.Column("level", sa.String(100), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_approver_dl_tower_id", "approver_dl_mapping", ["tower_id"])

    op.create_table(
        "tower_skill_mapping",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tower_id", sa.Integer(), sa.ForeignKey("tower_master.id"), nullable=False),
        sa.Column(
            "technology_id", sa.Integer(), sa.ForeignKey("technology_master.id"), nullable=False
        ),
        sa.UniqueConstraint("tower_id", "technology_id"),
    )

    op.create_table(
        "sap_capability_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("capability_name", sa.String(200), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "sap_skill_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("skill_name", sa.String(200), nullable=False),
        sa.Column(
            "capability_id",
            sa.Integer(),
            sa.ForeignKey("sap_capability_master.id"),
            nullable=True,
        ),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "export_history",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("export_type", sa.String(100), nullable=False),
        sa.Column("file_path", sa.String(500), nullable=False),
        sa.Column("created_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("is_deleted", sa.Boolean(), nullable=False, server_default=sa.false()),
    )
    op.create_index("ix_export_history_created_by", "export_history", ["created_by"])
    op.create_index("ix_export_history_is_deleted", "export_history", ["is_deleted"])

    op.create_table(
        "role_comment",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("role_id", sa.Integer(), sa.ForeignKey("role_master.id"), nullable=False),
        sa.Column("comment_text", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("role_comment")
    op.drop_table("export_history")
    op.drop_table("sap_skill_master")
    op.drop_table("sap_capability_master")
    op.drop_table("tower_skill_mapping")
    op.drop_table("approver_dl_mapping")
    op.drop_table("vendor_master")
    op.drop_table("source_master")
