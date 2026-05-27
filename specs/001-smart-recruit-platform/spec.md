# Feature Specification: Smart Recruit Platform

**Feature Branch**: `001-smart-recruit-platform`

**Created**: 2026-05-26

**Status**: Draft

**Stack**: React (frontend) · Python/FastAPI (backend) · PostgreSQL `smarthiremain001` (database)

**Input**: Full platform specification derived from BRD-AND-COMPLETE-DOCS.md

---

## Constitution Compliance Check

> All items MUST be confirmed before the spec is considered complete.

- [x] This feature is implementable with React + Python + PostgreSQL only
- [x] No Angular, Node.js, Spring Boot, or non-approved technology required
- [x] API endpoint contracts will be defined in `contracts/` before frontend work begins
- [x] Any new data entities will have Alembic migrations before ORM models

---

## Overview

**Smart Recruit** (also called SmartHire) is an end-to-end recruitment lifecycle management platform designed for a large-scale professional services organisation (Capgemini). It digitises the entire hiring pipeline: from candidate sourcing and interview scheduling, through multi-round feedback collection and multi-level offer approval, to date-of-joining tracking. It also includes an employee referral portal, supply/demand/bench visibility, and a rich suite of recruitment analytics dashboards.

### Target Users / Personas

| Persona | Description |
|---------|-------------|
| **Interviewer** | Technical panelist who marks availability slots and submits structured interview feedback |
| **Recruiter** | HR/TA team member who schedules interviews, manages candidate pipeline, uploads bulk data |
| **PMO** | Project Management Office — manages candidate-to-project allocation and joining processes |
| **Practice Lead** | Oversees candidates and interviewers within a technology practice |
| **Lead** | Individual tech lead with data upload/access rights |
| **Tower Lead / SL-BU Lead / NA Lead / Recruiter Lead** | Senior leads reviewing and approving offer workflows |
| **BU Admin / Practice Admin** | Manages master data for a Business Unit or Practice |
| **Admin / Super User** | Full-access administrator — manages all data, users, and configurations |
| **Referral SPOC** | Manages the employee referral programme end-to-end |
| **Referral User (Employee)** | Any employee who refers an external candidate via the referral portal |

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 — Authenticated Role-Based Access (Priority: P1)

A user (employee) navigates to the platform, is authenticated via corporate SSO, and is directed to the appropriate home screen based on their assigned role(s). Users with multiple roles choose which role to operate under for the session.

**Why this priority**: All modules and functionality depend on a working auth and role-routing layer. Without this, no other user story can be tested.

**Independent Test**: Navigate to the platform URL, complete SSO login, select a role, and confirm redirection to the expected landing page (e.g., Interviewer → `/dashboard`, Recruiter → `/todolist`).

**Acceptance Scenarios**:

1. **Given** an employee has a valid corporate SSO credential, **When** they access the platform, **Then** they are redirected to the SSO identity provider for authentication.
2. **Given** a user completes SSO login, **When** the system retrieves their roles, **Then** they see only the roles assigned to them on the role-selection screen.
3. **Given** a user selects a role with a BU of SAP, **When** they are a Recruiter or PMO, **Then** they land on `/upload`; for all other BUs they land on `/todolist`.
4. **Given** a user's JWT token expires, **When** they attempt a protected action, **Then** they are redirected to the login/SSO flow.
5. **Given** a user without any assigned roles logs in, **When** the role-selection screen loads, **Then** they see an empty role list and an appropriate message.

---

### User Story 2 — Panel Registration & Employee Management (Priority: P1)

An Admin registers a new employee as a panel member (interviewer), assigns their technology skills, roles, tower, and BU. The system creates the account in both the application database and the corporate identity provider (Keycloak).

**Why this priority**: All scheduling and feedback workflows depend on interviewer records existing in the system. Panel registration must be operational before any interviews can be booked.

**Independent Test**: An Admin creates a new panel member record; the new user can then log in and see the interviewer dashboard.

**Acceptance Scenarios**:

1. **Given** an Admin is on the Panel Registration screen, **When** they fill all required fields and submit, **Then** the employee record is created and the user can log in.
2. **Given** an Admin submits a duplicate employee email, **When** the system validates, **Then** an error message is displayed and no duplicate is created.
3. **Given** an existing panel member's skills change, **When** an Admin updates their profile, **Then** the updated skills appear immediately in slot searches.
4. **Given** an Admin removes a technology skill from a panel member, **When** a Recruiter searches for interviewers for that skill, **Then** that panel member no longer appears.
5. **Given** an Admin deletes an employee, **When** the delete is confirmed, **Then** the employee is removed from both the application and the identity provider.

---

### User Story 3 — Interviewer Slot Management (Priority: P1)

