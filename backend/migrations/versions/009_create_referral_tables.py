"""create referral tables

Revision ID: 009
Revises: 008
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "009"
down_revision: Union[str, None] = "008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "referral_technology_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tech_name", sa.String(100), nullable=False, unique=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
    )

    op.create_table(
        "referral_notice_period_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("period_label", sa.String(50), nullable=False, unique=True),
    )

    op.create_table(
        "referral_location_master",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("location_name", sa.String(100), nullable=False, unique=True),
    )

    op.create_table(
        "referral_candidate_info",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "referee_emp_id",
            sa.BigInteger(),
            sa.ForeignKey("employee_master.emp_id"),
            nullable=True,
        ),
        sa.Column("candidate_name", sa.String(200), nullable=False),
        sa.Column("candidate_email", sa.String(255), nullable=False),
        sa.Column("candidate_phone", sa.String(20)),
        sa.Column("certifications", sa.String(500)),
        sa.Column("notice_period", sa.String(50)),
        sa.Column("location", sa.String(100)),
        sa.Column("resume_path", sa.String(500)),
        sa.Column("image_path", sa.String(500)),
        sa.Column("status", sa.String(50), nullable=False, server_default="Pending"),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index("ix_referral_candidate_email", "referral_candidate_info", ["candidate_email"])
    op.create_index("ix_referral_status", "referral_candidate_info", ["status"])

    op.create_table(
        "referral_candidate_skills",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "referral_id",
            sa.BigInteger(),
            sa.ForeignKey("referral_candidate_info.id"),
            nullable=False,
        ),
        sa.Column(
            "tech_id",
            sa.Integer(),
            sa.ForeignKey("referral_technology_master.id"),
            nullable=False,
        ),
        sa.UniqueConstraint("referral_id", "tech_id"),
    )

    # Seed default notice periods
    op.bulk_insert(
        sa.table(
            "referral_notice_period_master",
            sa.column("period_label", sa.String),
        ),
        [
            {"period_label": "Immediate"},
            {"period_label": "15 Days"},
            {"period_label": "30 Days"},
            {"period_label": "60 Days"},
            {"period_label": "90 Days"},
        ],
    )

    # Seed default locations
    op.bulk_insert(
        sa.table(
            "referral_location_master",
            sa.column("location_name", sa.String),
        ),
        [
            {"location_name": "Bangalore"},
            {"location_name": "Hyderabad"},
            {"location_name": "Mumbai"},
            {"location_name": "Delhi"},
            {"location_name": "Chennai"},
            {"location_name": "Pune"},
        ],
    )


def downgrade() -> None:
    op.drop_table("referral_candidate_skills")
    op.drop_table("referral_candidate_info")
    op.drop_table("referral_location_master")
    op.drop_table("referral_notice_period_master")
    op.drop_table("referral_technology_master")
