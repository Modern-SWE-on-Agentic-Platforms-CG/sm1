"""create feedback tables

Revision ID: 006
Revises: 005
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "006"
down_revision: Union[str, None] = "005"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "feedback_form_template",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("tech_name", sa.String(100), nullable=False),
        sa.Column("practice", sa.String(100)),
        sa.Column("form_title", sa.String(200), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "feedback_parameter",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("template_id", sa.Integer(), sa.ForeignKey("feedback_form_template.id"), nullable=False),
        sa.Column("section_name", sa.String(200), nullable=False),
        sa.Column("parameter_name", sa.String(200), nullable=False),
        sa.Column("param_order", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("max_score", sa.Integer(), nullable=False, server_default="10"),
    )
    op.create_index("ix_feedback_parameter_template_id", "feedback_parameter", ["template_id"])

    op.create_table(
        "interviewer_feedback_form_details",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "recruiter_calendar_id",
            sa.BigInteger(),
            sa.ForeignKey("recruiter_calendar.recruiter_calendar_id"),
            nullable=False,
        ),
        sa.Column("template_id", sa.Integer(), sa.ForeignKey("feedback_form_template.id")),
        sa.Column("parameter_scores", postgresql.JSONB(), nullable=True),
        sa.Column(
            "overall_rating",
            sa.String(20),
            sa.CheckConstraint("overall_rating IN ('Select','Hold','Reject')"),
            nullable=True,
        ),
        sa.Column("overall_remarks", sa.Text()),
        sa.Column("submitted_by", sa.String(255)),
        sa.Column("submitted_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("pdf_path", sa.String(500)),
    )
    op.create_index(
        "ix_feedback_recruiter_cal_id",
        "interviewer_feedback_form_details",
        ["recruiter_calendar_id"],
    )

    op.create_table(
        "overall_feedback",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "recruiter_calendar_id",
            sa.BigInteger(),
            sa.ForeignKey("recruiter_calendar.recruiter_calendar_id"),
            nullable=False,
        ),
        sa.Column("rating", sa.String(20)),
        sa.Column("remarks", sa.Text()),
        sa.Column("is_revisit", sa.Boolean(), server_default=sa.false()),
    )


def downgrade() -> None:
    op.drop_table("overall_feedback")
    op.drop_table("interviewer_feedback_form_details")
    op.drop_table("feedback_parameter")
    op.drop_table("feedback_form_template")
