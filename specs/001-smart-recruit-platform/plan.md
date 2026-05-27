# Implementation Plan: Smart Recruit Platform

**Branch**: `001-smart-recruit-platform` | **Date**: 2026-05-26 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `/specs/001-smart-recruit-platform/spec.md`

---

## Summary

**Smart Recruit** is an end-to-end recruitment lifecycle management platform for Capgemini.
It digitises the full hiring pipeline: candidate sourcing, interview scheduling, multi-round
feedback, multi-level offer approval, and date-of-joining tracking. It also includes an
employee referral portal, supply/demand/bench visibility, and recruitment analytics.

**Technical approach**: Three-tier application — React 18 SPA (frontend), FastAPI Python REST
API (backend), PostgreSQL `smarthiremain001` (database). All original Angular/Spring Boot/
Node.js/AWS services are re-implemented within this approved stack. Implementation is
phased by user-story priority (P1 → P2 → P3).

**Phase 1 scope** (this plan): User Stories 1–5 (P1 priority):
1. Authenticated Role-Based Access
2. Panel Registration & Employee Management
3. Interviewer Slot Management
4. Candidate Upload & Profile Management
5. Interview Booking & Scheduling

---

## Technical Context

**Language/Version**: Python 3.11+ (backend) · React 18 / TypeScript 5+ (frontend)

**Primary Dependencies**:
- Backend: FastAPI · SQLAlchemy 2.x · Alembic · python-jose[cryptography] · passlib[bcrypt] · pandas · openpyxl · reportlab · apscheduler
- Frontend: Vite · React Router v6 · Axios · Material UI v5 · @fullcalendar/react · react-hook-form

**Storage**: PostgreSQL 14+ — database `smarthiremain001`, local installation, password via `DB_PASSWORD` env var

**Testing**: pytest + httpx (backend) · Vitest / React Testing Library (frontend)

**Target Platform**: Local server (Uvicorn ASGI, port 8000) + browser SPA (Vite dev, port 5173)

**Project Type**: Three-tier web application (React frontend / Python REST API / PostgreSQL)

**Performance Goals**: API p95 < 500 ms for standard CRUD; bulk Excel upload of 500 rows < 60 s

**Constraints**: All three tiers align with constitution Principles I–V. No legacy stack permitted.

**External service replacements**:
| Original | Local replacement | Rationale |
|---|---|---|
| Keycloak/Corporate SSO | Local JWT auth (email + password, bcrypt) | No external IdP for local dev |
| AWS S3 | `backend/uploads/` local filesystem | Local dev; interface abstracted behind `file_storage.py` |
| AWS SES email | File logger (`logs/email.log`) | Opt-in SMTP upgrade path preserved |
| Microsoft Teams Graph API | UUID-based meeting link generator | No Teams tenant for local dev |

**Scale/Scope**: 11 user personas · 23 feature modules (full list in `BRD-AND-COMPLETE-DOCS.md`)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-checked after Phase 1 design.*

- [x] Frontend implementation uses React (not Angular, Vue, or other frameworks)
- [x] Backend implementation uses Python / FastAPI (not Node.js, Java, or other runtimes)
- [x] Database target is PostgreSQL `smarthiremain001` (no other DB)
- [x] API contracts (Pydantic schemas + `contracts/` docs) defined before frontend development starts
- [x] Alembic migration created for every new DB entity (canonical location: `backend/migrations/`)
- [x] No hard-coded credentials in any source file — all via env vars (`DB_*`, `JWT_SECRET`)
- [x] OWASP Top 10 self-review noted for all auth, file-upload, and status-change endpoints

