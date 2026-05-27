from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class EmployeeSummary(BaseModel):
    emp_id: int
    emp_name: str
    email_id: str
    bu: str | None
    roles: list[str]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    employee: EmployeeSummary


class MeResponse(BaseModel):
    emp_id: int
    emp_name: str
    email_id: str
    bu: str | None
    roles: list[str]
    active_role: str | None = None
