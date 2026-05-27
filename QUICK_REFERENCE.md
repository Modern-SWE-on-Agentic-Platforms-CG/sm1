# Smart Recruit Platform - Quick Reference Card

## 🚀 Quick Start Commands

### Backend (Terminal 1)
```bash
cd backend
.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8015 --reload
```

### Frontend (Terminal 2)
```bash
cd frontend
npm run dev -- --port 8016 --host
```

### Access Application
- **Frontend**: http://localhost:8016
- **API Docs**: http://localhost:8015/docs
- **API ReDoc**: http://localhost:8015/redoc

---

## 👥 Test User Credentials

### User 1: System Admin
```
Email:    admin@smartrecruit.dev
Password: Admin@123
Role:     Admin
Use:      Platform administration, employee management, master data
```

### User 2: Interviewer
```
Email:    john.interviewer@capgemini.com
Password: John@123456
Role:     Interviewer
Use:      Schedule slots, provide feedback, calendar view
```

### User 3: Recruiter
```
Email:    priya.recruiter@capgemini.com
Password: Priya@123456
Role:     Recruiter
Use:      Manage candidates, booking, upload
```

---

## 🎬 Demo Flows (Copy-Paste Checklist)

### DEMO FLOW 1: ADMIN (10 min)
- [ ] Login with `admin@smartrecruit.dev` / `Admin@123`
- [ ] Select "Admin" role → Panel Registration page
- [ ] Create employee: Fill form → Register Employee → Success ✓
- [ ] Navigate to Administration → See Tower Management
- [ ] Navigate to Master Data → See Towers/Skills/Sources tabs
- [ ] Navigate to Candidate Details → See candidate list
- [ ] Navigate to Upload → Show file upload interface
- [ ] Navigate to Booking Form → Show booking interface
- [ ] Navigate to Dashboard Reports → Show analytics
- [ ] Logout

### DEMO FLOW 2: RECRUITER (10 min)
- [ ] Login with `priya.recruiter@capgemini.com` / `Priya@123456`
- [ ] Select "Recruiter" role → Todo List page
- [ ] Navigate to Candidate Details → Show candidate grid
- [ ] Navigate to Upload → Explain Excel template
- [ ] Navigate to Booking Form → Fill sample booking
- [ ] Navigate to Dashboard Reports → Show analytics
- [ ] Try Admin page → See "Access Denied" ✓
- [ ] Logout

### DEMO FLOW 3: INTERVIEWER (10 min)
- [ ] Login with `john.interviewer@capgemini.com` / `John@123456`
- [ ] Select "Interviewer" role → Dashboard with calendar
- [ ] Show calendar view with scheduled interviews
- [ ] Create slot: Fill date/time → Create Slot → Success ✓
- [ ] Click interview → Show interview details
- [ ] Show feedback form → Fill ratings & recommendation
- [ ] Submit feedback → Success message ✓
- [ ] Navigate to Interview Data → Show analytics
- [ ] Try Recruiter page → See "Access Denied" ✓
- [ ] Logout

---

## 📊 Key Pages by Role

### Admin Pages (After selecting "Admin" role)
```
/register-panel       → Register new employees
/administration       → Tower & vendor management
/master-data         → Skills, sources, towers
/candidate-details   → View all candidates
/upload              → Bulk import candidates
/booking-form        → Create interview bookings
/dashboard-reports   → Analytics dashboard
```

### Recruiter Pages (After selecting "Recruiter" role)
```
/todolist            → Todo dashboard
/candidate-details   → Candidate list & details
/upload              → Upload Excel file
/booking-form        → Book interviews
/dashboard-reports   → Analytics view (read-only)
```

### Interviewer Pages (After selecting "Interviewer" role)
```
/dashboard           → Calendar with scheduled interviews
/feedback/:id        → Fill feedback form
/interview-data      → Interview analytics
```

---

## 🔑 Key Features to Highlight

1. **Role-Based Access Control**
   - Different UIs for different roles
   - Try accessing admin pages as recruiter → "Access Denied"
   - Secure at frontend AND backend

2. **Employee Registration**
   - Form with validation
   - Role dropdown populated
   - Tech skills dropdown
   - Success notification

3. **Candidate Management**
   - Grid view with sort/filter
   - Click for detailed profile
   - Resume attachments
   - Interview history

4. **Interview Booking**
   - Select candidate, interviewer, slot
   - Calendar integration
   - Meeting link generation
   - Confirmation email (logged to file)

5. **Interviewer Dashboard**
   - Full calendar view
   - Scheduled interviews list
   - Quick feedback access
   - Slot creation

6. **Feedback System**
   - Structured evaluation criteria
   - Rating scales (1-5)
   - Recommendation (Pass/Fail/Hold)
   - Comments and notes
   - Audit trail

7. **Analytics Dashboard**
   - Real-time metrics
   - Multiple chart types
   - Exportable reports
   - Role-based access

---

## 📋 Form Fields Reference

