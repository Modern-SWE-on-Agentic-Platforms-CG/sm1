"""create candidate tables

Revision ID: 005
Revises: 004
Create Date: 2026-05-26

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "005"
down_revision: Union[str, None] = "004"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

STATUS_TRANSITIONS = [
    ("Profile Received", "L1 Scheduled"),
    ("L1 Scheduled", "L1 Selected"),
    ("L1 Scheduled", "L1 Rejected"),
    ("L1 Scheduled", "L1 Hold"),
    ("L1 Selected", "L2 Scheduled"),
    ("L2 Scheduled", "L2 Selected"),
    ("L2 Scheduled", "L2 Rejected"),
    ("L2 Scheduled", "L2 Hold"),
    ("L2 Selected", "Offered"),
    ("L2 Selected", "L3 Scheduled"),
    ("L3 Scheduled", "Offered"),
    ("Offered", "Offer Accepted"),
    ("Offered", "Offer Declined"),
    ("Offer Accepted", "Joined"),
    ("Offer Accepted", "Not Joined"),
]


def upgrade() -> None:
    op.create_table(
        "status_intermediate_mapping",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("from_status", sa.String(100), nullable=False),
        sa.Column("to_status", sa.String(100), nullable=False),
        sa.UniqueConstraint("from_status", "to_status"),
    )
    op.bulk_insert(
        sa.table(
            "status_intermediate_mapping",
            sa.column("from_status", sa.String),
            sa.column("to_status", sa.String),
        ),
        [{"from_status": f, "to_status": t} for f, t in STATUS_TRANSITIONS],
    )

    op.create_table(
        "candidate_detail",
        sa.Column("candidate_detail_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column("candidate_name", sa.String(200), nullable=False),
        sa.Column("email_id", sa.String(255), nullable=False),
        sa.Column("contact_number", sa.String(20)),
        sa.Column("gender", sa.String(20)),
        sa.Column("total_exp", sa.String(10)),
        sa.Column("rel_exp", sa.String(10)),
        sa.Column("current_company", sa.String(200)),
        sa.Column("current_location", sa.String(100)),
        sa.Column("preferred_location", sa.String(100)),
        sa.Column("notice_period", sa.String(50)),
        sa.Column("current_ctc", sa.String(50)),
        sa.Column("exp_ctc", sa.String(50)),
        sa.Column("offer_ctc", sa.String(50)),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("technology_master.id")),
        sa.Column("tower", sa.String(100)),
        sa.Column("skill_group", sa.String(100)),
        sa.Column("source", sa.String(100)),
        sa.Column("referred_vendor", sa.String(100)),
        sa.Column("college", sa.String(200)),
        sa.Column("level_based_on_exp", sa.String(50)),
        sa.Column("overall_status", sa.String(100), nullable=False, server_default="Profile Received"),
        sa.Column("dashboard_status", sa.String(100)),
        sa.Column("is_referral", sa.Boolean(), server_default=sa.false()),
        sa.Column("is_rehire", sa.Boolean(), server_default=sa.false()),
        sa.Column("bu_id", sa.Integer()),
        sa.Column("practice_id", sa.Integer()),
        sa.Column("account_name", sa.String(200)),
        sa.Column("region", sa.String(100)),
        sa.Column("pmo_coordinator", sa.String(200)),
        sa.Column("pmo_coordinator_email", sa.String(255)),
        sa.Column("hr_coordinator", sa.String(200)),
        sa.Column("jr_id", sa.String(100)),
        sa.Column("doj", sa.Date()),
        sa.Column("resume_path", sa.String(500)),
        sa.Column("created_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("recvd_date", sa.Date()),
    )
    op.create_index("ix_candidate_email_id", "candidate_detail", ["email_id"])
    op.create_index("ix_candidate_overall_status", "candidate_detail", ["overall_status"])
    op.create_index("ix_candidate_skill_id", "candidate_detail", ["skill_id"])
    op.create_index("ix_candidate_created_by", "candidate_detail", ["created_by"])
    op.create_index("ix_candidate_bu_status", "candidate_detail", ["bu_id", "overall_status"])

    op.create_table(
        "recruiter_calendar",
        sa.Column("recruiter_calendar_id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "candidate_detail_id", sa.BigInteger(),
            sa.ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
        ),
        sa.Column(
            "interviewer_calendar_id", sa.BigInteger(),
            sa.ForeignKey("interviewer_calendar.interviewer_calendar_id"), nullable=True
        ),
        sa.Column("interview_type", sa.String(10)),
        sa.Column("skill_id", sa.Integer(), sa.ForeignKey("technology_master.id")),
        sa.Column("from_time", sa.DateTime(timezone=True)),
        sa.Column("to_time", sa.DateTime(timezone=True)),
        sa.Column("interview_date", sa.Date()),
        sa.Column("panel_email", sa.String(255)),
        sa.Column("is_direct_booked", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("meeting_link", sa.String(500)),
        sa.Column("feedback_submitted", sa.Boolean(), nullable=False, server_default=sa.false()),
        sa.Column("booked_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index(
        "ix_recruiter_calendar_candidate_date",
        "recruiter_calendar", ["candidate_detail_id", "interview_date"]
    )
    op.create_index(
        "ix_recruiter_calendar_interviewer_id",
        "recruiter_calendar", ["interviewer_calendar_id"]
    )
    op.create_index("ix_recruiter_calendar_feedback", "recruiter_calendar", ["feedback_submitted"])

    op.create_table(
        "candidate_status_history",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "candidate_detail_id", sa.BigInteger(),
            sa.ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
        ),
        sa.Column("from_status", sa.String(100)),
        sa.Column("to_status", sa.String(100), nullable=False),
        sa.Column("changed_by", sa.String(255)),
        sa.Column("changed_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column("notes", sa.Text()),
    )

    op.create_table(
        "candidate_comments",
        sa.Column("id", sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column(
            "candidate_detail_id", sa.BigInteger(),
            sa.ForeignKey("candidate_detail.candidate_detail_id"), nullable=False
        ),
        sa.Column("comment_text", sa.Text()),
        sa.Column("attachment_path", sa.String(500)),
        sa.Column("attachment_filename", sa.String(255)),
        sa.Column("created_by", sa.String(255)),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade() -> None:
    op.drop_table("candidate_comments")
    op.drop_table("candidate_status_history")
    op.drop_index("ix_recruiter_calendar_feedback", "recruiter_calendar")
    op.drop_index("ix_recruiter_calendar_interviewer_id", "recruiter_calendar")
    op.drop_index("ix_recruiter_calendar_candidate_date", "recruiter_calendar")
    op.drop_table("recruiter_calendar")
    op.drop_index("ix_candidate_bu_status", "candidate_detail")
    op.drop_index("ix_candidate_created_by", "candidate_detail")
    op.drop_index("ix_candidate_skill_id", "candidate_detail")
    op.drop_index("ix_candidate_overall_status", "candidate_detail")
    op.drop_index("ix_candidate_email_id", "candidate_detail")
    op.drop_table("candidate_detail")
    op.drop_table("status_intermediate_mapping")
