---

description: "Task list for Smart Recruit Platform — All Phases (US1–US16, 23 BRD modules)"
---

# Tasks: Smart Recruit Platform — Full Implementation

**Input**: Design documents from `/specs/001-smart-recruit-platform/`

**Prerequisites**: plan.md ✅ · spec.md ✅ · data-model.md ✅ · contracts/ ✅ · research.md ✅ · quickstart.md ✅ · BRD-AND-COMPLETE-DOCS.md ✅

**Scope**: All 16 User Stories (US1–US16) · All 23 BRD modules · Complete platform.

**Organization**: Tasks grouped by phase and user story. Each phase has a checkpoint for independent testing.

## Format: `- [ ] [ID] [P?] [Story?] Description with file path`

- **[P]**: Parallelizable — different files, no blocking dependencies within phase
- **[USn]**: User story traceability label
- All file paths relative to repo root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Repository skeleton, tooling, and environment configuration.

- [X] T001 Create monorepo folder structure: `backend/`, `frontend/` per plan.md project structure
- [X] T002 [P] Initialise Python backend: create `backend/requirements.txt` with FastAPI, SQLAlchemy 2.x, Alembic, python-jose[cryptography], passlib[bcrypt], pandas, openpyxl, reportlab, apscheduler, httpx, pytest, python-dotenv, uvicorn, slowapi
- [X] T003 [P] Initialise React frontend: scaffold Vite + React 18 + TypeScript in `frontend/`; install axios, react-router-dom@6, @mui/material, @mui/x-data-grid, @mui/x-date-pickers, @fullcalendar/react, @fullcalendar/timegrid, react-hook-form, recharts
- [X] T004 [P] Create `backend/alembic.ini` and initialise Alembic: `alembic init backend/migrations/`
- [X] T005 [P] Create `.env.example` at repo root: `DB_HOST`, `DB_PORT`, `DB_NAME=smarthiremain001`, `DB_USER`, `DB_PASSWORD`, `JWT_SECRET`, `JWT_ALGORITHM=HS256`, `JWT_EXPIRE_MINUTES=480`, `VITE_API_BASE_URL`, `CORS_ORIGINS=http://localhost:5173`, `UPLOAD_DIR=backend/uploads`, `SMTP_ENABLED=false`, `SMTP_HOST`, `SMTP_PORT`, `SMTP_FROM`
- [X] T006 [P] Create `.gitignore`: `backend/.env`, `backend/uploads/`, `backend/logs/`, `frontend/.env`, `frontend/.env.local`, `frontend/node_modules/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`
- [X] T007 [P] Create `frontend/.env` with `VITE_API_BASE_URL=http://localhost:8000`
- [X] T008 [P] Create `frontend/vite.config.ts`: dev proxy `/api` → `http://localhost:8000`; Vitest config
- [X] T009 [P] Create `frontend/tsconfig.json`: strict mode; path alias `@/` → `src/`

**Checkpoint**: Repo skeleton + tooling ready.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core backend + frontend infrastructure that ALL user stories depend on.

**⚠️ CRITICAL**: Complete this phase before starting any user story. Migrations must precede ORM models.

### Core Backend Utilities

- [X] T010 Create `backend/app/core/database.py`: `create_engine`, `SessionLocal`, `Base`, `get_db()`; reads `DATABASE_URL` from env
- [X] T011 Create `backend/app/core/config.py`: Pydantic `Settings` reading all `.env` vars; exports `settings` singleton
- [X] T012 [P] Create `backend/app/core/logging.py`: JSON-structured logger; `get_logger(name)` helper
- [X] T013 [P] Create `backend/app/core/file_storage.py`: `save_file(file, subfolder)` → `backend/uploads/{subfolder}/`; `get_file_path(subfolder, filename)`; 5 MB enforcement; `generate_export_path(report_type)` timestamped path

### Alembic Migrations — Phase 1 Entities

*Run in this exact order (FK dependencies):*

- [X] T014 Create `backend/migrations/versions/001_create_role_master.py`: `role_master` table; seed 14 role names
- [X] T015 Create `backend/migrations/versions/002_create_master_data_tables.py`: `tower_master`, `technology_master` — **must precede employee FK tables**
- [X] T016 Create `backend/migrations/versions/003_create_employee_tables.py`: `employee_master`, `employee_role_details`, `employee_technology_details`, `employee_tower_details`; all FK constraints and indexes
- [X] T017 Create `backend/migrations/versions/004_create_interviewer_calendar.py`: `interviewer_calendar`; CheckConstraint on `slot_status IN ('Available','Booked','Interviewed','Pending')`
- [X] T018 Create `backend/migrations/versions/005_create_candidate_tables.py`: `status_intermediate_mapping`, `candidate_detail`, `recruiter_calendar`, `candidate_status_history`, `candidate_comments`; seed status-transition rows

### SQLAlchemy ORM Models (Phase 1)

- [X] T019 [P] Create `backend/app/models/master_data.py`: `RoleMaster`, `TowerMaster`, `TechnologyMaster` with `back_populates`
- [X] T020 [P] Create `backend/app/models/employee.py`: `EmployeeMaster`, `EmployeeRoleDetails`, `EmployeeTechnologyDetails`, `EmployeeTowerDetails`
- [X] T021 [P] Create `backend/app/models/interview.py`: `InterviewerCalendar`, `RecruiterCalendar`
- [X] T022 [P] Create `backend/app/models/candidate.py`: `CandidateDetail`, `CandidateStatusHistory`, `CandidateComments`, `StatusIntermediateMapping`

### Pydantic Schemas (Phase 1)

- [X] T023 Create `backend/app/schemas/common.py`: `ApiResponse[T]`; `success_response()`; `error_response()`
- [X] T024 [P] Create `backend/app/schemas/auth.py`: `LoginRequest`, `TokenResponse`, `EmployeeSummary`, `MeResponse`
- [X] T025 [P] Create `backend/app/schemas/employee.py`: `EmployeeCreate`, `EmployeeUpdate`, `EmployeeOut`, `EmployeeListResponse`
- [X] T026 [P] Create `backend/app/schemas/slot.py`: `SlotCreate`, `SlotOut`, `SlotListResponse`, `BulkSlotUploadResponse`
- [X] T027 [P] Create `backend/app/schemas/candidate.py`: `CandidateOut`, `CandidateUpdate`, `CommentCreate`, `CommentOut`, `StatusChangeRequest`, `BulkUploadResponse`
- [X] T028 [P] Create `backend/app/schemas/booking.py`: `BookingCreate`, `BookingOut`, `RescheduleRequest`, `TodoListResponse`

### Security, App Factory & Seed

- [X] T029 Create `backend/app/core/security.py`: `hash_password`, `verify_password`, `create_access_token`, `decode_token`, `require_role(*roles)` dependency — 401/403 on failure
- [X] T030 Create `backend/app/main.py`: FastAPI app; CORS from `settings.CORS_ORIGINS`; global exception handler returning `ApiResponse`; router registration stubs for Phase 1
- [X] T031 Create `backend/seed_data.py`: idempotent seed — Admin user, 14 roles, sample towers, technologies, and status transitions

### Frontend Core Infrastructure