An Interviewer marks their availability for interview slots by specifying date, time, and technology area. Slots appear on their calendar and become available for Recruiters to book.

**Why this priority**: Recruiter booking and candidate scheduling depend entirely on interviewers having published available slots. This is the supply side of the core matching flow.

**Independent Test**: An Interviewer creates a free slot; a Recruiter can see and book it.

**Acceptance Scenarios**:

1. **Given** an Interviewer is on the dashboard, **When** they create a free slot with date/time/technology, **Then** the slot appears as green (available) on their calendar.
2. **Given** a slot already exists at the same time, **When** the Interviewer attempts to create an overlapping slot, **Then** the system rejects it with a conflict error.
3. **Given** an Interviewer uploads a bulk panel slot Excel file, **When** the file is valid, **Then** all slots in the file are created and visible on the calendar.
4. **Given** an available slot exists, **When** a Recruiter books it, **Then** the slot status changes to "Booked" (pink) on the calendar.
5. **Given** a slot is in "Booked" state, **When** the Recruiter reschedules or cancels it, **Then** the slot reverts to available or is removed from the calendar respectively.
6. **Given** it is a weekend drive, **When** an Interviewer creates a slot with the weekend drive flag, **Then** the slot is treated separately from regular availability.

---

### User Story 4 — Candidate Upload & Profile Management (Priority: P1)

A Recruiter uploads a bulk candidate Excel sheet. The system parses, validates, and imports all candidate records. The Recruiter can then view and edit individual candidate profiles including status, skill, source, and comments.

**Why this priority**: All downstream scheduling, feedback, offer, and reporting functionality depends on candidate records existing in the system.

**Independent Test**: A Recruiter uploads the standard candidate Excel template; all valid rows appear as candidate records in the candidate list with correct field mapping.

**Acceptance Scenarios**:

1. **Given** a Recruiter uploads a correctly formatted candidate Excel sheet, **When** processing completes, **Then** all valid candidates are imported and visible in the candidate list.
2. **Given** the uploaded sheet contains duplicate candidate rows, **When** processing completes, **Then** duplicate rows are flagged and returned as a downloadable error Excel file; valid rows are still imported.
3. **Given** a Recruiter edits a candidate's skill, **When** the update is saved, **Then** the updated skill is immediately reflected in all views of that candidate.
4. **Given** a Recruiter adds a comment with an attachment (≤5 MB) to a candidate, **When** saved, **Then** the comment and file attachment are visible in the candidate's comment history.
5. **Given** a candidate's status needs to change (e.g., L1 Scheduled → L1 Selected), **When** the Recruiter/PMO updates the status, **Then** only valid next-state transitions (per the status transition map) are offered.
6. **Given** a candidate has been offered a position, **When** the PMO updates the date of joining, **Then** the DOJ is recorded and visible in the DOJ tracking screen.

---

### User Story 5 — Interview Booking & Scheduling (Priority: P1)

A Recruiter searches for available interviewers for a specific technology and time, then books a slot for a candidate. The system records the booking, generates a virtual meeting link (Teams), and sends invites to both the candidate and interviewer.

**Why this priority**: This is the central scheduling action of the platform — it connects candidates with interviewers and triggers the interview feedback workflow.

**Independent Test**: A Recruiter books a slot for a candidate; the booking appears on both the interviewer's calendar and the Recruiter's to-do list; a Teams meeting link is generated.

**Acceptance Scenarios**:

1. **Given** a Recruiter selects a technology and time window, **When** they search for available interviewers, **Then** only interviewers with matching skills and open slots in that window are returned.
2. **Given** a Recruiter selects an interviewer and books a slot for a candidate, **When** the booking is confirmed, **Then** a unique meeting link is generated and stored with the booking.
3. **Given** a booking is created, **When** the system processes it, **Then** calendar invitations are sent to the interviewer and candidate via email.
4. **Given** an existing booking needs to change, **When** the Recruiter reschedules it, **Then** the old slot reverts to available, a new slot is booked, and updated invitations are sent.
5. **Given** an interviewer is unavailable (no open slots), **When** a Recruiter needs to book them urgently, **Then** the Recruiter can create a "direct booking" that bypasses the availability check.
6. **Given** today's date, **When** a Recruiter views the to-do list, **Then** all interviews scheduled for today are shown with candidate and interviewer details.

---

### User Story 6 — Feedback Collection & PDF Generation (Priority: P2)

After an interview concludes, the interviewer fills a structured technology-specific feedback form (technical parameters + behavioural + recommendation). The system generates a PDF of the submitted feedback and stores it for download.

**Why this priority**: Feedback is required before a candidate can advance to the next stage. It is a mandatory gate in the pipeline.

**Independent Test**: An Interviewer submits feedback for a completed interview; a Recruiter can download the generated feedback PDF.

