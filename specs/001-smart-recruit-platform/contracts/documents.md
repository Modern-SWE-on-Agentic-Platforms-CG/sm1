# API Contract: PDF & Document Management

**Base path**: `/api/v1/exports`, `/api/v1/candidates/{id}/resume`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }` (except file downloads which return raw bytes)

---

## Resume & Attachment Downloads

### GET /api/v1/candidates/{id}/resume

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Admin, RecruiterLead

Returns the candidate's uploaded resume as a file download.

**Response 200**: `FileResponse` (PDF or DOCX) with `Content-Disposition: attachment`
**Response 404**: `{ "error": "Resume not found", "status": "error" }`

---

### GET /api/v1/candidates/{candidate_id}/comments/{comment_id}/attachment

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Admin, RecruiterLead, Interviewer

Returns the file attached to a specific comment.

**Response 200**: `FileResponse` with `Content-Disposition: attachment`
**Response 404**: `{ "error": "Attachment not found", "status": "error" }`

---

## Export History

### GET /api/v1/exports/history

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Admin, RecruiterLead

Returns the export history for the authenticated user.

### Query Parameters
| Param | Type | Description |
|---|---|---|
| `page` | int | Page number (default 1) |
| `page_size` | int | Max 100 (default 20) |

### Response 200
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "export_type": "candidate_report",
        "file_path": "backend/uploads/exports/candidate_report_20260526.xlsx",
        "created_by": "recruiter@example.com",
        "created_at": "2026-05-26T10:00:00Z",
        "is_deleted": false
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

---

### DELETE /api/v1/exports/history/{id}

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Admin

Soft-deletes an export history entry (sets `is_deleted=true`).

**Response 200**: `{ "data": { "message": "Export deleted" }, "error": null, "status": "success" }`
**Response 404**: `{ "error": "Export not found" }`

---

### GET /api/v1/exports/{id}/download

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, Admin, RecruiterLead

Re-downloads a previously generated export file.

**Response 200**: `FileResponse` (XLSX or PDF)
**Response 404**: `{ "error": "Export not found or deleted" }`
**Response 410**: `{ "error": "Export file has been deleted from storage" }`
