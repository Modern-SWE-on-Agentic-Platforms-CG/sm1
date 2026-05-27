# API Contract: Joining Bonus Management

**Base path**: `/api/v1/joining-bonus`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## GET /api/v1/joining-bonus

**Auth required**: Bearer token
**Roles**: RecruiterLead, Admin

Returns all candidates with a joining bonus commitment.

### Query Parameters
| Param | Type | Description |
|---|---|---|
| `status` | string | Filter by JB status |
| `page` | int | Page number (default 1) |
| `page_size` | int | Max 100 (default 20) |

### Response 200
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "candidate_detail_id": 42,
        "candidate_name": "Jane Smith",
        "bonus_amount": 50000,
        "status": "Pending",
        "dl_email": "hrbp@example.com",
        "updated_by": "recruiter@example.com",
        "updated_at": "2026-05-26T10:00:00Z"
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

## GET /api/v1/joining-bonus/bu

**Auth required**: Bearer token
**Roles**: BUAdmin, PracticeAdmin, RecruiterLead, Admin

Returns joining bonus candidates filtered by BU.

### Query Parameters
| Param | Type | Description |
|---|---|---|
| `bu` | string | Business unit name |
| `page` | int | Page number (default 1) |
| `page_size` | int | Max 100 |

### Response 200
```json
{
  "data": {
    "items": [ /* same as above */ ],
    "total": 5,
    "page": 1,
    "page_size": 20
  },
  "error": null,
  "status": "success"
}
```

---

## PUT /api/v1/joining-bonus/{id}

**Auth required**: Bearer token
**Roles**: RecruiterLead, Admin, BUAdmin

Update joining bonus status for a candidate.

### Request
```json
{
  "status": "Paid",
  "dl_email": "hrbp@example.com"
}
```

| Field | Type | Required | Values |
|---|---|---|---|
| `status` | string | yes | `Pending` / `Approved` / `Paid` / `Cancelled` |
| `dl_email` | string | no | Distribution list email |

### Response 200
```json
{
  "data": { "id": 1, "status": "Paid", "updated_by": "recruiter@example.com" },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/joining-bonus/dl-options

**Auth required**: Bearer token
**Roles**: RecruiterLead, Admin

Returns available distribution list email options for JB notifications.

### Response 200
```json
{
  "data": {
    "items": [
      { "dl_email": "hrbp-java@example.com", "dl_title": "HRBP Java Tower" }
    ]
  },
  "error": null,
  "status": "success"
}
```
