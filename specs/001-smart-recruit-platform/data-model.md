# Data Model: Smart Recruit Platform — Phase 1

**Date**: 2026-05-26 | **Feature**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

Phase 1 entities only (User Stories 1–5). All entities require a corresponding Alembic
migration in `backend/migrations/versions/` before any ORM model may reference them.

---

## Migration Execution Order

```
001_create_role_master
002_create_employee_tables
003_create_master_data_tables
004_create_interviewer_calendar
005_create_candidate_tables
```

---

## 001 — `role_master`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | SERIAL | PK |
| `role_name` | VARCHAR(100) | NOT NULL, UNIQUE |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() |

**Seed data** (14 rows):
`Interviewer`, `Recruiter`, `PMO`, `PracticeLead`, `Lead`, `TowerLead`, `SLBULead`,
`NALead`, `RecruiterLead`, `BUAdmin`, `PracticeAdmin`, `Admin`, `ReferralSPOC`, `ReferralUser`

---

## 002 — Employee Tables

### `employee_master`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `emp_id` | BIGSERIAL | PK |
| `emp_name` | VARCHAR(200) | NOT NULL |
| `email_id` | VARCHAR(255) | NOT NULL, UNIQUE |
| `password_hash` | VARCHAR(255) | NOT NULL |
| `location` | VARCHAR(100) | |
| `grade` | VARCHAR(50) | |
| `bu` | VARCHAR(100) | |
| `practice` | VARCHAR(100) | |
| `market_unit` | VARCHAR(100) | |
| `account` | VARCHAR(100) | |
| `organisation` | VARCHAR(100) | |
| `is_active` | BOOLEAN | NOT NULL DEFAULT TRUE |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() |
| `updated_at` | TIMESTAMPTZ | DEFAULT NOW() |

**Indexes**: `email_id` (unique), `bu`, `is_active`

### `employee_role_details`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | BIGSERIAL | PK |
| `emp_id` | BIGINT | NOT NULL, FK → `employee_master.emp_id` ON DELETE CASCADE |
| `role_id` | INT | NOT NULL, FK → `role_master.id` |
| `assigned_at` | TIMESTAMPTZ | DEFAULT NOW() |

**Unique constraint**: `(emp_id, role_id)`

### `employee_technology_details`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | BIGSERIAL | PK |
| `emp_id` | BIGINT | NOT NULL, FK → `employee_master.emp_id` ON DELETE CASCADE |
| `technology_id` | INT | NOT NULL, FK → `technology_master.id` |
| `added_at` | TIMESTAMPTZ | DEFAULT NOW() |

**Unique constraint**: `(emp_id, technology_id)`

### `employee_tower_details`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | BIGSERIAL | PK |
| `emp_id` | BIGINT | NOT NULL, FK → `employee_master.emp_id` ON DELETE CASCADE |
| `tower_name` | VARCHAR(100) | NOT NULL |

---

## 003 — Master Data Tables

### `tower_master`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | SERIAL | PK |
| `tower_name` | VARCHAR(100) | NOT NULL, UNIQUE |
| `is_active` | BOOLEAN | NOT NULL DEFAULT TRUE |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() |

### `technology_master`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | SERIAL | PK |
| `tech_name` | VARCHAR(100) | NOT NULL |
| `skill_group` | VARCHAR(100) | |
| `tower_id` | INT | FK → `tower_master.id` |
| `is_active` | BOOLEAN | NOT NULL DEFAULT TRUE |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() |

**Unique constraint**: `(tech_name, tower_id)`

---

## 004 — `interviewer_calendar`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `interviewer_calendar_id` | BIGSERIAL | PK |
| `emp_id` | BIGINT | NOT NULL, FK → `employee_master.emp_id` |
| `skill_id` | INT | FK → `technology_master.id` |
| `slot_date` | DATE | NOT NULL |
| `from_time` | TIMESTAMPTZ | NOT NULL |
| `to_time` | TIMESTAMPTZ | NOT NULL |
| `slot_status` | VARCHAR(20) | NOT NULL DEFAULT 'Available' — CHECK IN ('Available','Booked','Interviewed','Pending') |
| `is_weekend_drive` | BOOLEAN | NOT NULL DEFAULT FALSE |
| `created_by` | VARCHAR(255) | |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() |
| `updated_at` | TIMESTAMPTZ | DEFAULT NOW() |

**Indexes**: `(emp_id, slot_date)`, `(emp_id, slot_status)`, `skill_id`

**Overlap constraint**: Enforced in application layer via `slot_service.overlap_check()`.
Query: `SELECT 1 FROM interviewer_calendar WHERE emp_id = :emp_id AND slot_status != 'Cancelled' AND from_time < :new_to AND to_time > :new_from`.
Returns 409 if any row found.

---

## 005 — Candidate Tables

### `status_intermediate_mapping`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | SERIAL | PK |
| `from_status` | VARCHAR(100) | NOT NULL |
| `to_status` | VARCHAR(100) | NOT NULL |

**Unique constraint**: `(from_status, to_status)`

**Seed data** (core transitions):
| from_status | to_status |
|---|---|
| Profile Received | L1 Scheduled |
| L1 Scheduled | L1 Selected |
| L1 Scheduled | L1 Rejected |
| L1 Scheduled | L1 Hold |
| L1 Selected | L2 Scheduled |
| L2 Scheduled | L2 Selected |
| L2 Scheduled | L2 Rejected |
| L2 Scheduled | L2 Hold |
| L2 Selected | Offered |
| L2 Selected | L3 Scheduled |
| L3 Scheduled | Offered |
| Offered | Offer Accepted |
| Offered | Offer Declined |
| Offer Accepted | Joined |
| Offer Accepted | Not Joined |

