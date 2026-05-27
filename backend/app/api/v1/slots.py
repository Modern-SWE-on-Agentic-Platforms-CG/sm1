from fastapi import APIRouter, Depends, UploadFile, File, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.slot import SlotCreate
from app.schemas.common import success_response
from app.services import slot_service
from app.models.employee import EmployeeMaster

router = APIRouter(prefix="/api/v1/slots", tags=["slots"])


@router.post("", status_code=201)
def create_slot(
    body: SlotCreate,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Interviewer")),
):
    slot = slot_service.create_slot(current_user.emp_id, body, db)
    return success_response(slot)


@router.post("/bulk", status_code=201)
def bulk_upload_slots(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Interviewer", "Admin")),
):
    result = slot_service.bulk_create_slots(current_user.emp_id, file, db)
    return success_response(result)


@router.get("")
def list_slots(
    status: str | None = None,
    is_weekend_drive: bool | None = None,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role("Interviewer", "Recruiter", "Admin")),
):
    slots = slot_service.list_slots(current_user.emp_id, db, status, is_weekend_drive)
    return success_response({"items": slots, "total": len(slots)})


@router.put("/{slot_id}")
def update_slot(
    slot_id: int,
    new_status: str = Query(...),
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Interviewer", "Admin")),
):
    slot = slot_service.update_slot_status(slot_id, new_status, db)
    return success_response(slot)


@router.delete("/{slot_id}", status_code=204)
def delete_slot(
    slot_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Interviewer", "Admin")),
):
    slot_service.delete_slot(slot_id, db)