**Acceptance Scenarios**:

1. **Given** an interview is completed (slot status = "Interviewed"), **When** the Interviewer opens the feedback form, **Then** the form is pre-populated with the candidate's name, date, interview type, and the correct technology-specific rating parameters.
2. **Given** the Interviewer completes all required sections and submits, **When** the submission is saved, **Then** a PDF is generated and stored; the interview is marked as "Feedback Submitted."
3. **Given** multiple technology feedback form templates exist, **When** an Interviewer opens the form for a specific skill, **Then** the form displays sections and parameters specific to that technology.
4. **Given** a feedback PDF exists, **When** a Recruiter requests the PDF, **Then** the correct document is returned for download.
5. **Given** a candidate undergoes a re-interview (revisit), **When** feedback is submitted, **Then** it is stored separately from the original feedback and linked as a revisit entry.
6. **Given** an interview's feedback is pending beyond a configured SLA, **When** the daily reminder job runs, **Then** the interviewer receives an email reminder.

---

### User Story 7 — Offer Approval Workflow (Priority: P2)

A selected candidate's offer package is routed through a multi-level approval chain (Recruiter → Tower Lead → BU Lead → NA Lead). Each approver reviews CTC details, adds comments, and approves or rejects. The system tracks the full approval history and flags ARC deviations.

**Why this priority**: Offer approvals are required before an offer can be formally released to the candidate.

**Independent Test**: A Recruiter submits a candidate for offer approval; a Tower Lead sees the candidate in their workflow queue, approves it, and the candidate advances to the next approval level.

**Acceptance Scenarios**:

1. **Given** a candidate has a "Selected" status and CTC details, **When** the Recruiter submits for offer approval, **Then** the candidate appears in the Tower Lead's workflow queue.
2. **Given** a Tower Lead reviews an offer, **When** they approve it, **Then** the candidate moves to the next approver level (BU Lead).
3. **Given** a Tower Lead rejects an offer, **When** they add a rejection reason and submit, **Then** the candidate is returned to the Recruiter with the rejection reason visible.
4. **Given** an offered CTC exceeds the approved ARC threshold, **When** the workflow is submitted, **Then** an ARC deviation flag is raised and visible in the ARC Deviation Report.
5. **Given** an approver adds a comment during the approval process, **When** any authorised user views the candidate's approval history, **Then** all comments are visible in chronological order.
6. **Given** a candidate's CTC history has multiple revisions, **When** an approver views CTC history, **Then** all historical CTC values are shown with timestamps and who changed them.

---

### User Story 8 — Recruiter To-Do List & Daily Dashboard (Priority: P2)

A Recruiter/PMO/Practice Lead opens their daily task dashboard to see: pending feedback submissions, today's scheduled interviews, and candidates awaiting status updates — all in one consolidated view.

**Why this priority**: This is the primary daily driver for Recruiters and PMOs; it surfaces the most time-sensitive actions and reduces the risk of SLA breaches.

**Independent Test**: A Recruiter logs in and sees all their pending items (feedback overdue, interviews today, candidates requiring status action) in a single list.

**Acceptance Scenarios**:

1. **Given** there are interviews completed without feedback submissions, **When** the Recruiter views the to-do list, **Then** each pending feedback item is listed with the candidate name and interview date.
2. **Given** interviews are scheduled for today, **When** the Recruiter loads the to-do list, **Then** today's interviews appear sorted by time with interviewer and candidate details.
3. **Given** a candidate requires a status update, **When** the Recruiter updates the status from the to-do list, **Then** the status change is persisted and the item is removed from the pending list.
4. **Given** a Recruiter switches to the weekly view, **When** they view their slots by week, **Then** all interview slots for the current week are displayed in a calendar-style layout.

---

### User Story 9 — Recruitment Analytics & Reports (Priority: P3)

Managers and Recruiter Leads view recruitment performance analytics via interactive charts: select/reject ratios by skill/source/vendor, monthly interview volume trends, channel performance, L2 pipeline status, and aging reports. Data can be exported to Excel.

**Why this priority**: Analytics inform hiring decisions and SLA management, but the platform delivers operational value before reports are complete.

**Independent Test**: A Recruiter Lead applies date and skill filters to the analytics dashboard and sees updated charts reflecting real pipeline data, and can export to Excel.

**Acceptance Scenarios**:

