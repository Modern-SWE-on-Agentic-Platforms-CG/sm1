from fastapi import APIRouter, Depends, UploadFile, File, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.candidate import CandidateUpdate, StatusChangeRequest, CommentCreate
from app.schemas.common import success_response
from app.services import candidate_service
from app.models.candidate import StatusIntermediateMapping
from app.models.employee import EmployeeMaster
from app.core.file_storage import get_file_path

router = APIRouter(prefix="/api/v1/candidates", tags=["candidates"])


@router.post("/upload", status_code=201)
async def upload_candidates(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "Admin", "SAP Recruiter", "PMO")),
):
    result = await candidate_service.bulk_import(file, current_user.email_id, db)
    return success_response(result)


@router.get("/status-options")
def get_status_options(db: Session = Depends(get_db)):
    statuses = db.query(StatusIntermediateMapping).all()
    transitions: dict[str, list[str]] = {}
    for s in statuses:
        transitions.setdefault(s.from_status, []).append(s.to_status)
    return success_response(transitions)


@router.get("")
def list_candidates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    status: str | None = None,
    skill_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "PMO", "Admin", "RecruiterLead")),
):
    result = candidate_service.list_candidates(db, page, page_size, status, skill_id, current_user.email_id)
    return success_response(result)


@router.get("/{candidate_id}")
def get_candidate(
    candidate_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin", "RecruiterLead", "Interviewer")),
):
    c = candidate_service.get_candidate(candidate_id, db)
    return success_response(c)


@router.put("/{candidate_id}")
def update_candidate(
    candidate_id: int,
    body: CandidateUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin")),
):
    c = candidate_service.update_candidate(candidate_id, body, db)
    return success_response(c)


@router.post("/{candidate_id}/status")
def change_status(
    candidate_id: int,
    body: StatusChangeRequest,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "Admin", "RecruiterLead")),
):
    c = candidate_service.change_status(candidate_id, body, current_user.email_id, db)
    return success_response(c)


@router.post("/{candidate_id}/comments", status_code=201)
async def add_comment(
    candidate_id: int,
    comment_text: str | None = None,
    attachment: UploadFile | None = File(None),
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Recruiter", "PMO", "Admin", "Interviewer")),
):
    from app.schemas.candidate import CommentCreate
    data = CommentCreate(comment_text=comment_text)
    comment = await candidate_service.add_comment(candidate_id, data, attachment, current_user.email_id, db)
    return success_response(comment)


@router.get("/{candidate_id}/comments")
def list_comments(
    candidate_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin", "Interviewer")),
):
    from app.models.candidate import CandidateComments
    comments = db.query(CandidateComments).filter(
        CandidateComments.candidate_detail_id == candidate_id
    ).all()
    return success_response(comments)


@router.get("/{candidate_id}/resume")
def download_resume(
    candidate_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin")),
):
    c = candidate_service.get_candidate(candidate_id, db)
    if not c.resume_path:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="No resume on file")
    file_path = get_file_path("resumes", c.resume_path)
    return FileResponse(path=str(file_path), filename=c.resume_path)


@router.post("/{candidate_id}/resume", status_code=201)
async def upload_resume(
    candidate_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin", "RecruiterLead")),
):
    c = await candidate_service.upload_resume(candidate_id, file, db)
    return success_response(c)


@router.get("/{candidate_id}/comments/{comment_id}/attachment")
def download_attachment(
    candidate_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "PMO", "Admin", "Interviewer", "RecruiterLead")),
):
    from app.services import document_service
    return document_service.download_attachment(candidate_id, comment_id, db)
