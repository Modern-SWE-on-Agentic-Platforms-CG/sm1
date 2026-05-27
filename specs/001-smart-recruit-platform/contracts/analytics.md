# API Contract: Recruitment Analytics & Reports

**Base path**: `/api/v1/reports`, `/api/v1/l2`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }` (Excel exports return `StreamingResponse`)

---

## Common Filter Parameters (applicable to most report endpoints)

| Param | Type | Description |
|---|---|---|
| `from_date` | date | Start of date range (YYYY-MM-DD) |
| `to_date` | date | End of date range (YYYY-MM-DD) |
| `technology_id` | int | Filter by skill/technology |
| `source` | string | Filter by source name |
| `bu_id` | int | Filter by business unit |
| `vendor` | string | Filter by vendor name |

---

## Pie Charts

### GET /api/v1/reports/pie-chart

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, Recruiter, PMO

Returns outer pie chart data (select/reject counts by skill or source).

### Response 200
```json
{
  "data": {
    "labels": ["Java", "Python", "SAP"],
    "values": [45, 32, 28],
    "total": 105
  },
  "error": null,
  "status": "success"
}
```

---

## Line Charts

### GET /api/v1/reports/line-chart

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, Recruiter, PMO

### Query Parameters
| Param | Type | Values |
|---|---|---|
| `view` | string | `monthly` / `yearly` |
| `year` | int | e.g. 2026 |

### Response 200
```json
{
  "data": {
    "labels": ["Jan", "Feb", "Mar"],
    "datasets": [
      { "label": "Selected", "data": [12, 8, 15] },
      { "label": "Rejected", "data": [5, 3, 7] }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## Trend Chart

### GET /api/v1/reports/trend-chart

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, Recruiter, PMO

### Response 200
```json
{
  "data": {
    "labels": ["2026-01", "2026-02"],
    "datasets": [
      { "label": "Naukri", "data": [10, 12] },
      { "label": "LinkedIn", "data": [6, 8] }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## Interview Data

### GET /api/v1/reports/interview-data

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, Recruiter, PMO

Returns tabular interview data.

### Response 200
```json
{
  "data": {
    "items": [
      {
        "candidate_name": "John Doe",
        "skill": "Java",
        "interview_type": "L1",
        "interview_date": "2026-05-01",
        "panel_email": "interviewer@example.com",
        "outcome": "L1 Selected"
      }
    ],
    "total": 100,
    "page": 1,
    "page_size": 20
  },
  "error": null,
  "status": "success"
}
```

---

## Status Insights

### GET /api/v1/reports/status-insights

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, Recruiter, PMO

### Response 200
```json
{
  "data": {
    "labels": ["Profile Received", "L1 Scheduled", "Offered"],
    "values": [120, 80, 25]
  },
  "error": null,
  "status": "success"
}
```

---

## Channel Insights

### GET /api/v1/reports/channel-insights

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, Recruiter, PMO

### Response 200
```json
{
  "data": {
    "channels": [
      { "source": "Naukri", "total": 80, "selected": 30, "rejected": 40, "select_rate": 37.5 }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## ARC Deviation Report

### GET /api/v1/reports/arc-deviation

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, NALead

### Response 200
```json
{
  "data": {
    "items": [
      {
        "candidate_name": "Jane Smith",
        "skill": "SAP ABAP",
        "current_ctc": "12.0",
        "offer_ctc": "18.5",
        "threshold_percent": 15,
        "deviation_percent": 54.2
      }
    ],
    "total": 5
  },
  "error": null,
  "status": "success"
}
```

---

## Rejection Report

### GET /api/v1/reports/rejection

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, Recruiter, PMO

### Response 200
```json
{
  "data": {
    "by_stage": [{ "stage": "L1 Rejected", "count": 45 }],
    "by_technology": [{ "tech": "Java", "count": 20 }],
    "by_source": [{ "source": "Naukri", "count": 30 }]
  },
  "error": null,
  "status": "success"
}
```

---

## Offer Approve Candidates

### GET /api/v1/reports/offer-approve-candidates

**Auth**: Bearer | **Roles**: Admin, PMO

Returns candidates currently in BU/NA approval stage.

### Response 200
```json
{
  "data": {
    "items": [
      {
        "candidate_detail_id": 42,
        "candidate_name": "John Doe",
        "skill": "Java",
        "overall_status": "BU Approval Pending",
        "offer_ctc": "17.0",
        "workflow_level": "SLBULead"
      }
    ],
    "total": 10
  },
  "error": null,
  "status": "success"
}
```

---

## Feedback Form Report

### GET /api/v1/reports/feedback-form-report

**Auth**: Bearer | **Roles**: Admin, RecruiterLead

### Query Parameters: `from_date`, `to_date`, `technology_id`

### Response 200
```json
{
  "data": {
    "items": [
      {
        "candidate_name": "John Doe",
        "technology": "Java",
        "interview_date": "2026-05-01",
        "overall_rating": "Select",
        "submitted_by": "panel@example.com"
      }
    ],
    "total": 20
  },
  "error": null,
  "status": "success"
}
```

---

## Excel Export

### GET /api/v1/reports/export

**Auth**: Bearer | **Roles**: Admin, RecruiterLead, Recruiter, PMO

Returns a `StreamingResponse` XLSX file with all filtered interview/candidate data.

**Response 200**: `StreamingResponse` with `Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`

---

## Utility Endpoints

### GET /api/v1/reports/years

Returns years for which data is available.

**Response 200**: `{ "data": { "years": [2025, 2026] } }`

### GET /api/v1/reports/date-range

Returns earliest and latest record dates.

**Response 200**: `{ "data": { "min_date": "2025-01-01", "max_date": "2026-05-26" } }`

---

## L2 Report Endpoints

### POST /api/v1/l2/report

**Auth**: Bearer | **Roles**: PMO, RecruiterLead, Admin

Returns candidates at L2 Selected stage with days-since-L2.

### Request
```json
{ "from_date": "2026-01-01", "to_date": "2026-05-26", "bu_id": null }
```

### Response 200
```json
{
  "data": {
    "items": [
      {
        "candidate_detail_id": 42,
        "candidate_name": "Jane Smith",
        "skill": "Java",
        "l2_select_date": "2026-03-01",
        "days_since_l2": 86,
        "baseline": "30 days",
        "actionable": "Offer pending"
      }
    ],
    "total": 5
  },
  "error": null,
  "status": "success"
}
```

### POST /api/v1/l2/aging

Returns only candidates exceeding SLA threshold.

### Request
```json
{ "sla_threshold_days": 30 }
```

### Response 200: Same structure as `/l2/report` filtered to over-SLA candidates.

### POST /api/v1/l2/doj-status

Returns DOJ tracking data.

### GET /api/v1/l2/export

Returns L2 report as StreamingResponse XLSX.

### POST /api/v1/l2/upload

**Roles**: PMO, Admin

Upload an Excel file to update L2 select data.

**Request**: `multipart/form-data` with `file` field (`.xlsx`)

**Response 201**: `{ "data": { "created": 10, "updated": 3, "errors": [] } }`