1. **Given** a Recruiter Lead views the analytics dashboard, **When** they apply a date range and technology filter, **Then** the pie charts and trend charts update to reflect only matching data.
2. **Given** recruitment data exists across multiple sources, **When** a Manager views the channel insights screen, **Then** each sourcing channel shows volume, select rate, and reject rate.
3. **Given** candidates are in the L2 pipeline, **When** a PMO views the L2 report, **Then** all L2-stage candidates are listed with days-since-L2-select and status.
4. **Given** candidates exceed the L2 aging SLA threshold, **When** a PMO views the L2 aging report, **Then** only over-SLA candidates are highlighted.
5. **Given** a user requests an Excel export of any report, **When** the export is generated, **Then** the downloaded file contains all filtered data matching the screen view.
6. **Given** a reporting user selects the rejection report, **When** the data loads, **Then** rejection counts are broken down by reason, stage, technology, and source.

---

### User Story 10 — Employee Referral Portal (Priority: P3)

An employee submits a referral for an external candidate by filling a form with the candidate's details, skills, and uploading their resume. The Admin/Referral SPOC reviews, approves, or rejects referred candidates through a dedicated management view.

**Why this priority**: The referral portal is semi-independent from the core pipeline and can be developed and tested separately; it shares only master data lookups and employee records.

**Independent Test**: An employee submits a referral with resume; the Referral SPOC can view the submission and update its status to "Selected" or "Rejected."

**Acceptance Scenarios**:

1. **Given** an employee accesses the referral portal, **When** they complete the referral form and upload a resume (PDF/DOC), **Then** the referral is submitted and the employee sees a confirmation.
2. **Given** a Referral SPOC views the referral dashboard, **When** they filter by skill or status, **Then** only matching referral candidates are shown.
3. **Given** a Referral SPOC updates a referral's status to "Selected," **When** the update is saved, **Then** the new status is immediately visible to the submitting employee.
4. **Given** a referred candidate's profile exists, **When** the Referral SPOC downloads the resume, **Then** the correct file is downloaded from secure storage.
5. **Given** an employee registers for the referral portal for the first time, **When** the registration is validated against the employee master, **Then** access is granted only if the employee exists in the system.

---

### User Story 11 — Supply / Demand / Bench Visibility (Priority: P3)

PMOs and Leads upload demand (open positions) and bench resource data via Excel. They then view a combined dashboard to match open demands against available bench employees, with filters for location, BU, grade, and skill.

**Why this priority**: Supply/demand visibility supports workforce planning decisions but does not block the core interview and offer pipeline.

**Independent Test**: A PMO uploads a demand Excel and a bench Excel; the demand-supply dashboard reflects the uploaded data with all filter options working.

**Acceptance Scenarios**:

1. **Given** a PMO uploads a valid demand Excel file, **When** processing completes, **Then** all demand records appear in the demand view with correct field mapping.
2. **Given** both demand and bench data exist, **When** a Manager applies BU and skill filters, **Then** only matching demand and bench records are shown side by side.
3. **Given** a demand or bench record changes, **When** new data is uploaded, **Then** a history entry is created preserving the previous state.

---

### User Story 12 — Administration & Master Data Management (Priority: P2)

BU Admins and Admins manage all lookup and reference tables (skills, towers, vendors, sources, feedback form templates, approver distribution lists) through a self-service admin panel without requiring code changes.

**Why this priority**: All dropdowns, validations, and routing rules throughout the platform depend on accurate master data. This must be manageable by non-technical staff.

**Independent Test**: An Admin adds a new technology skill with tower mapping; the skill immediately appears as an option when a Recruiter searches for interviewers or creates a candidate.

**Acceptance Scenarios**:

1. **Given** an Admin adds a new skill with a tower mapping, **When** the skill is saved, **Then** it appears in all skill-related dropdowns immediately.
2. **Given** an Admin attempts to add a skill that already exists, **When** they submit, **Then** an error "TECHNOLOGY ALREADY EXISTS" is returned and no duplicate is created.
3. **Given** an Admin soft-deletes a skill, **When** the deletion is confirmed, **Then** the skill is no longer available in dropdowns but existing candidate records retaining that skill are unaffected.
4. **Given** a BU Admin accesses the master data screen, **When** they view it, **Then** they see only the data categories relevant to their BU (standard, SAP, or Invent).
5. **Given** an Admin updates an Approver Distribution List, **When** the next offer approval email is triggered, **Then** the updated DL recipients receive the notification.

---

### User Story 15 — Joining Bonus Management (Priority: P2)

A Recruiter Lead views and manages joining bonus commitments for selected candidates. The system tracks bonus amounts, approval status, and provides a BU-level view of all joining bonus candidates.

**Why this priority**: Joining bonus commitments are part of the offer package and must be tracked alongside the offer approval workflow before offers can be formally released.

**Independent Test**: A Recruiter Lead views the `/joiningbonus` page; a candidate with an assigned joining bonus appears with the correct amount and approval status; BU-level view shows all JB candidates for the BU.

**Acceptance Scenarios**:

