from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.security import verify_password, create_access_token, decode_token
from app.models.employee import EmployeeMaster, EmployeeRoleDetails
from app.models.master_data import RoleMaster


def _get_employee_roles(employee: EmployeeMaster, db: Session) -> list[str]:
    roles = (
        db.query(RoleMaster.role_name)
        .join(EmployeeRoleDetails, EmployeeRoleDetails.role_id == RoleMaster.id)
        .filter(EmployeeRoleDetails.emp_id == employee.emp_id)
        .all()
    )
    return [r.role_name for r in roles]


def authenticate_user(email: str, password: str, db: Session) -> EmployeeMaster:
    employee = (
        db.query(EmployeeMaster)
        .filter(EmployeeMaster.email_id == email, EmployeeMaster.is_active == True)  # noqa: E712
        .first()
    )
    if not employee or not verify_password(password, employee.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return employee


def get_current_user(token: str, db: Session) -> EmployeeMaster:
    payload = decode_token(token)
    email: str | None = payload.get("sub")
    if not email:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    employee = (
        db.query(EmployeeMaster)
        .filter(EmployeeMaster.email_id == email, EmployeeMaster.is_active == True)  # noqa: E712
        .first()
    )
    if not employee:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return employee


def build_token_response(employee: EmployeeMaster, db: Session) -> dict:
    roles = _get_employee_roles(employee, db)
    token = create_access_token({"sub": employee.email_id, "roles": roles})
    return {
        "access_token": token,
        "token_type": "bearer",
        "employee": {
            "emp_id": employee.emp_id,
            "emp_name": employee.emp_name,
            "email_id": employee.email_id,
            "bu": employee.bu,
            "roles": roles,
        },
    }
