from __future__ import annotations
import io
from datetime import datetime
from pathlib import Path

from fastapi import HTTPException
from fastapi.responses import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from sqlalchemy.orm import Session

from app.models.feedback import FeedbackFormTemplate, FeedbackParameter, InterviewerFeedbackFormDetails, OverallFeedback
from app.models.interview import RecruiterCalendar
from app.models.master_data import ExportHistory
from app.schemas.feedback import FeedbackSubmitRequest, FeedbackTemplateCreate
from app.core.config import settings
from app.core.logging import get_logger

logger = get_logger(__name__)

UPLOAD_DIR = Path(settings.UPLOAD_DIR)


def get_form_template(booking_id: int, db: Session) -> dict:
    booking = db.query(RecruiterCalendar).filter(
        RecruiterCalendar.recruiter_calendar_id == booking_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Find template by skill
    template = None
    if booking.skill_id:
        from app.models.master_data import TechnologyMaster
        tech = db.query(TechnologyMaster).filter(TechnologyMaster.id == booking.skill_id).first()
        if tech:
            template = db.query(FeedbackFormTemplate).filter(
                FeedbackFormTemplate.tech_name == tech.tech_name,
                FeedbackFormTemplate.is_active == True,
            ).first()

    if not template:
        # Return default/first active template
        template = db.query(FeedbackFormTemplate).filter(
            FeedbackFormTemplate.is_active == True
        ).first()

    if not template:
        # Auto-bootstrap a default template so interviewer flow works on fresh databases.
        template = FeedbackFormTemplate(
            tech_name="General",
            practice="Default",
            form_title="Standard Interview Feedback",
            is_active=True,
        )
        db.add(template)
        db.flush()

        default_params = [
            ("Technical", "Technical Knowledge", 1),
            ("Technical", "Problem Solving", 2),
            ("Behavioral", "Communication", 3),
        ]
        for section_name, parameter_name, order in default_params:
            db.add(
                FeedbackParameter(
                    template_id=template.id,
                    section_name=section_name,
                    parameter_name=parameter_name,
                    param_order=order,
                    max_score=5,
                )
            )

        db.commit()
        db.refresh(template)

    # Group parameters by section
    params = db.query(FeedbackParameter).filter(
        FeedbackParameter.template_id == template.id
    ).order_by(FeedbackParameter.param_order).all()

    sections: dict[str, list] = {}
    for p in params:
        sections.setdefault(p.section_name, []).append({
            "id": p.id,
            "parameter_name": p.parameter_name,
            "max_score": p.max_score,
            "param_order": p.param_order,
        })

    return {
        "template_id": template.id,
        "form_title": template.form_title,
        "tech_name": template.tech_name,
        "sections": [
            {"section_name": sec, "parameters": pars}
            for sec, pars in sections.items()
        ],
    }


def _generate_feedback_pdf(booking: RecruiterCalendar, feedback: InterviewerFeedbackFormDetails,
                            template: FeedbackFormTemplate, db: Session) -> str:
    """Generate a ReportLab PDF and return its file path."""
    exports_dir = UPLOAD_DIR / "exports"
    exports_dir.mkdir(parents=True, exist_ok=True)
    pdf_path = exports_dir / f"feedback_{feedback.id}.pdf"

    styles = getSampleStyleSheet()
    doc = SimpleDocTemplate(str(pdf_path), pagesize=A4)
    story = []

    story.append(Paragraph(f"Interview Feedback — {template.form_title}", styles["Title"]))
    story.append(Spacer(1, 12))

    from app.models.candidate import CandidateDetail
    candidate = db.query(CandidateDetail).filter(
        CandidateDetail.candidate_detail_id == booking.candidate_detail_id
    ).first()
    if candidate:
        story.append(Paragraph(f"Candidate: {candidate.candidate_name}", styles["Normal"]))
        story.append(Paragraph(f"Interview Type: {booking.interview_type}", styles["Normal"]))
        story.append(Paragraph(f"Interview Date: {booking.interview_date}", styles["Normal"]))
        story.append(Spacer(1, 12))

    # Parameter scores table
    params = db.query(FeedbackParameter).filter(
        FeedbackParameter.template_id == template.id
    ).order_by(FeedbackParameter.param_order).all()

    scores = feedback.parameter_scores or {}
    table_data = [["Parameter", "Section", "Score", "Max"]]
    for p in params:
        score = scores.get(str(p.id), "-")
        table_data.append([p.parameter_name, p.section_name, str(score), str(p.max_score)])

    if len(table_data) > 1:
        t = Table(table_data, colWidths=[200, 150, 50, 50])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.black),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
        ]))
        story.append(t)
        story.append(Spacer(1, 12))

    story.append(Paragraph(f"Overall Recommendation: {feedback.overall_rating or '-'}", styles["Heading3"]))
    if feedback.overall_remarks:
        story.append(Paragraph(f"Remarks: {feedback.overall_remarks}", styles["Normal"]))

    doc.build(story)
    logger.info(f"Generated feedback PDF: {pdf_path}")
    return str(pdf_path)


