# Smart Recruit Platform - Step-by-Step Demo Guide

## 📍 Pre-Demo Checklist (Do This First!)

- [ ] Backend running: `python -m uvicorn app.main:app --host 0.0.0.0 --port 8015 --reload`
- [ ] Frontend running: `npm run dev -- --port 8016`
- [ ] Open browser: http://localhost:8016
- [ ] See Smart Recruit login page
- [ ] Have test user credentials ready (see below)
- [ ] Clear browser cache (Ctrl+Shift+Delete)

---

## 🔐 Test User Credentials (Copy-Paste Ready)

### Admin User
```
Email:    admin@smartrecruit.dev
Password: Admin@123
```

### Recruiter User
```
Email:    priya.recruiter@capgemini.com
Password: Priya@123456
```

### Interviewer User
```
Email:    john.interviewer@capgemini.com
Password: John@123456
```

---

## 🎬 DEMO FLOW 1: ADMIN (Complete Employee Management)

### Step 1: Login as Admin
1. Go to: http://localhost:8016
2. **Email field**: `admin@smartrecruit.dev`
3. **Password field**: `Admin@123`
4. **Click**: "Sign In"
5. **Wait**: 2-3 seconds
6. **You see**: "Welcome, System Admin" message

### Step 2: Select Admin Role
1. **Click**: "Admin" button
2. **Wait**: Page loads
3. **You're now on**: Panel Registration page

### Step 3: Create New Employee
**Explain**: "This is where admins register new team members"

Fill these fields:
```
Full Name:      John Smith
Email:          john.smith@capgemini.com
Password:       John@Smith123
BU:             DCX
Grade:          C2
Location:       Mumbai
Role:           [Dropdown] Select "Interviewer"
Technologies:   [Dropdown] Select "Java"
```

Click: **"Register Employee"**

**Result**: Green notification "Employee registered successfully" ✓

### Step 4: Show Administration Page
1. **Look for**: Navigation (header or sidebar)
2. **Go to**: `/administration` (or find link)
3. **Show**:
   - Tower Management section
   - Buttons: Towers, Skills, Sources, Vendors, Approver DL

### Step 5: Show Master Data
1. **Navigate to**: Master Data
2. **You see**: Tabs for "Towers", "Skills", "Sources"
3. **Click**: Each tab to show data management

### Step 6: Candidate Overview
1. **Navigate to**: Candidate Details (`/candidate-details`)
2. **Show**: List of candidates in a grid
3. **Explain**: Columns show candidate status, applied date, etc.

### Step 7: Upload Interface
1. **Navigate to**: Upload (`/upload`)
2. **Show**: File upload area (drag & drop zone)
3. **Explain**: "Upload 100s of candidates at once via Excel"

### Step 8: Analytics
1. **Navigate to**: Dashboard Reports (`/dashboard-reports`)
2. **Show**: Charts and metrics
3. **Point out**: KPIs, conversion rates, trends

### Step 9: Logout
1. **Click**: "Logout" button (top right)
2. **Result**: Back to login page ✓

**Admin Demo Complete!** ✅ (7-8 minutes)

---

## 🎬 DEMO FLOW 2: RECRUITER (Candidate Recruitment)

### Step 1: Login as Recruiter
1. Go to: http://localhost:8016
2. **Email**: `priya.recruiter@capgemini.com`
3. **Password**: `Priya@123456`
4. **Click**: "Sign In"
5. **You see**: Role selection page

### Step 2: Select Recruiter Role
1. **Click**: "Recruiter" button
2. **Result**: Redirected to Todo List page

### Step 3: Todo/Recruiter Dashboard
**Explain**: "This is the recruiter's dashboard showing tasks"
1. **See**: List of recruitment tasks
2. **Explain**: Statuses, priorities, assignments

### Step 4: Candidate List
1. **Navigate to**: Candidate Details (`/candidate-details`)
2. **Show**: Grid of all candidates
3. **Features**:
   - Sort by clicking column headers
   - Filter by status/source
   - Search functionality
4. **Click**: A candidate row
5. **Result**: Candidate detail page with resume, history

### Step 5: Upload Candidates
1. **Navigate to**: Upload (`/upload`)
2. **Show**: Upload interface
3. **Explain**: 
   - Accepts Excel (.xlsx) files
   - Format: candidate_name, email, phone, position, source
   - Can upload 1000+ candidates at once
