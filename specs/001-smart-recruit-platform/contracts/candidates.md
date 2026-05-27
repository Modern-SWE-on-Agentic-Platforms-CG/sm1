# API Contract: Candidates

**Base path**: `/api/v1/candidates`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## POST /api/v1/candidates/upload (Bulk Excel import)

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Lead, Admin

### Request
`Content-Type: multipart/form-data`
- `file`: Excel file (`.xlsx` / `.xls`); max 5 MB
- Must match the 54-column candidate schema (see `research.md` R-005)

### Response 200
```json
{
  "data": {
    "imported": 47,
    "duplicates_skipped": 3,
    "errors": [
      { "row": 5, "reason": "Missing required field: Candidate Name" },
      { "row": 12, "reason": "Invalid skill: 'ReactNative'" }
    ],
    "error_file_url": "/api/v1/candidates/upload/errors/abc123.xlsx"
  },
  "error": null,
  "status": "success"
}
```

If `errors` is non-empty, an error Excel file is generated in `uploads/exports/` and the download URL is returned.

---

## GET /api/v1/candidates/upload/errors/{filename}

**Auth required**: Bearer token
**Roles**: Recruiter, Admin

Download the error Excel file from a previous bulk upload.

### Response 200
`Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`
Binary Excel file download.

---

## GET /api/v1/candidates

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Lead, Admin

### Query Parameters
| Param | Type | Required | Description |
|---|---|---|---|
| `skill_id` | int | no | Filter by technology |
| `status` | string | no | Filter by `overall_status` |
| `source` | string | no | Filter by sourcing channel |
| `from_date` | date | no | `recvd_date` range start |
| `to_date` | date | no | `recvd_date` range end |
| `created_by` | string | no | Filter by recruiter email |
| `bu` | string | no | Filter by Business Unit |
| `page` | int | no | Default 1 |
| `page_size` | int | no | Default 20, max 100 |

### Response 200
```json
{
  "data": {
    "items": [
      {
        "candidate_detail_id": 1001,
        "candidate_name": "Rahul Sharma",
        "email_id": "rahul.sharma@example.com",
        "overall_status": "L1 Scheduled",
        "skill_name": "Java",
        "source": "Vendor",
        "recvd_date": "2026-05-15",
        "aging_days": 11,
        "created_by": "recruiter@smartrecruit.local"
      }
    ],
    "total": 1,
    "page": 1,
    "page_size": 20
  },
  "error": null,
  "status": "success"
}
```

Note: `aging_days` is computed as `today - recvd_date` and returned in the response (not stored).

---

## GET /api/v1/candidates/{id}

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Interviewer (own interviews only), Admin

### Response 200
```json
{
  "data": {
    "candidate_detail_id": 1001,
    "candidate_name": "Rahul Sharma",
    "email_id": "rahul.sharma@example.com",
    "contact_number": "+91-9876543210",
    "gender": "Male",
    "total_exp": "5",
    "rel_exp": "3",
    "current_company": "Infosys",
    "current_location": "Bangalore",
    "overall_status": "L1 Scheduled",
    "skill_name": "Java",
    "source": "Vendor",
    "recvd_date": "2026-05-15",
    "aging_days": 11,
    "is_referral": false,
    "interviews": [
      {
        "recruiter_calendar_id": 501,
        "interview_type": "L1",
        "interview_date": "2026-05-20",
        "panel_email": "jane.doe@smartrecruit.local",
        "meeting_link": "https://meet.smartrecruit.local/meeting/abc-123",
        "feedback_submitted": false
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## PUT /api/v1/candidates/{id} (Update candidate profile)

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Admin

### Request
```json
{
  "contact_number": "+91-9999999999",
  "current_location": "Pune",
  "offer_ctc": "12.5"
}
```

Only provided fields are updated.

### Response 200
```json
{
  "data": { "candidate_detail_id": 1001, "..." : "updated fields" },
  "error": null,
  "status": "success"
}
```

---

## POST /api/v1/candidates/{id}/status (Change candidate status)

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Admin

### Request
```json
{
  "new_status": "L1 Selected",
  "notes": "Strong Java fundamentals, recommend L2"
}
```

### Response 200
```json
{
  "data": {
    "candidate_detail_id": 1001,
    "previous_status": "L1 Scheduled",
    "new_status": "L1 Selected",
    "changed_at": "2026-05-26T15:30:00Z"
  },
  "error": null,
  "status": "success"
}
```

### Response 400 — Invalid transition
```json
{
  "data": null,
  "error": "Invalid status transition: L1 Scheduled → Offered",
  "status": "error"
}
```

---

## GET /api/v1/candidates/{id}/status/valid-transitions

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Admin

Returns the list of valid next statuses for the current candidate status.

### Response 200
```json
{
  "data": {
    "current_status": "L1 Scheduled",
    "valid_next": ["L1 Selected", "L1 Rejected", "L1 Hold"]
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/candidates/{id}/history (Full interview cycle)

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Admin

### Response 200
```json
{
  "data": {
    "candidate_detail_id": 1001,
    "candidate_name": "Rahul Sharma",
    "status_history": [
      { "from_status": null, "to_status": "Profile Received", "changed_by": "recruiter@sr.local", "changed_at": "2026-05-15T09:00:00Z" },
      { "from_status": "Profile Received", "to_status": "L1 Scheduled", "changed_by": "recruiter@sr.local", "changed_at": "2026-05-18T11:00:00Z" }
    ],
    "interviews": [
      {
        "interview_type": "L1",
        "interview_date": "2026-05-20",
        "panel_email": "jane.doe@smartrecruit.local",
        "meeting_link": "https://meet.smartrecruit.local/meeting/abc-123",
        "feedback_submitted": false
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## POST /api/v1/candidates/{id}/comments (Add comment)

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Admin

### Request
`Content-Type: multipart/form-data`
- `comment_text` (string, optional): comment body
- `attachment` (file, optional): max 5 MB; PDF, DOC, DOCX, PNG, JPG allowed

At least one of `comment_text` or `attachment` must be provided.

### Response 201
```json
{
  "data": {
    "id": 77,
    "candidate_detail_id": 1001,
    "comment_text": "Discussed notice period — can join in 30 days.",
    "attachment_filename": null,
    "created_by": "recruiter@smartrecruit.local",
    "created_at": "2026-05-26T16:00:00Z"
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/candidates/{id}/comments

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Admin

### Response 200
```json
{
  "data": {
    "comments": [
      {
        "id": 77,
        "comment_text": "Discussed notice period — can join in 30 days.",
        "attachment_filename": null,
        "attachment_url": null,
        "created_by": "recruiter@smartrecruit.local",
        "created_at": "2026-05-26T16:00:00Z"
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## PUT /api/v1/candidates/{id}/skill (Update primary skill)

**Auth required**: Bearer token
**Roles**: Recruiter, Admin

### Request
```json
{ "skill_id": 5 }
```

### Response 200
```json
{
  "data": { "candidate_detail_id": 1001, "skill_id": 5, "skill_name": "Python" },
  "error": null,
  "status": "success"
}
```

---

## PUT /api/v1/candidates/{id}/doj (Update Date of Joining)

**Auth required**: Bearer token
**Roles**: PMO, Admin

### Request
```json
{ "doj": "2026-07-01" }
```

### Response 200
```json
{
  "data": { "candidate_detail_id": 1001, "doj": "2026-07-01" },
  "error": null,
  "status": "success"
}
```