- [X] T032 Create `frontend/src/contexts/AuthContext.tsx`: `AuthProvider` with `token`, `employee`, `activeRole`; `login()`, `logout()`, `setActiveRole()` via `useReducer`
- [X] T033 [P] Create `frontend/src/hooks/useAuth.ts`: typed hook; null-context guard
- [X] T034 [P] Create `frontend/src/hooks/useApi.ts`: generic hook wrapping Axios; handles `ApiResponse[T]`; surfaces errors
- [X] T035 Create `frontend/src/services/api.ts`: Axios instance; request interceptor (Bearer token from `localStorage` — local-dev only; note: constitution §IV requires httpOnly cookie in production); 401 response interceptor → clear token → redirect `/login`
- [X] T036 [P] Create `frontend/src/components/ProtectedRoute.tsx`: redirects unauthenticated to `/login`
- [X] T037 [P] Create `frontend/src/components/RoleRoute.tsx`: `allowedRoles` prop; shows "access denied" message if not matched — does NOT silently redirect on `/selectrole` itself (preserves empty-roles message per US1 SC5)
- [X] T038 [P] Create `frontend/src/components/ApiErrorBoundary.tsx`: React error boundary surfacing API errors per constitution §V
- [X] T039 [P] Create `frontend/src/components/Navbar.tsx`: MUI AppBar with title, active role chip, logout button
- [X] T040 Create `frontend/src/main.tsx`: `ReactDOM.createRoot` entry point mounting `<App />` into `#root`
- [X] T041 Create `frontend/src/App.tsx`: `AuthProvider` + `BrowserRouter` wrapping `<Routes>` from `routes.tsx`
- [X] T042 Create `frontend/src/routes.tsx`: Phase 1 routes: `/login`, `/selectrole`, `/dashboard`, `/todolist`, `/register-panel`, `/candidate-details`, `/candidate-details/:id`, `/booking-form`, `/upload` — all except `/login` wrapped in `ProtectedRoute`

**Checkpoint**: Foundation complete — DB migrated, ORM models importable, JWT security, FastAPI app, React core all ready.

---

## Phase 3: User Story 1 — Authenticated Role-Based Access (P1) 🎯 MVP

**Goal**: JWT login, role retrieval, BU-aware routing, token expiry handling.

**Independent Test**: Login → `/selectrole` → role click → correct landing page. Expired token → redirect `/login`.

- [X] T043 [US1] Create `backend/app/services/auth_service.py`: `authenticate_user(email, password, db)`; `get_current_user(token, db)`; `HTTPException(401)` for bad credentials or expired token
- [X] T044 [US1] Create `backend/app/api/v1/auth.py`: `POST /api/v1/auth/login` — validates creds, issues JWT, sets httpOnly cookie, returns `TokenResponse`; `GET /api/v1/auth/me`; per contracts/auth.md
- [X] T045 [US1] Register auth router in `backend/app/main.py`
- [X] T046 [US1] Create `frontend/src/services/authService.ts`: `login()`, `getMe()`, `logout()` (clears localStorage for local-dev)
- [X] T047 [US1] Create `frontend/src/pages/LoginPage.tsx` (`/login`): react-hook-form; calls `authService.login()`; stores token; redirects to `/selectrole`; inline API error display
- [X] T048 [US1] Create `frontend/src/pages/SelectRolePage.tsx` (`/selectrole`): role buttons; BU-aware routing: SAP Recruiter/PMO → `/upload`; Interviewer → `/dashboard`; Admin → `/register-panel`; TowerLead/SLBULead/NALead/RecruiterLead → `/work-flow`; BUAdmin/PracticeAdmin → `/master-data`; all others → `/todolist`; empty-roles → informative message (per spec US1 SC5)
- [X] T049 [US1] Wrap all Phase 1 routes in `ProtectedRoute` in `routes.tsx`; confirm 401 interceptor in `api.ts` clears token state and triggers redirect via Vitest integration test

**Checkpoint**: US1 complete — login, role selection, BU routing, token expiry all functional.

---

## Phase 4: User Story 2 — Panel Registration & Employee Management (P1)

**Goal**: Admin creates panel members; new user logs in and reaches their dashboard.

**Independent Test**: Admin creates employee → new user logs in, selects Interviewer role, lands on `/dashboard`.

- [X] T050 [US2] Create `backend/app/services/employee_service.py`: `create_employee` (hashes password, inserts all sub-tables, duplicate email → 400); `list_employees` (paginated + filtered); `get_employee`; `update_employee`; `delete_employee` (soft-delete `is_active=False`); `list_technologies(db)` for frontend dropdown
- [X] T051 [US2] Create `backend/app/api/v1/employees.py`: `POST /api/v1/employees` (Admin); `GET /api/v1/employees`; `GET/PUT/DELETE /api/v1/employees/{emp_id}`; `GET /api/v1/panel/roles`; `GET /api/v1/panel/bu`; `GET /api/v1/panel/technologies`; per contracts/employees.md
- [X] T052 [US2] Register employees router in `backend/app/main.py`
- [X] T053 [US2] Create `frontend/src/services/employeeService.ts`: typed wrappers for all employee CRUD + panel lookups + technology list
- [X] T054 [US2] Create `frontend/src/pages/PanelRegistrationPage.tsx` (`/register-panel`): MUI form; multi-select roles (from `/api/v1/panel/roles`) and technologies (from `/api/v1/panel/technologies`); calls `employeeService.createEmployee()`; inline duplicate-email error
- [X] T055 [P] [US2] Create `frontend/src/pages/DashboardPage.tsx` (`/dashboard`): Interviewer home shell; welcome message; placeholder sections for slots (US3) and todo items (US5)

**Checkpoint**: US2 complete — Admin registers panel member; employee can log in and reach dashboard.

---

## Phase 5: User Story 3 — Interviewer Slot Management (P1)

**Goal**: Create/bulk-upload slots; colour-coded calendar; overlaps rejected 409.

**Independent Test**: Create slot → green on calendar. Overlap → 409 error. Bulk upload → slots on calendar.

- [X] T056 [US3] Create `backend/app/services/slot_service.py`: `overlap_check`; `create_slot`; `bulk_create_slots` (pandas/openpyxl, error row collection); `list_slots`; `update_slot_status`; `delete_slot` (blocks delete of Booked slot)
- [X] T057 [US3] Create `backend/app/api/v1/slots.py`: `POST /api/v1/slots`; `POST /api/v1/slots/bulk` (multipart Excel); `GET /api/v1/slots`; `PUT /api/v1/slots/{slot_id}`; `DELETE /api/v1/slots/{slot_id}`; per contracts/slots.md
- [X] T058 [US3] Register slots router in `backend/app/main.py`
- [X] T059 [US3] Create `frontend/src/services/slotService.ts`: typed wrappers for all slot endpoints
- [X] T060 [US3] Create `frontend/src/components/SlotCalendar.tsx`: `@fullcalendar/react` timeGrid week; status→colour: Available=green, Booked=pink, Interviewed=grey, Pending=yellow; `events` prop; `onSlotClick` callback
- [X] T061 [US3] Add slot creation form to `frontend/src/pages/DashboardPage.tsx`: MUI form (skill, date, from/to time, weekend-drive toggle); 409 overlap error inline; calendar refresh on success
- [X] T062 [US3] Add bulk upload panel to `DashboardPage.tsx`: `<FileUpload>` for `.xlsx`; shows created/error count; error Excel download link
- [X] T063 [P] [US3] Create `frontend/src/components/FileUpload.tsx`: reusable MUI drag-drop; configurable `maxBytes` default 5 MB; `onChange` returns `File`

**Checkpoint**: US3 complete — create, bulk-upload, colour-coded calendar, overlap guard all functional.

---

## Phase 6: User Story 4 — Candidate Upload & Profile Management (P1)

**Goal**: Recruiter bulk-uploads Excel; valid rows imported; duplicates flagged; profile editable with status transitions and comments.

**Independent Test**: Upload template → candidates appear. Duplicates → downloadable error file. Status change → only valid transitions offered.

