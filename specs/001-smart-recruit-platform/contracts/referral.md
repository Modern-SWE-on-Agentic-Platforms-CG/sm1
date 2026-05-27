# API Contract: Employee Referral Portal

**Base path**: `/api/v1/referral`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## GET /api/v1/referral/form-headers (PUBLIC)

No authentication required.

Returns the master data needed to populate the referral submission form.

### Response 200
```json
{
  "data": {
    "technologies": [{ "id": 1, "tech_name": "Java" }],
    "certifications": [{ "id": 1, "cert_name": "AWS Certified" }],
    "notice_periods": ["Immediate", "15 Days", "30 Days", "60 Days", "90 Days"],
    "locations": ["Bangalore", "Hyderabad", "Mumbai", "Delhi", "Chennai"]
  },
  "error": null,
  "status": "success"
}
```

---

## POST /api/v1/referral/check-employee (PUBLIC)

No authentication required.

Verifies that the referrer is a registered employee.

### Request
```json
{ "emp_email": "employee@example.com" }
```

### Response 200
```json
{
  "data": { "is_registered": true, "emp_name": "John Doe", "emp_id": 42 },
  "error": null,
  "status": "success"
}
```

**Response 200** (not registered):
```json
{
  "data": { "is_registered": false },
  "error": null,
  "status": "success"
}
```

---

## POST /api/v1/referral (PUBLIC with employee check)

No JWT required but referee must pass `/check-employee` first.

Submits a new employee referral. File uploads via `multipart/form-data`.

### Request (multipart/form-data)
| Field | Type | Required |
|---|---|---|
| `referee_emp_email` | string | yes |
| `candidate_name` | string | yes |
| `candidate_email` | string | yes |
| `candidate_phone` | string | no |
| `skill_ids` | list[int] | yes |
| `certifications` | string | no |
| `notice_period` | string | yes |
| `location` | string | yes |
| `resume` | file | yes (max 5 MB) |
| `photo` | file | no (max 2 MB) |

### Response 201
```json
{
  "data": {
    "referral_id": 7,
    "candidate_name": "Jane Doe",
    "status": "Pending",
    "submitted_at": "2026-05-26T10:00:00Z"
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/referral

**Auth**: Bearer | **Roles**: Admin, ReferralSPOC

Returns all referrals with optional filters.

### Query Parameters
| Param | Type | Description |
|---|---|---|
| `status` | string | Filter by status |
| `technology_id` | int | Filter by skill |
| `page` | int | Page (default 1) |
| `page_size` | int | Max 100 (default 20) |

### Response 200
```json
{
  "data": {
    "items": [
      {
        "id": 7,
        "referee_emp_id": 42,
        "candidate_name": "Jane Doe",
        "candidate_email": "jane@example.com",
        "notice_period": "30 Days",
        "location": "Bangalore",
        "status": "Pending",
        "submitted_at": "2026-05-26T10:00:00Z"
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

## GET /api/v1/referral/{id}

**Auth**: Bearer | **Roles**: Admin, ReferralSPOC

Returns full referral profile.

### Response 200: full referral object including skills list.

---

## PUT /api/v1/referral/{id}

**Auth**: Bearer | **Roles**: Admin, ReferralSPOC

Update referral details.

---

## PUT /api/v1/referral/{id}/status

**Auth**: Bearer | **Roles**: Admin, ReferralSPOC

Update referral status.

### Request
```json
{ "status": "Shortlisted" }
```

| `status` values |
|---|
| `Pending`, `Shortlisted`, `Selected`, `Rejected`, `On Hold` |

### Response 200
```json
{
  "data": { "id": 7, "status": "Shortlisted" },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/referral/{id}/resume

**Auth**: Bearer | **Roles**: Admin, ReferralSPOC

Returns the referral candidate's resume as a file download.

**Response 200**: `FileResponse`