### `candidate_detail`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `candidate_detail_id` | BIGSERIAL | PK |
| `candidate_name` | VARCHAR(200) | NOT NULL |
| `email_id` | VARCHAR(255) | NOT NULL |
| `contact_number` | VARCHAR(20) | |
| `gender` | VARCHAR(20) | |
| `total_exp` | VARCHAR(10) | Years as string |
| `rel_exp` | VARCHAR(10) | Relevant exp |
| `current_company` | VARCHAR(200) | |
| `current_location` | VARCHAR(100) | |
| `preferred_location` | VARCHAR(100) | |
| `notice_period` | VARCHAR(50) | |
| `current_ctc` | VARCHAR(50) | In Lakhs |
| `exp_ctc` | VARCHAR(50) | Expected CTC |
| `offer_ctc` | VARCHAR(50) | Offered CTC |
| `skill_id` | INT | FK → `technology_master.id` |
| `tower` | VARCHAR(100) | |
| `skill_group` | VARCHAR(100) | |
| `source` | VARCHAR(100) | |
| `referred_vendor` | VARCHAR(100) | |
| `college` | VARCHAR(200) | |
| `level_based_on_exp` | VARCHAR(50) | |
| `overall_status` | VARCHAR(100) | NOT NULL DEFAULT 'Profile Received' |
| `dashboard_status` | VARCHAR(100) | |
| `is_referral` | BOOLEAN | DEFAULT FALSE |
| `is_rehire` | BOOLEAN | DEFAULT FALSE |
| `bu_id` | INT | |
| `practice_id` | INT | |
| `account_name` | VARCHAR(200) | |
| `region` | VARCHAR(100) | |
| `pmo_coordinator` | VARCHAR(200) | |
| `pmo_coordinator_email` | VARCHAR(255) | |
| `hr_coordinator` | VARCHAR(200) | |
| `jr_id` | VARCHAR(100) | |
| `doj` | DATE | Date of joining |
| `resume_path` | VARCHAR(500) | Path in uploads/ |
| `created_by` | VARCHAR(255) | |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() |
| `updated_at` | TIMESTAMPTZ | DEFAULT NOW() |
| `recvd_date` | DATE | Profile received date |

**Indexes**: `email_id`, `overall_status`, `skill_id`, `created_by`, `(bu_id, overall_status)`

**Duplicate detection**: Checked by `email_id` during bulk upload within the same upload batch. Existing candidates with the same email are flagged but not duplicated.

### `recruiter_calendar`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `recruiter_calendar_id` | BIGSERIAL | PK |
| `candidate_detail_id` | BIGINT | NOT NULL, FK → `candidate_detail.candidate_detail_id` |
| `interviewer_calendar_id` | BIGINT | FK → `interviewer_calendar.interviewer_calendar_id` (NULL for direct bookings) |
| `interview_type` | VARCHAR(10) | NOT NULL — L1/L2/L3 |
| `skill_id` | INT | FK → `technology_master.id` |
| `from_time` | TIMESTAMPTZ | NOT NULL |
| `to_time` | TIMESTAMPTZ | NOT NULL |
| `interview_date` | DATE | NOT NULL |
| `panel_email` | VARCHAR(255) | |
| `is_direct_booked` | BOOLEAN | NOT NULL DEFAULT FALSE |
| `meeting_link` | VARCHAR(500) | Generated UUID link |
| `feedback_submitted` | BOOLEAN | NOT NULL DEFAULT FALSE |
| `created_by` | VARCHAR(255) | |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() |

**Indexes**: `(candidate_detail_id, interview_date)`, `interviewer_calendar_id`, `interview_date`, `feedback_submitted`

### `candidate_status_history`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | BIGSERIAL | PK |
| `candidate_detail_id` | BIGINT | NOT NULL, FK → `candidate_detail.candidate_detail_id` |
| `from_status` | VARCHAR(100) | |
| `to_status` | VARCHAR(100) | NOT NULL |
| `changed_by` | VARCHAR(255) | |
| `changed_at` | TIMESTAMPTZ | DEFAULT NOW() |
| `notes` | TEXT | |

### `candidate_comments`

| Column | PostgreSQL Type | Constraints |
|---|---|---|
| `id` | BIGSERIAL | PK |
| `candidate_detail_id` | BIGINT | NOT NULL, FK → `candidate_detail.candidate_detail_id` |
| `comment_text` | TEXT | |
| `attachment_path` | VARCHAR(500) | Path in uploads/attachments/ |
| `attachment_filename` | VARCHAR(255) | Original filename |
| `created_by` | VARCHAR(255) | |
| `created_at` | TIMESTAMPTZ | DEFAULT NOW() |

---

## Entity Relationship Summary

```
role_master ──< employee_role_details >── employee_master
tower_master ──< technology_master
employee_master ──< employee_technology_details >── technology_master
employee_master ──< employee_tower_details
employee_master ──< interviewer_calendar >── technology_master
candidate_detail >── technology_master
candidate_detail ──< recruiter_calendar >── interviewer_calendar
candidate_detail ──< candidate_status_history
candidate_detail ──< candidate_comments
status_intermediate_mapping  (standalone lookup)
```

---

## SQLAlchemy Model Notes

- All models import `Base` from `backend/app/core/database.py`.
- Timestamps use `func.now()` server defaults; `onupdate=func.now()` on `updated_at`.
- Enums for `slot_status` use `ARRAY` or PostgreSQL `ENUM` type — use `VARCHAR` with a `CheckConstraint` to keep migrations simple.
- All FK relationships define `back_populates` for bidirectional access.
- `is_active` fields use soft-delete pattern — no records are physically deleted in master data.