- [X] T064 [US4] Create `backend/app/services/candidate_service.py`: `parse_excel`; `bulk_import`; `generate_error_excel`; `get_candidate`; `update_candidate`; `validate_status_transition` (queries `status_intermediate_mapping`); `change_status` (persists history); `add_comment` (saves attachment via `file_storage`); `list_candidates` (paginated/filtered); `update_doj`; `update_skill`
- [X] T065 [US4] Create `backend/app/api/v1/candidates.py`: `POST /api/v1/candidates/upload`; `GET /api/v1/candidates`; `GET/PUT /api/v1/candidates/{id}`; `POST /api/v1/candidates/{id}/status`; `POST/GET /api/v1/candidates/{id}/comments`; `GET /api/v1/candidates/{id}/resume`; `GET /api/v1/candidates/status-options`; per contracts/candidates.md; 5 MB limit enforced on comment attachments
- [X] T066 [US4] Register candidates router in `backend/app/main.py`
- [X] T067 [US4] Create `frontend/src/services/candidateService.ts`: typed wrappers for all candidate endpoints including status-options, update-DOJ, update-skill
- [X] T068 [US4] Create `frontend/src/pages/UploadPage.tsx` (`/upload`): `<FileUpload>` for `.xlsx`; import/error count summary; error Excel download link
- [X] T069 [US4] Create `frontend/src/pages/CandidateListPage.tsx` (`/candidate-details`): MUI DataGrid; name, skill, status, source, BU columns; filters; pagination; row → `/candidate-details/:id`
- [X] T070 [US4] Create `frontend/src/pages/CandidateDetailPage.tsx` (`/candidate-details/:id`): full profile; editable via react-hook-form; status dropdown (valid next states only); comment thread + `<FileUpload>`; DOJ date-picker (PMO role only)

**Checkpoint**: US4 complete — bulk upload, duplicate detection, profile editing, status transitions, comments all functional.

---

## Phase 7: User Story 5 — Interview Booking & Scheduling (P1)

**Goal**: Recruiter searches available slots, books for candidate, UUID meeting link generated, email logged.

**Independent Test**: Book slot → on calendar + todolist; meeting link in response; entry in `logs/email.log`.

- [X] T071 [US5] Create `backend/app/services/booking_service.py`: `search_available_slots`; `book_slot` (meeting_link=str(uuid4()), updates slot status); `direct_book` (`is_direct_booked=True`, `interviewer_calendar_id=NULL`); `reschedule_booking`; `cancel_booking`; `notify` (writes `logs/email.log`); `get_todo_list`; `get_weekly_view`; `get_pending_feedbacks`
- [X] T072 [US5] Create `backend/app/api/v1/bookings.py`: `GET /api/v1/bookings/available-slots`; `POST /api/v1/bookings`; `POST /api/v1/bookings/direct`; `PUT /api/v1/bookings/{id}/reschedule`; `DELETE /api/v1/bookings/{id}`; `GET /api/v1/bookings/todo`; `GET /api/v1/bookings/weekly`; `GET /api/v1/bookings/pending-feedback`; per contracts/bookings.md
- [X] T073 [US5] Register bookings router in `backend/app/main.py`
- [X] T074 [US5] Create `frontend/src/services/bookingService.ts`: typed wrappers for all booking endpoints
- [X] T075 [US5] Create `frontend/src/pages/BookingFormPage.tsx` (`/booking-form`): technology + date/time search; results table; candidate selector; Book / Direct-Book; confirmation with meeting link
- [X] T076 [US5] Create `frontend/src/pages/TodoListPage.tsx` (`/todolist`): tabs — "Today's Interviews" (sorted by time + meeting link), "Pending Feedback" (overdue list), "Weekly View" (`<SlotCalendar>` read-only); inline status-update per row

**Checkpoint**: US5 complete — booking, direct booking, reschedule, todo list, weekly view all functional.

---

## Phase 8: Phase 1 Polish & Smoke Tests

- [X] T077 [P] Create `backend/tests/conftest.py`: PostgreSQL test schema; `TestClient` (httpx); seeded Admin + Interviewer; `get_db` override
- [X] T078 [P] Create `backend/tests/test_auth.py`: valid login → 200 + token; invalid → 401; `GET /me` with token → 200
- [X] T079 [P] Create `backend/tests/test_slots.py`: create slot → 201; overlap → 409; list → 200
- [X] T080 [P] Create `backend/tests/test_candidates.py`: upload → 201; status change → 200; invalid transition → 400
- [X] T081 OWASP Phase 1 review: no hard-coded secrets; 5 MB limits; `require_role()` on every non-public endpoint; Pydantic validation at all POST/PUT boundaries; ORM-only DB access
- [X] T082 [P] Create `backend/uploads/` subdirs: `resumes/`, `attachments/`, `exports/` — each with `.gitkeep`
- [X] T083 [P] Create `backend/logs/` with `.gitkeep`; verify `.gitignore` excludes `email.log`
- [X] T084 Run quickstart.md Phase 1 validation: env → migrations → seed → backend start → frontend start → login flow

**Checkpoint**: Phase 1 complete — all 5 P1 user stories verified end-to-end.

---

## Phase 9a: Phase 2 API Contract Stubs

**Purpose**: Create all API contract documentation files required by constitution §II before any Phase 2 implementation begins. Frontend work on Phases 10–16 MUST NOT start until these exist.

- [X] T085a Create `specs/001-smart-recruit-platform/contracts/feedback.md`: document all endpoints for `GET /api/v1/feedback/template/{booking_id}`, `POST /api/v1/feedback/{booking_id}`, `GET /api/v1/feedback/{booking_id}/pdf`, `GET/POST /api/v1/feedback/templates` — request/response schemas using `ApiResponse[T]` envelope
- [X] T085b [P] Create `specs/001-smart-recruit-platform/contracts/workflow.md`: document workflow endpoints — candidates list, action (approve/reject/comment), CTC history, threshold, approver-DL CRUD
- [X] T085c [P] Create `specs/001-smart-recruit-platform/contracts/joining-bonus.md`: document JB endpoints — list, BU view, status update, DL options
- [X] T085d [P] Create `specs/001-smart-recruit-platform/contracts/admin.md`: document all master data CRUD endpoints for towers, skills, sources, vendors, SAP capabilities, approver DLs, role comments
- [X] T085e [P] Create `specs/001-smart-recruit-platform/contracts/documents.md`: document resume download, attachment download, export history list/delete/re-download endpoints
- [X] T085f [P] Create `specs/001-smart-recruit-platform/contracts/analytics.md`: document all analytics and report endpoints — pie chart, line chart, trend chart, L2 report, L2 aging, DOJ status, Excel export streams
- [X] T085g [P] Create `specs/001-smart-recruit-platform/contracts/referral.md`: document referral endpoints — form-headers (PUBLIC), check-employee (PUBLIC), submit (PUBLIC), list, CRUD, resume download
- [X] T085h [P] Create `specs/001-smart-recruit-platform/contracts/supply.md`: document demand/bench upload, list, history, filter-options endpoints
- [X] T085i [P] Create `specs/001-smart-recruit-platform/contracts/notifications.md`: document scheduler trigger endpoint `GET /api/v1/admin/trigger-job/{job_name}` and describe notification log format

**Checkpoint**: All 9 Phase 2+ API contracts documented — constitution §II gate cleared for Phases 10–23.

---

## Phase 9: Phase 2 Data Model Extensions

**Purpose**: Migrations and ORM models for all P2 features. BLOCKS Phases 10–16.

*Migration order (all new FKs reference earlier migrations):*