1. **Given** a candidate has a "Selected" status and a joining bonus is applicable, **When** the Recruiter Lead opens the Joining Bonus screen, **Then** the candidate appears in the JB candidates list with their bonus amount and current status.
2. **Given** a Recruiter Lead updates a joining bonus status, **When** the update is saved, **Then** the new status is immediately visible in the JB candidates list.
3. **Given** a BU Admin views the Joining Bonus screen, **When** it loads, **Then** only JB candidates belonging to their Business Unit are shown.
4. **Given** a distribution list (DL) is configured for joining bonus approvals, **When** a JB status is updated, **Then** the configured DL recipients receive a notification.
5. **Given** multiple CTC revisions exist for a candidate, **When** an approver views CTC history in the JB workflow, **Then** all revisions are shown in reverse chronological order with timestamps.

---

### User Story 16 — Weekend Drive Management (Priority: P3)

An Admin or Recruiter manages a special weekend interview drive event — creating bulk interview slots, importing candidate batches for the drive, and tracking drive-specific bookings separately from regular pipeline activity.

**Why this priority**: Weekend Drives are batch operations that share infrastructure with regular slot/booking modules but require dedicated bulk import templates and drive-specific tracking.

**Independent Test**: An Admin imports a weekend drive slot file; slots appear on the calendar with the `weekend_drive` flag; a candidate bulk-imported via the weekend drive template appears correctly in the candidate list.

**Acceptance Scenarios**:

1. **Given** an Admin uploads a weekend drive slot Excel file, **When** the import completes, **Then** all slots are created with the `is_weekend_drive` flag set to `true` and appear on the interviewer calendar.
2. **Given** a weekend drive import is in progress, **When** the bulk data is validated, **Then** invalid rows are flagged and returned as a downloadable error file; valid rows are still created.
3. **Given** weekend drive slots exist, **When** a Recruiter views the calendar, **Then** weekend drive slots are visually distinguished from regular availability.
4. **Given** candidates are imported via the weekend drive template, **When** import completes, **Then** all valid rows appear in the candidate list with correct field mapping and the `is_weekend_drive` context noted.
5. **Given** a weekend drive event is complete, **When** an Admin views the weekend drive management screen, **Then** they see a summary of slots created, interviews conducted, and feedback pending for that drive.

---

### User Story 13 — Automated Alerts & Scheduled Notifications (Priority: P3)

The platform automatically sends email notifications for SLA breaches (aging candidates), interview reminders (15 minutes before), feedback reminders (pending form), and daily digests — without any manual trigger from users.

**Why this priority**: Automated alerts prevent SLA breaches and missed feedback submissions, directly impacting pipeline quality. They run in background jobs and do not require real-time interaction.

**Independent Test**: A scheduled job can be triggered manually; it sends the correct emails to the correct recipients based on current data.

**Acceptance Scenarios**:

1. **Given** it is 9:00 AM daily, **When** the aging SLA job runs, **Then** all Recruiter Leads with aging candidates beyond SLA receive a summary email.
2. **Given** an interview is 15 minutes away, **When** the reminder job runs, **Then** both the interviewer and the candidate receive a reminder email with the meeting link.
3. **Given** a feedback form has not been submitted within the SLA window, **When** the daily reminder job runs, **Then** the interviewer receives an email prompting them to complete the form.
4. **Given** old Excel export files exist on the server, **When** the twice-daily cleanup job runs, **Then** all export files older than the retention threshold are deleted.

---

### User Story 14 — PDF & Document Management (Priority: P2)

Recruiters and PMOs download candidate resumes, interview feedback PDFs, email attachments, and export data to Excel from any module. Uploads include resume files, interview videos, and L1 project files.

**Why this priority**: Document management supports every step of the pipeline; interviewers and recruiters need documents to evaluate and process candidates.

**Independent Test**: A Recruiter uploads a resume for a candidate and successfully downloads it; a Recruiter downloads a feedback PDF for a completed interview.

**Acceptance Scenarios**:

1. **Given** a resume has been uploaded for a candidate, **When** a Recruiter requests the download, **Then** the correct file is returned from secure storage.
2. **Given** a user attempts to upload a file exceeding 5 MB, **When** the validation runs, **Then** the upload is rejected with a clear error message indicating the size limit.
3. **Given** a feedback form has been submitted, **When** a Recruiter downloads the feedback PDF, **Then** the PDF contains all submitted sections (technical ratings, behavioural scores, recommendation).
4. **Given** a user requests a bulk PDF dump of feedback forms, **When** the export processes, **Then** a downloadable archive containing all matching PDFs is generated.
5. **Given** a user exports any data module to Excel, **When** the export completes, **Then** the file is saved to the export history and available for re-download within the retention window.

---

### Edge Cases