**Constitution note — JWT storage**: Constitution §IV requires httpOnly cookies in production.
Local-dev builds may use `localStorage` as a documented fallback; any merge to a shared
environment must migrate to httpOnly cookies before the PR is approved.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-smart-recruit-platform/
├── plan.md          ← this file
├── research.md      ← Phase 0 output
├── data-model.md    ← Phase 1 output
├── quickstart.md    ← Phase 1 output
├── contracts/       ← Phase 1 output
│   ├── auth.md
│   ├── employees.md
│   ├── slots.md
│   ├── candidates.md
│   └── bookings.md
└── tasks.md         ← Phase 2 output (/speckit.tasks — NOT created here)
```

### Source Code (repository root)

```text
sm1/
├── backend/
│   ├── app/
│   │   ├── main.py                   # FastAPI app factory, CORS, router registration
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── auth.py           # POST /api/v1/auth/login  GET /api/v1/auth/me
│   │   │       ├── employees.py      # CRUD /api/v1/employees + GET /api/v1/panel/roles /api/v1/panel/bu /api/v1/panel/technologies
│   │   │       ├── slots.py          # /api/v1/slots — interviewer availability
│   │   │       ├── candidates.py     # /api/v1/candidates — bulk upload + profile
│   │   │       └── bookings.py       # /api/v1/bookings — interview scheduling
│   │   ├── models/
│   │   │   ├── employee.py           # EmployeeMaster + EmployeeRoleDetails + EmployeeTechnologyDetails + EmployeeTowerDetails
│   │   │   ├── candidate.py          # CandidateDetail + CandidateInterview + CandidateStatus + CandidateComments
│   │   │   ├── interview.py          # InterviewerCalendar + RecruiterCalendar
│   │   │   └── master_data.py        # RoleMaster + TechnologyMaster + TowerMaster + StatusTransition
│   │   ├── schemas/
│   │   │   ├── common.py             # ApiResponse[T] envelope — { data, error, status }
│   │   │   ├── auth.py
│   │   │   ├── employee.py
│   │   │   ├── slot.py
│   │   │   ├── candidate.py
│   │   │   └── booking.py
│   │   ├── services/
│   │   │   ├── auth_service.py       # verify_password, create_token, decode_token
│   │   │   ├── employee_service.py
│   │   │   ├── slot_service.py       # overlap_check(), bulk_create_slots()
│   │   │   ├── candidate_service.py  # parse_excel(), validate_transition()
│   │   │   └── booking_service.py    # generate_meeting_link(), notify()
│   │   └── core/
│   │       ├── config.py             # Pydantic Settings (reads .env)
│   │       ├── database.py           # Engine, SessionLocal, Base, get_db()
│   │       ├── security.py           # JWT issue/validate, require_role() dependency
│   │       ├── logging.py            # JSON structured logger
│   │       └── file_storage.py       # save_file(), get_file_path() — local filesystem
│   ├── migrations/
│   │   ├── env.py
│   │   └── versions/                 # Numbered Alembic migration scripts
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_auth.py
│   │   ├── test_slots.py
│   │   └── test_candidates.py
│   ├── uploads/                      # Local file storage (git-ignored)
│   │   ├── resumes/
│   │   ├── attachments/
│   │   └── exports/
│   ├── logs/
│   │   └── email.log                 # Email notification log (git-ignored)
│   ├── seed_data.py                  # Seeds roles, admin user, master data
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env                          # Git-ignored; copy from .env.example
│
├── frontend/
│   ├── src/
│   │   ├── main.tsx
│   │   ├── App.tsx                   # Router setup, AuthProvider wrapper
│   │   ├── routes.tsx                # React Router v6 route map
│   │   ├── contexts/
│   │   │   └── AuthContext.tsx       # Token, user, roles state
│   │   ├── hooks/
│   │   │   ├── useAuth.ts
│   │   │   └── useApi.ts
│   │   ├── services/
│   │   │   ├── api.ts                # Axios instance; Bearer token interceptor; 401 handler
│   │   │   ├── authService.ts
│   │   │   ├── employeeService.ts
│   │   │   ├── slotService.ts
│   │   │   ├── candidateService.ts
│   │   │   └── bookingService.ts
│   │   ├── components/
│   │   │   ├── ProtectedRoute.tsx    # Redirect to /login if unauthenticated
│   │   │   ├── RoleRoute.tsx         # Redirect if role not permitted
│   │   │   ├── Navbar.tsx
│   │   │   ├── SlotCalendar.tsx      # FullCalendar wrapper — green/pink/grey/yellow
│   │   │   ├── FileUpload.tsx        # Upload component; enforces 5 MB limit
│   │   │   └── ApiErrorBoundary.tsx  # Surfaces API errors to user (constitution §V)
│   │   └── pages/
│   │       ├── LoginPage.tsx              # /login
│   │       ├── SelectRolePage.tsx         # /selectrole — BU-aware role routing
│   │       ├── DashboardPage.tsx          # /dashboard (Interviewer)
│   │       ├── TodoListPage.tsx           # /todolist (Recruiter/PMO)
│   │       ├── PanelRegistrationPage.tsx  # /register-panel (Admin)
│   │       ├── CandidateListPage.tsx      # /candidate-details
│   │       ├── CandidateDetailPage.tsx    # /candidate-details/:id
│   │       ├── BookingFormPage.tsx        # /booking-form
│   │       └── UploadPage.tsx             # /upload
│   ├── tests/
│   ├── .env                          # VITE_API_BASE_URL=http://localhost:8000
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts
│
├── .env.example                      # Template: all required env var names, no values
├── docker-compose.yml                # Optional: postgres + backend + frontend services
└── .gitignore
```

---

## Complexity Tracking

| Area | Decision | Simpler Alternative Rejected Because |
|---|---|---|
| Phased implementation | P1 only in this plan | Full 23-module plan creates unmanageable task size |
| Local JWT vs Keycloak | Local JWT (email+password) | Keycloak requires Docker + realm config; over-engineered for local dev |
| Local filesystem vs MinIO | `uploads/` directory | MinIO requires Docker; unnecessary for single-server local dev |
| Email logger vs SMTP | File logger only | Real SMTP requires mail server; functional log equivalent for dev |

---

## Phase 0: Research

> **Output**: [research.md](research.md)

All NEEDS CLARIFICATION items resolved. Key decisions documented in `research.md`.

| Decision | Chosen | Rationale |
|---|---|---|
| Auth mechanism | JWT (HS256), bcrypt password hashing | Constitution §IV; standard Python ecosystem |
| Token storage | httpOnly cookie (preferred) / localStorage (local-dev fallback, documented) | Constitution §IV mandate |
| Excel parsing | pandas + openpyxl | pandas handles large sheets; openpyxl for column validation |
| PDF generation | ReportLab | Pure-Python; no system deps; good for structured forms |
| Calendar component | @fullcalendar/react (timeGrid plugin) | Purpose-built; colour-coded events out of the box |
| State management | React Context + useReducer | No global cross-module state beyond auth; Redux unjustified |
| Charts (Phase 3) | Recharts | React-native; sufficient for pie/line/trend charts |
| Background jobs (Phase 4) | APScheduler (in-process) | No separate worker needed at this scale |
| API versioning | `/api/v1/` prefix on all routes | Constitution §II; non-breaking future versioning |
| JSON envelope | `{ "data": T, "error": str\|null, "status": "success"\|"error" }` | Constitution §II mandate |
| Migration canonical location | `backend/migrations/` | Constitution §III mandate |

---

## Phase 1: Design & Contracts

### Data Model

> **Output**: [data-model.md](data-model.md)

Phase 1 entities with PostgreSQL column types, constraints, and relationships.

**Migration order** (dependency-safe — FK order corrected):
1. `001_create_role_master`
2. `002_create_master_data_tables` ← **must precede employee tables** (employee_technology_details FK → technology_master)
3. `003_create_employee_tables`
4. `004_create_interviewer_calendar`
5. `005_create_candidate_tables`

### API Contracts

> **Output**: [contracts/](contracts/)

All endpoint contracts defined before frontend implementation:
- [contracts/auth.md](contracts/auth.md) — `POST /api/v1/auth/login`, `GET /api/v1/auth/me`
- [contracts/employees.md](contracts/employees.md) — employee CRUD, role assignment, panel lookup
- [contracts/slots.md](contracts/slots.md) — create/bulk/get/reschedule/delete interviewer slots
- [contracts/candidates.md](contracts/candidates.md) — Excel upload, status change, profile, comments
- [contracts/bookings.md](contracts/bookings.md) — book, reschedule, cancel, todo list, weekly view

### Quickstart

> **Output**: [quickstart.md](quickstart.md)

Complete guide: clone → configure env → run migrations → seed data → start backend + frontend.

---

## Constitution Check (Post-Design)

- [x] All API routes use `/api/v1/` prefix
- [x] All responses use `{ "data": ..., "error": ..., "status": ... }` envelope
- [x] ORM models are the only database access mechanism (no raw SQL in app code)
- [x] All migrations in `backend/migrations/` before any ORM reference
- [x] JWT issued and validated exclusively by the backend
- [x] RBAC enforced on every endpoint via `require_role()` FastAPI dependency
- [x] Pydantic schemas validate all inbound data before reaching services
- [x] File upload size enforced at the API boundary (≤ 5 MB for attachments)
- [x] `.env.example` documents all required env var names; `.env` is git-ignored

---

## Implementation Phases Overview

| Phase | Priority | Modules | Status |
|---|---|---|---|
| Phase 1 | P1 | Auth · Employee Mgmt · Slot Mgmt · Candidate Upload · Interview Booking | **Tasks T001–T084** |
| Phase 2 | P2 | API Contract Stubs (T085a-i) · Feedback + PDF · Offer Approval Workflow · Joining Bonus · Master Data Admin · Document Downloads · To-Do List (full) · Candidate Approval Data · Feedback Form Report | **Tasks T085a–T143** |
| Phase 3 | P3 | Analytics/Charts · L2 Report & Aging · Status Insights · Channel Insights · ARC Deviation · Rejection Report · Referral Portal · Supply/Demand/Bench · Weekend Drive | **Tasks T144–T193** |
| Phase 4 | P3 | APScheduler background jobs (aging alerts · interview reminders · feedback reminders · export cleanup) | **Tasks T194–T199** |
| Phase 5 | — | OWASP hardening · rate limiting · pagination · security headers · additional routes · production env · performance benchmarks | **Tasks T200–T216** |

---

## Phase 2: Design & Contracts (P2 Modules)

### Additional Data Models Required

**Migration 006 — `feedback_form_template`, `feedback_parameter`, `interviewer_feedback_form_details`, `overall_feedback`**
- `feedback_form_template`: `id`, `tech_name VARCHAR(100)`, `practice VARCHAR(100)`, `form_title VARCHAR(200)`, `is_active BOOLEAN DEFAULT TRUE`, `created_at TIMESTAMPTZ`
- `feedback_parameter`: `id`, `template_id FK → feedback_form_template.id`, `section_name VARCHAR(200)`, `parameter_name VARCHAR(200)`, `param_order INT`, `max_score INT DEFAULT 10`
- `interviewer_feedback_form_details`: `id BIGSERIAL PK`, `recruiter_calendar_id BIGINT FK`, `interviewer_calendar_id BIGINT FK`, `template_id INT FK`, `parameter_scores JSONB`, `overall_rating VARCHAR(20) CHECK IN ('Select','Hold','Reject')`, `overall_remarks TEXT`, `submitted_by VARCHAR(255)`, `submitted_at TIMESTAMPTZ`, `pdf_path VARCHAR(500)`
- `overall_feedback`: `id BIGSERIAL PK`, `recruiter_calendar_id BIGINT FK`, `rating VARCHAR(20)`, `remarks TEXT`, `is_revisit BOOLEAN DEFAULT FALSE`

**Migration 007 — `offer_workflow`, `workflow_comments`, `ctc_history`, `joining_bonus`**
- `offer_workflow`: `id BIGSERIAL PK`, `candidate_detail_id BIGINT FK`, `current_level VARCHAR(50)`, `status VARCHAR(50)`, `created_at TIMESTAMPTZ`, `updated_at TIMESTAMPTZ`
- `workflow_comments`: `id BIGSERIAL PK`, `workflow_id BIGINT FK`, `commenter_email VARCHAR(255)`, `comment_text TEXT`, `action VARCHAR(20) CHECK IN ('Approved','Rejected','Comment')`, `created_at TIMESTAMPTZ`
- `ctc_history`: `id BIGSERIAL PK`, `candidate_detail_id BIGINT FK`, `ctc_value VARCHAR(50)`, `changed_by VARCHAR(255)`, `changed_at TIMESTAMPTZ`
- `joining_bonus`: `id BIGSERIAL PK`, `candidate_detail_id BIGINT FK`, `bonus_amount VARCHAR(50)`, `status VARCHAR(50)`, `dl_email VARCHAR(255)`, `updated_by VARCHAR(255)`, `updated_at TIMESTAMPTZ`

**Migration 008 — `demand_data`, `bench_data`, `demand_batch`, `bench_batch`**
- `demand_data`: `id BIGSERIAL PK`, `jr_id VARCHAR(100)`, `skill VARCHAR(100)`, `grade VARCHAR(50)`, `account VARCHAR(200)`, `bu VARCHAR(100)`, `demand_status VARCHAR(50) DEFAULT 'Open'`, `demand_date DATE`, `sourced_count INT DEFAULT 0`, `pipeline_count INT DEFAULT 0`, `batch_id BIGINT FK → demand_batch.id`, `created_at TIMESTAMPTZ`
- `bench_data`: `id BIGSERIAL PK`, `emp_name VARCHAR(200)`, `emp_email VARCHAR(255)`, `skill VARCHAR(100)`, `grade VARCHAR(50)`, `location VARCHAR(100)`, `bu VARCHAR(100)`, `bench_status VARCHAR(50)`, `batch_id BIGINT FK → bench_batch.id`, `created_at TIMESTAMPTZ`
- `demand_batch`: `id BIGSERIAL PK`, `uploaded_by VARCHAR(255)`, `uploaded_at TIMESTAMPTZ`, `row_count INT`
- `bench_batch`: `id BIGSERIAL PK`, `uploaded_by VARCHAR(255)`, `uploaded_at TIMESTAMPTZ`, `row_count INT`

**Migration 009 — Referral Tables**
- `referral_candidate_info`: `id BIGSERIAL PK`, `referee_emp_id BIGINT FK → employee_master.emp_id`, `candidate_name VARCHAR(200)`, `candidate_email VARCHAR(255)`, `candidate_phone VARCHAR(20)`, `certifications TEXT`, `notice_period VARCHAR(50)`, `location VARCHAR(100)`, `resume_path VARCHAR(500)`, `image_path VARCHAR(500)`, `status VARCHAR(50) DEFAULT 'Pending'`, `submitted_at TIMESTAMPTZ`
- `referral_technology_master`: `id SERIAL PK`, `tech_name VARCHAR(100) UNIQUE`, `is_active BOOLEAN DEFAULT TRUE`
- `referral_candidate_skills`: `id SERIAL PK`, `referral_id BIGINT FK`, `tech_id INT FK → referral_technology_master.id`
- `referral_notice_period_master`: `id SERIAL PK`, `value VARCHAR(50) UNIQUE`
- `referral_location_master`: `id SERIAL PK`, `value VARCHAR(100) UNIQUE`

**Migration 010 — Extended Master Data**
- `source_master`: `id SERIAL PK`, `source_name VARCHAR(100) UNIQUE`, `is_active BOOLEAN DEFAULT TRUE`
- `vendor_master`: `id SERIAL PK`, `vendor_name VARCHAR(100)`, `source_id INT FK → source_master.id`, `is_active BOOLEAN DEFAULT TRUE`; UNIQUE `(vendor_name, source_id)`
- `approver_dl_mapping`: `id SERIAL PK`, `tower_id INT FK → tower_master.id`, `dl_email VARCHAR(255)`, `dl_title VARCHAR(100)`, `level VARCHAR(50)` (TowerLead/BULead/NALead)
- `tower_skill_mapping`: `id SERIAL PK`, `tower_id INT FK → tower_master.id`, `technology_id INT FK → technology_master.id`; UNIQUE `(tower_id, technology_id)`
- `sap_capability_master`: `id SERIAL PK`, `capability_name VARCHAR(100) UNIQUE`, `is_active BOOLEAN DEFAULT TRUE`
- `sap_skill_master`: `id SERIAL PK`, `skill_name VARCHAR(100)`, `capability_id INT FK → sap_capability_master.id`, `is_active BOOLEAN DEFAULT TRUE`
- `export_history`: `id BIGSERIAL PK`, `export_type VARCHAR(100)`, `file_path VARCHAR(500)`, `created_by VARCHAR(255)`, `created_at TIMESTAMPTZ`, `is_deleted BOOLEAN DEFAULT FALSE`

**Migration 011 — L2 Tracking**
- `l2_select_data`: `id BIGSERIAL PK`, `candidate_detail_id BIGINT FK`, `l2_select_date DATE`, `days_since_l2 INT`, `baseline VARCHAR(100)`, `actionable VARCHAR(100)`, `batch_id BIGINT`, `created_at TIMESTAMPTZ`

### API Contracts (Phase 2+)

The following additional contract files are required before Phase 2 frontend work begins:
- `contracts/feedback.md` — feedback form templates, submission, PDF download
- `contracts/workflow.md` — offer approval levels, comments, CTC history, ARC threshold
- `contracts/joining-bonus.md` — JB candidates, BU-level view, DL management
- `contracts/admin.md` — master data CRUD (towers, skills, sources, vendors, templates, SAP)
- `contracts/documents.md` — resume download, PDF export, export history
- `contracts/analytics.md` — pie charts, line charts, trend charts, L2 report, Excel exports
- `contracts/referral.md` — referral portal registration, submission, SPOC management
- `contracts/supply.md` — demand/bench upload, history, filter options
- `contracts/notifications.md` — scheduler trigger endpoint, alert log

### Additional Routes (Frontend, Phase 2+)

```
/feedback                  → FeedbackFormPage (Interviewer)
/webFeedback               → WebFeedbackPage (Interviewer, mobile-accessible)
/work-flow                 → WorkflowPage (TowerLead / SLBULead / NALead / RecruiterLead)
/work-flow-info            → WorkflowInfoPage (same)
/joiningbonus              → JoiningBonusPage (RecruiterLead)
/jbcandidates              → JBCandidatesPage (RecruiterLead)
/administration            → AdministrationPage (Admin)
/master-data               → MasterDataPage (BUAdmin / PracticeAdmin)
/feedbackform-report       → FeedbackFormReportPage (Admin / RecruiterLead)
/candidate-approval-data   → CandidateApprovalDataPage (PMO / Admin)
/select-reject             → SelectRejectPage (Recruiter / PMO)
/dateofjoining             → DateOfJoiningPage (PMO)
/update-skill              → UpdateSkillPage (Admin / Recruiter)
/dashboard-reports         → DashboardReportsPage (RecruiterLead / Manager)
/line-chart                → LineChartPage (RecruiterLead)
/trend-chart               → TrendChartPage (RecruiterLead)
/interview-data            → InterviewDataPage (Recruiter / PMO)
/status-insights           → StatusInsightsPage (RecruiterLead)
/channel-insights          → ChannelInsightsPage (RecruiterLead)
/arc-deviation             → ArcDeviationPage (RecruiterLead)
/rejection-report          → RejectionReportPage (RecruiterLead)
/l2-report                 → L2ReportPage (PMO / RecruiterLead)
/l2-aging                  → L2AgingPage (PMO)
/demand-supply             → DemandSupplyPage (PMO / Lead)
/weekend-drive             → WeekendDrivePage (Admin / Recruiter)
/import-weekend-drive      → ImportWeekendDrivePage (Admin)
/candidate-referral        → CandidateReferralPage (Admin / ReferralSPOC)
/candidate-referral-details → CandidateReferralDetailsPage (Admin / ReferralSPOC)
/referral-form             → ReferralFormPage (PUBLIC — no auth guard)
/referral-portal/referralRegister  → ReferralRegisterPage (PUBLIC)
/referral-portal/ref-candidate-details → RefCandidateDetailsPage (ReferralAuthGuard)
/ref-reports-bybu          → ReferralReportsByBUPage (PUBLIC)
/ref-reports-byaccount     → ReferralReportsByAccountPage (PUBLIC)
```

### New Frontend Dependencies (Phase 2+)

Add to `frontend/package.json`:
- `recharts` — analytics charts (pie, line, trend)
- `@mui/x-date-pickers` — date range pickers for report filters
- `@mui/x-data-grid` — enhanced data grid for large datasets