- [X] T085 Create `backend/migrations/versions/006_create_feedback_tables.py`: `feedback_form_template` (id, tech_name, practice, form_title, is_active), `feedback_parameter` (id, template_id FK, section_name, parameter_name, param_order, max_score INT DEFAULT 10), `interviewer_feedback_form_details` (id, recruiter_calendar_id FK, template_id FK, parameter_scores JSONB, overall_rating CHECK(Select/Hold/Reject), overall_remarks TEXT, submitted_by, submitted_at, pdf_path), `overall_feedback` (id, recruiter_calendar_id FK, rating, remarks, is_revisit BOOLEAN)
- [X] T086 Create `backend/migrations/versions/007_create_workflow_tables.py`: `offer_workflow` (id, candidate_detail_id FK, current_level, status), `workflow_comments` (id, workflow_id FK, commenter_email, comment_text, action CHECK(Approved/Rejected/Comment), created_at), `ctc_history` (id, candidate_detail_id FK, ctc_value, changed_by, changed_at), `joining_bonus` (id, candidate_detail_id FK, bonus_amount, status, dl_email, updated_by, updated_at)
- [X] T087 Create `backend/migrations/versions/008_create_supply_tables.py`: `demand_batch`, `demand_data` (jr_id, skill, grade, account, bu, demand_status DEFAULT 'Open', demand_date, sourced_count, pipeline_count, batch_id FK), `bench_batch`, `bench_data` (emp_name, emp_email, skill, grade, location, bu, bench_status, batch_id FK)
- [X] T088 Create `backend/migrations/versions/009_create_referral_tables.py`: `referral_candidate_info` (id, referee_emp_id FK → employee_master, candidate_name, candidate_email, candidate_phone, certifications, notice_period, location, resume_path, image_path, status DEFAULT 'Pending', submitted_at), `referral_technology_master`, `referral_candidate_skills` (referral_id FK, tech_id FK), `referral_notice_period_master`, `referral_location_master`
- [X] T089 Create `backend/migrations/versions/010_create_extended_master_data.py`: `source_master` (id, source_name UNIQUE, is_active), `vendor_master` (id, vendor_name, source_id FK, is_active; UNIQUE(vendor_name, source_id)), `approver_dl_mapping` (id, tower_id FK, dl_email, dl_title, level), `tower_skill_mapping` (id, tower_id FK, technology_id FK; UNIQUE), `sap_capability_master`, `sap_skill_master`, `export_history` (id, export_type, file_path, created_by, created_at, is_deleted BOOLEAN DEFAULT FALSE)
- [X] T090 [P] Create `backend/app/models/feedback.py`: `FeedbackFormTemplate`, `FeedbackParameter`, `InterviewerFeedbackFormDetails`, `OverallFeedback`
- [X] T091 [P] Create `backend/app/models/workflow.py`: `OfferWorkflow`, `WorkflowComments`, `CTCHistory`, `JoiningBonus`
- [X] T092 [P] Create `backend/app/models/supply.py`: `DemandBatch`, `DemandData`, `BenchBatch`, `BenchData`
- [X] T093 [P] Create `backend/app/models/referral.py`: `ReferralCandidateInfo`, `ReferralTechnologyMaster`, `ReferralCandidateSkill`, `ReferralNoticePeriodMaster`, `ReferralLocationMaster`
- [X] T094 [P] Extend `backend/app/models/master_data.py`: add `SourceMaster`, `VendorMaster`, `ApproverDLMapping`, `TowerSkillMapping`, `SapCapabilityMaster`, `SapSkillMaster`, `ExportHistory`

**Checkpoint**: Phase 2 migrations applied; all Phase 2 ORM models importable without errors.

---

## Phase 10: User Story 6 — Feedback Collection & PDF Generation (P2)

**Goal**: Technology-specific form; PDF generated via ReportLab; Recruiter can download.

**Independent Test**: Interviewer submits feedback → PDF appears in `backend/uploads/exports/`; Recruiter downloads via API → correct PDF returned.

- [X] T095 [P] Create `backend/app/schemas/feedback.py`: `FeedbackTemplateOut`, `FeedbackSubmitRequest`, `FeedbackParameterOut`, `PDFDownloadResponse`
- [X] T096 [US6] Create `backend/app/services/feedback_service.py`: `get_form_template(booking_id, db)` returns blank template for the booking's technology; `submit_feedback(booking_id, data, submitted_by, db)` saves `InterviewerFeedbackFormDetails`, generates PDF with ReportLab (all sections + ratings + recommendation), stores in `backend/uploads/exports/`, updates `recruiter_calendar.feedback_submitted=True`; `get_feedback_pdf(booking_id, db)` returns `FileResponse`; `get_feedback_report(filters, db)`; `list_templates(db)`; `create_template(data, db)` (Admin); `handle_revisit(booking_id, data, db)` stores with `is_revisit=True`
- [X] T097 [US6] Create `backend/app/api/v1/feedback.py`: `GET /api/v1/feedback/template/{booking_id}` (Interviewer); `POST /api/v1/feedback/{booking_id}` (Interviewer); `GET /api/v1/feedback/{booking_id}/pdf` (Recruiter/Admin/PMO); `GET/POST /api/v1/feedback/templates` (Admin); per contracts/feedback.md
- [X] T098 [US6] Register feedback router in `backend/app/main.py`
- [X] T099 [P] [US6] Create `frontend/src/services/feedbackService.ts`: typed wrappers for template fetch, submit, PDF download, template management
- [X] T100 [US6] Create `frontend/src/pages/FeedbackFormPage.tsx` (`/feedback`): pre-populated candidate/interview details; dynamic sections from template; rating inputs per parameter; behavioural section; overall recommendation; submit → PDF download link shown on success
- [X] T101 [P] [US6] Create `frontend/src/pages/WebFeedbackPage.tsx` (`/webFeedback`): mobile-accessible feedback form; same data model; simplified MUI layout for small screens
- [X] T102 [US6] Add `/feedback` and `/webFeedback` to `frontend/src/routes.tsx` with `RoleRoute` (Interviewer)

**Checkpoint**: US6 complete — technology-specific forms, submission, PDF generation and download all functional.

---

## Phase 11: User Story 7 — Offer Approval Workflow (P2)

**Goal**: Multi-level approval chain (Recruiter → Tower Lead → BU Lead → NA Lead); ARC deviation flagged; full comments history.

**Independent Test**: Recruiter submits candidate → Tower Lead sees them in queue → approves → candidate moves to BU Lead queue.

- [X] T103 [P] Create `backend/app/schemas/workflow.py`: `WorkflowOut`, `WorkflowAction`, `CTCHistoryOut`, `WorkflowCommentOut`, `ThresholdOut`, `ApproverDLOut`
- [X] T104 [US7] Create `backend/app/services/workflow_service.py`: `submit_for_approval`; `get_workflow_candidates(approver_role, db)`; `update_workflow(workflow_id, action, comment, db)`; `get_comments_history`; `add_comment`; `check_arc_threshold`; `get_ctc_history`; `get_approver_dl`; `update_approver_dl`; `get_possible_statuses`
- [X] T105 [US7] Create `backend/app/api/v1/workflow.py`: `GET /api/v1/workflow/candidates`; `POST /api/v1/workflow/{id}/action`; `GET/POST /api/v1/workflow/{id}/comments`; `GET /api/v1/workflow/ctc-history/{candidate_id}`; `GET /api/v1/workflow/threshold`; `GET/PUT /api/v1/workflow/approver-dl`; `GET /api/v1/workflow/possible-status`; per contracts/workflow.md
- [X] T106 [US7] Register workflow router in `backend/app/main.py`
- [X] T107 [P] [US7] Create `frontend/src/services/workflowService.ts`: typed wrappers
- [X] T108 [US7] Create `frontend/src/pages/WorkflowPage.tsx` (`/work-flow`): candidates at current approver level; approve/reject with comment modal; ARC deviation badge; pagination
- [X] T109 [US7] Create `frontend/src/pages/WorkflowInfoPage.tsx` (`/work-flow-info`): full offer details; CTC history timeline; comments history; threshold info
- [X] T110 [US7] Add `/work-flow` and `/work-flow-info` to `routes.tsx` with `RoleRoute`

**Checkpoint**: US7 complete — multi-level approval chain, CTC history, ARC flag, comments all functional.

---

## Phase 12: User Story 15 — Joining Bonus Management (P2)

**Goal**: Recruiter Leads track joining bonus commitments; BU-level view; DL configuration.

**Independent Test**: JB candidate appears with correct bonus amount. BU Admin sees only their BU's JB candidates. Status update persists.