- What happens when an interviewer deletes a slot that already has a booking attached?
- How does the system handle a candidate upload sheet with all rows flagged as duplicates?
- What happens when a Teams meeting link cannot be generated due to a Graph API failure — should the booking still proceed?
- How does the workflow handle an approver who is out of office (no response)?
- What happens when an Excel export job runs while the same export is still in progress?
- How does the system respond if a referral candidate's email already exists in the main candidate pipeline?
- What is the behaviour when a user tries to transition a candidate to an invalid status?
- How are multi-BU employees (belonging to more than one BU) handled in reporting filters?

---

## Requirements *(mandatory)*

### Functional Requirements

**Authentication & Access**

- **FR-001**: The system MUST authenticate all users via corporate SSO (Keycloak-compatible OAuth2/OIDC flow).
- **FR-002**: The system MUST enforce role-based access control — each role sees only the screens and actions permitted to it (see Roles table).
- **FR-003**: The system MUST present a role-selection screen to users who have multiple assigned roles, allowing them to choose their active session role.
- **FR-004**: The system MUST automatically route authenticated users to the correct home screen based on their selected role and Business Unit.
- **FR-005**: The system MUST reject requests from unauthenticated or unauthorised users with the appropriate HTTP error responses.

**Employee & Panel Management**

- **FR-006**: The system MUST allow Admins to register employees with: employee ID, name, email, location, grade, BU, practice, market unit, account, organisation, technology skills, and roles.
- **FR-007**: The system MUST sync new and updated employee records with the corporate identity provider on creation/update.
- **FR-008**: The system MUST allow Admins to assign and update roles for any registered employee.
- **FR-009**: The system MUST prevent duplicate employee registration (same email address).
- **FR-010**: The system MUST allow Admins to soft-delete or fully remove employees from the system and the identity provider simultaneously.

**Interviewer Slot Management**

- **FR-011**: The system MUST allow Interviewers to create available time slots specifying date, start time, end time, and technology/skill area.
- **FR-012**: The system MUST reject slot creation where the proposed time overlaps with an existing slot for the same interviewer.
- **FR-013**: The system MUST allow bulk slot creation via an Excel upload template.
- **FR-014**: The system MUST display interviewer slots on a calendar with colour-coded status: available (green), booked (pink), unavailable (grey), pending (yellow).
- **FR-015**: The system MUST support a "weekend drive" slot flag that separates weekend drive events from regular availability.

**Candidate Management**

- **FR-016**: The system MUST allow bulk candidate import via an Excel upload (using the defined column schema).
- **FR-017**: The system MUST detect and flag duplicate candidate rows in upload sheets and return them as a downloadable error file.
- **FR-018**: The system MUST track the following per candidate: name, email, contact, experience (total and relevant), skills, current company, status, source, vendor, and interview history across L1/L2/L3 stages.
- **FR-019**: The system MUST enforce status transitions according to a defined valid transition map (no arbitrary status changes).
- **FR-020**: The system MUST allow attaching comments (with optional file attachments ≤5 MB) to any candidate record, with full history visible.
- **FR-021**: The system MUST allow PMOs to record and update the Date of Joining for offer-accepted candidates.
- **FR-022**: The system MUST calculate and display candidate aging (days since received date) automatically.

**Interview Scheduling**

- **FR-023**: The system MUST allow Recruiters to search for available interviewers by technology and time window.
- **FR-024**: The system MUST allow Recruiters to book a specific interviewer slot for a candidate, capturing: candidate details, interview type (L1/L2/L3), skill, and meeting link.
- **FR-025**: The system MUST generate a virtual meeting link for each booking (via Microsoft Teams integration).
- **FR-026**: The system MUST send email notifications to both interviewer and candidate upon booking, rescheduling, or cancellation.
- **FR-027**: The system MUST support "direct booking" where a Recruiter books an interviewer without requiring an existing availability slot.
- **FR-028**: The system MUST allow Recruiters to reschedule or cancel existing bookings.

**Feedback Management**

- **FR-029**: The system MUST serve technology-specific feedback form templates, with configurable sections and rating parameters per technology/practice.
- **FR-030**: The system MUST allow Interviewers to submit structured feedback including: technical parameter ratings, behavioural evaluation, overall recommendation (Select/Hold/Reject), and remarks.
- **FR-031**: The system MUST generate a PDF of each submitted feedback form and store it in secure document storage.
- **FR-032**: The system MUST allow Recruiters and Admins to download feedback PDFs by candidate and interview.
- **FR-033**: The system MUST support re-interview (revisit) feedback stored separately from original interview feedback.
- **FR-034**: The system MUST allow Admins to create and manage feedback form templates per technology/practice.

**Workflow & Offer Approval**

