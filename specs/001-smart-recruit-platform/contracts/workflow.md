# API Contract: Offer Approval Workflow

**Base path**: `/api/v1/workflow`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## GET /api/v1/workflow/candidates

**Auth required**: Bearer token
**Roles**: TowerLead, SLBULead, NALead, RecruiterLead, Admin

Returns candidates at the current approver's level in the workflow queue.

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
        "workflow_id": 1,
        "candidate_detail_id": 42,
        "candidate_name": "John Doe",
        "skill": "Java",
        "current_ctc": "12.5",
        "exp_ctc": "18.0",
        "offer_ctc": "17.0",
        "current_level": "TowerLead",
        "status": "Pending",
        "arc_deviation": false
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

## POST /api/v1/workflow/{workflow_id}/action

**Auth required**: Bearer token
**Roles**: TowerLead, SLBULead, NALead, RecruiterLead, Admin

Approve or reject a candidate at the current workflow level.

### Request
```json
{
  "action": "Approved",
  "comment": "Strong candidate, approved for offer"
}
```

| Field | Type | Required | Values |
|---|---|---|---|
| `action` | string | yes | `Approved` / `Rejected` / `Comment` |
| `comment` | string | no | Free text |

### Response 200
```json
{
  "data": { "workflow_id": 1, "status": "Approved", "next_level": "SLBULead" },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/workflow/{workflow_id}/comments

**Auth required**: Bearer token
**Roles**: TowerLead, SLBULead, NALead, RecruiterLead, Admin, Recruiter

Returns the full comment/action history for a workflow entry.

### Response 200
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "commenter_email": "recruiter@example.com",
        "comment_text": "Submitting for approval",
        "action": "Comment",
        "created_at": "2026-05-26T10:00:00Z"
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## POST /api/v1/workflow/{workflow_id}/comments

**Auth required**: Bearer token
**Roles**: TowerLead, SLBULead, NALead, RecruiterLead, Admin, Recruiter

Add a comment to a workflow entry.

### Request
```json
{ "comment_text": "Awaiting CTC approval", "action": "Comment" }
```

### Response 201
```json
{
  "data": { "id": 2, "comment_text": "Awaiting CTC approval" },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/workflow/ctc-history/{candidate_id}

**Auth required**: Bearer token
**Roles**: TowerLead, SLBULead, NALead, RecruiterLead, Admin

Returns the CTC change history for a candidate.

### Response 200
```json
{
  "data": {
    "items": [
      { "id": 1, "ctc_value": "15.0", "changed_by": "recruiter@example.com", "changed_at": "2026-05-26T09:00:00Z" }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/workflow/threshold

**Auth required**: Bearer token
**Roles**: Admin, TowerLead, SLBULead, NALead, RecruiterLead

Returns ARC threshold configuration used for deviation detection.

### Response 200
```json
{
  "data": { "arc_threshold_percent": 15.0, "description": "Max CTC deviation before ARC flag" },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/workflow/approver-dl

**Auth required**: Bearer token
**Roles**: Admin

Returns all approver distribution list mappings.

### Response 200
```json
{
  "data": {
    "items": [
      { "id": 1, "tower_id": 2, "dl_email": "towerlead-dl@example.com", "dl_title": "Java Tower Lead", "level": "TowerLead" }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## PUT /api/v1/workflow/approver-dl

**Auth required**: Bearer token
**Roles**: Admin

Update an approver DL mapping.

### Request
```json
{ "id": 1, "dl_email": "new-dl@example.com", "dl_title": "Updated Title" }
```

### Response 200
```json
{
  "data": { "id": 1, "dl_email": "new-dl@example.com" },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/workflow/possible-status

**Auth required**: Bearer token
**Roles**: Recruiter, Admin, RecruiterLead

Returns possible workflow status transitions for the current user's role.

### Response 200
```json
{
  "data": { "statuses": ["Pending", "Approved", "Rejected"] },
  "error": null,
  "status": "success"
}
```
