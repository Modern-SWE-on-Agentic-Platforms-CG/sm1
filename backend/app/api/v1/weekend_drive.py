from fastapi import APIRouter, Depends, Query, UploadFile, File
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.common import success_response
from app.services import slot_service

router = APIRouter(prefix="/api/v1/weekend-drive", tags=["weekend-drive"])


@router.get("/slots")
def list_weekend_slots(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Recruiter", "RecruiterLead", "Admin")),
):
    result = slot_service.get_weekend_drive_slots(db, page, page_size)
    return success_response(result)


@router.post("/import", status_code=201)
async def import_weekend_drive(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user=Depends(require_role("Recruiter", "RecruiterLead", "Admin")),
):
    result = await slot_service.bulk_import_weekend_drive(file, current_user.email_id, db)
    return success_response(result)
