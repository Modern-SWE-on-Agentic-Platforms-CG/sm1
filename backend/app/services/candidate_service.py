import io
from datetime import date
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

import pandas as pd
from openpyxl import Workbook

from app.models.candidate import CandidateDetail, CandidateStatusHistory, CandidateComments, StatusIntermediateMapping
from app.models.master_data import TechnologyMaster
from app.schemas.candidate import CandidateUpdate, StatusChangeRequest, CommentCreate
from app.core.file_storage import save_file, generate_export_path


def _get_valid_next_statuses(current_status: str, db: Session) -> list[str]:
    rows = (
        db.query(StatusIntermediateMapping.to_status)
        .filter(StatusIntermediateMapping.from_status == current_status)
        .all()
    )
    return [r.to_status for r in rows]


def parse_excel(content: bytes, db: Session) -> tuple[list[dict], list[dict]]:
    """Parse candidate Excel. Returns (valid_rows, error_rows)."""
    df = pd.read_excel(io.BytesIO(content))
    df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]

    valid: list[dict] = []
    errors: list[dict] = []

    for idx, row in df.iterrows():
        try:
            name = str(row.get("candidate_name", "")).strip()
            email = str(row.get("email_id", "")).strip().lower()
            if not name or not email or "@" not in email:
                raise ValueError("candidate_name and valid email_id are required")
            valid.append(row.to_dict())
        except Exception as e:
            errors.append({**row.to_dict(), "error": str(e)})

    return valid, errors


async def bulk_import(file: UploadFile, created_by: str, db: Session) -> dict:
    content = await file.read()
    if not content:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Empty file")

    valid_rows, error_rows = parse_excel(content, db)
    imported = 0
    duplicates = 0

    for row in valid_rows:
        email = str(row.get("email_id", "")).strip().lower()
        existing = db.query(CandidateDetail).filter(CandidateDetail.email_id == email).first()
        if existing:
            duplicates += 1
            error_rows.append({**row, "error": "Duplicate email"})
            continue

        # Map skill name to ID
        skill_name = str(row.get("skill", "") or row.get("tech_name", "")).strip()
        skill_id = None
        if skill_name:
            tech = db.query(TechnologyMaster).filter(TechnologyMaster.tech_name == skill_name).first()
            if tech:
                skill_id = tech.id

        candidate = CandidateDetail(
            candidate_name=str(row.get("candidate_name", "")),
            email_id=email,
            contact_number=str(row.get("contact_number", "") or ""),
            gender=str(row.get("gender", "") or ""),
            total_exp=str(row.get("total_exp", "") or ""),
            rel_exp=str(row.get("rel_exp", "") or ""),
            current_company=str(row.get("current_company", "") or ""),
            current_location=str(row.get("current_location", "") or ""),
            notice_period=str(row.get("notice_period", "") or ""),
            current_ctc=str(row.get("current_ctc", "") or ""),
            exp_ctc=str(row.get("exp_ctc", "") or ""),
            source=str(row.get("source", "") or ""),
            referred_vendor=str(row.get("referred_vendor", "") or ""),
            skill_id=skill_id,
            created_by=created_by,
        )
        db.add(candidate)
        imported += 1

    db.commit()

    error_file_url = None
    if error_rows:
        export_path = generate_export_path("candidate_errors")
        wb = Workbook()
        ws = wb.active
        headers = list(error_rows[0].keys())
        ws.append(headers)
        for r in error_rows:
            ws.append([r.get(h) for h in headers])
        wb.save(export_path)
        error_file_url = f"/api/v1/files/exports/{export_path.name}"

    return {
        "imported": imported,
        "duplicates": duplicates,
        "errors": len(error_rows) - duplicates,
        "error_file_url": error_file_url,
    }


def get_candidate(candidate_id: int, db: Session) -> CandidateDetail:
    c = db.query(CandidateDetail).filter(CandidateDetail.candidate_detail_id == candidate_id).first()
    if not c:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
    return c


def update_candidate(candidate_id: int, data: CandidateUpdate, db: Session) -> CandidateDetail:
    c = get_candidate(candidate_id, db)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(c, field, value)
    db.commit()
    db.refresh(c)
    return c


def validate_status_transition(current_status: str, new_status: str, db: Session) -> None:
    valid_next = _get_valid_next_statuses(current_status, db)
    if new_status not in valid_next:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid transition from '{current_status}' to '{new_status}'",
        )


def change_status(candidate_id: int, req: StatusChangeRequest, changed_by: str, db: Session) -> CandidateDetail:
    c = get_candidate(candidate_id, db)
    validate_status_transition(c.overall_status, req.to_status, db)

    history = CandidateStatusHistory(
        candidate_detail_id=candidate_id,
        from_status=c.overall_status,
        to_status=req.to_status,
        changed_by=changed_by,
        notes=req.notes,
    )
    db.add(history)
    c.overall_status = req.to_status
    db.commit()
    db.refresh(c)
    return c


async def add_comment(
    candidate_id: int,
    comment_data: CommentCreate,
    attachment: UploadFile | None,
    created_by: str,
    db: Session,
) -> CandidateComments:
    get_candidate(candidate_id, db)  # validates existence
    attachment_path = None
    attachment_filename = None
    if attachment and attachment.filename:
        attachment_path = await save_file(attachment, "attachments")
        attachment_filename = attachment.filename

    comment = CandidateComments(
        candidate_detail_id=candidate_id,
        comment_text=comment_data.comment_text,
        attachment_path=attachment_path,
        attachment_filename=attachment_filename,
        created_by=created_by,
    )
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


def list_candidates(
    db: Session,
    page: int = 1,
    page_size: int = 20,
    status_filter: str | None = None,
    skill_id: int | None = None,
    created_by: str | None = None,
) -> dict:
    query = db.query(CandidateDetail)
    if status_filter:
        query = query.filter(CandidateDetail.overall_status == status_filter)
    if skill_id:
        query = query.filter(CandidateDetail.skill_id == skill_id)
    if created_by:
        query = query.filter(CandidateDetail.created_by == created_by)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def update_doj(candidate_id: int, doj: date, db: Session) -> CandidateDetail:
    c = get_candidate(candidate_id, db)
    c.doj = doj
    db.commit()
    db.refresh(c)
    return c


def update_skill(candidate_id: int, skill_id: int, db: Session) -> CandidateDetail:
    c = get_candidate(candidate_id, db)
    tech = db.query(TechnologyMaster).filter(TechnologyMaster.id == skill_id).first()
    if not tech:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Skill not found")
    c.skill_id = skill_id
    db.commit()
    db.refresh(c)
    return c


async def upload_resume(candidate_id: int, resume_file: UploadFile, db: Session) -> CandidateDetail:
    c = get_candidate(candidate_id, db)
    if not resume_file or not resume_file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Resume file is required")

    filename = resume_file.filename.lower()
    if not filename.endswith((".pdf", ".doc", ".docx")):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only .pdf, .doc, and .docx resume files are allowed",
        )

    saved_name = await save_file(resume_file, "resumes")
    c.resume_path = saved_name
    db.commit()
    db.refresh(c)
    return c
