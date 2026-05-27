from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import hash_password
from app.models.employee import EmployeeMaster, EmployeeRoleDetails, EmployeeTechnologyDetails, EmployeeTowerDetails
from app.models.master_data import RoleMaster, TechnologyMaster
from app.schemas.employee import EmployeeCreate, EmployeeUpdate


def _employee_to_out(emp: EmployeeMaster, db: Session) -> dict:
    roles = (
        db.query(RoleMaster.role_name)
        .join(EmployeeRoleDetails, EmployeeRoleDetails.role_id == RoleMaster.id)
        .filter(EmployeeRoleDetails.emp_id == emp.emp_id)
        .all()
    )
    techs = (
        db.query(TechnologyMaster.tech_name)
        .join(EmployeeTechnologyDetails, EmployeeTechnologyDetails.technology_id == TechnologyMaster.id)
        .filter(EmployeeTechnologyDetails.emp_id == emp.emp_id)
        .all()
    )
    towers = [t.tower_name for t in emp.towers]
    return {
        "emp_id": emp.emp_id,
        "emp_name": emp.emp_name,
        "email_id": emp.email_id,
        "location": emp.location,
        "grade": emp.grade,
        "bu": emp.bu,
        "practice": emp.practice,
        "market_unit": emp.market_unit,
        "account": emp.account,
        "organisation": emp.organisation,
        "is_active": emp.is_active,
        "created_at": emp.created_at,
        "roles": [r.role_name for r in roles],
        "technologies": [t.tech_name for t in techs],
        "tower_names": towers,
    }


def create_employee(data: EmployeeCreate, db: Session) -> dict:
    existing = db.query(EmployeeMaster).filter(EmployeeMaster.email_id == data.email_id).first()
    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")

    emp = EmployeeMaster(
        emp_name=data.emp_name,
        email_id=data.email_id,
        password_hash=hash_password(data.password),
        location=data.location,
        grade=data.grade,
        bu=data.bu,
        practice=data.practice,
        market_unit=data.market_unit,
        account=data.account,
        organisation=data.organisation,
    )
    db.add(emp)
    db.flush()

    for role_id in data.role_ids:
        db.add(EmployeeRoleDetails(emp_id=emp.emp_id, role_id=role_id))
    for tech_id in data.technology_ids:
        db.add(EmployeeTechnologyDetails(emp_id=emp.emp_id, technology_id=tech_id))
    for tower_name in data.tower_names:
        db.add(EmployeeTowerDetails(emp_id=emp.emp_id, tower_name=tower_name))

    db.commit()
    db.refresh(emp)
    return _employee_to_out(emp, db)


def list_employees(db: Session, page: int = 1, page_size: int = 20, bu: str | None = None) -> dict:
    query = db.query(EmployeeMaster)
    if bu:
        query = query.filter(EmployeeMaster.bu == bu)
    total = query.count()
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "items": [_employee_to_out(e, db) for e in items],
        "total": total,
        "page": page,
        "page_size": page_size,
    }


def get_employee(emp_id: int, db: Session) -> dict:
    emp = db.query(EmployeeMaster).filter(EmployeeMaster.emp_id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    return _employee_to_out(emp, db)


def update_employee(emp_id: int, data: EmployeeUpdate, db: Session) -> dict:
    emp = db.query(EmployeeMaster).filter(EmployeeMaster.emp_id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")

    for field in ("emp_name", "location", "grade", "bu", "practice", "market_unit", "account", "organisation", "is_active"):
        value = getattr(data, field)
        if value is not None:
            setattr(emp, field, value)

    if data.role_ids is not None:
        db.query(EmployeeRoleDetails).filter(EmployeeRoleDetails.emp_id == emp_id).delete()
        for role_id in data.role_ids:
            db.add(EmployeeRoleDetails(emp_id=emp_id, role_id=role_id))

    if data.technology_ids is not None:
        db.query(EmployeeTechnologyDetails).filter(EmployeeTechnologyDetails.emp_id == emp_id).delete()
        for tech_id in data.technology_ids:
            db.add(EmployeeTechnologyDetails(emp_id=emp_id, technology_id=tech_id))

    if data.tower_names is not None:
        db.query(EmployeeTowerDetails).filter(EmployeeTowerDetails.emp_id == emp_id).delete()
        for name in data.tower_names:
            db.add(EmployeeTowerDetails(emp_id=emp_id, tower_name=name))

    db.commit()
    db.refresh(emp)
    return _employee_to_out(emp, db)


def delete_employee(emp_id: int, db: Session) -> None:
    emp = db.query(EmployeeMaster).filter(EmployeeMaster.emp_id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
    emp.is_active = False
    db.commit()


def list_technologies(db: Session) -> list[dict]:
    techs = db.query(TechnologyMaster).filter(TechnologyMaster.is_active == True).all()  # noqa: E712
    return [{"id": t.id, "tech_name": t.tech_name, "skill_group": t.skill_group} for t in techs]
