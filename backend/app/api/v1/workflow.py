from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.models.employee import EmployeeMaster
from app.schemas.common import success_response
from app.schemas.workflow import WorkflowAction, ApproverDLUpdate
from app.services import workflow_service

router = APIRouter(prefix="/api/v1/workflow", tags=["workflow"])

APPROVER_ROLES = ("TowerLead", "SLBULead", "NALead", "RecruiterLead", "Admin")


@router.get("/candidates")
def list_candidates(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role(*APPROVER_ROLES)),
):
    # Determine the role for filtering — use the first matching approver role
    roles = [r.role.role_name for r in current_user.roles]
    approver_role = next((r for r in roles if r in APPROVER_ROLES), "Admin")
    result = workflow_service.get_workflow_candidates(approver_role, db, page, page_size)
    return success_response(result)


@router.post("/{workflow_id}/action")
def workflow_action(
    workflow_id: int,
    body: WorkflowAction,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role(*APPROVER_ROLES)),
):
    result = workflow_service.update_workflow(workflow_id, body, current_user.email_id, db)
    return success_response(result)


@router.get("/{workflow_id}/comments")
def get_comments(
    workflow_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role(*APPROVER_ROLES, "Recruiter")),
):
    comments = workflow_service.get_comments_history(workflow_id, db)
    return success_response({"items": comments})


@router.post("/{workflow_id}/comments", status_code=201)
def add_comment(
    workflow_id: int,
    body: WorkflowAction,
    db: Session = Depends(get_db),
    current_user: EmployeeMaster = Depends(require_role(*APPROVER_ROLES, "Recruiter")),
):
    result = workflow_service.update_workflow(workflow_id, body, current_user.email_id, db)
    return success_response(result)


@router.get("/ctc-history/{candidate_id}")
def ctc_history(
    candidate_id: int,
    db: Session = Depends(get_db),
    _: object = Depends(require_role(*APPROVER_ROLES)),
):
    history = workflow_service.get_ctc_history(candidate_id, db)
    return success_response({"items": history})


@router.get("/threshold")
def threshold(
    _: object = Depends(require_role(*APPROVER_ROLES)),
):
    return success_response(workflow_service.get_threshold())


@router.get("/approver-dl")
def list_approver_dl(
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin")),
):
    items = workflow_service.get_approver_dl(db)
    return success_response({"items": items})


@router.put("/approver-dl")
def update_approver_dl(
    body: ApproverDLUpdate,
    db: Session = Depends(get_db),
    _: object = Depends(require_role("Admin")),
):
    dl = workflow_service.update_approver_dl(body, db)
    return success_response(dl)


@router.get("/possible-status")
def possible_statuses(
    _: object = Depends(require_role("Recruiter", "Admin", "RecruiterLead")),
):
    return success_response({"statuses": ["Pending", "Approved", "Rejected"]})
