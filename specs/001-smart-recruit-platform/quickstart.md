# Quickstart: Smart Recruit Platform

**Time to first run**: < 10 minutes (assumes Python 3.11+, Node 18+, PostgreSQL 14+ installed)

---

## Prerequisites

| Tool | Minimum version | Check command |
|---|---|---|
| Python | 3.11 | `python --version` |
| pip | 23+ | `pip --version` |
| Node.js | 18+ | `node --version` |
| npm | 9+ | `npm --version` |
| PostgreSQL | 14+ | `psql --version` |

---

## Step 1 — Create the database

```sql
-- Connect to PostgreSQL as postgres user
psql -U postgres -h localhost

-- Create the database
CREATE DATABASE smarthiremain001;
\q
```

> The database password used is `niit@123` — this is configured via the `.env` file only.
> **Never put the password in source code.**

---

## Step 2 — Configure environment variables

### Backend

```bash
cd backend
copy .env.example .env   # Windows
# or: cp .env.example .env  (macOS/Linux)
```

Edit `backend/.env`:

```env
# Database
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smarthiremain001
DB_USER=postgres
DB_PASSWORD=niit@123

# JWT
JWT_SECRET=smart-recruit-local-dev-secret-change-in-prod
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=480

# File storage
UPLOAD_DIR=./uploads
LOG_DIR=./logs

# Server
APP_ENV=development
```

### Frontend

```bash
cd frontend
copy .env.example .env   # Windows
```

Edit `frontend/.env`:

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## Step 3 — Install backend dependencies

```bash
cd backend

# Create virtual environment
python -m venv .venv

# Activate (Windows PowerShell)
.venv\Scripts\Activate.ps1

# Activate (macOS/Linux)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Step 4 — Run database migrations

```bash
# From backend/ directory with venv activated
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001, create role_master
INFO  [alembic.runtime.migration] Running upgrade 001 -> 002, create employee tables
INFO  [alembic.runtime.migration] Running upgrade 002 -> 003, create master data tables
INFO  [alembic.runtime.migration] Running upgrade 003 -> 004, create interviewer_calendar
INFO  [alembic.runtime.migration] Running upgrade 004 -> 005, create candidate tables
INFO  [alembic.runtime.migration] Running upgrade 005 -> 006, create feedback tables
INFO  [alembic.runtime.migration] Running upgrade 006 -> 007, create workflow tables
INFO  [alembic.runtime.migration] Running upgrade 007 -> 008, create supply tables
INFO  [alembic.runtime.migration] Running upgrade 008 -> 009, create referral tables
INFO  [alembic.runtime.migration] Running upgrade 009 -> 010, create extended master data
INFO  [alembic.runtime.migration] Running upgrade 010 -> 011, ...
INFO  [alembic.runtime.migration] Running upgrade 011 -> 012, create l2 tracking
```

---

## Step 5 — Seed initial data

```bash
# From backend/ directory with venv activated
python seed_data.py
```

This creates:
- 14 default roles (Interviewer, Recruiter, PMO, RecruiterLead, Admin, BUAdmin, etc.)
- 1 Admin user: `admin@smartrecruit.dev` / `Admin@123`
- Sample towers and technology skills
- Status transition mapping rules (22 transitions)
- Source and vendor master data
- Referral portal master data (technologies, notice periods, locations)

---

## Step 6 — Start the backend

```bash
# From backend/ directory with venv activated
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Verify: open `http://localhost:8000/docs` — Swagger UI should load showing all `/api/v1/` routes.

---

## Step 7 — Install frontend dependencies

Open a new terminal:

```bash
cd frontend
npm install
```

---

## Step 8 — Start the frontend

```bash
# From frontend/ directory
npm run dev
```

Expected output:
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

---

## Step 9 — Login

1. Open `http://localhost:5173` in your browser
2. Log in with: `admin@smartrecruit.dev` / `Admin@123`
3. Select the **Admin** role
4. You are redirected to `/candidate-referral` (Admin home route)

---

## JWT Storage — Local Dev Note

> **Security note**: In this local development setup, the JWT access token is stored in
> `localStorage` as a convenience. **Before deploying to any shared or production environment,
> you must switch to `httpOnly` cookies** by updating `frontend/src/contexts/AuthContext.tsx`
> and ensuring the backend sets `Set-Cookie: access_token=...; HttpOnly; SameSite=Lax`.
> See constitution §IV for the requirement.