- [X] T111 [P] Create `backend/app/schemas/joining_bonus.py`: `JoiningBonusOut`, `JoiningBonusUpdate`, `JBCandidateOut`
- [X] T112 [US15] Create `backend/app/services/joining_bonus_service.py`: `list_jb_candidates`, `list_jb_by_bu`, `update_jb_status`, `get_jb_bonus`, `get_dl_options`
- [X] T113 [US15] Create `backend/app/api/v1/joining_bonus.py`: `GET /api/v1/joining-bonus`; `GET /api/v1/joining-bonus/bu`; `PUT /api/v1/joining-bonus/{id}`; `GET /api/v1/joining-bonus/dl-options`; per contracts/joining-bonus.md
- [X] T114 [US15] Register joining_bonus router in `backend/app/main.py`
- [X] T115 [P] [US15] Create `frontend/src/services/joiningBonusService.ts`: typed wrappers
- [X] T116 [US15] Create `frontend/src/pages/JoiningBonusPage.tsx` (`/joiningbonus`): JB candidates table; status update action; DL info
- [X] T117 [P] [US15] Create `frontend/src/pages/JBCandidatesPage.tsx` (`/jbcandidates`): Recruiter-facing JB list with BU filter
- [X] T118 [US15] Add `/joiningbonus` and `/jbcandidates` to `routes.tsx` with `RoleRoute`

**Checkpoint**: US15 complete — joining bonus tracking, BU-scoped view, DL configuration functional.

---

## Phase 13: User Story 12 — Administration & Master Data (P2)

**Goal**: Admin manages all lookup tables; BU-scoped view; duplicate guards; soft-delete with reference checks.

**Independent Test**: Admin adds skill → immediately in dropdowns. Duplicate → "TECHNOLOGY ALREADY EXISTS". BU Admin sees only their BU data types.

- [X] T119 [P] Create `backend/app/schemas/admin.py`: `TowerCreate/Out`, `SkillCreate/Out`, `SourceCreate`, `VendorCreate/Out`, `SapCapabilityOut`, `SapSkillOut`, `ApproverDLUpdate`, `RoleCommentCreate`
- [X] T120 [US12] Create `backend/app/services/admin_service.py`: CRUD for towers, skills, skill-groups, sources, vendors, role-comments, feedback templates, approver-DL; BU-scope filter (standard/SAP/Invent BU sees different subset); duplicate check → 400 with standard message (TECHNOLOGY ALREADY EXISTS, TOWER ALREADY EXISTS etc.); soft-delete with active-reference guard
- [X] T121 [US12] Create `backend/app/api/v1/admin.py`: full CRUD for all master data types; BU-scoped responses; per contracts/admin.md
- [X] T122 [US12] Register admin router in `backend/app/main.py`
- [X] T123 [P] [US12] Create `frontend/src/services/adminService.ts`: typed wrappers for all admin endpoints
- [X] T124 [US12] Create `frontend/src/pages/AdministrationPage.tsx` (`/administration`): MUI tabbed layout; tabs: Tower, Skill, SkillGroup, Source, Vendor, Feedback Form, Role Comment, Approver DL, BU Account, SAP (conditional); each tab has add-form + data table with delete action
- [X] T125 [US12] Create `frontend/src/pages/MasterDataPage.tsx` (`/master-data`): BUAdmin/PracticeAdmin scoped view; shows only BU-relevant tabs; reuses `adminService`
- [X] T126 [US12] Add `/administration` and `/master-data` to `routes.tsx` with `RoleRoute`

**Checkpoint**: US12 complete — all master data CRUD, duplicate guards, BU scoping, soft-delete with reference checks functional.

---

## Phase 14: User Story 14 — PDF & Document Management (P2)

**Goal**: Resume/attachment download, feedback PDF download, export history tracking and cleanup, batch select/reject, DOJ page.

**Independent Test**: Download resume → correct file. Download feedback PDF → contains all submitted sections. Export history shows file with re-download link within retention window.

- [X] T127 Check whether `export_history` was created by migration 010 (T089): if yes, mark this task complete with note `[COVERED BY T089]`; if absent from migration 010, create `backend/migrations/versions/011_create_export_history.py` with schema matching plan.md Migration 010 spec
- [X] T128 [US14] Create `backend/app/services/document_service.py`: `download_resume(candidate_id, db)` → `FileResponse`; `download_attachment(candidate_id, comment_id, db)`; `list_export_history(created_by, db)`; `delete_export(export_id, db)` sets `is_deleted=True`; `cleanup_old_exports(db)` deletes records + files older than 7 days
- [X] T129 [US14] Create `backend/app/api/v1/exports.py`: `GET /api/v1/exports/history`; `DELETE /api/v1/exports/history/{id}`; `GET /api/v1/exports/{id}/download`; per contracts/documents.md
- [X] T130 [US14] Register exports router in `backend/app/main.py`; wire resume download in `candidates.py` via `document_service`
- [X] T131 [P] [US14] Create `frontend/src/services/documentService.ts`: typed wrappers for resume download, attachment, export history, re-download
- [X] T132 [P] [US14] Add resume download button to `CandidateDetailPage.tsx`: calls `documentService.downloadResume()`; blob URL + `<a download>` pattern
- [X] T133 [US14] Create `frontend/src/pages/SelectRejectPage.tsx` (`/select-reject`): batch L1 select/reject on candidate table; calls `candidateService.changeStatus()` in bulk
- [X] T134 [P] [US14] Create `frontend/src/pages/DateOfJoiningPage.tsx` (`/dateofjoining`): PMO view; editable DOJ date-picker; calls `candidateService.updateDOJ()`
- [X] T135 [P] [US14] Create `frontend/src/pages/UpdateSkillPage.tsx` (`/update-skill`): update candidate primary skill; calls `candidateService.updateSkill()`
- [X] T136 [US14] Add `/select-reject`, `/dateofjoining`, `/update-skill` to `routes.tsx` with `RoleRoute`

**Checkpoint**: US14 complete — resume/attachment download, export history, DOJ page, batch select/reject all functional.

---

## Phase 15: User Story 8 — Full To-Do List (P2)

**Goal**: Pending feedbacks tab, inline status update from to-do list, todo status dropdown.

- [X] T137 [US8] Extend `frontend/src/pages/TodoListPage.tsx`: add "Pending Feedback" tab calling `GET /api/v1/bookings/pending-feedback`; each row shows candidate name, interview date, link to `/feedback`; overdue items highlighted in orange
- [X] T138 [US8] Add inline status dropdown on "Today's Interviews" rows calling `candidateService.changeStatus()`; item removed from list on successful update

**Checkpoint**: US8 complete — pending feedback, today's interviews, weekly view, inline status update all in one dashboard.

---

## Phase 16: Candidate Approval Data & Feedback Form Report (P2)

- [X] T139 Create `backend/app/api/v1/reports.py`: `GET /api/v1/reports/offer-approve-candidates` (Admin/PMO); `GET /api/v1/reports/feedback-form-report` (Admin/RecruiterLead) with date + technology filters; per contracts/analytics.md
- [X] T140 Register reports router in `backend/app/main.py`
- [X] T141 [P] Create `frontend/src/pages/CandidateApprovalDataPage.tsx` (`/candidate-approval-data`): candidates in BU/NA approval stage; filter controls; MUI DataGrid
- [X] T142 [P] Create `frontend/src/pages/FeedbackFormReportPage.tsx` (`/feedbackform-report`): submitted feedback report; date + technology filters; Excel export button
- [X] T143 Add `/candidate-approval-data` and `/feedbackform-report` to `routes.tsx` with `RoleRoute`

**Checkpoint**: Phase 2 complete — all P2 features functional (Feedback, Workflow, JB, Master Data, Docs, Full ToDo, Reports).

---

## Phase 17: Phase 3 Data Model Extensions

- [X] T144 Create `backend/migrations/versions/012_create_l2_tracking.py`: `l2_select_data` (id, candidate_detail_id FK, l2_select_date DATE, days_since_l2 INT, baseline VARCHAR(100), actionable VARCHAR(100), batch_id BIGINT, created_at TIMESTAMPTZ)
- [X] T145 [P] Create `backend/app/models/l2.py`: `L2SelectData` ORM class

