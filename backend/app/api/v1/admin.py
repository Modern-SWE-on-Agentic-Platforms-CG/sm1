from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import require_role
from app.schemas.admin import (
    TowerCreate, SkillCreate, SkillUpdate, SourceCreate, VendorCreate,
    ApproverDLCreate, RoleCommentCreate
)
from app.schemas.common import success_response
from app.services import admin_service

router = APIRouter(prefix="/api/v1/admin", tags=["admin"])

ADMIN_ROLES = ("Admin",)
BU_ADMIN_ROLES = ("Admin", "BUAdmin", "PracticeAdmin")


# --- Towers ---

@router.get("/towers")
def list_towers(db: Session = Depends(get_db), _: object = Depends(require_role(*BU_ADMIN_ROLES))):
    items = admin_service.list_towers(db)
    return success_response({"items": items})


@router.post("/towers", status_code=201)
def create_tower(body: TowerCreate, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    tower = admin_service.create_tower(body, db)
    return success_response(tower)


@router.delete("/towers/{tower_id}")
def delete_tower(tower_id: int, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    admin_service.delete_tower(tower_id, db)
    return success_response({"message": "Tower deactivated"})


# --- Skills ---

@router.get("/skills")
def list_skills(db: Session = Depends(get_db), _: object = Depends(require_role(*BU_ADMIN_ROLES))):
    items = admin_service.list_skills(db)
    return success_response({"items": items})


@router.post("/skills", status_code=201)
def create_skill(body: SkillCreate, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    skill = admin_service.create_skill(body, db)
    return success_response(skill)


@router.put("/skills/{skill_id}")
def update_skill(skill_id: int, body: SkillUpdate, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    skill = admin_service.update_skill(skill_id, body, db)
    return success_response(skill)


@router.delete("/skills/{skill_id}")
def delete_skill(skill_id: int, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    admin_service.delete_skill(skill_id, db)
    return success_response({"message": "Skill deactivated"})


# --- Sources ---

@router.get("/sources")
def list_sources(db: Session = Depends(get_db), _: object = Depends(require_role(*BU_ADMIN_ROLES))):
    return success_response({"items": admin_service.list_sources(db)})


@router.post("/sources", status_code=201)
def create_source(body: SourceCreate, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    return success_response(admin_service.create_source(body, db))


@router.delete("/sources/{source_id}")
def delete_source(source_id: int, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    admin_service.delete_source(source_id, db)
    return success_response({"message": "Source deactivated"})


# --- Vendors ---

@router.get("/vendors")
def list_vendors(db: Session = Depends(get_db), _: object = Depends(require_role(*BU_ADMIN_ROLES))):
    return success_response({"items": admin_service.list_vendors(db)})


@router.post("/vendors", status_code=201)
def create_vendor(body: VendorCreate, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    return success_response(admin_service.create_vendor(body, db))


@router.delete("/vendors/{vendor_id}")
def delete_vendor(vendor_id: int, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    admin_service.delete_vendor(vendor_id, db)
    return success_response({"message": "Vendor deactivated"})


# --- SAP ---

@router.get("/sap-capabilities")
def list_sap_capabilities(db: Session = Depends(get_db), _: object = Depends(require_role(*BU_ADMIN_ROLES))):
    return success_response({"items": admin_service.list_sap_capabilities(db)})


@router.post("/sap-capabilities", status_code=201)
def create_sap_capability(body: dict, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    cap = admin_service.create_sap_capability(body.get("capability_name", ""), db)
    return success_response(cap)


@router.get("/sap-skills")
def list_sap_skills(db: Session = Depends(get_db), _: object = Depends(require_role(*BU_ADMIN_ROLES))):
    return success_response({"items": admin_service.list_sap_skills(db)})


@router.post("/sap-skills", status_code=201)
def create_sap_skill(body: dict, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    skill = admin_service.create_sap_skill(body.get("skill_name", ""), body.get("capability_id"), db)
    return success_response(skill)


# --- Approver DL ---

@router.get("/approver-dl")
def list_approver_dl(db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    return success_response({"items": admin_service.list_approver_dl(db)})


@router.post("/approver-dl", status_code=201)
def create_approver_dl(body: ApproverDLCreate, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    dl = admin_service.create_approver_dl(body, db)
    return success_response(dl)


@router.delete("/approver-dl/{dl_id}")
def delete_approver_dl(dl_id: int, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    admin_service.delete_approver_dl(dl_id, db)
    return success_response({"message": "Approver DL removed"})


# --- Role Comments ---

@router.get("/role-comments")
def list_role_comments(db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    return success_response({"items": admin_service.list_role_comments(db)})


@router.post("/role-comments", status_code=201)
def create_role_comment(body: RoleCommentCreate, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    comment = admin_service.create_role_comment(body, db)
    return success_response(comment)


@router.delete("/role-comments/{comment_id}")
def delete_role_comment(comment_id: int, db: Session = Depends(get_db), _: object = Depends(require_role(*ADMIN_ROLES))):
    admin_service.delete_role_comment(comment_id, db)
    return success_response({"message": "Role comment deleted"})


# --- Trigger Job (dev/Admin only) ---

@router.get("/trigger-job/{job_name}")
def trigger_job(
    job_name: str,
    db: Session = Depends(get_db),
    _: object = Depends(require_role(*ADMIN_ROLES)),
):
    from app.core import scheduler as sched_module
    valid_jobs = {
        "aging-sla": "job_aging_sla",
        "interview-reminder": "job_interview_reminder",
        "feedback-reminder": "job_feedback_reminder",
        "export-cleanup": "job_export_cleanup",
    }
    if job_name not in valid_jobs:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail=f"Unknown job name: {job_name}")
    
    fn = getattr(sched_module, valid_jobs[job_name], None)
    processed = 0
    if fn:
        try:
            import asyncio
            result = fn(db)
            if asyncio.iscoroutine(result):
                processed = asyncio.get_event_loop().run_until_complete(result) or 0
            else:
                processed = result or 0
        except Exception as exc:
            from app.core.logging import get_logger
            get_logger(__name__).warning(f"Job {job_name} failed: {exc}")

    return success_response({"job_name": job_name, "message": "Job triggered successfully", "entries_processed": processed})