---

## Verification Checklist

Run through these checks after setup:

- [ ] `http://localhost:8000/docs` shows all `/api/v1/` routes
- [ ] `POST /api/v1/auth/login` with `{ "email": "admin@smartrecruit.dev", "password": "Admin@123" }` returns a JWT
- [ ] React app at `http://localhost:5173` shows the login page
- [ ] Login works and role selection screen shows "Admin"
- [ ] `/api/v1/referral/technologies` returns referral tech list (no auth required)
- [ ] `/api/v1/admin/towers` returns 401 when called without auth

---

## Complete Feature Routes

| Route | Feature | Roles |
|---|---|---|
| `/feedback/:bookingId` | L1/L2 feedback form | Interviewer |
| `/work-flow` | Offer workflow approvals | TowerLead, RecruiterLead, Admin |
| `/joiningbonus` | JB candidate management | RecruiterLead, Admin, BUAdmin |
| `/administration` | Master data admin | Admin |
| `/select-reject` | L1 select/reject | Recruiter, RecruiterLead, Admin |
| `/dateofjoining` | Set DOJ for offers | PMO, Admin |
| `/dashboard-reports` | Analytics dashboard | Admin, RecruiterLead, PMO |
| `/arc-deviation` | ARC deviation report | Admin, RecruiterLead |
| `/l2-report` | L2 interview tracking | Recruiter, RecruiterLead, Admin |
| `/weekend-drive` | Weekend drive slots | Recruiter, RecruiterLead, Admin |
| `/referral` | Public referral portal | (public) |
| `/referral-candidates` | Referral management | Recruiter, RecruiterLead, Admin |
| `/demand-supply` | Demand/supply view | PMO, Admin, RecruiterLead |
| `/panel-insights` | Panel analytics | Admin, RecruiterLead |
| `/change-roles` | Change employee roles | Admin |

---

## Environment Variables — Production Notes

When deploying to production, set these additional variables:

```env
SMTP_ENABLED=true
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=noreply@example.com
SMTP_PASS=<secret>
SMTP_FROM=noreply@example.com
SMTP_TLS=true
APP_ENV=production
```

The APScheduler will automatically run 4 background jobs:
- **09:00** — pending feedback email reminders
- **10:00** — offer expiry reminders (3 days before)
- **11:00** — L2 aging alerts (>7 days pending)
- **02:00** — export file cleanup (>7 days old)
- [ ] Admin can navigate to Panel Registration (`/register-panel`) and see the form
- [ ] Register a new Interviewer user, then log in as that user — lands on `/dashboard`
- [ ] Interviewer can create a free slot — green event appears on calendar
- [ ] `alembic history` shows 5 applied migrations
- [ ] `backend/logs/email.log` is created after first booking

---

## API Reference

Interactive API docs (Swagger UI): `http://localhost:8000/docs`
OpenAPI JSON: `http://localhost:8000/openapi.json`

---

## Troubleshooting

| Problem | Solution |
|---|---|
| `psycopg2.OperationalError: connection refused` | Ensure PostgreSQL is running on port 5432 |
| `alembic.util.exc.CommandError: Can't locate revision identified by...` | Run `alembic stamp head` then `alembic upgrade head` |
| `ModuleNotFoundError: No module named 'app'` | Ensure you're running `uvicorn` from the `backend/` directory with venv active |
| Frontend shows CORS error | Confirm `VITE_API_BASE_URL=http://localhost:8000` in `frontend/.env` and backend allows `http://localhost:5173` in CORS config |
| `401 Unauthorized` on all requests | Token expired (8 h default) — log in again |
| `uploads/` directory errors | Create `backend/uploads/resumes`, `backend/uploads/attachments`, `backend/uploads/exports` manually if not auto-created |

---

## Useful Commands

```bash
# Check migration status
alembic current
alembic history

# Create a new migration (after editing models)
alembic revision --autogenerate -m "describe the change"

# Roll back one migration
alembic downgrade -1

# Reset all migrations (WARNING: drops all data)
alembic downgrade base

# Run backend tests
cd backend && pytest tests/ -v

# Run frontend tests
cd frontend && npm test
```
