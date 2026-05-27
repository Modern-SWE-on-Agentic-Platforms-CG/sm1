from fastapi import APIRouter, Depends, Response, Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.core.database import get_db
from app.core.config import settings
from app.core.security import decode_token
from app.schemas.auth import LoginRequest, TokenResponse, MeResponse
from app.schemas.common import success_response, error_response
from app.services.auth_service import authenticate_user, build_token_response, get_current_user
from app.models.master_data import RoleMaster
from app.models.employee import EmployeeRoleDetails

router = APIRouter(prefix="/api/v1/auth", tags=["auth"])
_bearer = HTTPBearer(auto_error=False)
_limiter = Limiter(key_func=get_remote_address)


@router.post("/login")
@_limiter.limit("10/minute")
def login(request: Request, body: LoginRequest, response: Response, db: Session = Depends(get_db)):
    employee = authenticate_user(body.email, body.password, db)
    token_data = build_token_response(employee, db)

    # Set httpOnly cookie
    response.set_cookie(
        key="access_token",
        value=token_data["access_token"],
        httponly=True,
        samesite="lax",
        max_age=settings.JWT_EXPIRE_MINUTES * 60,
        path="/",
    )
    return success_response(token_data)


@router.get("/me")
def me(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = Depends(_bearer),
    db: Session = Depends(get_db),
):
    token = None
    if credentials and credentials.credentials:
        token = credentials.credentials
    else:
        token = request.cookies.get("access_token")

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")

    employee = get_current_user(token, db)
    roles = (
        db.query(RoleMaster.role_name)
        .join(EmployeeRoleDetails, EmployeeRoleDetails.role_id == RoleMaster.id)
        .filter(EmployeeRoleDetails.emp_id == employee.emp_id)
        .all()
    )
    role_names = [r.role_name for r in roles]
    payload = decode_token(token)

    return success_response(
        {
            "emp_id": employee.emp_id,
            "emp_name": employee.emp_name,
            "email_id": employee.email_id,
            "bu": employee.bu,
            "roles": role_names,
            "active_role": payload.get("active_role"),
        }
    )


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token", path="/")
    return success_response({"message": "Logged out successfully"})
