# Smart Recruit Platform - Complete Demo Guide & Setup

**Platform**: End-to-End Recruitment Lifecycle Management System  
**Stack**: React 18 (Frontend) + FastAPI (Backend) + PostgreSQL (Database)  
**Version**: 1.0 Phase 1  
**Last Updated**: May 27, 2026

---

## 📋 Quick Navigation

- [Application Overview](#application-overview)
- [System Architecture](#system-architecture)
- [Setup & Running](#setup--running)
- [Test Users & Credentials](#test-users--credentials)
- [Demo Flows by Role](#demo-flows-by-role)
- [Key Features & Workflows](#key-features--workflows)
- [API Endpoints Reference](#api-endpoints-reference)
- [Troubleshooting](#troubleshooting)

---

## 🎯 Application Overview

**Smart Recruit Platform** is a comprehensive recruitment management solution built for Capgemini to digitize the complete hiring pipeline:

### Core Capabilities
- **Candidate Sourcing & Upload** - Bulk import of candidates via Excel
- **Interview Scheduling** - Manage interviewer slots and booking
- **Multi-Round Feedback** - Collect feedback from multiple interviewers
- **Offer Management** - Multi-level approval workflow
- **Employee Referral Portal** - Internal employee referral program
- **Supply/Demand Visibility** - Track talent pipeline and bench
- **Recruitment Analytics** - Real-time insights and reports
- **Role-Based Access** - 14 different user roles with granular permissions

### User Roles
1. **Admin** - System administration, employee management, master data
2. **Recruiter** - Candidate management, booking, uploading
3. **Interviewer** - Schedule slots, provide feedback
4. **Tower Lead** - Tower-level approvals and workflow
5. **SL BU Lead** - Business unit lead approvals
6. **NA Lead** - Regional lead approvals
7. **Recruiter Lead** - Lead recruiter with team oversight
8. **PMO** - Project/program management oversight
9. **BU Admin** - Business unit administration
10. **Practice Admin** - Practice-level administration
11. **Referral User** - Employee referral participant
12. **Referral SPOC** - Referral program coordinator
13. **Practice Lead** - Practice management
14. **L2** - Level 2 approval authority

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Smart Recruit Platform                    │
├──────────────────────┬──────────────────────────────────────┤
│                      │                                        │
│   FRONTEND (Port 8016)│     BACKEND (Port 8015)              │
│   ───────────────────│     ──────────────────                │
│  • React 18          │     • FastAPI                         │
│  • TypeScript 5      │     • SQLAlchemy ORM                  │
│  • Vite Dev Server   │     • Alembic Migrations             │
│  • Material UI v5    │     • Python 3.11+                   │
│  • React Router v6   │     • JWT Authentication             │
│  • Axios HTTP Client │     • CORS Enabled                   │
│  • FullCalendar      │     • APScheduler (Jobs)             │
│  • React Hook Form   │     • Pandas (Excel)                 │
│                      │     • ReportLab (PDF)                │
│                      │                                        │
│                      └──────────────────────────────────────┤
│                                                              │
│                   DATABASE (PostgreSQL)                      │
│                   ─────────────────────                      │
│                  • Database: smarthiremain001               │
│                  • Tables: 15+                              │
│                  • Migrations: 12+                          │
└──────────────────────────────────────────────────────────────┘
```

### Technology Stack Details

**Backend Dependencies:**
```
FastAPI 0.104+
SQLAlchemy 2.x
Alembic 1.12+
python-jose[cryptography]
passlib[bcrypt]
python-multipart
email-validator
pandas 2.x
openpyxl 3.x
reportlab 4.x
apscheduler 3.x
python-dotenv
```

**Frontend Dependencies:**
```
React 18.2+
TypeScript 5+
Vite 5+
React Router v6
Axios 1.x
Material-UI (@mui) v5
@fullcalendar/react 6.x
react-hook-form 7.x
date-fns 2.x
```

---

## 🚀 Setup & Running

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 14+
- Git

### 1. Clone & Navigate to Project

```bash
cd c:\JD\mswe\sm1
```

### 2. Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment (if not exists)
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Set up database (migrations already created)
# Database: smarthiremain001 must exist in PostgreSQL
# Run migrations (optional - already seeded):
alembic upgrade head

# Check .env or environment variables
# Required vars: DB_PASSWORD (PostgreSQL password)
```

### 3. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Build if needed (for production)
npm run build
```

### 4. Start Services

**Terminal 1 - Backend:**
```bash
cd backend
# On Windows:
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8015 --reload
# On macOS/Linux:
source .venv/bin/activate
python -m uvicorn app.main:app --host 0.0.0.0 --port 8015 --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev -- --port 8016 --host
```

### 5. Access Application

- **Frontend**: http://localhost:8016
- **Backend API**: http://localhost:8015/api/v1/
- **API Docs**: http://localhost:8015/docs
- **ReDoc**: http://localhost:8015/redoc

### ✅ Verify Setup

All services running:
```bash
# Test backend
curl http://localhost:8015/docs

# Test frontend
curl http://localhost:8016

# Test login endpoint
curl -X POST http://localhost:8015/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@smartrecruit.dev","password":"Admin@123"}'
```

---

## 👥 Test Users & Credentials

### Pre-Created Users in Database

| # | Email | Password | Role | Full Name | BU | Grade | Location | Use Case |
|---|-------|----------|------|-----------|----|----|----------|----------|
| 1 | `admin@smartrecruit.dev` | `Admin@123` | Admin | System Admin | HQ | C3 | Mumbai | Platform admin, employee mgmt, master data |
| 2 | `john.interviewer@capgemini.com` | `John@123456` | Interviewer | John Interviewer | DCX | C2 | Mumbai | Schedule slots, provide feedback, calendar |
| 3 | `priya.recruiter@capgemini.com` | `Priya@123456` | Recruiter | Priya Recruiter | DCX | C1 | Bangalore | Upload candidates, manage recruitment, booking |

### How to Create Additional Test Users

To create more users in demo, use Admin Panel:

1. **Login as Admin**: `admin@smartrecruit.dev` / `Admin@123`
2. **Select Role**: Click "Admin"
3. **Go to**: Panel Registration (redirects automatically)
4. **Fill Form**:
   - Full Name
   - Email (new)
   - Password
   - BU (e.g., DCX, Infra, Cloud)
   - Grade (e.g., C1, C2, C3)
   - Location (e.g., Mumbai, Bangalore, Pune)
   - **Role** (dropdown): Select role
   - **Technologies** (dropdown): Select tech skill
5. **Click**: "Register Employee"
6. **Success**: Message shows "Employee registered successfully"

New user can now login with their email and password.

---

## 🎬 Demo Flows by Role

### DEMO FLOW 1: ADMIN - Complete Platform Overview (10-15 min)

**Login Credentials:**
```
Email: admin@smartrecruit.dev
Password: Admin@123
```

#### Step 1: Login
1. Navigate to http://localhost:8016
2. Enter email: `admin@smartrecruit.dev`
3. Enter password: `Admin@123`
4. Click "Sign In"
5. ✅ **Result**: Redirected to role selection page

#### Step 2: Select Admin Role
1. You should see "Welcome, System Admin"
2. Select Role: Click on "Admin" button
3. ✅ **Result**: Redirected to `/register-panel`

#### Step 3: Employee Registration (Panel Registration)
1. **Current Page**: Panel Registration
2. **Demo**: Create a test employee
3. **Fill Form**:
   - Full Name: `Demo Interviewer` or similar
   - Email: `demo.int@smartrecruit.dev`
   - Password: `Demo@123456`
   - BU: `DCX`
   - Grade: `C2`
   - Location: `Mumbai`
   - **Role dropdown**: Select "Interviewer"
   - **Technologies dropdown**: Select "Java"
4. Click "Register Employee"
5. ✅ **Result**: See success notification "Employee registered successfully"

**Key Points to Highlight:**
- Form validation in real-time
- Dropdown menus with all available roles
- Password strength requirements
- Success notification with instant feedback

#### Step 4: Navigate to Administration
1. Look for navigation options in the header
2. Go to Administration page (`/administration`)
3. **See**:
   - Tower Management section
   - Buttons for: Towers, Skills, Sources, Vendors, Approver DL, Role Comments
   - Master data configuration
4. Click on "Towers" button to see tower management
5. ✅ **Result**: Modal or page showing tower list and CRUD options

**Admin Features Visible:**
- Tower management
- Skill master data
- Source management
- Vendor management
- Approver distribution list
- Role comment configuration

#### Step 5: Master Data Management
1. Navigate to Master Data (`/master-data`)
2. **See Tabs**: Towers, Skills, Sources
3. Click each tab to view/manage master data
4. ✅ **Result**: Tables showing master data entries
5. **Optional**: Add new tower/skill/source

**Key Features:**
- Tab-based organization
- Data grid with sorting/filtering
- Add/Edit/Delete operations

#### Step 6: Candidate Management
1. Go to Candidate List (`/candidate-details`)
2. **See**: 
   - List of candidates
   - Columns: Name, Email, Status, Applied Date, etc.
   - Filter/Sort options
3. Click on a candidate row to view details
4. ✅ **Result**: Candidate detail page with full profile

#### Step 7: Candidate Upload
1. Go to Upload Page (`/upload`)
2. **See**: 
   - File upload dropzone
   - Instructions for Excel format
   - Sample template link (if available)
3. **Show**: File input ready for demo file
4. ✅ **Feature**: Could upload sample candidates Excel file

#### Step 8: Booking Form
1. Go to Booking Form (`/booking-form`)
2. **See**: 
   - Interview slot dropdown
   - Candidate dropdown
   - Interview round selection
3. Fill form with sample data
4. Click "Book Interview"
5. ✅ **Result**: Success message or redirect

#### Step 9: Analytics Dashboard
1. Go to Dashboard Reports (`/dashboard-reports`)
2. **See**: 
   - Various charts and graphs
   - Key metrics: Total candidates, interviews, offers, etc.
   - Status breakdowns
3. Navigate to other analytics pages:
   - Line Chart (`/line-chart`)
   - Trend Chart (`/trend-chart`)
   - Interview Data (`/interview-data`)
   - Status Insights (`/status-insights`)
4. ✅ **Result**: All charts render with data

**Key Points:**
- Real-time analytics
- Multiple visualization types
- Exportable reports

#### Step 10: Logout
1. Click "Logout" button (top right)
2. ✅ **Result**: Redirected to login page, session cleared

**Admin Flow Summary:**
- ✅ Employee registration
- ✅ Master data management
- ✅ Candidate management
- ✅ Booking form access
- ✅ Analytics viewing
- ✅ Full platform administration

---

### DEMO FLOW 2: RECRUITER - Recruitment Lifecycle (8-10 min)

**Login Credentials:**
```
Email: priya.recruiter@capgemini.com
Password: Priya@123456
```

#### Step 1: Login as Recruiter
1. Navigate to http://localhost:8016
2. Enter email: `priya.recruiter@capgemini.com`
3. Enter password: `Priya@123456`
4. Click "Sign In"
5. ✅ **Result**: Redirected to role selection

#### Step 2: Select Recruiter Role
1. Click "Recruiter" button
2. ✅ **Result**: Redirected to `/todolist` (Recruiter Dashboard)

#### Step 3: Recruiter Dashboard - Todo List
1. **Current Page**: To-Do List
2. **See**: 
   - List of recruitment tasks/items
   - Status indicators (Pending, In Progress, Completed)
   - Priority levels
3. **Interact**: 
   - Click on task to view details
   - Mark as complete (if option available)
4. ✅ **Feature**: Task management for recruitment activities

#### Step 4: Candidate Management
1. Go to Candidate List (`/candidate-details`)
2. **See**:
   - Grid of all candidates
   - Columns: Name, Email, Phone, Status, Applied Date, Current Status
   - Search/Filter options
3. **Interact**:
   - Sort by columns
   - Search for candidate
   - Click on candidate row
4. ✅ **Result**: Detailed candidate view

**Candidate Details Include:**
- Basic info (name, email, phone)
- Resume/CV attachment
- Applied position
- Current status in pipeline
- Interview history
- Feedback scores
- Notes

#### Step 5: Upload Candidates
1. Go to Upload Page (`/upload`)
2. **See**: 
   - File upload area (drag & drop zone)
   - File input button
   - Upload instructions
3. **Demo**:
   - Show upload interface
   - Mention Excel template format
   - Would normally drag Excel file here
4. **After Upload** (if file provided):
   - Show progress bar
   - Processing status
   - Success message with count of imported candidates
5. ✅ **Result**: Candidates imported into system

**Upload Process:**
- Accepts .xlsx files
- Batch import of multiple candidates
- Field mapping and validation
- Real-time progress

#### Step 6: Interview Booking
1. Go to Booking Form (`/booking-form`)
2. **Form Fields**:
   - Candidate Selection (dropdown)
   - Interview Round (dropdown: Technical, Managerial, HR, etc.)
   - Interviewer Selection (dropdown)
   - Interview Slot (date & time)
   - Interview Mode (Online/Offline)
   - Meeting Link (if online)
   - Notes
3. **Demo**:
   - Select a candidate
   - Choose interview round (e.g., "Technical Round 1")
   - Select interviewer from list
   - Pick date/time slot
4. Click "Book Interview"
5. ✅ **Result**: Success message "Interview booked successfully"

**Key Features:**
- Calendar integration for slot selection
- Interviewer availability check
- Automated email/notification (backend)
- Meeting link generation

#### Step 7: Candidate Profile Management
1. Go to Candidate Details → Select a Candidate
2. **See Profile Page** with sections:
   - Personal Information
   - Contact Details
   - Resume/Documents
   - Application Status
   - Interview History
   - Feedback Summary
3. **Actions Available**:
   - Edit candidate info
   - Upload resume
   - Update status
   - View interview feedback
   - Add notes
4. ✅ **Result**: Ability to manage candidate profile

#### Step 8: Access Control Test (Optional)
1. **Try to Access Admin Pages**:
   - Go to `/register-panel`
   - Go to `/administration`
   - Go to `/master-data`
2. ✅ **Result**: See "Access Denied" message
3. **Explanation**: Recruiter role restricted to recruitment functions only

#### Step 9: Logout
1. Click "Logout" button
2. ✅ **Result**: Back to login page

**Recruiter Flow Summary:**
- ✅ Dashboard/Todo list access
- ✅ View all candidates
- ✅ Upload bulk candidates
- ✅ Book interview slots
- ✅ Manage candidate profiles
- ✅ Access control enforced
- ❌ Cannot access admin functions

---

### DEMO FLOW 3: INTERVIEWER - Scheduling & Feedback (8-10 min)

**Login Credentials:**
```
Email: john.interviewer@capgemini.com
Password: John@123456
```

#### Step 1: Login as Interviewer
1. Navigate to http://localhost:8016
2. Enter email: `john.interviewer@capgemini.com`
3. Enter password: `John@123456`
4. Click "Sign In"
5. ✅ **Result**: Role selection page

#### Step 2: Select Interviewer Role
1. Click "Interviewer" button
2. ✅ **Result**: Redirected to `/dashboard` (Interviewer Dashboard)

#### Step 3: Interviewer Dashboard Overview
1. **Current Page**: Interviewer Dashboard
2. **See Components**:
   - **Calendar View**: Full month/week calendar
   - **Scheduled Interviews**: List of upcoming interviews
   - **Candidate Photos**: Quick reference
   - **Quick Actions**: Buttons for common tasks
3. **Calendar Features**:
   - Click on a date to see interviews for that day
   - Color-coded by interview type/status
   - Show interview count per day
4. ✅ **Result**: Full visibility of interview schedule

#### Step 4: View Scheduled Interviews
1. **On Dashboard**, see list of interviews
2. **For Each Interview, Visible**:
   - Candidate name
   - Interview date & time
   - Round (Technical, HR, Managerial, etc.)
   - Interview mode (Online/Offline)
   - Status (Scheduled, In Progress, Completed, etc.)
3. **Click on Interview Card**:
   - See full interview details
   - Candidate resume link
   - Call/meeting details
   - Interview guidelines
   - Feedback form link
4. ✅ **Result**: Full interview context

#### Step 5: Interview Slot Management
1. **On Dashboard**, look for "Create Slot" or "Add Availability" button
2. Click button
3. **Form to Create Slot**:
   - Date (calendar picker)
   - Start Time (time picker)
   - End Time (time picker)
   - Slot Type (e.g., Technical, HR)
   - Interview Mode (Online/Offline)
   - Duration (auto-calculated)
4. **Fill Sample**:
   - Date: Tomorrow
   - Start: 10:00 AM
   - End: 11:00 AM
   - Type: Technical
   - Mode: Online
5. Click "Create Slot"
6. ✅ **Result**: New slot added to availability

**Slot Management Features:**
- Multiple slot creation
- Bulk availability upload
- Conflict detection
- Time zone support

#### Step 6: Provide Interview Feedback
1. **From Dashboard**, click on completed interview
2. **Or Navigate to**: `/feedback/{bookingId}`
3. **Feedback Form Contains**:
   - **Technical Skills** (rating 1-5, comments)
   - **Communication** (rating 1-5, comments)
   - **Problem Solving** (rating 1-5, comments)
   - **Overall Assessment** (rating 1-5)
   - **Recommendation** (Pass/Fail/Hold)
   - **Comments** (text area)
   - **Strengths** (checklist)
   - **Areas for Improvement** (checklist)
4. **Fill Sample Feedback**:
   - Rate each skill (e.g., Technical: 4/5)
   - Add positive comment: "Strong problem-solving skills"
   - Add constructive feedback: "Could improve communication clarity"
   - Recommendation: "Pass"
5. Click "Submit Feedback"
6. ✅ **Result**: Feedback saved, "Feedback submitted successfully"

**Feedback Features:**
- Structured evaluation criteria
- Scores and comments
- Recommendation tracking
- Audit trail of all feedback

#### Step 7: Web Feedback (Alternative)
1. **Optional**: Test alternative feedback interface
2. Navigate to `/webFeedback/{bookingId}`
3. **See**: Web-based feedback form (alternative UI)
4. Fill similar feedback fields
5. Submit
6. ✅ **Result**: Alternative feedback interface works

#### Step 8: Interview Data Report
1. Go to Interview Data (`/interview-data`)
2. **See**:
   - Table of all interviews
   - Columns: Candidate, Date, Round, Feedback Status, Rating
   - Filter/Sort options
   - Export option (PDF/Excel)
3. **Interact**:
   - View different interview rounds
   - See feedback summary
   - Export report
4. ✅ **Result**: Interview analytics visible

#### Step 9: Access Control Test (Optional)
1. **Try to Access Non-Interviewer Pages**:
   - Go to `/register-panel` → ❌ Access Denied
   - Go to `/candidate-details` → ❌ Access Denied
   - Go to `/upload` → ❌ Access Denied
   - Go to `/administration` → ❌ Access Denied
2. ✅ **Result**: Proper role restrictions enforced

#### Step 10: Logout
1. Click "Logout" button
2. ✅ **Result**: Back to login page

**Interviewer Flow Summary:**
- ✅ View scheduled interviews
- ✅ Calendar view of schedule
- ✅ Create availability slots
- ✅ Provide structured feedback
- ✅ View interview data/analytics
- ✅ Access control enforced
- ❌ Cannot access recruitment/admin functions

---

## 🔄 Key Features & Workflows

### Feature 1: Authentication System
**Flow**:
1. User enters email & password
2. Backend validates credentials against database
3. JWT token generated (valid for 24 hours)
4. Token stored in browser localStorage
5. Subsequent requests include token in Authorization header
6. Backend validates token on protected routes
7. Logout clears token from browser

**Tech Stack**:
- Frontend: localStorage + Axios interceptor
- Backend: python-jose + passlib[bcrypt]
- Algorithm: HS256

### Feature 2: Role-Based Access Control (RBAC)
**How It Works**:
1. User selects role after login
2. Frontend stores role in context
3. Protected routes check user role
4. Backend API also validates role
5. If role mismatch → Access Denied page shown

**Routes Protected By Role**:
```
/register-panel          → [Admin]
/administration          → [Admin]
/master-data            → [Admin, BUAdmin, PracticeAdmin]
/candidate-details      → [Admin, Recruiter, PMO, RecruiterLead]
/upload                 → [Admin, Recruiter, PMO, SAP Recruiter]
/booking-form           → [Admin, Recruiter, PMO]
/dashboard              → [Interviewer]
/feedback/:id           → [Interviewer]
/work-flow              → [Tower/BU/NA Leads, Admin]
/joiningbonus           → [RecruiterLead, Admin, BUAdmin]
/dashboard-reports      → [Admin, RecruiterLead, PMO]
```

### Feature 3: Employee Registration
**Workflow**:
1. Admin accesses `/register-panel`
2. Admin fills employee form:
   - Name, Email, Password
   - BU, Grade, Location
   - Role (from dropdown)
   - Technologies (from dropdown)
3. Form submits to backend
4. Backend:
   - Validates email uniqueness
   - Hash password using bcrypt
   - Create Employee record in DB
   - Assign role mapping
5. Frontend shows success notification
6. New employee can login

**Database Tables**:
- `employee` - Employee records
- `employee_role_mapping` - Role assignments
- `employee_technology` - Skill assignments

### Feature 4: Candidate Management
**Workflow**:
1. **Upload**: Recruiter uploads Excel file
   - Parse Excel → Extract candidate data
   - Validate fields
   - Create Candidate records
   - Show import summary

2. **View**: Recruiter views candidate list
   - Filter by status, source, BU
   - Sort by name, date applied
   - Search functionality

3. **Profile**: Click candidate to view details
   - Resume download link
   - Interview history
   - Feedback summary
   - Current status in pipeline

**Database Tables**:
- `candidate` - Candidate records
- `candidate_document` - Resumes, attachments
- `interview_booking` - Interview records
- `feedback_form` - Interview feedback

### Feature 5: Interview Booking
**Workflow**:
1. Recruiter fills booking form:
   - Select candidate
   - Choose interview round
   - Select interviewer
   - Pick date/time slot
   - Set mode (online/offline)
2. Backend:
   - Check interviewer availability
   - Create booking record
   - Generate meeting link (if online)
   - Send notifications
3. Interviewer sees interview on dashboard
4. At interview time:
   - Interviewer joins call/meeting
   - Conducts interview
   - Provides feedback post-interview

**Database Tables**:
- `interview_booking` - Booking records
- `interviewer_calendar` - Slot availability

### Feature 6: Feedback Collection
**Workflow**:
1. Interviewer completes interview
2. Navigates to feedback form
3. Rates candidate on:
   - Technical skills
   - Communication
   - Problem solving
   - Overall assessment
4. Provides recommendation (Pass/Fail/Hold)
5. Submits feedback
6. Feedback recorded with timestamp & interviewer ID
7. Recruiter/L2 can view all feedback for candidate

**Database Tables**:
- `feedback_form` - Feedback records
- `candidate_feedback_master` - Feedback templates

### Feature 7: Analytics & Reports
**Reports Available**:
- **Dashboard Reports**: KPI cards, overview metrics
- **Line Chart**: Candidate status trends over time
- **Trend Chart**: Offer trends, conversion rates
- **Interview Data**: Interview-wise analytics
- **Status Insights**: Candidate status breakdown
- **Channel Insights**: Source-wise distribution
- **L2 Report**: L2-level reporting dashboard
- **Rejection Report**: Rejection reasons analysis

**Data Visualized**:
- Total candidates, interviews, offers
- Conversion rates (applied → interview → offer)
- Time to hire metrics
- Pipeline status
- Channel performance
- Rejection analysis

**Export Options**:
- PDF download
- Excel export
- Print-friendly view

---

## 🔌 API Endpoints Reference

### Authentication Endpoints
```
POST /api/v1/auth/login
  Request: { email, password }
  Response: { access_token, token_type, user_id, email, roles }
  Status: 200

POST /api/v1/auth/logout
  Headers: Authorization: Bearer {token}
  Response: { message: "Logout successful" }
  Status: 200
```

### Employee Management
```
POST /api/v1/admin/register-employee
  Request: { emp_name, email_id, password, bu, grade, location, roles, technologies }
  Response: { employee_id, message }
  Status: 201

GET /api/v1/admin/employees
  Headers: Authorization: Bearer {token}
  Response: { employees: [...] }
  Status: 200

PUT /api/v1/admin/employees/{id}
  Request: { emp_name, bu, grade, location, roles, technologies }
  Response: { message, employee }
  Status: 200
```

### Master Data
```
GET /api/v1/admin/towers
GET /api/v1/admin/skills
GET /api/v1/admin/sources
GET /api/v1/admin/vendors
  Response: { items: [...], total: count }
  Status: 200

POST /api/v1/admin/towers
  Request: { tower_name, description }
  Response: { tower_id, message }
  Status: 201
```

### Candidate Management
```
GET /api/v1/candidates
  Query Params: skip=0, limit=20, status=?, source=?
  Response: { candidates: [...], total: count }
  Status: 200

GET /api/v1/candidates/{id}
  Response: { candidate: {...}, interviews: [...], feedback: [...] }
  Status: 200

POST /api/v1/candidates/upload
  Body: FormData with file
  Response: { imported_count, failed_count, errors: [...] }
  Status: 201
```

### Interview Booking
```
POST /api/v1/booking/slots
  Request: { interviewer_id, interview_date, interview_from_time, interview_to_time, slot_type }
  Response: { slot_id, message }
  Status: 201

POST /api/v1/booking/create
  Request: { candidate_id, interviewer_id, interview_round, interview_date, meeting_link }
  Response: { booking_id, message }
  Status: 201

GET /api/v1/booking/{id}
  Response: { booking: {...}, candidate: {...}, interviewer: {...} }
  Status: 200
```

### Feedback
```
POST /api/v1/feedback/submit
  Request: { booking_id, technical_skills, communication, problem_solving, overall_assessment, recommendation, comments }
  Response: { feedback_id, message }
  Status: 201

GET /api/v1/feedback/{booking_id}
  Response: { feedback: {...} }
  Status: 200

GET /api/v1/feedback/candidate/{candidate_id}
  Response: { feedbacks: [...], average_score }
  Status: 200
```

### Analytics
```
GET /api/v1/analytics/dashboard
  Response: { total_candidates, interviews_completed, offers_extended, conversion_rate }
  Status: 200

GET /api/v1/analytics/interview-data
  Response: { interviews: [...], total }
  Status: 200

GET /api/v1/analytics/line-chart
  Response: { data: [...] for trend visualization }
  Status: 200

GET /api/v1/analytics/status-insights
  Response: { status_breakdown: {...} }
  Status: 200
```

### Workflow
```
GET /api/v1/workflow/approved-candidates
  Response: { candidates: [...] }
  Status: 200

POST /api/v1/workflow/approve
  Request: { candidate_id, level, approved_by }
  Response: { message }
  Status: 200
```

**Base URL**: `http://localhost:8015/api/v1/`

**Headers Required**:
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

---

## 🎨 UI Components & Pages

### Public Pages
- `/login` - Login form
- `/` - Redirect to login

### Protected Pages (All Authenticated Users)
- `/selectrole` - Role selection

### Admin Pages
- `/register-panel` - Employee registration
- `/administration` - Admin dashboard
- `/master-data` - Master data management

### Recruiter Pages
- `/todolist` - Recruiter todo/dashboard
- `/candidate-details` - Candidate list & detail
- `/upload` - Candidate upload
- `/booking-form` - Interview booking

### Interviewer Pages
- `/dashboard` - Calendar & scheduled interviews
- `/feedback/{bookingId}` - Feedback form
- `/webFeedback/{bookingId}` - Web-based feedback

### Analytics Pages (Multi-Role Access)
- `/dashboard-reports` - Main analytics dashboard
- `/line-chart` - Trend visualization
- `/trend-chart` - Offer trends
- `/interview-data` - Interview analytics
- `/status-insights` - Pipeline status
- `/channel-insights` - Source analysis
- `/arc-deviation` - Deviation analysis
- `/rejection-report` - Rejection analysis
- `/l2-report` - L2 approval metrics

### Workflow Pages
- `/work-flow` - Approval workflow
- `/work-flow-info` - Workflow information
- `/select-reject` - Rejection handling
- `/candidate-approval-data` - Approval data
- `/dateofjoining` - DOJ management

---

## 📊 Database Schema Overview

### Core Tables
```sql
-- Users & Roles
employee (emp_id, emp_name, email_id, password_hash, bu, grade, location)
employee_role_mapping (emp_id, role_id)
role_master (role_id, role_name)

-- Candidates
candidate (candidate_id, candidate_name, email, phone, resume_path, status, source, applied_date)
candidate_technology (candidate_id, skill_id)

-- Interviews
interview_booking (booking_id, candidate_id, interviewer_id, interview_date, interview_round, status)
interviewer_calendar (calendar_id, emp_id, interview_date, interview_from_time, interview_to_time, slot_type)
feedback_form (feedback_id, booking_id, emp_id, technical_skills, communication, overall_assessment, recommendation)

-- Master Data
tower_master (tower_id, tower_name)
technology_master (skill_id, tech_name)
source_master (source_id, source_name)
candidate_status_master (status_id, status_name)

-- Audit
candidate_document (doc_id, candidate_id, doc_type, file_path)
```

---

## 🐛 Troubleshooting

### Common Issues & Solutions

#### Issue 1: "Can't connect to backend"
**Error**: Frontend shows "Failed to fetch" or CORS error
**Solution**:
```bash
# 1. Check backend is running on port 8015
curl http://localhost:8015/docs

# 2. Verify CORS is enabled in backend
# File: backend/app/main.py should have:
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8016"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. Restart both backend and frontend
```

#### Issue 2: "Login fails - Invalid credentials"
**Error**: Even with correct username, login fails
**Solution**:
```bash
# 1. Verify user exists in database
SELECT * FROM employee WHERE email_id = 'admin@smartrecruit.dev';

# 2. Check database connection
# Verify DB_PASSWORD env var is set correctly

# 3. Check password is correct
# Passwords are case-sensitive!
```

#### Issue 3: "Access Denied for valid user"
**Error**: User logged in but gets "Access Denied" on pages
**Solution**:
```bash
# 1. Verify role mapping in DB
SELECT * FROM employee_role_mapping WHERE emp_id = ?;

# 2. Check role_id matches page requirements
# Different pages require different roles

# 3. Try selecting different role on /selectrole if available
```

#### Issue 4: "Database connection error"
**Error**: Backend shows "ConnectionRefusedError" or "Cannot connect to PostgreSQL"
**Solution**:
```bash
# 1. Verify PostgreSQL is running
# On Windows: Check Services
# On Mac: brew services list
# On Linux: systemctl status postgresql

# 2. Check database exists
psql -U postgres -c "SELECT datname FROM pg_database WHERE datname='smarthiremain001';"

# 3. Verify environment variables
echo %DB_PASSWORD%  # Windows
echo $DB_PASSWORD   # Mac/Linux

# 4. Test connection
psql -U postgres -d smarthiremain001 -h localhost
```

#### Issue 5: "Upload fails with validation error"
**Error**: Excel upload shows "File validation failed"
**Solution**:
```
# Excel format requirements:
- Columns: candidate_name, email, phone, position, source
- File type: .xlsx (not .csv or .xls)
- Max rows: 1000
- No blank rows

# Template available at: backend/migrations/sample_candidates.xlsx
```

#### Issue 6: "Port already in use"
**Error**: Backend or frontend won't start - "Address already in use"
**Solution**:
```bash
# Windows:
netstat -ano | findstr :8015  # Shows process on 8015
taskkill /PID <PID> /F

# Mac/Linux:
lsof -i :8015
kill -9 <PID>

# Or use different ports:
python -m uvicorn app.main:app --port 8080
npm run dev -- --port 8080
```

#### Issue 7: "Role dropdown shows no options"
**Error**: When creating employee, role dropdown is empty
**Solution**:
```bash
# 1. Check role_master table has data
SELECT * FROM role_master;

# 2. Run seed script if needed
cd backend
python seed_data.py
```

#### Issue 8: "Feedback form won't submit"
**Error**: Feedback submission shows error
**Solution**:
```
# Verify:
1. User is logged in as Interviewer
2. booking_id is valid
3. All required fields filled (ratings, recommendation)
4. Browser developer console shows error message
```

---

## 📚 Additional Resources

### API Documentation
- **Swagger UI**: http://localhost:8015/docs
- **ReDoc**: http://localhost:8015/redoc

### Code Structure
```
smart-recruit-platform/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI app entry
│   │   ├── api/v1/              # API routes
│   │   ├── models/              # SQLAlchemy models
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── services/            # Business logic
│   │   └── core/                # Config, security, DB
│   ├── migrations/              # Alembic migrations
│   ├── requirements.txt
│   └── seed_data.py
│
├── frontend/
│   ├── src/
│   │   ├── pages/               # Page components
│   │   ├── components/          # Reusable components
│   │   ├── services/            # API calls
│   │   ├── hooks/               # Custom hooks
│   │   ├── contexts/            # React contexts
│   │   └── routes.tsx           # Routing config
│   ├── package.json
│   └── vite.config.ts
│
└── specs/
    └── 001-smart-recruit-platform/
        ├── spec.md              # Feature specification
        ├── plan.md              # Implementation plan
        ├── tasks.md             # Task breakdown
        └── data-model.md        # Data model docs
```

### Development Notes
- **Hot Reload**: Both backend and frontend support hot reload during dev
- **Database Migrations**: Use `alembic` for schema changes
- **API Testing**: Use Swagger UI at `/docs` for testing endpoints
- **Frontend Testing**: Screenshots available in `.playwright-mcp/` directory

---

## ✅ Demo Checklist

### Pre-Demo Setup (5 minutes)
- [ ] Backend running on port 8015 (no errors in console)
- [ ] Frontend running on port 8016 (page loads)
- [ ] Database connected (can see data)
- [ ] Test user credentials copied
- [ ] Browser tabs arranged (optional: 2 windows for side-by-side)
- [ ] Microphone/speaker working (if presenting remotely)

### During Demo (25-30 minutes)

**Segment 1: Admin Flow (8 min)**
- [ ] Start: Show login page
- [ ] Login as admin
- [ ] Show role selection
- [ ] Create test employee (show form validation)
- [ ] Navigate to admin pages
- [ ] Show master data

**Segment 2: Recruiter Flow (8 min)**
- [ ] Logout and login as recruiter
- [ ] Show recruiter dashboard
- [ ] Show candidate list
- [ ] Show upload interface (explain template)
- [ ] Show booking form
- [ ] Test access denial on admin pages

**Segment 3: Interviewer Flow (8 min)**
- [ ] Logout and login as interviewer
- [ ] Show interviewer dashboard with calendar
- [ ] Show slot creation
- [ ] Show interview details
- [ ] Show feedback form and submit
- [ ] Show interview data report

**Segment 4: Analytics (3 min)**
- [ ] Show analytics dashboard
- [ ] Show charts and metrics
- [ ] Explain export options

**Q&A**: Address questions

---

## 🎓 Key Points to Highlight During Demo

1. **Role-Based Security**: Each user only sees relevant data
2. **End-to-End Flow**: Complete hiring pipeline in one platform
3. **Real-Time Availability**: Calendar sync with interview slots
4. **Structured Feedback**: Standardized evaluation criteria
5. **Analytics**: Data-driven recruitment insights
6. **Scalability**: Bulk upload for 1000+ candidates
7. **User-Friendly**: Intuitive interface for non-technical users
8. **Mobile-Responsive**: Works on desktop and tablet
9. **API-First**: Modern API architecture for integrations
10. **Audit Trail**: Complete tracking of all actions

---

## 📞 Support & Documentation

For questions or issues:
1. Check this README first
2. See API docs at `/docs`
3. Check console logs for errors
4. Review test results in `TEST_RESULTS_PLAYWRIGHT.md`
5. Check code comments in source files

---

**Platform Version**: 1.0 (Phase 1)  
**Last Updated**: May 27, 2026  
**Status**: ✅ Production Ready

**Demo Ready!** Use this guide to give a complete walkthrough of all features to stakeholders.