**Checkpoint**: Phase 3 migrations applied.

---

## Phase 18: User Story 9 — Recruitment Analytics & Reports (P3)

**Goal**: Pie charts (select/reject by skill/source/vendor), line charts (monthly volume), trend charts, Excel exports with filters.

**Independent Test**: Apply date + technology filter → charts update. Excel export → file contains only filtered data.

- [X] T146 [P] Create `backend/app/schemas/analytics.py`: `PieChartData`, `LineChartData`, `TrendChartData`, `ReportFilter`, `InterviewDataRow`
- [X] T147 [US9] Create `backend/app/services/analytics_service.py`: `outer_pie_chart(filters, db)`; `inner_pie_chart(filters, db)` drill-down by source/vendor; `line_chart_by_month`; `line_chart_by_year`; `trend_chart`; `reject_select_ratio`; `interview_data(filters, db)`; `generate_excel_report(filters, db)` → `StreamingResponse` with openpyxl; `status_insight_data`; `channel_insight_data`; `arc_deviation_data`; `rejection_report_data`; `get_available_years`; `get_date_range`
- [X] T148 [US9] Extend `backend/app/api/v1/reports.py`: `GET /api/v1/reports/pie-chart`; `GET /api/v1/reports/line-chart`; `GET /api/v1/reports/trend-chart`; `GET /api/v1/reports/interview-data`; `GET /api/v1/reports/status-insights`; `GET /api/v1/reports/channel-insights`; `GET /api/v1/reports/arc-deviation`; `GET /api/v1/reports/rejection`; `GET /api/v1/reports/export` (Excel StreamingResponse); `GET /api/v1/reports/years`; `GET /api/v1/reports/date-range`
- [X] T149 [P] [US9] Create `frontend/src/services/analyticsService.ts`: typed wrappers for all analytics endpoints
- [X] T150 [US9] Create `frontend/src/pages/DashboardReportsPage.tsx` (`/dashboard-reports`): Recharts `PieChart` (outer + inner); filter controls (date range, skill, BU, source, vendor); Excel export button
- [X] T151 [P] [US9] Create `frontend/src/pages/LineChartPage.tsx` (`/line-chart`): Recharts `LineChart`; year/month selectors; monthly + yearly tabs
- [X] T152 [P] [US9] Create `frontend/src/pages/TrendChartPage.tsx` (`/trend-chart`): Recharts `AreaChart`; source/vendor trend; filter controls; Excel export
- [X] T153 [P] [US9] Create `frontend/src/pages/InterviewDataPage.tsx` (`/interview-data`): tabular interview data; MUI DataGrid; paginated; Excel export
- [X] T154 [P] [US9] Create `frontend/src/pages/StatusInsightsPage.tsx` (`/status-insights`): status distribution bar chart + table; Excel export
- [X] T155 [P] [US9] Create `frontend/src/pages/ChannelInsightsPage.tsx` (`/channel-insights`): source/vendor volume + select/reject rate per channel; trend overlay
- [X] T156 [P] [US9] Create `frontend/src/pages/ArcDeviationPage.tsx` (`/arc-deviation`): ARC deviation cases table; CTC vs threshold column; Excel export
- [X] T157 [P] [US9] Create `frontend/src/pages/RejectionReportPage.tsx` (`/rejection-report`): rejection counts by reason/stage/technology/source; Recharts bar chart + table; Excel export
- [X] T158 Add all analytics routes to `frontend/src/routes.tsx`: `/dashboard-reports`, `/line-chart`, `/trend-chart`, `/interview-data`, `/status-insights`, `/channel-insights`, `/arc-deviation`, `/rejection-report`

**Checkpoint**: US9 complete — all chart types, filter controls, Excel exports all functional.

---

## Phase 19: L2 Report & Aging (P3)

**Goal**: L2-stage candidates with aging; over-SLA highlighted; DOJ tracking; L2 Excel import/export.

**Independent Test**: PMO views `/l2-report` → candidates with days-since-L2-select. `/l2-aging` → only over-SLA candidates shown.

- [X] T159 [P] Create `backend/app/services/l2_service.py`: `get_l2_status_info`; `get_l2_aging_report(sla_threshold, db)` (returns only over-SLA); `get_doj_status_info`; `export_l2_excel` → `StreamingResponse`; `export_doj_excel`; `upload_l2_select_file(file, db)` parses and upserts `l2_select_data`
- [X] T160 [P] Create `backend/app/api/v1/l2.py`: `POST /api/v1/l2/report`; `POST /api/v1/l2/aging`; `POST /api/v1/l2/doj-status`; `GET /api/v1/l2/export`; `POST /api/v1/l2/upload`; per contracts/analytics.md
- [X] T161 Register l2 router in `backend/app/main.py`
- [X] T162 [P] Create `frontend/src/services/l2Service.ts`: typed wrappers
- [X] T163 Create `frontend/src/pages/L2ReportPage.tsx` (`/l2-report`): L2 candidates list; days-since-L2 column; filters; Excel export; L2 Excel import button
- [X] T164 [P] Create `frontend/src/pages/L2AgingPage.tsx` (`/l2-aging`): filtered to over-SLA only; highlighted rows; export
- [X] T165 Add `/l2-report` and `/l2-aging` to `routes.tsx` with `RoleRoute` (PMO/RecruiterLead)

**Checkpoint**: L2 Report & Aging complete — dashboard, aging filter, DOJ tracking, Excel import/export all functional.

---

## Phase 20: User Story 16 — Weekend Drive Management (P3)

**Goal**: Admin bulk-creates weekend drive slots; imports weekend drive candidate batches; drive summary view.

**Independent Test**: Upload weekend drive slot file → slots created with `is_weekend_drive=True`. Candidate import → correct field mapping.

- [X] T166 [US16] Add `is_weekend_drive: bool = False` parameter to `bulk_create_slots()` in `slot_service.py`; add `is_weekend_drive` filter to `list_slots()` query; write unit test in `test_slots.py` confirming the flag persists through creation and is filterable on retrieval
- [X] T167 [US16] Create `backend/app/api/v1/weekend_drive.py`: `POST /api/v1/weekend-drive/slots/bulk` (Admin — reuses `slot_service.bulk_create_slots` with flag forced True); `POST /api/v1/weekend-drive/candidates/upload` (Admin — reuses `candidate_service.parse_excel`); `GET /api/v1/weekend-drive/summary?date=` (slot count, interviews conducted, feedback pending); per contracts/notifications.md
- [X] T168 [US16] Register weekend_drive router in `backend/app/main.py`
- [X] T169 [P] [US16] Create `frontend/src/services/weekendDriveService.ts`: typed wrappers
- [X] T170 [US16] Create `frontend/src/pages/WeekendDrivePage.tsx` (`/weekend-drive`): drive management screen; summary cards (slots, interviews, pending feedback); date picker for drive selection
- [X] T171 [P] [US16] Create `frontend/src/pages/ImportWeekendDrivePage.tsx` (`/import-weekend-drive`): two `<FileUpload>` panels — slot import and candidate import; result summaries for each
- [X] T172 Add `/weekend-drive` and `/import-weekend-drive` to `routes.tsx`

**Checkpoint**: US16 complete — weekend drive bulk slot + candidate import, summary view all functional.

---

## Phase 21: User Story 10 — Employee Referral Portal (P3)

**Goal**: Employees submit referrals; Referral SPOC manages; separate auth guard for portal sub-routes.

**Independent Test**: Employee submits referral + resume → confirmed. SPOC filters by skill → results. SPOC updates status to "Selected" → visible to employee.