4. **Demo**: Show file upload area (don't upload unless you have test file)

### Step 6: Interview Booking
1. **Navigate to**: Booking Form (`/booking-form`)
2. **Show form fields**:
   - Candidate dropdown
   - Interview Round dropdown
   - Interviewer dropdown
   - Date picker
   - Time picker
3. **Fill sample** (don't submit unless needed):
   - Select a candidate
   - Select "Technical Round"
   - Select an interviewer
   - Pick a date/time
4. **Explain**: "When you click Book, notification sent to interviewer"

### Step 7: Test Access Control
1. **Navigate to**: `/register-panel` (Admin page)
2. **Result**: "Access Denied — you do not have the required role" ✓
3. **Explain**: "Recruiters can only see recruitment-related pages"

### Step 8: Analytics (Read-only)
1. **Navigate to**: Dashboard Reports (`/dashboard-reports`)
2. **Show**: Can view but not edit analytics

### Step 9: Logout
1. **Click**: "Logout"
2. **Result**: Back to login ✓

**Recruiter Demo Complete!** ✅ (7-8 minutes)

---

## 🎬 DEMO FLOW 3: INTERVIEWER (Interview Management)

### Step 1: Login as Interviewer
1. Go to: http://localhost:8016
2. **Email**: `john.interviewer@capgemini.com`
3. **Password**: `John@123456`
4. **Click**: "Sign In"
5. **You see**: Role selection

### Step 2: Select Interviewer Role
1. **Click**: "Interviewer" button
2. **Result**: Redirected to Dashboard

### Step 3: Interviewer Dashboard
1. **Current Page**: Interviewer Dashboard
2. **See**: Full calendar view
3. **Explain**: 
   - Shows availability
   - Can see scheduled interviews
   - Can manage slots
4. **Show**: 
   - Current month calendar
   - Interview count per day
   - Upcoming interviews list

### Step 4: Create Interview Slot
**Explain**: "Interviewers create their availability slots"

1. **Look for**: "Create Slot" or "Add Availability" button
2. **Click**: It
3. **Form appears**:
   - Date picker (select tomorrow)
   - Start Time (10:00 AM)
   - End Time (11:00 AM)
   - Slot Type (Technical)
   - Interview Mode (Online)
4. **Click**: "Create Slot"
5. **Result**: Slot added, calendar updates ✓

### Step 5: View Scheduled Interviews
1. **On Dashboard**: See list of scheduled interviews
2. **Show**:
   - Candidate name
   - Date and time
   - Interview round
   - Status
3. **Click**: An interview card
4. **Result**: Interview details page

### Step 6: Interview Details
1. **See**:
   - Candidate information
   - Resume link
   - Call details (for online interviews)
   - Interview guidelines
   - Feedback form link
2. **Explain**: "Click link to provide feedback after interview"

### Step 7: Provide Interview Feedback
1. **Click**: "Provide Feedback" link
2. **Navigate to**: `/feedback/{bookingId}`
3. **See Feedback Form**:
   ```
   Technical Skills:      [1-5 rating] + Comments
   Communication:         [1-5 rating] + Comments
   Problem Solving:       [1-5 rating] + Comments
   Overall Assessment:    [1-5 rating]
   Recommendation:        [Pass/Fail/Hold]
   Strengths:            [Checklist]
   Areas to Improve:     [Checklist]
   Comments:             [Text area]
   ```

4. **Fill sample feedback**:
   - Technical Skills: 4/5 - "Strong coding ability"
   - Communication: 3/5 - "Good but can improve clarity"
   - Problem Solving: 4/5 - "Excellent logical thinking"
   - Overall: 4/5
   - Recommendation: "Pass"
   - Strengths: Check "Problem Solving", "Communication"
   - Comments: "Good candidate, recommend for next round"

5. **Click**: "Submit Feedback"
6. **Result**: Success message "Feedback submitted successfully" ✓

### Step 8: Interview Analytics
1. **Navigate to**: Interview Data (`/interview-data`)
2. **Show**: Table of all interviews
3. **Columns**:
   - Candidate name
   - Date
   - Interview round
   - Feedback status
   - Ratings
4. **Feature**: Filter, sort, export

### Step 9: Test Access Control
1. **Navigate to**: `/candidate-details` (Recruiter page)
2. **Result**: "Access Denied" ✓
3. **Explain**: "Interviewers can only see interview-related pages"

### Step 10: Logout
1. **Click**: "Logout"
2. **Result**: Back to login ✓

**Interviewer Demo Complete!** ✅ (7-8 minutes)

---

## 📋 Demo Script Template

Use this script to narrate the demo:

```
"Welcome to Smart Recruit Platform, a complete recruitment lifecycle 
management system.

[SHOW LOGIN PAGE]
The platform uses email and password authentication with role-based access.

[LOGIN AS ADMIN]
First, let's see the Admin view. Admins manage the entire platform.

[SHOW ADMIN PAGES]
Admins can:
- Register new employees with specific roles
- Manage towers, skills, and master data
- View all candidates and analytics
- Create interview bookings

[CREATE EMPLOYEE]
Here's an example of registering a new employee. I fill in their details,
select their role and technologies, and register them. They can now login.

[NAVIGATE PAGES]
Let me show you the candidate management, uploads, and analytics.

[LOGOUT AND LOGIN AS RECRUITER]
Now let's look at the Recruiter view.

[SHOW RECRUITER PAGES]
Recruiters can:
- View candidate list with filters
- Bulk upload candidates from Excel
- Book interviews with available interviewers
- See recruitment analytics

[SHOW CANDIDATE PAGE]
Here's the candidate list. Recruiters can search, filter, and view 
detailed profiles including resumes and interview history.

[SHOW BOOKING]
For interview booking, they select candidate, interviewer, date and time.

[LOGOUT AND LOGIN AS INTERVIEWER]
Finally, let's see the Interviewer view.

[SHOW DASHBOARD]
Interviewers have a calendar showing their availability and scheduled 
interviews. They can create time slots for interviews.

[CREATE SLOT]
I'm creating a slot on [tomorrow's date] from 10-11 AM.

[SHOW FEEDBACK]
After an interview, interviewers provide structured feedback with ratings
and recommendations.

[FILL FEEDBACK]
The feedback form captures technical skills, communication, problem solving,
and an overall recommendation.

[SHOW ACCESS DENIED]
Notice each role only sees their relevant pages. If an interviewer tries 
to access recruiter pages, they get an 'Access Denied' message.

[SHOW ANALYTICS]
Everyone can see relevant analytics. The dashboard shows key metrics,
trends, and insights.

Questions?
"
```

---

## ⏱️ Time Breakdown

- Admin Demo: 7-8 minutes
- Recruiter Demo: 7-8 minutes  
- Interviewer Demo: 7-8 minutes
- Q&A: 5 minutes
- **Total: ~30 minutes**

---

## ✅ Features to Highlight

1. **Role-Based Security**: Different UI for different roles
2. **End-to-End Pipeline**: From upload to feedback
3. **Calendar Integration**: Interview scheduling
4. **Structured Feedback**: Standardized evaluation
5. **Analytics**: Real-time insights
6. **Scalability**: Handles 1000s of candidates
7. **User-Friendly**: No training needed
8. **API-First**: Integration-ready

---

## 🚨 If Something Goes Wrong

| Problem | Quick Fix |
|---------|-----------|
| Login fails | Check email spelling (case-sensitive) |
| Page won't load | Refresh (F5) or restart services |
| Form won't submit | Scroll down, check all fields filled |
| Can't see backend | Start: `python -m uvicorn app.main:app...` |
| Can't see frontend | Start: `npm run dev -- --port 8016` |
| Access Denied unexpected | Logout, select different role |

---

## 📸 Screenshots for Reference

See `.playwright-mcp/` folder for test screenshots:
- `test-01-login-page.png` - Login interface
- `test-02-role-selection.png` - Role selection
- `test-03-admin-dashboard-panel-registration.png` - Admin page
- `test-13-recruiter-dashboard-redirect.png` - Recruiter dashboard
- And many more...

---

## 🎯 Key Talking Points

**For Management:**
- "End-to-end visibility of recruitment process"
- "Reduces hiring time and improves consistency"
- "Data-driven recruitment decisions"
- "Scalable to enterprise requirements"

**For HR/Recruitment Team:**
- "Easy to learn, no training needed"
- "Automates repetitive tasks"
- "One central platform for all recruitment"
- "Real-time candidate tracking"

**For IT/Technical:**
- "Modern stack: React + FastAPI + PostgreSQL"
- "Role-based security at UI and API"
- "RESTful API for integrations"
- "Scalable architecture"

---

## 📞 Providing Access

After demo, to give stakeholders access:

1. Share test credentials (in this doc)
2. Share `README_DEMO.md` for full documentation
3. Share `QUICK_REFERENCE.md` for quick lookup
4. Provide backend URL: `http://localhost:8015`
5. Provide frontend URL: `http://localhost:8016`
6. Explain database is local, they need same setup

---

## ✨ Demo Success Criteria

✅ All 3 roles login successfully  
✅ No errors in browser console  
✅ Form submissions work  
✅ Access control shows "Access Denied" appropriately  
✅ Analytics dashboard shows data  
✅ Feedback submission successful  
✅ Navigation smooth and responsive  

---

## 🎬 You're Ready to Demo!

Go through each flow following the steps above.
Audience will see a complete, working recruitment platform.

**Good luck with your demo!** 🚀

---

**Smart Recruit Platform v1.0**  
**Demo Date**: May 27, 2026  
**Status**: ✅ Ready to Present
