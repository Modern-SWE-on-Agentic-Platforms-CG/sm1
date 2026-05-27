# API Contract: Supply / Demand / Bench Visibility

**Base path**: `/api/v1/supply`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }` (Excel uploads return JSON summary)

---

## POST /api/v1/supply/demand/upload

**Auth**: Bearer | **Roles**: PMO, Admin

Upload a demand Excel file. Creates a new `demand_batch` and inserts `demand_data` rows.

**Request**: `multipart/form-data` with `file` field (`.xlsx`, max 5 MB)

### Response 201
```json
{
  "data": {
    "batch_id": 5,
    "created": 120,
    "errors": [{ "row": 3, "reason": "Missing JR ID" }]
  },
  "error": null,
  "status": "success"
}
```

---

## POST /api/v1/supply/bench/upload

**Auth**: Bearer | **Roles**: PMO, Admin

Upload a bench Excel file. Creates a new `bench_batch` and inserts `bench_data` rows.

**Request**: `multipart/form-data` with `file` field (`.xlsx`, max 5 MB)

### Response 201
```json
{
  "data": {
    "batch_id": 3,
    "created": 85,
    "errors": []
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/supply/demand

**Auth**: Bearer | **Roles**: PMO, RecruiterLead, Admin, TowerLead, SLBULead, NALead

Returns demand data with filters.

### Query Parameters
| Param | Type | Description |
|---|---|---|
| `skill` | string | Filter by skill name |
| `grade` | string | Filter by grade |
| `account` | string | Filter by account name |
| `bu` | string | Filter by business unit |
| `demand_status` | string | Filter by status (Open/Closed/In Progress) |
| `page` | int | Page number (default 1) |
| `page_size` | int | Max 100 (default 20) |

### Response 200
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "jr_id": "JR-2026-001",
        "skill": "Java",
        "grade": "Senior",
        "account": "ACME Corp",
        "bu": "Digital",
        "demand_status": "Open",
        "demand_date": "2026-05-01",
        "sourced_count": 5,
        "pipeline_count": 2,
        "batch_id": 5
      }
    ],
    "total": 50,
    "page": 1,
    "page_size": 20
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/supply/bench

**Auth**: Bearer | **Roles**: PMO, RecruiterLead, Admin, TowerLead, SLBULead, NALead

Returns bench data with filters.

### Query Parameters
| Param | Type | Description |
|---|---|---|
| `skill` | string | Filter by skill |
| `grade` | string | Filter by grade |
| `location` | string | Filter by location |
| `bu` | string | Filter by BU |
| `bench_status` | string | Filter by bench status |
| `page` | int | Page number |
| `page_size` | int | Max 100 |

### Response 200
```json
{
  "data": {
    "items": [
      {
        "id": 1,
        "emp_name": "John Smith",
        "emp_email": "john@example.com",
        "skill": "Java",
        "grade": "Senior",
        "location": "Bangalore",
        "bu": "Digital",
        "bench_status": "Available",
        "batch_id": 3
      }
    ],
    "total": 30,
    "page": 1,
    "page_size": 20
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/supply/demand/history

**Auth**: Bearer | **Roles**: PMO, Admin

Returns all demand batch uploads with metadata.

### Response 200
```json
{
  "data": {
    "items": [
      { "batch_id": 5, "uploaded_by": "pmo@example.com", "uploaded_at": "2026-05-26T09:00:00Z", "row_count": 120 }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/supply/bench/history

**Auth**: Bearer | **Roles**: PMO, Admin

Same structure as demand history for bench batches.

---

## GET /api/v1/supply/filter-options

**Auth**: Bearer | **Roles**: PMO, RecruiterLead, Admin, TowerLead

Returns available filter values for the supply dashboard.

### Response 200
```json
{
  "data": {
    "locations": ["Bangalore", "Mumbai", "Hyderabad"],
    "bench_statuses": ["Available", "On Project", "Shadowing"],
    "grades": ["Analyst", "Consultant", "Senior Consultant", "Manager"],
    "bus": ["Digital", "Cloud", "SAP"]
  },
  "error": null,
  "status": "success"
}
```