- [X] T173 [P] Create `backend/app/schemas/referral.py`: `ReferralSubmitRequest`, `ReferralOut`, `ReferralMasterData`, `ReferralStatusUpdate`
- [X] T174 [US10] Create `backend/app/services/referral_service.py`: `check_referral_employee`; `get_referral_form_headers` (returns skills, certs, notice periods, locations); `submit_referral(data, resume, image, db)`; `list_referrals(filters, db)`; `get_referral`; `update_referral_status`; `download_resume(referral_id, db)`
- [X] T175 [US10] Create `backend/app/api/v1/referral.py`: `GET /api/v1/referral/form-headers` (PUBLIC); `POST /api/v1/referral/check-employee` (PUBLIC); `POST /api/v1/referral` (PUBLIC with employee check); `GET /api/v1/referral` (Admin/ReferralSPOC); `GET/PUT /api/v1/referral/{id}`; `PUT /api/v1/referral/{id}/status`; `GET /api/v1/referral/{id}/resume`; per contracts/referral.md
- [X] T176 [US10] Register referral router in `backend/app/main.py`
- [X] T177 [P] [US10] Create `frontend/src/services/referralService.ts`: typed wrappers
- [X] T178 [US10] Create `frontend/src/components/ReferralProtectedRoute.tsx`: separate auth guard for referral portal sub-routes; reuses the main JWT stored in localStorage (local-dev) — no separate referral token; verifies `employee` context has referral portal access by checking `employee.emp_email` against the referral_candidate_info table via `GET /api/v1/referral/check-employee`; redirects to `/referral-portal/referralRegister` if not registered
- [X] T179 [US10] Create `frontend/src/pages/CandidateReferralPage.tsx` (`/candidate-referral`): Admin/SPOC view; all referrals; filter by skill/status; row → details
- [X] T180 [P] [US10] Create `frontend/src/pages/CandidateReferralDetailsPage.tsx` (`/candidate-referral-details`): full referral profile; resume download; status update
- [X] T181 [US10] Create `frontend/src/pages/ReferralFormPage.tsx` (`/referral-form`): PUBLIC — no auth guard; employee email check; multi-select skills + certs; `<FileUpload>` for resume; confirmation message
- [X] T182 [P] [US10] Create `frontend/src/pages/ReferralRegisterPage.tsx` (`/referral-portal/referralRegister`): PUBLIC — employee registers to access referral portal
- [X] T183 [P] [US10] Create `frontend/src/pages/RefCandidateDetailsPage.tsx` (`/referral-portal/ref-candidate-details`): wrapped in `ReferralProtectedRoute`; referred candidate status view
- [X] T184 [P] [US10] Create `frontend/src/pages/ReferralReportsByBUPage.tsx` (`/ref-reports-bybu`): PUBLIC — referral data grouped by BU
- [X] T185 [P] [US10] Create `frontend/src/pages/ReferralReportsByAccountPage.tsx` (`/ref-reports-byaccount`): PUBLIC — referral data grouped by account
- [X] T186 [US10] Add all referral routes to `routes.tsx`: public routes unwrapped; `/candidate-referral` + `/candidate-referral-details` under `ProtectedRoute` + `RoleRoute`; `/referral-portal/ref-candidate-details` under `ReferralProtectedRoute`

**Checkpoint**: US10 complete — referral submission, SPOC management, referral portal auth, resume download all functional.

---

## Phase 22: User Story 11 — Supply / Demand / Bench Visibility (P3)

**Goal**: PMO uploads demand/bench Excel; combined dashboard with filters; history preserved.

**Independent Test**: Upload demand Excel → records appear. Apply BU + skill filters → only matching shown. Re-upload → history entry created.

- [X] T187 [P] Create `backend/app/schemas/supply.py`: `DemandDataOut`, `BenchDataOut`, `SupplyFilter`, `UploadResponse`, `HistoryOut`
- [X] T188 [US11] Create `backend/app/services/supply_service.py`: `upload_demand`; `upload_bench`; `get_demand(filters, db)`; `get_bench(filters, db)`; `get_demand_history`; `get_bench_history`; `get_filter_options` (locations, bench statuses, grades); `get_supply_info(filters, db)`
- [X] T189 [US11] Create `backend/app/api/v1/supply.py`: `POST /api/v1/supply/demand/upload`; `POST /api/v1/supply/bench/upload`; `GET /api/v1/supply/demand`; `GET /api/v1/supply/bench`; `GET /api/v1/supply/demand/history`; `GET /api/v1/supply/bench/history`; `GET /api/v1/supply/filter-options`; per contracts/supply.md
- [X] T190 [US11] Register supply router in `backend/app/main.py`
- [X] T191 [P] [US11] Create `frontend/src/services/supplyService.ts`: typed wrappers
- [X] T192 [US11] Create `frontend/src/pages/DemandSupplyPage.tsx` (`/demand-supply`): two-panel layout (demand | bench); filter controls (location, BU, account, skill, grade, bench status); `<FileUpload>` panels for uploads; history view
- [X] T193 Add `/demand-supply` to `routes.tsx` with `RoleRoute` (PMO/Lead)

**Checkpoint**: US11 complete — demand/bench upload, combined view, filters, history tracking all functional.

---

## Phase 23: User Story 13 — Automated Alerts & Scheduled Notifications (P3)

**Goal**: APScheduler runs 4 jobs: aging SLA (daily), interview reminders (every 15 min), feedback reminders (daily), export cleanup (twice daily).

**Independent Test**: Trigger `GET /api/v1/admin/trigger-job/aging-sla` → entries written to `logs/email.log`. All 4 jobs registered in APScheduler at startup.

- [X] T194 [US13] Create `backend/app/services/notification_service.py`: `format_aging_email(candidate, email)`; `format_interview_reminder(booking)`; `format_feedback_reminder(booking)`; `send_notification(payload)` — always writes to `logs/email.log`; if `settings.SMTP_ENABLED` sends via `smtplib.SMTP`
- [X] T195 [US13] Create `backend/app/core/scheduler.py`: APScheduler `AsyncIOScheduler`; `create_scheduler()` registers 4 jobs: `sendAgingSLAs` (cron daily 9AM), `sendInterviewReminder` (interval 15 min), `feedbackFormReminder` (cron daily 9AM), `deleteExcelHistory` (cron 9AM + 9PM)
- [X] T196 [US13] Implement all 4 job functions in `scheduler.py`: `job_aging_sla(db)` queries candidates beyond SLA, calls `notification_service` per RecruiterLead; `job_interview_reminder(db)` queries bookings within 15 min; `job_feedback_reminder(db)` queries `feedback_submitted=False` bookings past SLA; `job_export_cleanup(db)` calls `document_service.cleanup_old_exports()`
- [X] T197 [US13] Add APScheduler lifespan to `backend/app/main.py`: `@asynccontextmanager lifespan` starts scheduler on startup, shuts down on shutdown
- [X] T198 [US13] Add `GET /api/v1/admin/trigger-job/{job_name}` to `backend/app/api/v1/admin.py` (Admin only) for manual dev testing
- [X] T199 [US13] Create `backend/tests/test_notifications.py`: smoke test `notification_service` output structure; verify log entry written to temp file; test job functions importable without error

**Checkpoint**: US13 complete — all 4 scheduled jobs registered and functional; SMTP upgrade path documented in `.env.example`.

---

## Phase 24: Final Routes, OWASP Hardening & Production Readiness

**Purpose**: Security hardening, rate limiting, pagination, correlation IDs, remaining page stubs, full test coverage, final audit.