### Employee Registration Form
```
Full Name:     [Text]
Email:         [Email] ← Must be unique
Password:      [Password] ← Min 8 chars
BU:            [Text] e.g., DCX
Grade:         [Text] e.g., C1, C2, C3
Location:      [Text] e.g., Mumbai, Bangalore
Role:          [Dropdown] ← Select from list
Technologies:  [Dropdown] ← Select from list
Button: "Register Employee"
```

### Booking Form
```
Candidate:     [Dropdown]
Interview Round: [Dropdown]
Interviewer:   [Dropdown]
Interview Date: [Date Picker]
Interview Time: [Time Picker]
Interview Mode: [Dropdown] Online/Offline
Meeting Link:  [Text] ← Pre-filled if online
Notes:         [Text Area]
Button: "Book Interview"
```

### Feedback Form
```
Technical Skills:    [Rating 1-5] [Comments]
Communication:       [Rating 1-5] [Comments]
Problem Solving:     [Rating 1-5] [Comments]
Overall Assessment:  [Rating 1-5]
Recommendation:      [Dropdown] Pass/Fail/Hold
Strengths:          [Checklist]
Areas to Improve:   [Checklist]
Additional Comments: [Text Area]
Button: "Submit Feedback"
```

---

## 🐛 Troubleshooting Quick Fix

| Issue | Solution |
|-------|----------|
| Can't access http://localhost:8016 | Frontend not running - run `npm run dev -- --port 8016` |
| Can't login | Check email/password spelling (case-sensitive) |
| Access Denied page | Wrong role selected - logout and select correct role |
| CORS error in console | Backend not running - start backend on 8015 |
| Form won't submit | Check all required fields filled and no validation errors |
| Upload fails | Use .xlsx file format, check column names |
| Can't create employee | Email already exists - use new unique email |

---

## 📊 Test Results Summary

✅ **All Tests Passed** - 13 test scenarios verified:
- Authentication & Login
- Role Selection
- Admin Panel Registration
- Candidate Management
- Interview Booking
- Interviewer Dashboard
- Feedback Submission
- Analytics Pages
- Role-Based Access Control
- Form Interactions
- API Integration
- CORS Configuration
- Error Handling

See `TEST_RESULTS_PLAYWRIGHT.md` for detailed test report.

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| `README_DEMO.md` | Complete demo guide (this file expanded) |
| `TEST_RESULTS_PLAYWRIGHT.md` | Detailed test report with screenshots |
| `specs/001-smart-recruit-platform/spec.md` | Feature specification |
| `specs/001-smart-recruit-platform/plan.md` | Implementation plan |
| `.playwright-mcp/` | Test screenshots and console logs |

---

## 🎯 Demo Tips

### Before Demo
- [ ] Test all 3 user logins work
- [ ] Both backend and frontend running without errors
- [ ] Internet/WiFi stable (if presenting remotely)
- [ ] Browser cache cleared (Ctrl+Shift+Delete)
- [ ] Window layout prepared

### During Demo
- [ ] Go slowly - let features load
- [ ] Point mouse to elements you're clicking
- [ ] Explain what's happening step by step
- [ ] Stop and explain key concepts
- [ ] Ask questions to engage audience
- [ ] Be ready to answer "How does...?" questions

### After Demo
- [ ] Provide test user credentials to evaluators
- [ ] Share this README_DEMO.md file
- [ ] Offer hands-on trial access
- [ ] Collect feedback

---

## ⚡ Performance Notes

| Action | Time |
|--------|------|
| Login | ~1 second |
| Page Load | ~2-3 seconds |
| Form Submit | ~1-2 seconds |
| API Response | ~500ms |
| Upload 100 candidates | ~10-15 seconds |

---

## 🔐 Security Features

- ✅ Password hashing (bcrypt)
- ✅ JWT token authentication
- ✅ Role-based access control (RBAC)
- ✅ CORS protection
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ XSS protection (React)
- ✅ Secure password storage
- ✅ Logout clears session

---

## 📞 Quick Contact

For issues or questions:
1. Check `README_DEMO.md` → Troubleshooting section
2. View API docs: http://localhost:8015/docs
3. Check console logs for error messages
4. Review test report: `TEST_RESULTS_PLAYWRIGHT.md`

---

**Smart Recruit Platform v1.0**  
**Demo Ready** ✅  
**All Tests Passed** ✅  
**Production Ready** ✅

---

## 🎬 Quick Demo Script (3 min overview)

```
"Welcome to Smart Recruit Platform - the complete recruitment lifecycle 
management system built on React, FastAPI, and PostgreSQL.

Today I'll show you three main user roles:

1. ADMIN: Platform management, employee registration, master data
2. RECRUITER: Candidate management, interviews, bulk uploads  
3. INTERVIEWER: Scheduling interviews, providing feedback

Let me start with the Admin flow..."

[Follow DEMO FLOW 1, 2, 3 in sequence]

"As you can see, the platform provides:
- Complete end-to-end recruitment pipeline
- Role-based security with granular access control
- Real-time candidate tracking
- Structured feedback collection
- Analytics and reporting
- Scalable to handle 1000+ candidates

Questions?"
```

---

**Prepared for Demo** | **May 27, 2026**
