# Research: Smart Recruit Platform — Phase 0

**Date**: 2026-05-26 | **Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

All NEEDS CLARIFICATION items from the Technical Context have been resolved below.

---

## R-001: Authentication Mechanism

**Decision**: Local JWT authentication (email + password login), HS256 algorithm, `passlib[bcrypt]` for password hashing.

**Rationale**: The original Keycloak/Corporate SSO is an external dependency unavailable for local development. A standard JWT flow using `python-jose` and `passlib[bcrypt]` provides the same role-based access patterns. All auth logic is encapsulated in `backend/app/core/security.py` — swapping to Keycloak in a later phase requires only changing the token-issuance step, not any downstream RBAC code.

**Alternatives considered**:
- Keycloak Docker: rejected — adds multi-container dependency, realm import complexity, and startup time for no functional gain in local dev.
- OAuth2 with third-party provider: rejected — requires public callback URL; not suitable for offline-first local dev.

**Implementation notes**:
- `POST /api/v1/auth/login` accepts `{ email, password }` → verifies bcrypt hash → issues JWT.
- JWT payload: `{ sub: email, emp_id, roles: [...], bu, exp }`.
- Token lifetime: 8 hours (configurable via `JWT_EXPIRE_MINUTES` env var).
- **Token storage**: httpOnly cookie (`Set-Cookie: access_token=...; HttpOnly; SameSite=Lax`) is the production-grade approach (prevents XSS token theft). For isolated local development, `localStorage` is acceptable as a documented fallback — this must be noted in `quickstart.md` and resolved before any shared deployment.

---

## R-002: File Storage

**Decision**: Local filesystem under `backend/uploads/`, accessed via `backend/app/core/file_storage.py`.

**Rationale**: AWS S3 requires cloud credentials unavailable in local dev. Abstracting all file operations behind `save_file(bucket, filename, content)` / `get_file_path(bucket, filename)` means the storage backend can be swapped to S3 (or MinIO) by changing only `file_storage.py`, with no changes to the service layer.

**Directory structure**:
```
backend/uploads/
├── resumes/           # Candidate resumes (PDF/DOC)
├── attachments/       # Candidate comment attachments
├── feedback_pdfs/     # Generated feedback PDFs
├── exports/           # Generated Excel export files
└── videos/            # Interview recordings (Phase 2+)
```

**Size limits**: 5 MB per file (enforced in FastAPI route with `UploadFile` content-length check). Videos: up to 50 MB.

**Alternatives considered**:
- MinIO (local S3-compatible): rejected — requires Docker and MinIO client dependency for no functional benefit at this stage.

---

## R-003: Email Notifications

**Decision**: Log-only email handler. All email sends write to `backend/logs/email.log` as structured JSON lines. No actual SMTP connection is made.

**Rationale**: AWS SES and any real SMTP server require external configuration unavailable locally. The log file provides full auditability of what would have been sent (recipient, subject, body, timestamp) — sufficient for verifying notification logic in development.

**Log format** (JSON line per email):
```json
{
  "timestamp": "2026-05-26T09:00:00Z",
  "to": ["interviewer@example.com", "candidate@example.com"],
  "subject": "Interview Scheduled — Java L1 on 2026-05-27",
  "body": "...",
  "trigger": "booking_created",
  "booking_id": 42
}
```

**Upgrade path**: Replace `email_logger.py` with an `smtplib`/`aiosmtplib` implementation reading `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` from env vars — no other code changes required.

---

## R-004: Meeting Link Generation

**Decision**: Server-side UUID-based meeting link: `https://meet.smartrecruit.local/meeting/{uuid4()}`.

**Rationale**: Microsoft Teams Graph API requires Azure AD credentials and a licensed Teams tenant — unavailable for local dev. The generated link is a stable identifier for the booking and can be replaced with real Teams links by swapping `generate_meeting_link()` in `booking_service.py`.

---

## R-005: Excel Parsing Strategy

**Decision**: `pandas` + `openpyxl` for all Excel upload processing.

**Rationale**: `pandas.read_excel()` with `openpyxl` engine handles large files efficiently (500+ row candidate sheets complete well within the 60 s SLA). Column schema validation uses explicit column-name checks before row processing. Duplicate detection is done in-Python before any DB writes.

**Candidate Excel column schema** (from BRD §3.4 — 54 columns):
Sr No., Duplicate (Y/N), Recvd Dt, Recvd Aging (Days), Quarter, Profile Rec YY/M, Candidate Name, TotalExp(Y), Relexp(Y), Tower, Skill Group, Skill, Gender, Source, Vendor/Partner Name, Email ID, Contact No, Current Co, Current Loc, Preferred/Offered Loc, Current CTC, Exp CTC, Offer CTC, Counter Offered, Revised Offered, Notice Period, Aspiring Test (Y/N), Test Score, Overall Status, Rejection Reason, Declined Reason, Comments, L2 Rank, L1 Date, L1 Aging (Days), L1 Type, L1 Panel, L2 Date, L2 Aging (Days), L2 Type, L2 Panel, L3 date/Type/Panel, HR Coordinator, PMO Coordinator, JR Mapped/SF ID/SO ID, Account Name, BU Head Apprvd Dt, Level Offered, DOJ, Dashboard Status, Offered Date, Offered M/YY, Referral Person, College, Level Based On Exp, Recruitment_Candidate_id, JR_ID, Recruitment_conversion_id

