from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.employee import EmployeeMaster
from app.schemas.common import success_response
from app.schemas.feedback import FeedbackSubmitRequest, FeedbackTemplateCreate
from app.services import feedback_service

router = APIRouter(prefix="/api/v1/feedback", tags=["feedback"])


@router.get("/template/{booking_id}")
def get_template(
    booking_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Interviewer")),
):
    template = feedback_service.get_form_template(booking_id, db)
    return success_response(template)


@router.post("/{booking_id}", status_code=201)
def submit_feedback(
    booking_id: int,
    body: FeedbackSubmitRequest,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Interviewer")),
):
    result = feedback_service.submit_feedback(booking_id, body, current_user.email_id, db)
    return success_response(result)


@router.get("/{booking_id}/pdf")
def download_pdf(
    booking_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "Admin", "PMO", "RecruiterLead")),
):
    return feedback_service.get_feedback_pdf(booking_id, db)


@router.get("/templates")
def list_templates(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin", "RecruiterLead")),
):
    templates = feedback_service.list_templates(db)
    return success_response({"items": templates, "total": len(templates)})


@router.post("/templates", status_code=201)
def create_template(
    body: FeedbackTemplateCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin")),
):
    template = feedback_service.create_template(body, db)
    return success_response({"id": template.id, "form_title": template.form_title})
