import io
from datetime import datetime
from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from sqlalchemy import and_

import pandas as pd
from openpyxl import Workbook

from app.models.interview import InterviewerCalendar
from app.models.employee import EmployeeMaster
from app.schemas.slot import SlotCreate
from app.core.file_storage import generate_export_path


def overlap_check(emp_id: int, from_time: datetime, to_time: datetime, db: Session, exclude_id: int | None = None) -> bool:
    query = db.query(InterviewerCalendar).filter(
        InterviewerCalendar.emp_id == emp_id,
        InterviewerCalendar.slot_status != "Cancelled",
        InterviewerCalendar.from_time < to_time,
        InterviewerCalendar.to_time > from_time,
    )
    if exclude_id:
        query = query.filter(InterviewerCalendar.interviewer_calendar_id != exclude_id)
    return query.first() is not None


def create_slot(emp_id: int, data: SlotCreate, db: Session) -> InterviewerCalendar:
    if overlap_check(emp_id, data.from_time, data.to_time, db):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slot overlaps with an existing slot")
    slot = InterviewerCalendar(
        emp_id=emp_id,
        skill_id=data.skill_id,
        slot_date=data.slot_date,
        from_time=data.from_time,
        to_time=data.to_time,
        is_weekend_drive=data.is_weekend_drive,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    return slot


def bulk_create_slots(
    emp_id: int,
    file: UploadFile,
    db: Session,
    is_weekend_drive: bool = False,
) -> dict:
    content = file.file.read()
    try:
        df = pd.read_excel(io.BytesIO(content))
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Excel file")

    required_cols = {"slot_date", "from_time", "to_time"}
    if not required_cols.issubset(set(df.columns.str.lower())):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Excel must have columns: {required_cols}",
        )
    df.columns = [c.lower() for c in df.columns]

    created = 0
    error_rows: list[dict] = []

    for idx, row in df.iterrows():
        try:
            slot_date = pd.to_datetime(row["slot_date"]).date()
            from_time = pd.to_datetime(row["from_time"])
            to_time = pd.to_datetime(row["to_time"])
            if from_time >= to_time:
                raise ValueError("from_time must be before to_time")
            skill_id = int(row["skill_id"]) if "skill_id" in row and pd.notna(row["skill_id"]) else None

            if overlap_check(emp_id, from_time, to_time, db):
                error_rows.append({**row.to_dict(), "error": "Overlap with existing slot"})
                continue

            slot = InterviewerCalendar(
                emp_id=emp_id,
                skill_id=skill_id,
                slot_date=slot_date,
                from_time=from_time,
                to_time=to_time,
                is_weekend_drive=is_weekend_drive,
            )
            db.add(slot)
            created += 1
        except Exception as e:
            error_rows.append({**row.to_dict(), "error": str(e)})

    db.commit()

    error_file_url = None
    if error_rows:
        export_path = generate_export_path("slot_errors")
        wb = Workbook()
        ws = wb.active
        headers = list(error_rows[0].keys())
        ws.append(headers)
        for r in error_rows:
            ws.append([r.get(h) for h in headers])
        wb.save(export_path)
        error_file_url = f"/api/v1/files/exports/{export_path.name}"

    return {"created": created, "errors": len(error_rows), "error_file_url": error_file_url}


def list_slots(
    emp_id: int | None,
    db: Session,
    status_filter: str | None = None,
    is_weekend_drive: bool | None = None,
) -> list[InterviewerCalendar]:
    query = db.query(InterviewerCalendar)
    if emp_id:
        query = query.filter(InterviewerCalendar.emp_id == emp_id)
    if status_filter:
        query = query.filter(InterviewerCalendar.slot_status == status_filter)
    if is_weekend_drive is not None:
        query = query.filter(InterviewerCalendar.is_weekend_drive == is_weekend_drive)
    return query.all()


def update_slot_status(slot_id: int, new_status: str, db: Session) -> InterviewerCalendar:
    slot = db.query(InterviewerCalendar).filter(
        InterviewerCalendar.interviewer_calendar_id == slot_id
    ).first()
    if not slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
    slot.slot_status = new_status
    db.commit()
    db.refresh(slot)
    return slot


def delete_slot(slot_id: int, db: Session) -> None:
    slot = db.query(InterviewerCalendar).filter(
        InterviewerCalendar.interviewer_calendar_id == slot_id
    ).first()
    if not slot:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Slot not found")
    if slot.slot_status == "Booked":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete a booked slot",
        )
    db.delete(slot)
    db.commit()


def get_weekend_drive_slots(db: Session, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(InterviewerCalendar).filter(InterviewerCalendar.is_weekend_drive == True)
    total = query.count()
    items = query.order_by(InterviewerCalendar.slot_date.desc()).offset((page - 1) * page_size).limit(page_size).all()
    return {"items": items, "total": total, "page": page, "page_size": page_size}


async def bulk_import_weekend_drive(file, created_by: str, db: Session) -> dict:
    from fastapi import UploadFile
    return bulk_create_slots.__wrapped__(None, file, db, is_weekend_drive=True) if hasattr(bulk_create_slots, '__wrapped__') else await _do_bulk_import_weekend_drive(file, created_by, db)


async def _do_bulk_import_weekend_drive(file, created_by: str, db: Session) -> dict:
    import io
    import pandas as pd
    content = await file.read()
    try:
        df = pd.read_excel(io.BytesIO(content))
    except Exception:
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Excel file")

    df.columns = [c.lower() for c in df.columns]
    required = {"emp_id", "slot_date", "from_time", "to_time"}
    if not required.issubset(set(df.columns)):
        from fastapi import HTTPException, status
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Excel must have: {required}")

    created = 0
    errors = []
    for _, row in df.iterrows():
        try:
            emp_id_val = int(row["emp_id"])
            slot_date = pd.to_datetime(row["slot_date"]).date()
            from_time = pd.to_datetime(row["from_time"])
            to_time = pd.to_datetime(row["to_time"])
            skill_id = int(row["skill_id"]) if "skill_id" in row and pd.notna(row.get("skill_id")) else None
            if not overlap_check(emp_id_val, from_time, to_time, db):
                slot = InterviewerCalendar(
                    emp_id=emp_id_val, skill_id=skill_id,
                    slot_date=slot_date, from_time=from_time, to_time=to_time,
                    is_weekend_drive=True, created_by=created_by,
                )
                db.add(slot)
                created += 1
            else:
                errors.append({"row": str(row.to_dict()), "error": "Overlap"})
        except Exception as exc:
            errors.append({"row": str(row.to_dict()), "error": str(exc)})
    db.commit()
    return {"created": created, "errors": len(errors)}
