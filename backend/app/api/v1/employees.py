from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.employee import EmployeeCreate, EmployeeUpdate
from app.schemas.common import success_response
from app.services import employee_service
from app.models.master_data import RoleMaster, TowerMaster

router = APIRouter(prefix="/api/v1", tags=["employees"])


@router.post("/employees", status_code=201)
def create_employee(
    body: EmployeeCreate,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin")),
):
    return success_response(employee_service.create_employee(body, db))


@router.get("/employees")
def list_employees(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    bu: str | None = None,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin", "RecruiterLead")),
):
    return success_response(employee_service.list_employees(db, page, page_size, bu))


@router.get("/employees/{emp_id}")
def get_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin", "RecruiterLead")),
):
    return success_response(employee_service.get_employee(emp_id, db))


@router.put("/employees/{emp_id}")
def update_employee(
    emp_id: int,
    body: EmployeeUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin")),
):
    return success_response(employee_service.update_employee(emp_id, body, db))


@router.delete("/employees/{emp_id}", status_code=204)
def delete_employee(
    emp_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin")),
):
    employee_service.delete_employee(emp_id, db)


@router.get("/panel/roles")
def get_panel_roles(db: Session = Depends(get_db)):
    roles = db.query(RoleMaster).all()
    return success_response([{"id": r.id, "role_name": r.role_name} for r in roles])


@router.get("/panel/bu")
def get_panel_bu(
    email: str,
    db: Session = Depends(get_db),
    _: object = Depends(require_role()),
):
    from app.models.employee import EmployeeMaster
    emp = db.query(EmployeeMaster).filter(EmployeeMaster.email_id == email).first()
    bu_name = emp.bu if emp else None
    return success_response({"bu_name": bu_name})


@router.get("/panel/technologies")
def get_panel_technologies(
    db: Session = Depends(get_db),
    _: object = Depends(require_role()),
):
    return success_response(employee_service.list_technologies(db))