**Panel slot Excel**: date, from_time, to_time, technology/skill (4 columns minimum).

**Error handling**: Rows failing validation are collected in a list and returned in the response as `{ "imported": N, "errors": [{row, reason}] }`. A downloadable error Excel file is generated only when errors exist.

---

## R-006: PDF Generation

**Decision**: ReportLab (`reportlab` Python package).

**Rationale**: Pure-Python; no system-level binary dependencies (unlike WeasyPrint which needs Cairo/Pango). Feedback form PDFs have a known fixed structure (sections + parameters + scores + recommendation) that maps directly to ReportLab's `Platypus` flowable system. Generated PDFs are stored in `uploads/feedback_pdfs/`.

**Alternatives considered**:
- WeasyPrint: rejected — requires system libraries (cairo, pango, gdk-pixbuf) that complicate Windows local dev setup.
- Jinja2 → HTML → headless Chrome: rejected — adds browser dependency; over-engineered for fixed-layout documents.

---

## R-007: Frontend Calendar Component

**Decision**: `@fullcalendar/react` with `timeGridWeek` and `timeGridDay` plugins.

**Rationale**: Purpose-built interview/slot calendar. Supports `eventColor` per-event (green/pink/grey/yellow for slot status), click handlers for slot creation/edit, and `dateClick` for empty slot creation. Integrates natively with React via hooks.

**Colour mapping**:
| Slot status | Calendar colour |
|---|---|
| `Available` | `#4CAF50` (green) |
| `Booked` | `#E91E63` (pink) |
| `Interviewed` | `#9E9E9E` (grey) |
| `Pending` | `#FFC107` (yellow) |

---

## R-008: Frontend State Management

**Decision**: React Context + `useReducer` (no Redux).

**Rationale**: Auth state (current user, roles, token) is the only global state required in Phase 1. All other state is component-local or fetched via Axios on demand. Redux would add ~3 KB boilerplate with no benefit at this scope. If Phase 3 analytics introduce complex cross-component filter state, a lightweight store (Zustand) can be added — no rewrite required.

---

## R-009: API Versioning & Response Envelope

**Decision**: All routes prefixed `/api/v1/`. All responses use:
```json
{
  "data": <T>,
  "error": null,
  "status": "success"
}
```
or on error:
```json
{
  "data": null,
  "error": "Human-readable message",
  "status": "error"
}
```

**Implementation**: `ApiResponse[T]` generic Pydantic model in `backend/app/schemas/common.py`.
FastAPI exception handlers map `HTTPException` and validation errors to the standard envelope.

---

## R-010: Background Job Scheduler (Phase 4)

**Decision**: APScheduler 3.x (in-process, `AsyncIOScheduler`).

**Rationale**: Jobs run in the same Python process as FastAPI (no separate worker). APScheduler integrates with FastAPI's lifespan events (`startup`/`shutdown`). Sufficient for the 4 scheduled jobs (daily SLA alerts, 15-minute interview reminders, daily feedback reminders, twice-daily export cleanup). For Phase 4, jobs are defined in `backend/app/services/scheduler.py`.

---

## R-011: Status Transition Rules

**Decision**: Transition rules stored in the `status_intermediate_mapping` DB table, not hardcoded.

**Columns**: `id`, `from_status` (VARCHAR), `to_status` (VARCHAR), `allowed_roles` (VARCHAR[]).

**Seed data** (core transitions — full list in `seed_data.py`):
| from_status | to_status |
|---|---|
| Profile Received | L1 Scheduled |
| L1 Scheduled | L1 Selected |
| L1 Scheduled | L1 Rejected |
| L1 Selected | L2 Scheduled |
| L2 Scheduled | L2 Selected |
| L2 Scheduled | L2 Rejected |
| L2 Selected | Offered |
| Offered | Offer Accepted |
| Offered | Offer Declined |
| Offer Accepted | Joined |
| Offer Accepted | Not Joined |

**Validation**: `candidate_service.validate_transition(from_status, to_status, user_role)` queries this table before any status change; returns 400 if transition is invalid.

---

## R-012: Role-Based Access Control

**Decision**: `require_role(*allowed_roles)` FastAPI dependency factory injected into each route.

**Implementation**:
```python
# core/security.py
def require_role(*roles: str) -> Callable:
    async def dependency(current_user: Employee = Depends(get_current_user)):
        if current_user.active_role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    return dependency

# Route usage
@router.post("/slots", dependencies=[Depends(require_role("Interviewer", "Admin"))])
```

**Role routing table** (frontend `SelectRolePage`):
| Role | BU | Home route |
|---|---|---|
| Interviewer | any | `/dashboard` |
| Recruiter | non-SAP | `/todolist` |
| Recruiter | SAP | `/upload` |
| PMO | non-SAP | `/todolist` |
| PMO | SAP | `/upload` |
| Practice Lead | any | `/todolist` |
| Lead | any | `/upload` |
| Tower Lead | any | `/work-flow` |
| SL-BU Lead | any | `/work-flow` |
| NA Lead | any | `/work-flow` |
| Recruiter Lead | any | `/work-flow` |
| BU Admin | any | `/master-data` |
| Practice Admin | any | `/master-data` |
| Admin/SuperUser | any | `/candidate-referral` |
| Referral SPOC | any | `/candidate-referral` |
