# API Contract: Automated Alerts & Scheduled Notifications

**Base path**: `/api/v1/admin`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## Scheduled Jobs Overview

The platform uses **APScheduler** (`AsyncIOScheduler`) to run four background jobs:

| Job Name | Schedule | Function |
|---|---|---|
| `aging-sla` | Cron — daily 9:00 AM | Sends aging SLA notifications for candidates beyond threshold |
| `interview-reminder` | Interval — every 15 minutes | Sends upcoming interview reminders |
| `feedback-reminder` | Cron — daily 9:00 AM | Sends pending feedback reminders to interviewers |
| `export-cleanup` | Cron — 9:00 AM + 9:00 PM | Deletes export files/records older than 7 days |

All jobs write to `backend/logs/email.log`.  
If `SMTP_ENABLED=true` in `.env`, they also send via `smtplib.SMTP`.

---

## Notification Log Format

Every notification attempt writes a structured entry to `backend/logs/email.log`:

```
[2026-05-26T09:00:00.000Z] TO=recruiter@example.com SUBJECT=Aging SLA Alert
Candidate: John Doe | Skill: Java | Days in L2: 45 | SLA: 30 days
---
```

---

## Manual Job Trigger (Dev/Admin only)

### GET /api/v1/admin/trigger-job/{job_name}

**Auth required**: Bearer token
**Roles**: Admin only

Manually triggers a scheduled job for development/testing purposes.

### Path Parameter
| Param | Values |
|---|---|
| `job_name` | `aging-sla`, `interview-reminder`, `feedback-reminder`, `export-cleanup` |

### Response 200
```json
{
  "data": {
    "job_name": "aging-sla",
    "message": "Job triggered successfully",
    "entries_processed": 3
  },
  "error": null,
  "status": "success"
}
```

### Response 400
```json
{
  "data": null,
  "error": "Unknown job name: invalid-job",
  "status": "error"
}
```

---

## Weekend Drive Endpoints

### POST /api/v1/weekend-drive/slots/bulk

**Auth**: Bearer | **Roles**: Admin

Bulk-creates weekend drive slots (reuses `slot_service.bulk_create_slots` with `is_weekend_drive=True`).

**Request**: `multipart/form-data` with `file` field (`.xlsx`, max 5 MB)

**Response 201**:
```json
{
  "data": { "created": 20, "errors": [{ "row": 5, "reason": "Overlap detected" }] },
  "error": null,
  "status": "success"
}
```

---

### POST /api/v1/weekend-drive/candidates/upload

**Auth**: Bearer | **Roles**: Admin

Bulk-imports weekend drive candidate data (reuses `candidate_service.parse_excel`).

**Request**: `multipart/form-data` with `file` field (`.xlsx`, max 5 MB)

**Response 201**:
```json
{
  "data": { "created": 15, "duplicates": 2, "errors": [] },
  "error": null,
  "status": "success"
}
```

---

### GET /api/v1/weekend-drive/summary

**Auth**: Bearer | **Roles**: Admin, Recruiter

Returns a summary for a specific weekend drive date.

### Query Parameters
| Param | Type | Required |
|---|---|---|
| `date` | date | yes (YYYY-MM-DD) |

### Response 200
```json
{
  "data": {
    "drive_date": "2026-06-01",
    "total_slots": 20,
    "booked_slots": 14,
    "interviews_conducted": 10,
    "feedback_pending": 4
  },
  "error": null,
  "status": "success"
}
```
