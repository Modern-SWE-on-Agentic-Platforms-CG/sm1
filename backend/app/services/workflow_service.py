from __future__ import annotations

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.workflow import OfferWorkflow, WorkflowComments, CTCHistory
from app.models.candidate import CandidateDetail
from app.models.master_data import ApproverDLMapping
from app.schemas.workflow import WorkflowAction, ApproverDLUpdate
from app.core.logging import get_logger

logger = get_logger(__name__)

# Level progression for multi-level approval
LEVEL_ORDER = ["TowerLead", "SLBULead", "NALead"]
ARC_THRESHOLD_PERCENT = 15.0  # configurable in future via DB setting


def submit_for_approval(candidate_id: int, submitted_by: str, db: Session) -> OfferWorkflow:
    existing = db.query(OfferWorkflow).filter(
        OfferWorkflow.candidate_detail_id == candidate_id,
        OfferWorkflow.status == "Pending",
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Workflow already in progress for this candidate")

    workflow = OfferWorkflow(
        candidate_detail_id=candidate_id,
        current_level="TowerLead",
        status="Pending",
    )
    db.add(workflow)
    db.flush()

    comment = WorkflowComments(
        workflow_id=workflow.id,
        commenter_email=submitted_by,
        comment_text="Submitted for approval",
        action="Comment",
    )
    db.add(comment)
    db.commit()
    db.refresh(workflow)
    return workflow


def get_workflow_candidates(approver_role: str, db: Session, page: int = 1, page_size: int = 20) -> dict:
    query = db.query(OfferWorkflow, CandidateDetail).join(
        CandidateDetail,
        OfferWorkflow.candidate_detail_id == CandidateDetail.candidate_detail_id,
    ).filter(
        OfferWorkflow.status == "Pending",
        OfferWorkflow.current_level == approver_role,
    )
    total = query.count()
    rows = query.offset((page - 1) * page_size).limit(page_size).all()

    items = []
    for wf, cand in rows:
        arc = _check_arc(cand)
        items.append({
            "workflow_id": wf.id,
            "candidate_detail_id": cand.candidate_detail_id,
            "candidate_name": cand.candidate_name,
            "skill": None,
            "current_ctc": cand.current_ctc,
            "exp_ctc": cand.exp_ctc,
            "offer_ctc": cand.offer_ctc,
            "current_level": wf.current_level,
            "status": wf.status,
            "arc_deviation": arc,
        })
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def _check_arc(candidate: CandidateDetail) -> bool:
    try:
        if candidate.current_ctc and candidate.offer_ctc:
            base = float(candidate.current_ctc)
            offer = float(candidate.offer_ctc)
            if base > 0:
                deviation = abs(offer - base) / base * 100
                return deviation > ARC_THRESHOLD_PERCENT
    except (ValueError, TypeError):
        pass
    return False


def update_workflow(workflow_id: int, action_data: WorkflowAction, actor_email: str, db: Session) -> dict:
    workflow = db.query(OfferWorkflow).filter(OfferWorkflow.id == workflow_id).first()
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")

    comment = WorkflowComments(
        workflow_id=workflow_id,
        commenter_email=actor_email,
        comment_text=action_data.comment,
        action=action_data.action,
    )
    db.add(comment)

    next_level = None
    if action_data.action == "Approved":
        current_idx = LEVEL_ORDER.index(workflow.current_level) if workflow.current_level in LEVEL_ORDER else -1
        if current_idx >= 0 and current_idx + 1 < len(LEVEL_ORDER):
            next_level = LEVEL_ORDER[current_idx + 1]
            workflow.current_level = next_level
        else:
            workflow.status = "Approved"
    elif action_data.action == "Rejected":
        workflow.status = "Rejected"

    db.commit()
    return {"workflow_id": workflow_id, "status": workflow.status, "next_level": next_level}


def get_comments_history(workflow_id: int, db: Session) -> list:
    return db.query(WorkflowComments).filter(
        WorkflowComments.workflow_id == workflow_id
    ).order_by(WorkflowComments.created_at).all()


def get_ctc_history(candidate_id: int, db: Session) -> list:
    return db.query(CTCHistory).filter(
        CTCHistory.candidate_detail_id == candidate_id
    ).order_by(CTCHistory.changed_at.desc()).all()


def get_approver_dl(db: Session) -> list:
    return db.query(ApproverDLMapping).all()


def update_approver_dl(data: ApproverDLUpdate, db: Session) -> ApproverDLMapping:
    dl = db.query(ApproverDLMapping).filter(ApproverDLMapping.id == data.id).first()
    if not dl:
        raise HTTPException(status_code=404, detail="Approver DL not found")
    dl.dl_email = data.dl_email
    if data.dl_title is not None:
        dl.dl_title = data.dl_title
    db.commit()
    db.refresh(dl)
    return dl


def get_threshold() -> dict:
    return {
        "arc_threshold_percent": ARC_THRESHOLD_PERCENT,
        "description": "Max CTC deviation before ARC flag",
    }