- [X] T200 Add `slowapi` rate limiter to `backend/app/main.py`: 100 req/min per IP default; 10 req/min on `/api/v1/auth/login` (brute-force protection per constitution §IV)
- [X] T201 Add security headers middleware to `backend/app/main.py`: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: strict-origin-when-cross-origin`, `X-XSS-Protection: 1; mode=block`
- [X] T202 [P] Verify pagination on all list endpoints: `GET /api/v1/candidates`, `/api/v1/employees`, `/api/v1/slots`, `/api/v1/referral`, `/api/v1/supply/demand`, `/api/v1/supply/bench` — confirm `page` + `page_size` params with `max_size=100` enforced
- [X] T203 Add request correlation ID middleware to `backend/app/main.py`: generate `X-Request-ID` UUID; include in every response header and log entry
- [X] T204 [P] Create `frontend/src/pages/PanelInsightsPage.tsx` stub (`/panel-insights`): placeholder with "Coming Soon" message for future panel insights module
- [X] T205 [P] Create `frontend/src/pages/ChangeRolesPage.tsx` (`/changeroles`): allows user to switch active role without re-login; calls `AuthContext.setActiveRole()`; re-applies BU-aware routing
- [X] T206 Add `/panel-insights` and `/changeroles` to `routes.tsx`
- [X] T207 Update `frontend/src/routes.tsx`: final pass — add ALL routes from plan.md Phase 2+ route list that have not yet been added in prior phases; verify no route is missing
- [X] T208 Final OWASP Top 10 full audit across ALL backend routers: SQL injection (ORM-only ✅); no hard-coded secrets ✅; Pydantic at every POST/PUT ✅; 5 MB on all upload endpoints ✅; RBAC on every non-public endpoint ✅; CORS from env var ✅; file path traversal check in `file_storage.py`; rate limiting on auth ✅
- [X] T209 [P] Create `backend/tests/test_workflow.py`: workflow submit → 201; approve → 200; ARC flag triggered on CTC exceed
- [X] T210 [P] Create `backend/tests/test_admin.py`: add skill → 201; duplicate → 400; delete → 200; BU-scoped response
- [X] T211 [P] Create `backend/tests/test_analytics.py`: pie chart → 200 with expected structure; Excel export → 200 streaming
- [X] T212 [P] Create `backend/tests/test_referral.py`: form-headers → 200; submit → 201; SPOC status update → 200
- [X] T213 Update `backend/seed_data.py`: add sample `source_master`, `vendor_master`, `approver_dl_mapping`, SAP capability + skill rows, and L2 select transitions
- [X] T214 Update `quickstart.md`: add Phase 2–5 notes — recharts install, APScheduler startup log verification, SMTP env var guide, export history cleanup schedule, test command for each phase
- [X] T215 Run full end-to-end validation: all migrations → seed → backend → frontend → login → smoke test each of the 16 user stories
- [X] T216 [P] Create performance benchmark suite in `backend/tests/test_performance.py`: (a) `locust` or `pytest-benchmark` scenario for 500 concurrent users hitting `/api/v1/candidates` (SC-002); (b) time bulk candidate upload of 500-row Excel (SC-003); (c) time feedback PDF generation (SC-005); (d) time `/api/v1/reports/pie-chart` with 10 000-row dataset (SC-007); (e) time Excel export of 10 000 rows (SC-008); assert each result meets its SC threshold

---

## Summary: BRD Module Coverage

| BRD Module | BRD § | User Story | Key Tasks |
|------------|--------|-----------|-----------|
| Role Selection | 3.1 | US1 | T043–T049 |
| Interviewer Dashboard | 3.2 | US2 + US3 | T050–T063 |
| Feedback Management | 3.3 | US6 | T095–T102 |
| Candidate Management | 3.4 | US4 | T064–T070 |
| Recruiter Module | 3.5 | US5 + US8 | T071–T076, T137–T138 |
| Supply / Demand / Bench | 3.6 | US11 | T187–T193 |
| Workflow & Offer Approval | 3.7 | US7 | T103–T110 |
| Joining Bonus | 3.8 | US15 | T111–T118 |
| To-Do List | 3.9 | US8 | T137–T138 |
| Reports & Analytics | 3.10 | US9 | T146–T158 |
| L2 Report & Aging | 3.11 | Phase 19 | T159–T165 |
| Status Insights | 3.12 | US9 sub | T154 |
| Channel Insights | 3.13 | US9 sub | T155 |
| ARC Deviation Report | 3.14 | US9 sub | T156 |
| Rejection Report | 3.15 | US9 sub | T157 |
| Administration | 3.16 | US12 | T119–T126 |
| Employee Referral Portal | 3.17 | US10 | T173–T186 |
| Weekend Drive | 3.18 | US16 | T166–T172 |
| Alerts & Notifications | 3.19 | US13 | T194–T199 |
| PDF & Document Management | 3.20 | US14 | T127–T136 |
| Candidate Approval Data | 3.21 | Phase 16 | T141–T143 |
| Panel Registration | 3.22 | US2 | T050–T055 |
| Feedback Form Report | 3.23 | Phase 16 | T142–T143 |

**Total tasks**: T001–T215 = **215 tasks**

---

## Dependencies & Execution Order

```
Phase 1 (Setup)               → Start immediately
Phase 2 (Foundational)        → Requires Phase 1 — BLOCKS all user stories
Phase 3 (US1)                 → Requires Phase 2
Phase 4 (US2)                 → Requires Phase 2 + US1
Phase 5 (US3)                 → Requires Phase 2 + US2
Phase 6 (US4)                 → Requires Phase 2 + US1
Phase 7 (US5)                 → Requires US3 + US4
Phase 8 (Phase 1 Polish)      → Requires Phases 3–7
Phase 9 (Phase 2 Migrations)  → Requires Phase 8 — BLOCKS Phases 10–16
Phase 10 (US6 Feedback)       → Requires Phase 9
Phase 11 (US7 Workflow)       → Requires Phase 9
Phase 12 (US15 JoiningBonus)  → Requires Phase 11
Phase 13 (US12 Admin)         → Requires Phase 9
Phase 14 (US14 Documents)     → Requires Phase 10 + US4
Phase 15 (US8 Full ToDo)      → Requires Phase 10
Phase 16 (Reports P2)         → Requires Phase 10 + Phase 11
Phase 17 (Phase 3 Migrations) → Requires Phase 16 — BLOCKS Phases 18–22
Phase 18 (US9 Analytics)      → Requires Phase 17
Phase 19 (L2 Report)          → Requires Phase 17
Phase 20 (US16 Weekend Drive) → Requires Phase 5 (slot service)
Phase 21 (US10 Referral)      → Requires Phase 9 (referral migrations)
Phase 22 (US11 Supply)        → Requires Phase 17
Phase 23 (US13 Alerts)        → Requires Phase 10 + Phase 15
Phase 24 (Hardening)          → Requires all prior phases
```

### Incremental Delivery Milestones

| Milestone | Phases | Delivers |
|-----------|--------|---------|
| M1 — Core Loop | 1–8 | Full P1 pipeline: Auth + Employees + Slots + Candidates + Booking |
| M2 — Feedback & Approval | 9–16 | Feedback PDF + Offer Workflow + Joining Bonus + Master Data + Documents |
| M3 — Analytics & Reporting | 17–19 | All charts, L2 aging, Excel exports |
| M4 — Full Platform | 20–23 | Referral Portal + Supply/Demand + Weekend Drive + Alerts |
| M5 — Production-Ready | 24 | OWASP hardening, rate limiting, security headers, full test coverage |

---

## Notes

- [P] = parallelizable within phase — safe to assign to separate developers
- [USn] = user story traceability label
- **Critical migration order**: 001 role_master → 002 master_data (tech/tower) → 003 employees → 004 calendar → 005 candidates → 006 feedback → 007 workflow → 008 supply → 009 referral → 010 extended_master → 011 export_history → 012 l2_tracking
- NEVER create a migration FK referencing a table defined in a higher-numbered migration
- JWT in localStorage (T035) is local-dev only — constitution §IV httpOnly cookie path must be wired before any shared-env deployment
- File upload 5 MB limit enforced at both API layer (`file_storage.py`) and `FileUpload.tsx`
- SMTP disabled by default (`SMTP_ENABLED=false`); all notification output goes to `logs/email.log` for local dev
- Rate limiter (T200): auth endpoint 10 req/min; all others 100 req/min per IP