def submit_feedback(booking_id: int, data: FeedbackSubmitRequest, submitted_by: str, db: Session) -> dict:
    booking = db.query(RecruiterCalendar).filter(
        RecruiterCalendar.recruiter_calendar_id == booking_id
    ).first()
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")

    # Find template
    template_info = get_form_template(booking_id, db)
    template = db.query(FeedbackFormTemplate).filter(
        FeedbackFormTemplate.id == template_info["template_id"]
    ).first()

    feedback = InterviewerFeedbackFormDetails(
        recruiter_calendar_id=booking_id,
        template_id=template.id if template else None,
        parameter_scores=data.parameter_scores,
        overall_rating=data.overall_rating,
        overall_remarks=data.overall_remarks,
        submitted_by=submitted_by,
    )
    db.add(feedback)
    db.flush()

    # Generate PDF
    pdf_path = None
    if template:
        try:
            pdf_path = _generate_feedback_pdf(booking, feedback, template, db)
        except Exception as exc:
            logger.warning(f"PDF generation failed: {exc}")

    feedback.pdf_path = pdf_path
    booking.feedback_submitted = True

    # If revisit, record in overall_feedback
    if data.is_revisit:
        of = OverallFeedback(
            recruiter_calendar_id=booking_id,
            rating=data.overall_rating,
            remarks=data.overall_remarks,
            is_revisit=True,
        )
        db.add(of)

    # Track export history
    if pdf_path:
        hist = ExportHistory(
            export_type="feedback_pdf",
            file_path=pdf_path,
            created_by=submitted_by,
        )
        db.add(hist)

    db.commit()
    db.refresh(feedback)
    return {"feedback_id": feedback.id, "pdf_path": pdf_path, "overall_rating": feedback.overall_rating}


def get_feedback_pdf(booking_id: int, db: Session) -> FileResponse:
    feedback = db.query(InterviewerFeedbackFormDetails).filter(
        InterviewerFeedbackFormDetails.recruiter_calendar_id == booking_id
    ).order_by(InterviewerFeedbackFormDetails.submitted_at.desc()).first()
    if not feedback or not feedback.pdf_path:
        raise HTTPException(status_code=404, detail="Feedback PDF not found")
    path = Path(feedback.pdf_path)
    if not path.exists():
        raise HTTPException(status_code=404, detail="PDF file missing from storage")
    return FileResponse(str(path), media_type="application/pdf", filename=path.name)


def list_templates(db: Session) -> list:
    return db.query(FeedbackFormTemplate).filter(FeedbackFormTemplate.is_active == True).all()


def create_template(data: FeedbackTemplateCreate, db: Session) -> FeedbackFormTemplate:
    template = FeedbackFormTemplate(
        tech_name=data.tech_name,
        practice=data.practice,
        form_title=data.form_title,
    )
    db.add(template)
    db.flush()

    for idx, p in enumerate(data.parameters or []):
        param = FeedbackParameter(
            template_id=template.id,
            section_name=p.get("section_name", "General"),
            parameter_name=p["parameter_name"],
            param_order=p.get("param_order", idx),
            max_score=p.get("max_score", 10),
        )
        db.add(param)

    db.commit()
    db.refresh(template)
    return template