- **FR-035**: The system MUST route selected candidates through a configurable multi-level approval workflow: Recruiter → Tower Lead → BU Lead → NA Lead.
- **FR-036**: The system MUST allow each approver to approve, reject (with reason), or add comments to a candidate's offer.
- **FR-037**: The system MUST preserve a full immutable comment and status history for every candidate in the workflow.
- **FR-038**: The system MUST flag offers where the CTC exceeds the Approved Range of Compensation (ARC) threshold, visible in the ARC Deviation Report.
- **FR-039**: The system MUST maintain a full CTC revision history per candidate.
- **FR-040**: The system MUST allow configuration of approver distribution lists per tower.

**Joining Bonus**

- **FR-041**: The system MUST allow Recruiter Leads to track joining bonus offers for selected candidates, recording bonus amounts and approval status.
- **FR-042**: The system MUST provide a BU-level view of all joining bonus candidates.

**To-Do List / Daily Dashboard**

- **FR-043**: The system MUST display, for each Recruiter/PMO/Practice Lead: pending feedback submissions, today's scheduled interviews, and candidates awaiting status action.
- **FR-044**: The system MUST allow Recruiters to update candidate status directly from the to-do list.

**Reports & Analytics**

- **FR-045**: The system MUST provide a pie chart showing select vs. reject ratios, with drill-down by source and vendor.
- **FR-046**: The system MUST provide line charts for interview volumes by month and year.
- **FR-047**: The system MUST provide a trend chart showing sourcing channel performance over time.
- **FR-048**: The system MUST provide an L2 report showing all L2-stage candidates with aging since L2 select date.
- **FR-049**: The system MUST provide an ARC deviation report listing all offers outside the approved compensation band.
- **FR-050**: The system MUST provide a rejection report showing rejection reasons by stage, skill, and source.
- **FR-051**: The system MUST allow all reports to be exported to Excel.
- **FR-052**: The system MUST support report filters including: date range, technology/skill, interview type, BU, account, source, and vendor.

**Employee Referral Portal**

- **FR-053**: The system MUST provide a self-registration flow for employees to access the referral portal.
- **FR-054**: The system MUST allow employees to submit referrals with: candidate contact info, skills (multi-select), certifications, notice period, location, and resume file upload.
- **FR-055**: The system MUST allow Referral SPOCs to review, select, or reject referral submissions.
- **FR-056**: The system MUST store referral resumes and profile images in secure document storage.
- **FR-057**: The system MUST provide referral reporting views grouped by BU and by account.

**Supply / Demand / Bench**

- **FR-058**: The system MUST allow bulk upload of demand data and bench resource data via Excel.
- **FR-059**: The system MUST display demand and bench records side by side with filters for location, BU, account, skill, and grade.
- **FR-060**: The system MUST maintain history of demand and bench data changes.

**Administration & Master Data**

- **FR-061**: The system MUST allow authorised Admins to add, update, and soft-delete the following master data types: towers, skills, skill groups, sources, vendors, role comments, feedback form templates, technology templates, PMO DL skill mappings, approver DL mappings, BU accounts, demand type master, account region mappings, SAP capabilities, and SAP skills.
- **FR-062**: The system MUST prevent creation of duplicate master data entries (same name within the same category).
- **FR-063**: The system MUST prevent deletion of master data entities that are actively referenced by candidates or interviews.
- **FR-064**: The system MUST scope the master data view to the BU of the logged-in Admin (standard BU, SAP BU, or Invent BU — each sees a different subset of configurable data types).

**Alerts & Notifications**

- **FR-065**: The system MUST send daily aging SLA alerts to Recruiter Leads for candidates exceeding their SLA threshold.
- **FR-066**: The system MUST send interview reminder notifications 15 minutes before scheduled interviews to both interviewer and candidate.
- **FR-067**: The system MUST send daily feedback form reminders to interviewers with outstanding pending feedback submissions.
- **FR-068**: The system MUST automatically purge old Excel export files on a twice-daily schedule.

**Document Management**

- **FR-069**: The system MUST store all uploaded files (resumes, videos, attachments, PDFs) in secure private cloud storage.
- **FR-070**: The system MUST enforce an upload size limit of 5 MB per file for most uploads.
- **FR-071**: The system MUST provide download access to resumes, feedback PDFs, email attachments, and interview videos for authorised users.
- **FR-072**: The system MUST maintain an export history for all generated Excel files and allow re-download within the retention window.

**Weekend Drive**

- **FR-073**: The system MUST support batch creation of interview slots specifically designated as weekend drive events.
- **FR-074**: The system MUST allow bulk candidate import with a weekend drive template.

---

### Key Entities

