"""create supply tables

Revision ID: 008
Revises: 007
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "008"
down_revision: Union[str, None] = "007"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "demand_batch",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("uploaded_by", sa.String(255)),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("row_count", sa.Integer(), server_default="0"),
    )

    op.create_table(
        "demand_data",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("jr_id", sa.String(100)),
        sa.Column("skill", sa.String(100)),
        sa.Column("grade", sa.String(50)),
        sa.Column("account", sa.String(200)),
        sa.Column("bu", sa.String(100)),
        sa.Column("demand_status", sa.String(50), nullable=False, server_default="Open"),
        sa.Column("demand_date", sa.Date()),
        sa.Column("sourced_count", sa.Integer(), server_default="0"),
        sa.Column("pipeline_count", sa.Integer(), server_default="0"),
        sa.Column("batch_id", sa.BigInteger(), sa.ForeignKey("demand_batch.id"), nullable=False),
    )
    op.create_index("ix_demand_data_batch_id", "demand_data", ["batch_id"])
    op.create_index("ix_demand_data_skill_bu", "demand_data", ["skill", "bu"])

    op.create_table(
        "bench_batch",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("uploaded_by", sa.String(255)),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("row_count", sa.Integer(), server_default="0"),
    )

    op.create_table(
        "bench_data",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("emp_name", sa.String(200)),
        sa.Column("emp_email", sa.String(255)),
        sa.Column("skill", sa.String(100)),
        sa.Column("grade", sa.String(50)),
        sa.Column("location", sa.String(100)),
        sa.Column("bu", sa.String(100)),
        sa.Column("bench_status", sa.String(50), nullable=False, server_default="Available"),
        sa.Column("batch_id", sa.BigInteger(), sa.ForeignKey("bench_batch.id"), nullable=False),
    )
    op.create_index("ix_bench_data_batch_id", "bench_data", ["batch_id"])
    op.create_index("ix_bench_data_skill_bu", "bench_data", ["skill", "bu"])


def downgrade() -> None:
    op.drop_table("bench_data")
    op.drop_table("bench_batch")
    op.drop_table("demand_data")
    op.drop_table("demand_batch")
