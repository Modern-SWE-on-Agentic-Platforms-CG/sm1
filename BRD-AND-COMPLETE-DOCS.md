# Smart Recruit — Comprehensive Specification Document

> **Status**: Generated from codebase analysis — May 2026  
> **Purpose**: Stack-agnostic source-of-truth for fresh implementation  
> **Projects Covered**: SmartHireUI · smarthiremicro · smarthiremicro 1 · smarthireReusable

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Authentication & Authorization](#2-authentication--authorization)
3. [Modules / Features](#3-modules--features)
   - 3.1 Role Selection
   - 3.2 Interviewer Dashboard
   - 3.3 Feedback Management
   - 3.4 Candidate Management
   - 3.5 Recruiter Module
   - 3.6 Supply / Demand / Bench Screen
   - 3.7 Workflow & Offer Approval
   - 3.8 Joining Bonus
   - 3.9 To-Do List
   - 3.10 Reports & Analytics
   - 3.11 L2 Report & Aging
   - 3.12 Status Insights
   - 3.13 Channel Insights
   - 3.14 ARC Deviation Report
   - 3.15 Rejection Report
   - 3.16 Administration (Master Data)
   - 3.17 Employee Referral Portal
   - 3.18 Weekend Drive
   - 3.19 Alerts & Scheduled Notifications
   - 3.20 PDF & Document Management
   - 3.21 Candidate Approval Data
   - 3.22 Panel Registration
   - 3.23 Feedback Form Report
4. [Data Models](#4-data-models)
5. [API Contract](#5-api-contract)
6. [Shared Components & Services](#6-shared-components--services)
7. [Navigation & Routing Map](#7-navigation--routing-map)
8. [Configuration & Environment](#8-configuration--environment)
9. [Non-Functional Requirements](#9-non-functional-requirements)

---

## 1. Project Overview

### Purpose
Smart Recruit (also called SmartHire) is an **end-to-end recruitment lifecycle management platform**. It digitises the full hiring pipeline: from candidate sourcing and interview scheduling, through feedback collection and offer approval, to date-of-joining tracking. It also includes an employee referral portal and a rich suite of recruitment analytics.

### Target Users / Personas

| Persona | Description |
|---------|-------------|
| **Interviewer** | Technical panelist who records slot availability and submits interview feedback |
| **Recruiter** | HR/TA team member who schedules interviews, manages candidate data, uploads bulk sheets |
| **PMO (Project Management Office)** | Manages candidate-to-project allocation and joining processes |
| **Practice Lead** | Oversees candidates and interviewers in a technology practice |
| **Lead** | Individual tech lead with upload/data access |
| **Tower Lead** | Reviews offer workflow for a technology tower |
| **SL-BU Lead / NA Lead / Recruiter Lead** | Senior leads reviewing offer approval workflows |
| **BU Admin / Practice Admin** | Manages master data for a Business Unit or Practice |
| **Admin / Super User** | Full-access admin who can manage all data, users, and configurations |
| **Referral SPOC** | Manages the employee referral program |
| **Referral User (Employee)** | Any employee who refers an external candidate via the referral portal |

### Detected Tech Stack (for reference only)

| Layer | Technology |
|-------|-----------|
| Frontend | Angular 7 + Ionic 4 (Hybrid Web + Mobile PWA) |
| Java Backend | Spring Boot 1.4.7 (REST API Microservice) |
| Node.js Backend | Express 4.17 + Sequelize ORM (REST API + file processing) |
| Shared Library | Java Maven (JPA entity and utility library shared by the Java service) |
| Database | PostgreSQL (AWS RDS, eu-west-1 region, schema: `sr_prod`) |
| Auth | Keycloak SSO + JWT |
| File Storage | AWS S3 (bucket: `smarthireprod`) |
| Email | AWS SES (SMTP) |
| Meetings | Microsoft Teams via Microsoft Graph API |
| Deployment | Docker + IBM Cloud Foundry (manifest.yml present) |

---

## 2. Authentication & Authorization

### 2.1 Login Flow

**Production (SSO Enabled)**
1. User accesses the application URL (`https://www.smartrecruit-portal.com`).
2. Frontend detects `enableSso = true` and redirects to the **Keycloak** authorization server.
   - Realm: `Smartrecruit`
   - Client ID: `Smartrecruit_id`
   - Keycloak URL: `https://www.smartrecruit-portal.com/auth`
3. Keycloak redirects to **Capgemini Corporate SSO** (`https://signin.capgemini.com`) for identity validation.
4. On successful SSO login, Capgemini SSO issues an OAuth2 authorization code.
5. The frontend exchanges the code for tokens via `POST https://signin.capgemini.com/as/token.oauth2` with:
   - `grant_type`, `code`, `redirect_uri`
   - Basic Auth header (base64 of `Smart Recruit:smartrecurit@123$`)
6. The `id_token` (JWT) is extracted and stored in `localStorage` as `token`.
7. The decoded JWT payload is stored in `localStorage` as `employeeInfo`.
8. Employee email is used to fetch roles via the Node.js backend (`panel/fetchEmpRoles`).
9. Available roles are stored in `localStorage` as `roles` (array).
10. User is redirected to `/selectrole` to pick an active role.

**Development (SSO Disabled)**
- `enableSso = false` bypasses all auth guards; all routes are accessible directly.

**Node.js Token Verification**
- All Node.js routes (except a few public ones) are wrapped in `authChecking` middleware.
- Middleware extracts `Authorization: Bearer <token>` from the request header.
- Verifies with the JWT secret key: `2018-Smart%2Recruit%2@1234#`.
- Returns HTTP 401 if token is invalid or missing.

### 2.2 Roles & Permissions Matrix

| Role | Home Route | Key Permissions |
|------|-----------|-----------------|
| Interviewer | `/dashboard` | View/manage own slots, submit feedback, view booking calendar |
| Recruiter (non-SAP BU) | `/todolist` | Upload candidate sheets, schedule interviews, manage candidate pipeline |
| Recruiter (SAP BU) | `/upload` | Same as Recruiter but with SAP-specific workflows |
| PMO (non-SAP BU) | `/todolist` | Manage date-of-joining, candidate status, L2 processes |
| PMO (SAP BU) | `/upload` | Same as PMO for SAP track |
| Practice Lead | `/todolist` | Candidate oversight for a practice area |
| Lead | `/upload` | Upload access |
| Tower Lead | `/work-flow` | Offer approval workflow for towers |
| SL-BU Lead | `/work-flow` | Offer approval workflow for SL-BU |
| NA Lead | `/work-flow` | Offer approval workflow for NA region |
| Recruiter Lead | `/work-flow` | Offer approval workflow |
| BU Admin | `/master-data` | Manage BU-level master data |
| Practice Admin | `/master-data` | Manage practice-level master data |
| Admin/SuperUser | `/candidate-referral` | Full access to all modules |
| Referral SPOC | `/candidate-referral` | Manage referral portal |

### 2.3 Auth Guards

| Guard | Mechanism | Applied To |
|-------|-----------|-----------|
| `AuthGuard` | Checks `environment.enableSso`; if true, calls `authService.canActivateRoute()` | All main application routes |
| `ReferralAuthGuard` | Separate guard for referral portal sub-routes | `/referral-portal/ref-candidate-details` |

### 2.4 Session & Token Management
- JWT access token stored in `localStorage['token']`
- Decoded employee info stored in `localStorage['employeeInfo']`
- Current active role stored in `localStorage['role']`
- All available roles stored in `localStorage['roles']` (JSON array)
- Employee name stored in `localStorage['name']`
- Employee email stored in `localStorage['email']`
- BU name stored in `localStorage['bu_name']`
- On logout, relevant localStorage keys are cleared and user is redirected to the logout page.

### 2.5 Role-Based Authorization (Node.js)
- Certain routes use `validateRecruiterAuthorization` middleware (e.g., candidate fetching).
- This queries `employee_master` and `role_master` tables to verify the requesting user has `Recruiter`, `PMO`, or `Lead` roles.
- Returns HTTP 403 `NOT_AUTHORISED_RECRUITER` if unauthorized.
- Returns HTTP 403 `RECRUITER_NOT_REGISTERED` if employee not found.

---

## 3. Modules / Features

### 3.1 Role Selection

**Purpose**: Post-login screen where authenticated users select which role to operate under for the current session.

**User Stories**
- As a logged-in user with multiple roles, I want to choose which role I'll act as, so that I see the correct screens and permissions.

**Screens / Pages**
- `/selectrole` — Displays all roles available to the user fetched from backend; user selects one and proceeds.

**Navigation Flow**
1. After login → `/selectrole`
2. User selects a role → system routes to the role-specific home page (see role routing table in §2.2)

**Data Inputs**
- Role selection (radio/button per role)

**Business Rules**
- Roles array is fetched from backend using the employee's email.
- BU name determines sub-routing for Recruiter and PMO roles (SAP BU gets `/upload`, others get `/todolist`).
- BU name is fetched from backend via `panel/fetchBU`.

**Actions**
| Action | Outcome |
|--------|---------|
| Click a role button | Sets `localStorage['role']` and navigates to the role's home route |

---

### 3.2 Interviewer Dashboard

**Purpose**: Central hub for interviewers to manage their availability slots, view scheduled/booked interviews, and navigate to feedback submission.

**User Stories**
- As an Interviewer, I want to mark my available time slots so that Recruiters can book me for interviews.
- As an Interviewer, I want to see all my upcoming scheduled interviews in a calendar view.
- As an Interviewer, I want to submit interview feedback after completing an interview.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Interviewer Dashboard | `/dashboard` | Landing page with calendar and slot management |
| Upload Popup | `/upload` | Modal for uploading files (candidate sheets, panel slots) |
| Web Feedback | `/webFeedback` | Web-based feedback form submission |
| Available Slots | `/available` | View all available (unbooked) slots |
| Booked Slots | `/booked` | View all booked interview slots |
| Interviewed | `/interviewed` | View completed interviews |
| Panel Availability | `/panel-availability` | View available panel members |
| Booking View | `/booking-view` | Calendar view of all bookings |
| Booking Form | `/booking-form` | Form to book a specific slot |

**Navigation Flow**
1. Login as Interviewer → `/dashboard`
2. From dashboard → view available/booked/interviewed tabs
3. Click a free slot → `/booking-form` to book a candidate
4. After interview → `/webFeedback` or `/feedback` to submit feedback

**Data Inputs**
- Slot creation: date, from-time, to-time, duration, practice/skill area
- Booking form: candidate details, interview type, skill, panel email, meeting link
- Feedback form: technical evaluation scores, behavioural evaluation, overall rating, recommendation

**Data Displayed**
- Calendar with colour-coded events:
  - Green: available slots
  - Pink: booked/used slots
  - Grey: unavailable
  - Yellow: pending

**Actions**
| Action | Outcome |
|--------|---------|
| Save free slot | Calls Java `/interviewer/saveFreeSlot`; slot recorded in calendar |
| Save interview slot | Calls Java `/interviewer/saveInterviewSlot` |
| Reschedule slot | Calls Java `/recruiter/rescheduleSlot` |
| Delete slot | Calls Java `/recruiter/deleteSlot` |
| Upload panel slot file | POST to Java `/slot/panelSlotUpload` (Excel upload) |
| Submit feedback | Saves via Java `/interviewer/saveFeedback` |

**Business Rules**
- Weekend drive slots are treated separately from regular slots.
- Slot saving includes a `weekendDriveCheck` flag on the DTO.
- Interviewers can only see and modify their own slots.

**Error States**
- Slot overlap: handled server-side; error returned in `ResponseDto.exception` field.
- File upload errors returned in `FileDTO.errorList`.

---

### 3.3 Feedback Management

**Purpose**: Enables interviewers and recruiters to view, generate, submit, and download interview feedback forms in structured and PDF formats.

**User Stories**
- As an Interviewer, I want to fill a structured feedback form with technical and behavioural evaluation sections.
- As a Recruiter, I want to generate a pre-populated feedback PDF for completed interviews.
- As an Admin, I want to create custom feedback form templates for different technology skill areas.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Feedback Form | `/feedback` | Interactive feedback form for an interview |
| Web Feedback | `/webFeedback` | Alternative web-accessible feedback form |
| Feedback Form Report | `/feedbackform-report` | Report view of all submitted feedback forms |

**Data Inputs (Feedback Form)**
- Interviewer name, candidate name, interview date
- Technical sections (per template): parameter name, rating (numeric scale), comments
- Behavioural evaluation: communication skills, attitude, etc.
- Overall recommendation: Select / Hold / Reject
- Overall remarks / comments

**Business Rules**
- Feedback form templates are linked to a technology/practice combination.
- Templates are managed in `FeedbackTemplateEntity` and `TechnologyTemplateEntity`.
- A blank (placeholder) form is fetched from the DB before filling.
- On submission, a PDF is generated server-side and stored in S3.
- Custom feedback forms (`CustomFeedbackFormDataEntity`) support admin-defined structures.
- `InterviewerFeedbackFormDetails` and `OverallFeedbackEntity` store submitted responses.
- Revisit feedback (re-interview) is stored separately in `RevisitInterviewFeedbackDataEntity`.

**API Dependencies**
- `POST /recruiter/feedbackForm` — generate blank feedback form by interview type
- `GET /recruiter/feedbackFormPDf` — fetch filled PDF
- `POST /feedbackForm/addFeedbackForm` — add a new form template
- `POST /feedbackForm/getFeedbackFormHeadings` — fetch form headings by technology + practice
- `POST /report/feedbackFormReport` — fetch submitted feedback report data
- `POST /report/exportFeedbackExcel` — download feedback report as Excel

---

### 3.4 Candidate Management

**Purpose**: Full candidate lifecycle management — from initial data entry, through interview stages, to final status and date-of-joining.

**User Stories**
- As a Recruiter, I want to upload a bulk candidate Excel sheet and have all candidates imported into the system.
- As a Recruiter/PMO, I want to view and edit candidate details including status, skill, source, and comments.
- As a PMO, I want to update a candidate's date of joining.
- As a user, I want to view a candidate's full interview cycle history.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Candidate Details | `/candidate-details` | Detailed view/edit of a single candidate's profile |
| Select/Reject | `/select-reject` | Batch L1 select/reject action on candidates |
| Date of Joining | `/dateofjoining` | View/update DOJ for offer-accepted candidates |
| Update Skill | `/update-skill` | Update a candidate's technology skill |
| Master Data | `/master-data` | Master table view (used by Admins) |

**Candidate Data Fields** (from `CandidateDataDTO`)

| Field | Type | Notes |
|-------|------|-------|
| candidateName | String | Required |
| candidateEmailID | String | Required |
| totalExp | String | Total experience in years |
| relExp | String | Relevant experience in years |
| gender | String | |
| skill | String | Primary technology |
| fromTime / toTime | Date | Interview time slot |
| contactNumber | String | |
| pmoCoordinator | String | PMO coordinator name |
| panelEmailID | String | Interviewer email |
| pmoCoordinatorEmailId | String | |
| interviewType | String | L1/L2/L3 etc. |
| revisitFlag | Boolean | Whether this is a re-interview |
| isReferral | Boolean | Whether candidate was referred |
| isRehire | Boolean | Whether candidate is a rehire |
| previousInterviewsInfo | List | Prior interview data |
| practiceId / buId | Long | Practice and BU associations |
| meetingLink | String | MS Teams / virtual meeting URL |
| role | String | Role being interviewed for |
| inventFlag | Boolean | Invent program flag |
| createdBy | String | Creator email |
| source | String | Sourcing channel |
| referredVendor | String | Vendor who referred |
| capability | String | SAP capability |
| currentCompany | String | Candidate's current employer |
| accountName | String | Target account |
| region | String | Geographic region |

**Excel Bulk Upload Columns** (from config.json `array` field)

Sr No., Duplicate (Y/N), Recvd Dt, Recvd Aging (Days), Quarter, Profile Rec YY/M, Candidate Name, TotalExp(Y), Relexp(Y), Tower, Skill Group, Skill, Gender, Source, Vendor/Partner Name, Email ID, Contact No, Current Co, Current Loc, Preferred/Offered Loc, Current CTC, Exp CTC, Offer CTC, Counter Offered, Revised Offered, Notice Period, Aspiring Test (Y/N), Test Score, Overall Status, Rejection Reason, Declined Reason, Comments, L2 Rank, L1 Date, L1 Aging (Days), L1 Type, L1 Panel, L2 Date, L2 Aging (Days), L2 Type, L2 Panel, L3 date/Type/Panel, HR Coordinator, PMO Coordinator, JR Mapped/SF ID/SO ID, Account Name, BU Head Apprvd Dt, Level Offered, DOJ, Dashboard Status, Offered Date, Offered M/YY, Referral Person, College, Level Based On Exp, Recruitment_Candidate_id, JR_ID, Recruitment_conversion_id

**Actions**
| Action | Outcome |
|--------|---------|
| Upload candidate Excel | POST `/s3Upload/upload` → parse → store candidates in DB |
| Update candidate status | POST `/excel/statusChange` |
| Update date of joining | POST `/excel/dateOfJoining` |
| Add comments | POST `/candidateInfo/addComments` (supports file attachments) |
| Fetch candidate comments | POST `/candidateInfo/fetchCandidateComments` |
| Update candidate info | POST `/candidateInfo/updateCandidateInfo` |
| Fetch candidate cycle | POST `/candidateInfo/fetchCandidateCycle` |
| Update skill | POST `/candidateInfo/updateSkill` |
| Rejection reason | POST `/excel/rejectionReason` |

**Business Rules**
- Duplicate detection flag (`Duplicate (Y/N)`) is present in the upload sheet.
- Candidate aging is calculated automatically from received date.
- Status transitions follow a defined `status_intermediate_mapping` table.
- L1/L2/L3 interview stages are distinct; each has its own date, panel, and result tracking.
- Aspiring Test results are captured separately.

**Error States**
- Duplicate rows flagged and returned in `ErrorExcelDTO`.
- Invalid row data generates error Excel file downloadable by user.
- Comments with attachments validated for file size (5MB limit on uploads).

---

### 3.5 Recruiter Module

**Purpose**: Enables Recruiters to manage the interview scheduling calendar, assign panel members, book slots, and track interview outcomes.

**User Stories**
- As a Recruiter, I want to search for available panel members for a specific technology and time slot.
- As a Recruiter, I want to book a slot for a candidate with a specific interviewer.
- As a Recruiter, I want to generate and download feedback PDFs after interviews.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| To-Do List | `/todolist` | Daily task view: pending feedbacks, scheduled interviews, candidates to process |
| Upload Popup | `/upload` | File upload modal for candidate data, L2 sheets, etc. |

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Get recruiter direct slots | POST `/recruiter/getDirectRecruiterSlots` | Fetch recruiter's directly-booked slots |
| Save interview slot | POST `/recruiter/saveInterviewSlot` | Book a slot for a candidate |
| Reschedule slot | POST `/recruiter/rescheduleSlot` | Reschedule existing booking |
| Delete slot | POST `/recruiter/deleteSlot` | Cancel a booked slot |
| Generate feedback form | POST `/recruiter/feedbackForm` | Create blank feedback form |
| Get pending feedbacks | POST `/todoController/fetchPendingFeedbacks` | Fetch interviews missing feedback |
| Get slots by week | POST `/todoController/fetchSlotsByWeek` | Weekly view of interview slots |
| Interviews scheduled today | POST `/todoController/interviewscheduledtoday` | Today's interview list |

**Business Rules**
- Recruiters can see all panel slots (not just their own).
- Direct booking (without interviewer availability) is supported via `DirectBookedDTO`.
- Teams meeting links are generated via Microsoft Graph API (`/getMeetingLink`) and stored with the interview.
- Resume download is available for candidates (`/excel/downloadResume`).

---

### 3.6 Supply / Demand / Bench Screen

**Purpose**: Dashboard to view and analyse the resource demand (open positions) against available bench resources (employees on bench), providing supply visibility.

**User Stories**
- As a PMO/Lead, I want to see all open demands and match them against bench resources.
- As a Manager, I want to filter demand/bench/supply data by location, BU, account, skill, and grade.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Demand Supply | `/demand-supply` | Combined view of demands vs supply |

**Data Inputs (Filters)**
- Hybrid location
- Primary location
- Bench status
- Grade/level
- BU, Account, Skill, Tower

**Data Displayed**
- Open demand records from `demand_data` table
- Bench resource records from `bench_data` table
- Supply information from `supply_screen`

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Get supply info | POST `/supplyScreen/getSupplyInfo` | Fetch supply/bench data |
| Get demand info | POST `/demandScreen/getDemandInfo` | Fetch demand data |
| Get bench info | POST `/benchScreen/getBenchInfo` | Fetch bench data |
| Upload demand Excel | POST `/demandUpload/upload` | Bulk import demand records |
| Upload bench Excel | POST `/benchUpload/upload` | Bulk import bench records |
| Fetch hybrid locations | GET `/supplyVSdemandVSbench/fetchAllHybridLocation` | Filter options |
| Fetch primary locations | GET `/supplyVSdemandVSbench/fetchAllPrimaryLocation` | Filter options |
| Fetch bench statuses | GET `/supplyVSdemandVSbench/fetchBenchStatus` | Filter options |
| Fetch grade statuses | GET `/supplyVSdemandVSbench/fetchGradeStatus` | Filter options |
| View demand history | GET `/demandHistory/getHistory` | Historical demand data |
| View bench history | GET `/benchHistory/getHistory` | Historical bench data |

**Demand Upload Sheet Columns**: "Open-Demand" sheet in Excel template.
**Bench Upload Sheet Columns**: "Sheet1" in Excel template.

**Business Rules**
- Demand and bench data are uploaded via Excel and parsed server-side.
- Changes to demand/bench go through history tracking (`demand_batch`, `bench_batch` tables).

---

### 3.7 Workflow & Offer Approval

**Purpose**: Multi-stage offer approval workflow where selected candidates' offers are routed through Tower Lead, BU Lead, NA Lead, and other approvers before finalisation.

**User Stories**
- As a Tower Lead, I want to review and approve/reject offers for candidates in my tower.
- As a Recruiter, I want to track where in the approval chain a candidate's offer stands.
- As a PMO, I want to see the full CTC history and offer revision trail for a candidate.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Workflow | `/work-flow` | Main workflow approval view |
| Workflow Info | `/work-flow-info` | Detailed candidate offer information |

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Fetch workflow candidates | POST `/workflow/fetchFlowCandidates` | Get candidates pending approval |
| Update workflow candidates | POST `/workflow/updateFlowCandidates` | Submit approval/rejection decision |
| Fetch comments history | POST `/workflow/commentsHistory` | View all comments on a candidate |
| Add comments | POST `/workflow/addComments` | Add approval/rejection comment |
| Comment dropdown | POST `/workflow/commentDropdown` | Pre-set comment options |
| Fetch JB candidates | POST `/workflow/fetchJBCandidates` | Get joining bonus eligible candidates |
| Fetch JB bonus | POST `/workflow/fetchJBBonus` | Get joining bonus details |
| Fetch all statuses | POST `/workflow/fetchAllStatuses` | Dropdown: workflow status options |
| Update JB candidates | POST `/workflow/updateJBCandidates` | Update joining bonus status |
| CTC history | POST `/workflow/ctcHistory` | View CTC change history |
| Rejection reason dropdown | POST `/workflow/rejectionReasonDropdown` | Rejection reason options |
| Fetch DL recipients | POST `/workflow/jbDLDropdown` | Distribution list for approvals |
| Threshold API | POST `/workflow/thresholdApi` | Get threshold values for offer deviation |
| Source by vendor | POST `/workflow/sourceByVendor` | Fetch source for a vendor |
| Fetch project code | POST `/workflow/getCode` | JR/project code lookup |
| Get average offered CTC | GET `/workflow/getAverageOfferedCTC` | Benchmark CTC data |
| Get approver DL details | GET `/workflow/getApproverDLDetails` | Fetch approver distribution list |
| Update approver DL details | POST `/workflow/updateApproverDLDetails` | Update approver DL |
| Fetch DL title | GET `/workflow/fetchDLTitle` | Fetch DL title options |
| Fetch new tower for lead | GET `/workflow/fetchNewTowerForLead` | Fetch tower assignments for lead |
| Get possible status | GET `/workflow/getPossibleStatus` | Valid next-state transitions |

**Business Rules**
- CTC conversion to words (Lakhs, Thousands) is performed server-side for offer letters.
- Offer approval chain: Recruiter → Tower Lead → BU Lead → NA Lead → final.
- Threshold values define when ARC (deviation from approved range) triggers an alert.
- Approver DL emails are configured per tower in `TowerApproverMasterEntity`.
- Comments history is preserved in `CandidateCommentsEntity`.

**Error States**
- If a candidate's offer CTC exceeds the threshold, an ARC deviation flag is raised.
- Unauthorized role attempting to approve returns HTTP 403.

---

### 3.8 Joining Bonus

**Purpose**: Manage and track joining bonus payments for selected candidates.

**User Stories**
- As a Recruiter Lead, I want to manage joining bonus offers for candidates to track retention commitments.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Joining Bonus | `/joiningbonus` | View and manage joining bonus candidates |
| JB Recruiter | `/jbcandidates` | Recruiter view of JB candidates |

**Data Displayed**
- Candidate name, joining bonus amount, status, approver, BU, account

**Business Rules**
- Joining bonus managed through the workflow system (`fetchJBCandidates`, `updateJBCandidates`).
- BU-level view available via `fetchJBCandidatesForBU`.
- Bonus amounts stored in `joining_bonus_master`.

---

### 3.9 To-Do List

**Purpose**: Task management dashboard showing pending actions for the logged-in user: pending feedback submissions, today's scheduled interviews, and candidates awaiting status update.

**User Stories**
- As a Recruiter/PMO/Practice Lead, I want to see my pending tasks for the day in one consolidated view.
- As a Recruiter, I want to quickly update candidate status from the to-do list.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| To-Do List | `/todolist` | Aggregated pending tasks dashboard |

**Data Displayed**
- Pending feedback submissions (interviews done, form not submitted)
- Interviews scheduled for today
- Candidate statuses requiring update
- Weekly slot summary

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Fetch all candidates | POST `/todoController/fetchAllCandidates` | All candidates for the user |
| Status dropdown | POST `/todoController/todoStatusDropdown` | Available statuses |
| Update candidate status | POST `/todoController/updateStatus` | Change candidate status |
| Fetch pending feedbacks | POST `/todoController/fetchPendingFeedbacks` | Interviews needing feedback |
| Fetch slots by week | POST `/todoController/fetchSlotsByWeek` | Weekly interview slots |
| Interviews today | POST `/todoController/interviewscheduledtoday` | Today's schedule |

---

### 3.10 Reports & Analytics

**Purpose**: Visual analytics for recruitment performance via pie charts, line charts, and trend charts.

**User Stories**
- As a Recruiter Lead, I want to see selection vs rejection ratios by skill, source, and vendor.
- As a Manager, I want to view monthly/yearly interview volume trends.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Dashboard Reports | `/dashboard-reports` | Summary dashboard with charts |
| Line Chart | `/line-chart` | Month/year-wise interview volume |
| Trend Chart | `/trend-chart` | Source/vendor trend analysis |
| Interview Data | `/interview-data` | Tabular interview data view |

**Data Displayed**
- Outer pie chart: overall select/reject distribution
- Inner pie chart: drill-down by source or vendor
- Line chart: interviews by month and year
- Trend chart: source/vendor recruitment trend over time

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Filter outer pie chart | POST `/reports/filterOuterPieChart` | Apply filters to outer pie |
| Filter inner pie chart | POST `/reports/filterInnerPieChart` | Apply filters to inner pie |
| Initial outer pie chart | GET `/reports/initialOuterPieChart` | Load default pie chart |
| Reject/select ratio | POST `/report/rejectSelectRatio` | L1/L2 select-reject ratio |
| L2 select ratio by source | POST `/report/l2selectRatioForSource` | L2 ratios per source |
| Day-wise chart | POST `/report/fetchInterviewScheduledCountDay` | Interviews per day |
| Line chart by month | POST `/lineChart/fetchInterviewtakenCountByMonth` | Monthly volume |
| Line chart by year | POST `/lineChart/fetchInterviewtakenCountByYear` | Yearly volume |
| Fetch years | GET `/lineChart/fetchAllYears` | Available year options |
| Fetch months | GET `/lineChart/fetchAllMonths` | Available month options |
| Get start/end date | GET `/reports/getStartEndDate` | Report date range |
| Fetch skills by tower | POST `/reports/fetchSkillsByTowers` | Skills dropdown for filter |
| Fetch vendors by source | POST `/reports/fetchVendorsBySources` | Vendors dropdown for filter |
| Source/vendor trend | POST `/supplyScreen/getSourceVendorTrendInfo` | Trend chart data |
| Trend chart Excel | POST `/supplyScreen/getTrendChartExcelData` | Download trend chart data |
| Generate Excel report | PUT `/report/generateReport` | Download Excel report by filters |

**Filters Available**
- Date range (from/to)
- Technology/Skill
- Interview type
- BU
- Account
- Source, Vendor

---

### 3.11 L2 Report & Aging

**Purpose**: Tracks L2 (second-round) interview outcomes, aging of candidates stuck at L2 stage, and generates comprehensive L2 status reports.

**User Stories**
- As a PMO, I want to monitor candidates at the L2 stage and identify those with aging beyond SLA thresholds.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| L2 Report | `/l2-report` | L2 status dashboard |
| L2 Aging | `/l2-aging` | Candidates exceeding L2 aging SLA |

**L2 Sheet Upload Columns**
Candidate Detail ID, Candidate name, FTE, Skill, Skill Cluster, Email ID, Phone Number, Account Mapped/Bench, SO, Profile received date, L2 Select Date, Vendor Name, Recruiter Coordinator, Notice Period, Level/Grade Offered, Docs Sub date, Test taken Dt, Sent for appr, BU Aprv Dt, NA Approval dt, DG Appr Dt, Offer Release date, Current/Previous Status, Last Updated on, Comment, Total Exp, Rel Exp, Current/Exp/Offer CTC, Counter/Revised Offered, DOJ, HR Coordinator, Days since L2, Days since Doc received, Skill Group, Dashboard Status, Error, Baseline, Offer tracking team, actionable, gender, Offered Location, l1/l2 account name, Recruitment IDs, Days Since L2 Select Category, Referral, Rehire, Referred Vendor, Source Name, College, Level Based On Exp, Business Unit, Current Company, Employee Id, Capgemini Email Id, Project Code, Region

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Get L2 status info | POST `/l2_dashboard_reports/reports` | L2 report data |
| Get L2 Excel | POST `/l2_dashboard_reports/getL2StatusInfoExcel` | Download L2 Excel |
| Get DOJ status info | POST `/l2_dashboards_reports/getDOJStatusInfo` | DOJ tracking data |
| L2 aging report | POST `/l2_dashboard_reports/agingReport` | Aging analysis |
| Export L2 aging Excel | POST `/downloadExcel/exportExcelL2AgingReport` | Download aging report |
| Export DOJ report Excel | POST `/downloadExcel/exportExcelDOJReport` | Download DOJ report |
| Upload L2 select file | POST `/l2SelectUpload/upload` | Bulk L2 data import |

---

### 3.12 Status Insights

**Purpose**: Dashboard to analyse candidate status distribution, track movements between stages, and export status reports.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Status Insights | `/status-insights` | Status distribution analytics |

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Export status insight | POST `/statusInsight/exportStatusInsight` | Download status report |
| Update status in reports | POST `/statusInsight/updateStatusInReports` | Sync status to reporting layer |

---

### 3.13 Channel Insights

**Purpose**: Analyses recruitment sourcing channels (sources and vendors) showing volume, trend, and performance metrics.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Channel Insights | `/channel-insights` | Source/vendor performance metrics |

**Data Displayed**
- Candidates by source
- Select/reject ratio by source
- Vendor performance
- Channel trend over time

**API Dependencies**
- POST `/sourceVendorInfoScreen/getSourceInfo` — source performance data
- POST `/supplyScreen/getSourceVendorTrendInfo` — trend data
- GET `/reports/initialOuterPieChart` — initial pie chart
- POST `/reports/filterReferralOuterPieChart` — referral channel pie
- POST `/reports/filterReferralInnerPieChart` — referral channel inner pie

---

### 3.14 ARC Deviation Report

**Purpose**: Tracks deviations from the Approved Range of Compensation (ARC) — cases where offered CTC falls outside the approved band.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| ARC Deviation | `/arc-deviation` | ARC deviation cases |

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Get ARC deviation info | POST `/arc_deviation_reports/getArcDeviationInfo` | Fetch deviation records |
| Export ARC Excel | POST `/arc_deviation_reports/exportExcelArcDeviationReport` | Download report |

---

### 3.15 Rejection Report

**Purpose**: Provides analysis of rejection reasons across the hiring pipeline.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Rejection Report | `/rejection-report` | Rejection analysis view |

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Get rejection reason report | POST `/rejectionReasonReport/rejectionReport` | Report data |
| Export rejection Excel | POST `/rejectionReasonExcelReport/rejectionExcelReport` | Download |

---

### 3.16 Administration (Master Data Management)

**Purpose**: Manage all lookup/reference tables that drive dropdowns and validations throughout the application.

**User Stories**
- As an Admin/BU Admin, I want to add, update, or deactivate master data (skills, towers, vendors, etc.) without code changes.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Administration | `/administration` | Admin panel with tabbed master data management |
| Master Data | `/master-data` | BU/Practice Admin view of master tables |

**Manageable Master Data Types**

| Category | Data Types |
|----------|-----------|
| Skills | Tower, Skill, Skill Group, Source, Vendor |
| Forms | Feedback Form, Role Comment, Technology Template |
| Mapping | PMO DL Skill Mapping, Approver DL Mapping, Tower-Skill Mapping, Source-Vendor Mapping |
| Org Structure | Bu Account, Demand Type Master, Account Region Mapping |
| SAP-specific | Capability, SAP Skill |

**BU-Specific Source Types**
- **Standard/Europe BU**: Tower, Skill, Skill Group, Source, Vendor, Role Comment, Feedback Form, PMO DL Skill Mapping, Approver DL Mapping, Bu Account, Demand Type Master, Account Region Mapping
- **SAP BU**: Capability, Skill, Skill Group, Source, Vendor, Feedback Form
- **Invent BU**: Tower, Skill, Source, Feedback Form

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Fetch all towers | POST `/admin/fetchAllTowers` | Tower list |
| Fetch all skills | POST `/admin/fetchAllSkill` | Skills list |
| Fetch skill groups | POST `/admin/fetchAllSkillGroup` | Skill groups |
| Fetch skills by tower | POST `/admin/fetchSkillBasedOnSkillGrpTower` | Filtered skills |
| Fetch skill practices | POST `/admin/fetchAllSkillPractice` | Practice list |
| Fetch all vendors | GET `/admin/fetchAllVendors` | Vendors list |
| Fetch vendors by source | POST `/admin/fetchVendorsBasedOnSource` | Filtered vendors |
| Add skill with mapping | POST `/admin/addSkillWithMapping` | Add skill + tower mapping |
| Add tower | POST `/admin/addTower` | Add new tower |
| Add skill group | POST `/admin/addSkillGroup` | Add skill group |
| Add source | POST `/admin/addSource` | Add sourcing channel |
| Add vendor with mapping | POST `/admin/addVendorWithMapping` | Add vendor + source mapping |
| Add role comment | POST `/admin/addRoleComment` | Add role-specific comment |
| Delete skill | POST `/admin/deleteSkillWithMapping` | Soft delete skill |
| Delete vendor | POST `/admin/deleteVendorWithMapping` | Soft delete vendor |
| Fetch role comments | POST `/admin/fetchRoleCommentBasedOnSkill` | Role comment by skill |
| Delete role comment | POST `/admin/deleteRoleCommentWithMapping` | Remove role comment |
| Fetch BU account master | GET `/admin/fetchBuAccountMaster` | BU account data |
| Add BU account | POST `/admin/addBUAccount` | New BU account |
| Fetch type master | GET `/admin/fetchTypeMaster` | Type lookup |
| Add type master | POST `/admin/addTypeMaster` | Add type entry |
| Fetch skill by template | POST `/admin/fetchSkillByTemplate` | Template-linked skills |
| Fetch all market units | GET `/admin/fetchAllmarketUnit` | Market units |
| Fetch all employee names | GET `/admin/fetchAllEmpName` | Employee email/ID |
| Manage Keycloak users | POST/PUT/DELETE `/keycloak/*` | Add/update/delete Keycloak users |

**Business Rules**
- Skills, towers, and vendors use soft delete (never physically removed).
- Cannot add a skill/tower/vendor that already exists (duplicate check).
- Cannot delete an entity that is referenced by candidates or interviews.
- SAP capability map is maintained separately in `sap_capability_master` and `sap_skill_master`.

**Error States**
- Duplicate entity: returns message `TECHNOLOGY ALREADY EXISTS` / `TOWER ALREADY EXISTS` etc.
- Empty field: returns `ANY SKILL FIELD CANNOT BE EMPTY` / `TOWER NAME CANNOT BE EMPTY` etc.

---

### 3.17 Employee Referral Portal

**Purpose**: Separate sub-portal allowing employees to refer external candidates. Features its own registration, submission flow, and admin management.

**User Stories**
- As an Employee, I want to refer a candidate by filling a form with their details and uploading their resume.
- As a Referral SPOC/Admin, I want to review, approve, or reject referred candidates.
- As a referred candidate, I want to view my application status through a dedicated link.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Referral Register | `/referral-portal/referralRegister` | Employee registers to use referral portal |
| Referral User Register | `/referralUserRegister` | Admin registers referral users |
| Referral Form | `/referral-form` | Employee submits a referral |
| Ref Candidate Details | `/referral-portal/ref-candidate-details` | View referred candidate profile (ReferralAuthGuard) |
| Referral Upload Popup | `/referral-portal/upload` | Upload referral documents |
| Referral Logout | `/referral-portal/logout` | Log out of referral portal |
| Referral Select/Reject | `/referral-select-reject` | Admin action to select/reject referral |
| Referral Error | `/referral-portal/error` | Error page |
| Reports by BU | `/ref-reports-bybu` | Referral reports grouped by BU |
| Reports by Account | `/ref-reports-byaccount` | Referral reports grouped by account |
| Candidate Referral Data | `/candidate-referral` | Admin view of all referred candidates |
| Candidate Referral Details | `/candidate-referral-details` | Detail view of a referred candidate |

**Referral Form Fields** (from `ReferralFormEntity` and `referral_candidate_info` model)
- Referee employee name, email, BU
- Candidate name, email, phone
- Skills (multi-select from `ReferralTechnologyMasterEnity`)
- Certifications (from `ReferralCertificationsMasterEntity`)
- Notice period (from `ReferralNoticePeriodMasterEntity`)
- Location (from `ReferralLocationMasterEntity`)
- Resume upload (PDF/DOC)
- Profile image upload

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Upload referral data (bulk) | POST `/referralcandidates/upload` | Bulk referral import |
| Submit referral form | POST `/referralcandidates/referralForm` | Single referral submission |
| Upload referral resume | POST `/referralresume` | Attach resume |
| Download referral resume | POST `/downloadRefResume` | Download by skill |
| Upload referral image | POST `/referralImage` | Profile image |
| Get referral form headers | GET `/referralCandidate/getReferralFormHeaders` | Master data for form dropdowns |
| Check referral employee | POST `/referralAdmin/checkReferralEmployee` | Validate employee exists |
| Fetch referral emp name | POST `/referralAdmin/getReferralEmpName` | Get employee name |
| Fetch referral emp roles | POST `/referralAdmin/fetchReferralEmpRoles` | Employee's referral roles |

**Business Rules**
- Referral portal uses a separate auth guard (`ReferralAuthGuard`).
- Referral candidates exist separately from regular pipeline candidates (`referral_candidate_info` vs `candidate_detail`).
- Resume and image files are stored in AWS S3 with `private` ACL.
- Admin approver DL emails include specific distribution lists (e.g., all towers, NA lead, recruiter lead).

---

### 3.18 Weekend Drive

**Purpose**: Manage special weekend interview drive events where large batches of candidates are interviewed simultaneously.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Weekend Drive | `/weekend-drive` | Weekend drive event management |
| Import Weekend Drive | `/import-weekend-drive` | Bulk import of weekend drive data |

**Actions**
- Import candidates via Excel using a dedicated weekend drive template.
- Weekend drive slots are flagged with `weekenDriveCheck = true` in `InterviewerSaveSlotDto`.
- Slot saving follows the same flow as regular slots but in bulk mode.

---

### 3.19 Alerts & Scheduled Notifications

**Purpose**: Automated email notifications for SLA breaches, interview reminders, and feedback reminders.

**Scheduled Jobs**

| Schedule | Job | Description |
|----------|-----|-------------|
| Daily 9:00 AM IST | `sendAgingSLAs` | Send aging SLA alerts to recruiter leads |
| Daily 9:00 AM IST | `sendTowerAgingSLAs` | Send tower-level aging SLA alerts |
| Every 15 minutes | `sendInterviewReminder` | Remind interviewers of upcoming interviews |
| Every 15 minutes | `sendInterviewStatus` | Update/alert on interview status changes |
| Daily 9:00 AM IST | `feedbackFormReminder` | Remind interviewers to submit pending feedback |
| Daily 10:00 AM (cron) | `sendfeedBackEmailRemainder` (Node.js) | Feedback submission reminder (Node.js) |
| Hourly (Mon–Sat) | `triggerEmailReminders` (Node.js) | General email reminder trigger |
| Daily 9 AM & 9 PM | `deleteExcelHistory` (Node.js) | Clean up old exported Excel files |

**Email Configuration**
- SMTP Host: `email-smtp.eu-west-1.amazonaws.com`
- SMTP Port: 25
- From address: `smartrecruit@capgemini.com`
- Signature: "Smart Recruit Team"
- Key distribution lists: `alltowers@capgemini.com`, `nalead@capgemini.com`, `recruiterlead@capgemini.com`, `allrecruiters@capgemini.com`, `sl-bulead@capgemini.com`

---

### 3.20 PDF & Document Management

**Purpose**: Generate, store, retrieve, and download various documents: feedback PDFs, resume files, email attachments, and Excel exports.

**User Stories**
- As a Recruiter, I want to download a candidate's resume from the system.
- As a Recruiter, I want to download the filled interview feedback form as a PDF.
- As a PMO, I want to export filtered candidate data to Excel.

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Download resume | GET `/excel/downloadResume?candidate_detail_id=` | Download resume from S3 |
| Download email attachment | GET `/excel/downloadEmail?candidate_detail_id=` | Download email from S3 |
| Download referral screenshot | GET `/excel/downlodeReferralScreenshot` | Download referral screenshot |
| Download interview video | POST `/excel/downloadInterviewVideo` | Download video from S3 |
| Upload interview video | POST `/upload/interviewVideoUpload` | Upload interview recording |
| Upload project file (L1) | POST `/projectUpload/l1FileUpload` | L1 project file upload |
| Generate report PDF | GET `/report/generatePdf` | PDF from feedback form data |
| Export PMO Excel | POST `/downloadExcel/exportExcelPMO` | PMO-specific Excel export |
| Fetch excel history | GET `/fetchAllExcelHistory` | List past Excel exports |
| Delete excel history | GET `/deleteExcelHistory` | Purge old export files |
| PDF dump | POST `/download/dump` | Bulk PDF download |
| Candidate feedback dump | POST `/downloadExcel/pdfDump` | Feedback PDF bulk export |

**Business Rules**
- All file operations use AWS S3 with `private` ACL (not public-read).
- File size limit: 5MB for most uploads; 10MB for Java-side multipart forms.
- Body size limit: 50MB JSON/form-data on the Node.js server.
- Excel export history is maintained and auto-cleaned twice daily.

---

### 3.21 Candidate Approval Data

**Purpose**: View and manage candidates who have received offers and are in the BU/NA approval stage.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Candidate Approval Data | `/candidate-approval-data` | Candidates pending offer approval |

**Actions**
- POST `/reports/getOfferApproveCandidate` — fetch candidates in offer approval stage

---

### 3.22 Panel Registration

**Purpose**: Allows Admins to register employees as interview panel members with their technology expertise.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Register Panel | `/register-panel` | Register/manage interviewers |

**Registration Data** (from `UserRegisterDTO`)
| Field | Type | Description |
|-------|------|-------------|
| empId | Long | Employee ID |
| empName | String | Full name |
| email | String | Corporate email |
| userpass | String | Password (for non-SSO) |
| location | String | Work location |
| grade | String | Job grade/level |
| technology | List\<String\> | Technology skills |
| roles | List\<String\> | System roles assigned |
| userTowerNames | List\<String\> | Tower assignments |
| account | String | Account |
| marketUnit | String | Market unit |
| organization | String | Organisation |
| bu | String | Business Unit |
| practice | String | Practice area |

**Actions**
| Action | API | Description |
|--------|-----|-------------|
| Register new user | POST `/register/registerNewUser` | Create new panel/employee |
| Update user details | POST `/register/updateUserDetails` | Edit existing user |
| Remove skill | POST `/register/removeSkill` | Remove a technology from user profile |
| Update assigned role | POST `/users/updateAssignedRole` | Assign/change user role |
| Get all users | POST `/users/getUsers` | Fetch all registered users |

**Keycloak Sync**
- On user registration/update, the Java service syncs with Keycloak to create/update the identity account.
- DELETE `/keycloak/deleteEmployee` — removes user from both DB and Keycloak.

---

### 3.23 Feedback Form Report

**Purpose**: Reporting module that aggregates submitted feedback forms by various filters for quality analysis.

**Screens / Pages**
| Screen | Route | Description |
|--------|-------|-------------|
| Feedback Form Report | `/feedbackform-report` | Report of feedback form submissions |

**Actions**
- POST `/report/feedbackFormReport` — fetch report data
- POST `/report/exportFeedbackExcel` — download as Excel
- Automated daily email via `sendfeedBackEmailRemainder` (Node.js cron)

---

## 4. Data Models

### Employee

| Field | Type | Notes |
|-------|------|-------|
| emp_id | Long (PK) | Auto-generated |
| emp_name | String | Full name |
| email_id | String | Corporate email (unique) |
| location | String | Work location |
| grade | String | Job grade |
| bu | String | Business Unit |
| practice | String | Practice area |
| market_unit | String | Market Unit |
| account | String | Account name |
| organisation | String | Organisation |

**Relations**: One-to-many with `EmployeeRoleDetailsEntity`, `EmployeeTechnologyDetailsEntity`, `EmployeeAccountDetails`

### Candidate Detail

| Field | Type | Notes |
|-------|------|-------|
| candidate_detail_id | Long (PK) | |
| candidate_name | String | |
| email_id | String | |
| contact_number | String | |
| gender | String | |
| total_exp | String | Years |
| rel_exp | String | Years |
| current_company | String | |
| current_location | String | |
| notice_period | String | |
| current_ctc | String | In Lakhs |
| exp_ctc | String | Expected CTC |
| source | String | Sourcing channel |
| referred_vendor | String | |
| college | String | |
| level_based_on_exp | String | |
| created_by | String | Email |
| created_date | Date | |
| is_referral | Boolean | |
| is_rehire | Boolean | |

**Relations**: Many-to-one with `TechnologyMasterEntity`; One-to-many with `CandidateInterviewEntity`, `CandidateStatusEntity`, `CandidateCommentsEntity`, `CandidateSkillEntity`

### Candidate Interview (Recruiter Calendar)

| Field | Type | Notes |
|-------|------|-------|
| recruiter_calendar_id | Long (PK) | |
| candidate_detail_id | Long (FK) | Links to CandidateDetail |
| interviewer_calendar_id | Long (FK) | Links to InterviewerCalendar |
| interview_type_id | Long (FK) | L1/L2/L3 |
| from_time | DateTime | Interview start |
| to_time | DateTime | Interview end |
| interview_date | Date | |
| is_direct_booked | Boolean | Booked without availability slot |
| meeting_link | String | Teams/virtual link |
| created_by | String | |
| feedback_submitted | Boolean | |

### Interviewer Calendar

| Field | Type | Notes |
|-------|------|-------|
| interviewer_calendar_id | Long (PK) | |
| emp_id | Long (FK) | Links to EmployeeMaster |
| from_time | DateTime | Available from |
| to_time | DateTime | Available to |
| slot_status | String | Available / Booked / Interviewed |
| is_weekend_drive | Boolean | |
| skill_id | Long (FK) | |
| created_date | Date | |

### Demand Data

| Field | Type | Notes |
|-------|------|-------|
| demand_id | Long (PK) | |
| jr_id | String | Job Request ID |
| skill | String | Required technology |
| grade | String | Required grade |
| account | String | Target account |
| bu | String | Business Unit |
| demand_status | String | Open / Closed |
| demand_date | Date | |
| sourced_count | Integer | |
| pipeline_count | Integer | |

### Referral Candidate

| Field | Type | Notes |
|-------|------|-------|
| referral_id | Long (PK) | |
| referee_emp_id | Long (FK) | Employee who referred |
| candidate_name | String | |
| candidate_email | String | |
| candidate_phone | String | |
| skills | List | From ReferralTechnologyMaster |
| certifications | List | From ReferralCertificationsMaster |
| notice_period | String | |
| location | String | |
| resume_s3_key | String | S3 object key |
| image_s3_key | String | S3 object key |
| submission_date | Date | |
| status | String | Pending / Selected / Rejected |

### Feedback Form Data

| Field | Type | Notes |
|-------|------|-------|
| feedback_id | Long (PK) | |
| recruiter_calendar_id | Long (FK) | |
| interviewer_calendar_id | Long (FK) | |
| technology | String | |
| technical_sections | JSON/List | Parameterised rating sections |
| overall_rating | String | Select / Hold / Reject |
| overall_remarks | String | |
| submitted_by | String | Email |
| submitted_date | DateTime | |
| pdf_s3_key | String | Generated PDF location in S3 |

### Lookup Master

| Field | Type | Notes |
|-------|------|-------|
| lookup_id | Long (PK) | |
| lookup_type | String | Category/screen ID |
| lookup_code | String | |
| lookup_value | String | Display label |
| is_active | Boolean | |

### Status Master

| Field | Type | Notes |
|-------|------|-------|
| status_id | Long (PK) | |
| status_name | String | e.g., "L1 Scheduled", "L2 Selected", "Offered" |
| dashboard_status | String | Rolled-up display status |
| is_active | Boolean | |

**Status Transition**: Governed by `StatusIntermediateMapping` table which defines valid `from_status → to_status` transitions.

---

## 5. API Contract

### Java Microservice (smarthiremicro) — Base URL: `/smartrecruitmicro/`

| Method | Endpoint | Purpose | Request Body | Response Shape |
|--------|----------|---------|--------------|----------------|
| POST | `/login/validateSession` | Validate/create Keycloak session | `{ userName }` | `ResponseDto` |
| POST | `/register/registerNewUser` | Register interviewer/employee | `UserRegisterDTO` | `ResponseDto { message }` |
| POST | `/register/updateUserDetails` | Update user details | `UserRegisterDTO` | `ResponseDto { message }` |
| POST | `/register/removeSkill` | Remove technology from user | `RemoveSkillDTO` | `ResponseDto { message }` |
| POST | `/users/getUsers` | Get all users | `{ email, role }` | `List<UserDataDTO>` |
| POST | `/users/updateAssignedRole` | Assign role to user | `{ empId, role }` | `ResponseDto` |
| POST | `/candidateData/saveCandidateData` | Save new candidate data | `CandidateDataDTO` | `ResponseDto` |
| POST | `/candidateData/getCandidateData` | Get candidate data | `CheckCandidateDTO` | `ResponseDto<CandidateDataDTO>` |
| POST | `/candidateData/saveSkillDL` | Save skill DL mapping | `JSONObject` | `ResponseDto` |
| POST | `/interviewer/getInterviewerSlots` | Get interviewer availability | `CheckAvailabilityDTO` | `ResponseDto<List<InterviewerCalenderDetailsDto>>` |
| POST | `/interviewer/getAllScheduleSlots` | Get all scheduled slots | `CheckScheduleDTO` | `ResponseDto<List<InterviewerCalenderDetailsDto>>` |
| POST | `/interviewer/saveFreeSlot` | Save interviewer free slot | `InterviewerSaveSlotDto` | `ResponseDto<InterviewerCalendarSavedSlotDTO>` |
| POST | `/interviewer/saveInterviewSlot` | Save direct interview slot | `SaveInterviewerSlotDto` | `ResponseDto<InterviewerCalendarSavedSlotDTO>` |
| POST | `/recruiter/getDirectRecruiterSlots` | Get recruiter direct bookings | `DirectBookedDTO` | `ResponseDto<List<RecruiterCalendarDetailsDto>>` |
| POST | `/recruiter/saveInterviewSlot` | Book interview for candidate | `SaveRecruiterSlotDto` | `ResponseDto<RecruiterCalendarDetailsDto>` |
| POST | `/recruiter/rescheduleSlot` | Reschedule existing slot | `SaveRecruiterSlotDto` | `ResponseDto` |
| POST | `/recruiter/deleteSlot` | Cancel a slot | `SaveRecruiterSlotDto` | `ResponseDto` |
| POST | `/recruiter/feedbackForm` | Generate blank feedback form | `InterviewTypeDTO` | `ResponseDto<FormDTO>` |
| GET | `/recruiter/feedbackFormPDf` | Fetch feedback PDF link | `?interviewTypeId&recruiterCalendarId` | `ResponseDto` |
| POST | `/feedbackForm/addFeedbackForm` | Add feedback form template | `NewFeedbackFormDTO` | `Map<String, Object>` |
| POST | `/feedbackForm/getFeedbackFormHeadings` | Get form headings | `{ technology, practice_id }` | `JSONObject` |
| GET | `/lookup/fetchDropdown` | Fetch dropdown data | `?screenId` | `ResponseDto<List<LookupDTO>>` |
| GET | `/lookup/fetchMarketUnit` | Fetch market units by BU | `?buId` | `List<MarketUnitDTO>` |
| GET | `/lookup/fetchPractices` | Fetch practices by BU | `?buId` | `List<MarketUnitDTO>` |
| POST | `/lookup/fetchAccountsByMu` | Fetch accounts by MU | `MuDTO` | `List<MarketUnitDTO>` |
| PUT | `/report/generateReport` | Generate Excel report | Query params | Binary Excel file |
| GET | `/report/generatePdf` | Generate feedback PDF | `?interviewTypeId&recruiterCalendarId&interviewerCalendarId` | String (S3 URL) |
| POST | `/slot/panelSlotUpload` | Upload panel slot Excel | Multipart file | `FileDTO` |
| GET | `/configuration/constants` | Get app config constants | — | `ResponseDto<Map>` |
| POST | `/keycloak/fetchAllKeycloakUsers` | List Keycloak users | `KeycloakTokenDTO` | String (JSON) |
| DELETE | `/keycloak/deleteEmployee` | Delete employee from Keycloak | `?employeeId` + `KeycloakTokenDTO` | Boolean |
| PUT | `/keycloak/updateEmployee` | Update employee in Keycloak | `KeycloakTokenDTO` | Boolean |
| GET | `/prescreen/updatePrescreenDetails` | Update prescreen record | `?prescreenId&recuiterEmailId&recuiterName` | void |
| GET | `/referralCandidate/getReferralFormHeaders` | Get referral form master data | — | `ReferralMasterDataDTO` |
| GET | `/getCode` | Get Teams OAuth code (redirect) | — | Redirect |
| POST | `/getMeetingLink` | Generate Teams meeting | `TeamsMeetingDTO1` | String (URL) |
| POST | `/sendMeetingInvite` | Send Teams meeting invite | `TeamsMeetingDTO1` | `ResponseDto` |
| GET/POST | `/alerts/sendAgingSLAs` | Trigger aging SLA emails | — | void |
| GET/POST | `/alerts/sendInterviewReminder` | Trigger interview reminders | — | void |

### Node.js Microservice (smarthiremicro 1) — Base URL: `/smartrecruitnodejs/`

| Method | Endpoint | Auth | Purpose |
|--------|----------|------|---------|
| POST | `/s3Upload/upload` | JWT | Upload files to S3 |
| POST | `/referralcandidates/upload` | JWT | Bulk referral upload |
| POST | `/referralcandidates/referralForm` | JWT | Submit referral form |
| POST | `/referralresume` | JWT | Upload referral resume |
| POST | `/downloadRefResume` | JWT | Download referral resume |
| POST | `/referralImage` | JWT | Upload referral profile image |
| POST | `/demandUpload/upload` | JWT | Bulk demand data import |
| POST | `/benchUpload/upload` | JWT | Bulk bench data import |
| POST | `/resumeUpload/upload` | JWT | Upload candidate resume |
| POST | `/emailUpload/upload` | JWT | Upload email attachment |
| POST | `/l2SelectUpload/upload` | JWT | Upload L2 select sheet |
| POST | `/projectUpload/l1FileUpload` | None | L1 project file |
| POST | `/upload/interviewVideoUpload` | None | Interview video upload |
| GET | `/demandHistory/getHistory` | JWT | Demand history |
| GET | `/benchHistory/getHistory` | JWT | Bench history |
| POST | `/download/dump` | JWT | PDF dump export |
| POST | `/downloadExcel/pdfDump` | JWT | Candidate feedback dump |
| GET | `/downloadExcel/agingCalc` | JWT | Aging calculation |
| POST | `/downloadExcel/exportExcelPMO` | JWT | PMO Excel export |
| POST | `/downloadExcel/exportExcelL2AgingReport` | JWT | L2 aging Excel export |
| POST | `/downloadExcel/exportExcelDOJReport` | JWT | DOJ report Excel export |
| GET | `/fetchAllExcelHistory` | JWT | List Excel exports |
| GET | `/deleteExcelHistory` | JWT | Delete Excel history |
| GET | `/excel/downloadResume` | None | Download resume |
| GET | `/excel/downloadEmail` | JWT | Download email |
| POST | `/excel/fetchAllTechnology` | JWT | Fetch all technologies |
| GET | `/excel/fetchAllSources` | JWT | Fetch all sources |
| POST | `/excel/dateOfJoining` | JWT | Update DOJ |
| POST | `/excel/statusChange` | JWT | Update candidate status |
| POST | `/excel/statusDropdown` | JWT | Status dropdown options |
| GET | `/excel/declineReasonDropdown` | JWT | Decline reason options |
| POST | `/excel/updateDeclineReason` | JWT | Set decline reason |
| POST | `/excel/rejectionReason` | JWT | Get rejection reasons |
| POST | `/excel/fetchFilteredCandidatesDataByQuery` | JWT | Filtered candidate list |
| POST | `/excel/downloadFile` | JWT | Download project file |
| POST | `/excel/downloadInterviewVideo` | JWT | Download interview video |
| POST | `/report/rejectSelectRatio` | JWT | Reject/select ratio |
| POST | `/report/l2selectRatioForSource` | JWT | L2 ratio by source |
| POST | `/report/fetchInterviewScheduledCountDay` | JWT | Day-wise interview count |
| POST | `/report/feedbackFormReport` | JWT | Feedback form report |
| POST | `/report/exportFeedbackExcel` | JWT | Export feedback Excel |
| POST | `/candidateInfo/fetchCandidateInfo` | JWT | Fetch candidate info |
| POST | `/candidateInfo/updateCandidateInfo` | JWT | Update candidate info |
| GET | `/candidateInfo/regions` | JWT | Region list |
| POST | `/candidateInfo/addComments` | JWT | Add candidate comments |
| POST | `/candidateInfo/fetchCandidateComments` | JWT | Fetch candidate comments |
| POST | `/candidateInfo/updateSkill` | JWT | Update candidate skill |
| POST | `/candidateInfo/fetchSources` | JWT | Source list |
| POST | `/candidateInfo/fetchVendorsBySource` | JWT | Vendors by source |
| POST | `/candidateInfo/fetchClientReqId` | JWT | Client request ID lookup |
| POST | `/candidateInfo/fetchCandidateCycle` | JWT | Candidate lifecycle |
| POST | `/lineChart/fetchInterviewtakenCountByMonth` | JWT | Monthly interview count |
| POST | `/lineChart/fetchInterviewtakenCountByYear` | JWT | Yearly interview count |
| GET | `/lineChart/fetchAllYears` | JWT | Year options |
| GET | `/lineChart/fetchAllMonths` | JWT | Month options |
| POST | `/admin/fetchAllTowers` | JWT | Tower list |
| POST | `/admin/fetchSkillBasedOnSkillGrpTower` | JWT | Skills by group/tower |
| POST | `/admin/fetchAllSkillPractice` | JWT | Practice list |
| POST | `/admin/fetchAllSkill` | JWT | All skills |
| POST | `/admin/fetchAllSkillGroup` | JWT | Skill groups |
| GET | `/admin/fetchAllmarketUnit` | JWT | Market units |
| GET | `/admin/fetchAllEmpName` | JWT | Employee emails |
| GET | `/admin/fetchAllVendors` | JWT | All vendors |
| POST | `/admin/addSkillWithMapping` | JWT | Add skill |
| POST | `/admin/addTower` | JWT | Add tower |
| POST | `/admin/addSkillGroup` | JWT | Add skill group |
| POST | `/admin/addSource` | JWT | Add source |
| POST | `/admin/addVendorWithMapping` | JWT | Add vendor |
| POST | `/admin/addRoleComment` | JWT | Add role comment |
| POST | `/admin/deleteSkillWithMapping` | JWT | Delete skill |
| POST | `/admin/deleteVendorWithMapping` | JWT | Delete vendor |
| GET | `/admin/fetchBuAccountMaster` | JWT | BU accounts |
| POST | `/admin/addBUAccount` | JWT | Add BU account |
| GET | `/admin/fetchTypeMaster` | JWT | Type master data |
| POST | `/admin/addTypeMaster` | JWT | Add type |
| POST | `/admin/fetchSkillByTemplate` | JWT | Skills by template |
| POST | `/supplyScreen/getSupplyInfo` | JWT | Supply data |
| POST | `/reports/filterOuterPieChart` | JWT | Outer pie chart |
| POST | `/reports/filterInnerPieChart` | JWT | Inner pie chart |
| POST | `/reports/filterReferralOuterPieChart` | JWT | Referral outer pie |
| POST | `/reports/filterReferralInnerPieChart` | JWT | Referral inner pie |
| POST | `/reports/fetchSkillsByTowers` | JWT | Skills by tower (filter) |
| POST | `/reports/fetchVendorsBySources` | JWT | Vendors by source (filter) |
| GET | `/reports/getStartEndDate` | JWT | Date range for reports |
| GET | `/reports/initialOuterPieChart` | JWT | Initial pie chart |
| POST | `/reports/getOfferApproveCandidate` | JWT | Offer approval candidates |
| POST | `/sap_capability/fetchAllSapCapability` | JWT | SAP capabilities |
| POST | `/sap_capability/fetchAllSapSkill` | JWT | SAP skills |
| POST | `/sap_capability/fetchSkillsByCapability` | JWT | SAP skills by capability |
| GET | `/supplyVSdemandVSbench/fetchAllHybridLocation` | JWT | Hybrid locations |
| GET | `/supplyVSdemandVSbench/fetchAllPrimaryLocation` | JWT | Primary locations |
| GET | `/supplyVSdemandVSbench/fetchBenchStatus` | JWT | Bench status options |
| GET | `/supplyVSdemandVSbench/fetchGradeStatus` | JWT | Grade options |
| POST | `/demandScreen/getDemandInfo` | JWT | Demand data |
| POST | `/benchScreen/getBenchInfo` | JWT | Bench data |
| POST | `/panel/employeeInfo` | JWT | Employee panel info |
| POST | `/panel/getInterviewData` | JWT | Interview data for panel |
| POST | `/panel/fetchAccountLeadMail` | JWT | Account lead email |
| POST | `/todoController/fetchAllCandidates` | JWT | Todo: all candidates |
| POST | `/todoController/todoStatusDropdown` | JWT | Status dropdown |
| POST | `/todoController/updateStatus` | JWT | Update status |
| POST | `/todoController/fetchPendingFeedbacks` | JWT | Pending feedbacks |
| POST | `/todoController/fetchSlotsByWeek` | JWT | Weekly slots |
| POST | `/todoController/interviewscheduledtoday` | JWT | Today's interviews |
| POST | `/l2_dashboard_reports/reports` | JWT | L2 report data |
| POST | `/l2_dashboard_reports/getL2StatusInfoExcel` | JWT | L2 report Excel |
| POST | `/l2_dashboards_reports/getDOJStatusInfo` | JWT | DOJ status info |
| POST | `/l2_dashboard_reports/agingReport` | JWT | L2 aging report |
| POST | `/arc_deviation_reports/getArcDeviationInfo` | JWT | ARC deviation data |
| POST | `/arc_deviation_reports/exportExcelArcDeviationReport` | JWT | ARC Excel export |
| POST | `/sourceVendorInfoScreen/getSourceInfo` | JWT | Source channel info |
| POST | `/supplyScreen/getSourceVendorTrendInfo` | JWT | Trend chart data |
| POST | `/supplyScreen/getTrendChartExcelData` | JWT | Trend chart Excel |
| POST | `/statusInsight/exportStatusInsight` | JWT | Status insight export |
| POST | `/statusInsight/updateStatusInReports` | JWT | Update status in reports |
| POST | `/rejectionReasonReport/rejectionReport` | JWT | Rejection report |
| POST | `/rejectionReasonExcelReport/rejectionExcelReport` | JWT | Rejection Excel |
| POST | `/panel/fetchEmpRoles` | JWT | Employee roles |
| POST | `/panel/getEmpName` | JWT | Employee name |
| POST | `/panel/checkEmployee` | JWT | Check if employee exists |
| GET | `/panel/fetchBU` | JWT | BU list |
| POST | `/workflow/fetchFlowCandidates` | JWT | Workflow candidates |
| POST | `/workflow/updateFlowCandidates` | JWT | Update workflow |
| POST | `/workflow/commentsHistory` | JWT | Comments history |
| POST | `/workflow/commentDropdown` | JWT | Comment options |
| POST | `/workflow/addComments` | JWT | Add comment |
| POST | `/workflow/fetchJBCandidates` | JWT | JB candidates |
| POST | `/workflow/fetchJBBonus` | JWT | JB bonus details |
| POST | `/workflow/fetchAllStatuses` | JWT | All statuses |
| POST | `/workflow/updateJBCandidates` | JWT | Update JB candidate |
| POST | `/workflow/fetchJBCandidatesForBU` | JWT | JB candidates for BU |
| POST | `/workflow/updateJBCandidatesForBU` | JWT | Update JB for BU |
| POST | `/workflow/ctcHistory` | JWT | CTC history |
| POST | `/workflow/rejectionReasonDropdown` | JWT | Rejection reasons |
| POST | `/workflow/jbDLDropdown` | JWT | JB distribution list |
| POST | `/workflow/thresholdApi` | JWT | Threshold values |
| POST | `/workflow/sourceByVendor` | JWT | Source by vendor |
| POST | `/workflow/getCode` | JWT | Project/JR code |
| GET | `/workflow/getAverageOfferedCTC` | JWT | Average offered CTC |
| GET | `/workflow/getApproverDLDetails` | JWT | Approver DL |
| POST | `/workflow/updateApproverDLDetails` | JWT | Update approver DL |
| GET | `/workflow/fetchDLTitle` | JWT | DL title options |
| GET | `/workflow/fetchNewTowerForLead` | JWT | New tower for lead |
| GET | `/workflow/getPossibleStatus` | JWT | Next status options |
| POST | `/token/generateToken` | None | Generate JWT token |
| POST | `/referralAdmin/fetchReferralEmpRoles` | JWT | Referral employee roles |
| POST | `/referralAdmin/getReferralEmpName` | JWT | Referral employee name |
| POST | `/referralAdmin/checkReferralEmployee` | JWT | Check referral employee |

---

## 6. Shared Components & Services

### Angular Services (SmartHireUI)

| Service | Purpose | Key Methods |
|---------|---------|-------------|
| `DataService` | Core HTTP service; manages all Java backend calls; shared state (email, role, slots, calendar events) | Calendar event management, interview slot data sharing |
| `AuthService` | Authentication: SSO token exchange, role fetching, JWT decoding | `getTokenId()`, `getRoles()`, `getEmpName()`, `getEmpBU()`, `canActivateRoute()`, `outlookCode()` |
| `DatashareService` | Cross-component data sharing via RxJS Subjects | Event emitters for role/filter changes |
| `AdministrationService` | All admin module HTTP calls (master data CRUD) | Tower/Skill/Vendor CRUD |
| `ReportsService` | All report-related HTTP calls | Pie charts, line charts, Excel exports |
| `UploadPopupService` | File upload management | S3 upload, candidate data import |
| `WorkflowService` | Workflow module HTTP calls | Offer approval, JB management |
| `TodoService` | To-do list HTTP calls | Fetch candidates, update status |
| `UpdatedetailsService` | Update candidate details calls | |
| `PanelInsightsService` | Panel insights HTTP calls | |
| `LoaderMobileService` | Global loading spinner state | Show/hide spinner |
| `ToastrMobileService` | Global notification toasts | Success/error notifications |

### HTTP Interceptor

`httpSetHeaders.interceptor.ts` — Adds the JWT token from `localStorage` to every outbound HTTP request as an `Authorization: Bearer <token>` header.

### Shared UI Library Components

Located in `SmartHireUI/src/app/Shared/`:
- **URL Constants** (`app.constant.ts`): Centralised API endpoint string definitions
- **Data Modals** (`dataModal/bookingSlot.modal.ts`): `BookingEvent`, `LookupEvent` TypeScript interfaces for calendar events

### Reusable Java Library (smarthireReusable)

- **`Properties.java`**: Loads environment-specific properties from `application.properties`
- **`Utils.java`**: Shared utility methods (date formatting, string manipulation)
- **Entity package** (`transaction/entity/`): All JPA entity classes shared across Java services (~80+ entities covering all DB tables)

---

## 7. Navigation & Routing Map

### Full Route Tree

```
/ (root)
├── home                          [PUBLIC]
├── select                        [PUBLIC]
├── selectrole                    [PUBLIC] — Role selection after login
├── register                      [PUBLIC] — Employee self-registration
├── error                         [PUBLIC]
├── logout                        [PUBLIC]
│
├── dashboard                     [AuthGuard] — Interviewer dashboard
├── upload                        [AuthGuard] — File upload popup
├── webFeedback                   [AuthGuard]
├── select-reject                 [AuthGuard] — L1 select/reject
├── booking-view                  [AuthGuard]
│   ├── available                 [AuthGuard]
│   ├── booked                    [AuthGuard]
│   ├── interviewed               [AuthGuard]
│   └── panel-availability        [AuthGuard]
├── booking-form                  [AuthGuard]
├── feedback                      [AuthGuard]
├── line-chart                    [AuthGuard]
├── dashboard-reports             [AuthGuard]
├── candidate-details             [AuthGuard]
├── changeroles                   [AuthGuard]
├── demand-supply                 [AuthGuard]
├── administration                [AuthGuard]
├── panel-insights                [AuthGuard]
├── todolist                      [AuthGuard]
├── weekend-drive                 [AuthGuard]
├── import-weekend-drive          [AuthGuard]
├── channel-insights              [AuthGuard]
├── rejection-report              [AuthGuard]
├── status-insights               [AuthGuard]
├── l2-report                     [AuthGuard]
├── interview-data                [AuthGuard]
├── dateofjoining                 [AuthGuard]
├── l2-aging                      [AuthGuard]
├── trend-chart                   [AuthGuard]
├── master-data                   [AuthGuard]
├── candidate-approval-data       [AuthGuard]
├── update-skill                  [AuthGuard]
├── work-flow                     [AuthGuard]
├── work-flow-info                [AuthGuard]
├── joiningbonus                  [AuthGuard]
├── jbcandidates                  [AuthGuard]
├── register-panel                [AuthGuard]
├── feedbackform-report           [AuthGuard]
├── arc-deviation                 [AuthGuard]
├── candidate-referral            [AuthGuard]
├── candidate-referral-details    [AuthGuard]
├── referral-select-reject        [AuthGuard]
├── referralUserRegister          [AuthGuard]
│
├── referral-portal/
│   ├── referralRegister          [PUBLIC]
│   ├── error                     [PUBLIC]
│   ├── upload                    [PUBLIC]
│   ├── logout                    [PUBLIC]
│   └── ref-candidate-details     [ReferralAuthGuard]
│
├── referral-form                 [PUBLIC]
├── ref-reports-bybu              [PUBLIC]
└── ref-reports-byaccount         [PUBLIC]
```

### Role-Based Initial Routing

| Role | Default Landing Route |
|------|-----------------------|
| Interviewer | `/dashboard` |
| Recruiter (non-SAP BU) | `/todolist` |
| Recruiter (SAP BU) | `/upload` |
| PMO (non-SAP BU) | `/todolist` |
| PMO (SAP BU) | `/upload` |
| Practice Lead | `/todolist` |
| Lead | `/upload` |
| Tower Lead / SL-BU Lead / NA Lead / Recruiter Lead | `/work-flow` |
| BU Admin / Practice Admin | `/master-data` |
| Admin/SuperUser | `/candidate-referral` |
| Referral SPOC | `/candidate-referral` |

---

## 8. Configuration & Environment

### Frontend Environment Variables

| Variable | Dev Value | Prod Value | Description |
|----------|-----------|------------|-------------|
| `production` | false | true | Build mode flag |
| `enableSso` | false | true | Enable Keycloak SSO |
| `BASE_URL` | `http://localhost:7001/` | `https://www.smartrecruit-portal.com/` | Root URL |
| `MICRO_URL` | `` (empty) | `smartrecruitmicro/` | Java service sub-path |
| `NODE_URL` | `` (empty) | `smartrecruitnodejs/` | Node.js service sub-path |
| `PYTHON_URL` | `smarthirepythonmicro/` | `smartrecruitpythonmicro/` | Python service sub-path |
| `KEY_CLOCK_URL` | `https://52.214.113.246:8000/auth` | `https://www.smartrecruit-portal.com/auth` | Keycloak auth URL |
| `keycloak.realm` | `SmartHire` | `Smartrecruit` | Keycloak realm name |
| `keycloak.clientId` | `Smarthireui` | `Smartrecruit_id` | Keycloak client ID |

### Download Template URLs (S3)

| Template | S3 Key |
|----------|--------|
| Candidate Sheet | `template/Candidate_Sheet_Template.xlsx` |
| Candidate Sheet (Invent) | `template/Candidate_Sheet_Template_Invent.xlsx` |
| Panel Slot Template | `template/panel_slot_template.xlsx` |
| Demand Template | `template/demand_template.xlsx` |
| Bench Template | `template/bench_Template.xlsx` |
| L2 Sheet Template | `template/L2_sheet_template.xlsx` |
| Instant Interview | `template/Instant_Interview_template.xlsx` |
| Instant Interview (GCCA) | `template/Instant_Interview_GCCA_template.xlsx` |
| Referral Sheet | `template/Referral_sheet_template.xlsx` |
| PDF Dump Template | `template/Pdf_dump_template.xlsx` |
| Interviewer Manual | `template/SmartRecruitInterviewerManual.pdf` |
| Admin SPOC Guide | `template/GuideForAdminSpoc.docx` |
| End User Guide | `template/GuideForEndUser.docx` |

### Java Backend Configuration

| Property | Value |
|----------|-------|
| Server Port | 8083 |
| Database | PostgreSQL (AWS RDS eu-west-1) |
| DB Host | `smarthire.caxuaavs6epi.eu-west-1.rds.amazonaws.com:5432` |
| DB Name | `smartrecruit` |
| DB Schema | `sr_prod` |
| JPA Dialect | PostgreSQL |
| Max File Upload | 10MB |
| Active Profile | `prod` |

### Node.js Backend Configuration

| Property | Value |
|----------|-------|
| Port | 7001 (or `VCAP_APP_PORT` env var) |
| Database | PostgreSQL (same AWS RDS) |
| ORM | Sequelize |
| JWT Secret | `2018-Smart%2Recruit%2@1234#` |
| S3 Bucket | `smarthireprod` |
| S3 ACL | `private` |
| SMTP Host | `email-smtp.eu-west-1.amazonaws.com:25` |
| From Email | `smartrecruit@capgemini.com` |
| Body Size Limit | 50MB |
| Default Environment | `production` |

### External Service Dependencies

| Service | Purpose | Integration Point |
|---------|---------|-------------------|
| **Keycloak** | Identity and access management | Frontend + Java backend |
| **Capgemini SSO** | Corporate identity provider | `https://signin.capgemini.com/as/token.oauth2` |
| **AWS S3** | File and document storage | Node.js middleware (`aws-sdk`) |
| **AWS SES** | Transactional email delivery | Node.js email service |
| **AWS RDS (PostgreSQL)** | Primary database | Both Java and Node.js |
| **Microsoft Graph API** | Teams meeting creation | Java `TeamsMeetingService` |
| **Microsoft Azure AD** | OAuth for Teams | Tenant `76a2ae5a-9f00-4f6b-95ed-5d33d77c4d61`, Client `b0b61d51-4fc7-4e70-9ec4-33819aed7a53` |

---

## 9. Non-Functional Requirements

### Performance Patterns Observed
- **Lazy Loading**: Angular router uses `loadChildren` for all modules — no module is bundled eagerly except the bootstrap shell.
- **Pre-loading Strategy**: `PreloadAllModules` is set in the router, so all lazy modules are pre-fetched after initial load.
- **Compression**: Node.js uses `compression` middleware on selected report routes (e.g., `fetchFilteredCandidatesDataByQuery`) for response gzip.
- **Pagination**: Candidate list queries use filter-based querying (`fetchFilteredCandidatesDataByQuery`) rather than full table loads.
- **Caching Headers**: Node.js sets `Cache-Control: public, max-age=0, no-cache, no-store, must-revalidate` — effectively disabling client-side caching to ensure fresh data.
- **Body Size Limits**: Node.js limits JSON and form body to 50MB; Java limits multipart to 10MB — preventing unbounded memory consumption.
- **Async Cron Jobs**: Background jobs (email reminders, Excel cleanup) run outside the request lifecycle via `node-cron`.

### Security Patterns Observed
- **JWT Authentication**: All protected Node.js routes require `Authorization: Bearer <token>` header; token verified with HMAC secret.
- **HTTP Interceptor**: Angular automatically injects the token into every outgoing HTTP request.
- **CORS Whitelisting**: Node.js CORS allows only explicitly listed origins (`smartrecruit-portal.com`, `localhost:4200/4201`).
- **Role-Based Middleware**: `validateRecruiterAuthorization` checks DB-level role before allowing candidate data access.
- **Private S3 ACL**: All uploaded files stored with `private` ACL — not publicly accessible without signed URLs.
- **Keycloak Integration**: Production uses enterprise SSO, eliminating local password management for employees.
- **⚠ Security Note for Re-implementation**: The development `config.json` contains hardcoded AWS IAM keys and SMTP credentials. In a fresh implementation, all secrets must be injected via environment variables or a secrets manager (e.g., AWS Secrets Manager). The JWT secret is also hardcoded — replace with a secure, randomly-generated environment variable.

### Accessibility
- Ionic Angular framework provides baseline accessible markup.
- No explicit ARIA roles or custom accessibility configurations observed beyond framework defaults.
- PWA manifest (`manifest.json`, `ngsw-config.json`) is present — application is installable as a Progressive Web App.

### PWA / Offline Capabilities
- Angular service worker configuration (`ngsw-config.json`) is present.
- Application is installable as a PWA (`manifest.json`).
- Offline capability depends on service worker caching strategy (configuration not fully inspected).
- Mobile support via Ionic 4 hybrid framework — Android/iOS packaging possible via `config.xml` (Cordova).

### Error Handling Patterns
- Java services use `ResponseDto` wrapper with `message`, `response`, and `exception` fields.
- Exception field is populated on server errors; frontend checks this field before processing response data.
- Node.js controllers return `{ error: true, Message: <error> }` objects on failure.
- HTTP status codes: 401 (auth failed), 403 (not authorised), 500 (server error) returned from Node.js middleware.
- Excel upload errors are returned as downloadable error Excel files (`ErrorExcelDTO`) so users can identify and correct bad rows.
- Scheduler/alert failures are logged server-side; no user-facing error handling for background jobs.

### Containerisation
- Both `smarthiremicro` and `smarthiremicro 1` have `Dockerfile`s — containerised deployment ready.
- `SmartHireUI` has a `Dockerfile` for containerised static serving.
- `manifest.yml` present in `smarthiremicro 1` — original deployment target was IBM Cloud Foundry.

---

## Appendix: Ambiguities & Recommended Review Points

| Item | Observation | Recommended Action |
|------|-------------|-------------------|
| **Python Microservice** | `PYTHON_URL: 'smartrecruitpythonmicro/'` is referenced in environment config but no Python project exists in this workspace | Locate the Python service repo and document its endpoints |
| **Login Page** | `login.page.ts` is entirely commented out — login is handled via SSO redirect; no local login UI | Confirm no fallback local auth is needed |
| **`smarthiremicro` Security** | `LoginController.java` uses a trust-all SSL manager that accepts any certificate — security risk in production | Replace with proper certificate validation in fresh implementation |
| **Hardcoded Secrets** | `config.json` contains IAM keys, SMTP credentials, JWT secret | Migrate all secrets to environment variables or a secrets vault |
| **Duplicate Node/Java Routes** | Some functionality (e.g., admin data) appears to be split between the Java and Node.js backends — exact boundary is not always clear | Define a clear service boundary: Java for scheduling/feedback/Keycloak; Node.js for data processing/uploads/reports |
| **`select` and `select-page` routes** | `/select` route exists but purpose unclear from available code | Inspect `SelectPageModule` for full spec |
| **`ref-reports-bybu` and `ref-reports-byaccount`** | These routes have no `canActivate` guard — verify if public access is intentional | Audit and add auth guard if needed |
| **`smarthireReusable` scope** | The reusable library is only imported by `smarthiremicro` — `smarthiremicro 1` uses Sequelize models instead | In fresh implementation, choose one ORM/DB strategy |
| **`changeroles` module** | Route exists but feature purpose not documented | Inspect `ChangerolesModule` source |
| **Keycloak realm mismatch** | Dev uses realm `SmartHire`, prod uses `Smartrecruit` — ensure consistent naming in fresh setup | Standardise realm name across environments |

---

## Recommended Next Steps for Fresh Development

1. **Normalise the architecture**: Replace the dual Java+Node.js backend with a single consistent backend (choose one stack or define a clear domain split with documented API gateway rules).
2. **Secrets management**: Implement environment variable injection for all credentials before any other work.
3. **Auth first**: Implement Keycloak realm, client, and role mappings before any feature work — all routes depend on it.
4. **Data model**: Start with the PostgreSQL schema using the 80+ entities documented in §4 as the source of truth.
5. **Core flow**: Implement in order — Employee Registration → Role Assignment → Interviewer Slot Management → Candidate Upload → Interview Booking → Feedback Submission.
6. **Reports last**: Analytics and reporting modules depend on all data being correctly populated — implement them after the core pipeline is stable.
7. **Referral portal**: Can be developed in parallel as a semi-independent module sharing only the Employee and Master Data tables.