- **Employee**: Represents a registered user of the platform. Has roles, technology skills, tower assignments, BU, practice, account, and grade. Is the identity record for both Interviewers and Recruiter-side staff.
- **Candidate**: A job applicant being processed through the hiring pipeline. Has multi-stage interview history (L1/L2/L3), status, CTC details, source/vendor, and DOJ.
- **InterviewerSlot**: A time window where an Interviewer is available for interviews. Has date/time, technology, status (available/booked/interviewed), and a weekend drive flag.
- **InterviewBooking**: The linkage between a Candidate and an InterviewerSlot for a specific interview. Captures interview type, meeting link, feedback submission status.
- **FeedbackForm**: A submitted evaluation for a specific InterviewBooking. Contains technology-specific sections, ratings, behavioural scores, overall recommendation, and a reference to the generated PDF.
- **FeedbackTemplate**: An admin-configured template defining the sections and parameters for feedback collection for a specific technology/practice.
- **OfferWorkflow**: Tracks the multi-level approval status of a candidate's offer package. Links to approver decisions, comments history, and CTC revision history.
- **JoiningBonus**: A record of a joining bonus commitment for a selected candidate.
- **MasterData** (umbrella): Includes Tower, Skill, SkillGroup, Source, Vendor, BUAccount, DemandType, AccountRegion, SapCapability, SapSkill, RoleComment, ApproverDL.
- **ReferralCandidate**: An externally referred candidate submitted via the Referral Portal. Stored separately from the main candidate pipeline; links to the referring employee.
- **DemandRecord**: An open hiring demand (job request) with skill, grade, account, BU, and status.
- **BenchRecord**: A bench resource (available employee) with skill, grade, location, and status.
- **StatusTransition**: Governs valid from-state → to-state transitions in the candidate pipeline.
- **ExportHistory**: A record of generated Excel export files with timestamps and retention tracking.

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A Recruiter can complete the full candidate-to-interview cycle (upload → book slot → submit feedback) in under 10 minutes for a single candidate.
- **SC-002**: The platform supports at least 500 concurrent users across all roles without response degradation.
- **SC-003**: Bulk candidate Excel uploads of up to 500 rows complete within 60 seconds.
- **SC-004**: 100% of interview slots booked via the platform include a valid virtual meeting link.
- **SC-005**: Feedback PDFs are generated and available for download within 30 seconds of form submission.
- **SC-006**: All scheduled notification jobs execute within 5 minutes of their scheduled trigger time.
- **SC-007**: Report pages with active filters load and render within 3 seconds for data sets up to 10,000 records.
- **SC-008**: Excel export files for standard reports (up to 10,000 rows) are generated within 2 minutes.
- **SC-009**: 95% of users successfully complete their primary daily task (for Recruiters: booking or status update; for Interviewers: slot creation or feedback submission) without needing support.
- **SC-010**: Zero data loss for candidate records, feedback submissions, and offer workflow decisions — all changes are persisted and auditable.
- **SC-011**: All protected routes return a 401/403 response within 500ms when accessed without valid authentication.
- **SC-012**: Master data changes (add/update/delete) are reflected across all dropdowns and filters within 5 seconds of the change being saved.

---

## Assumptions

- **A-001**: Corporate SSO (Keycloak-compatible OIDC) will be available as an external dependency; the platform integrates with it but does not host it.
- **A-002**: Microsoft Teams (via Graph API) is the authorised virtual meeting tool for the organisation; meeting links are generated via this API.
- **A-003**: All file storage (resumes, PDFs, attachments, exports) uses a private-access cloud object storage service; no files are publicly accessible.
- **A-004**: Email notifications are sent via an SMTP relay service provided by the organisation (AWS SES or equivalent); the platform does not manage the email infrastructure.
- **A-005**: The application is web-first; mobile-responsive layout is required but a native mobile app is out of scope for the initial implementation.
- **A-006**: PostgreSQL is the exclusive database; the fresh implementation uses a single ORM layer (no dual Java/Node.js split).
- **A-007**: All secrets (database credentials, API keys, SMTP credentials, JWT signing secrets) are injected via environment variables or a secrets management service — no hardcoded credentials anywhere in source code.
- **A-008**: The SAP Business Unit and Invent Business Unit have specific workflow and data model variations (different skill structures, upload templates) that are handled within the same platform.
- **A-009**: Status transition rules (valid from_status → to_status paths) are configurable in a database table, not hardcoded in business logic.
- **A-010**: The referral portal is a semi-independent sub-module accessible via a distinct URL path, sharing only the employee master and master data lookup tables with the main application.
- **A-011**: Weekend Drive is a batch scheduling event type; it reuses the same slot and booking infrastructure with a flag, not a separate system.
- **A-012**: All CTC values are stored in Lakhs (Indian numbering system); conversion to display format (words) is performed at rendering time.
- **A-013**: The platform supports multi-BU operations; employees and candidates belong to a BU, and data visibility is scoped by BU for Admin roles.
- **A-014**: Excel upload templates are fixed schemas; the system validates column presence and order against the defined schema before processing.
