# API Contract: Feedback Collection & PDF Generation

**Base path**: `/api/v1/feedback`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## GET /api/v1/feedback/template/{booking_id}

**Auth required**: Bearer token
**Roles**: Interviewer

Returns the blank feedback form template for the booking's technology.

### Response 200
```json
{
  "data": {
    "template_id": 1,
    "form_title": "Java Backend Feedback",
    "tech_name": "Java",
    "sections": [
      {
        "section_name": "Technical Skills",
        "parameters": [
          { "id": 1, "parameter_name": "Core Java", "max_score": 10, "param_order": 1 }
        ]
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## POST /api/v1/feedback/{booking_id}

**Auth required**: Bearer token
**Roles**: Interviewer

Submit feedback for a booking. Generates PDF in `backend/uploads/exports/`.

### Request
```json
{
  "parameter_scores": { "1": 8, "2": 7 },
  "overall_rating": "Select",
  "overall_remarks": "Strong candidate with good Java fundamentals"
}
```

| Field | Type | Required | Values |
|---|---|---|---|
| `parameter_scores` | object | yes | `{ param_id: score }` |
| `overall_rating` | string | yes | `Select` / `Hold` / `Reject` |
| `overall_remarks` | string | no | Free text |

### Response 201
```json
{
  "data": {
    "feedback_id": 42,
    "pdf_path": "backend/uploads/exports/feedback_42.pdf",
    "overall_rating": "Select"
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/feedback/{booking_id}/pdf

**Auth required**: Bearer token
**Roles**: Recruiter, Admin, PMO

Returns the generated feedback PDF as a file download.

### Response 200
File download (`application/pdf`)

---

## GET /api/v1/feedback/templates

**Auth required**: Bearer token
**Roles**: Admin

Returns all feedback form templates.

### Response 200
```json
{
  "data": [
    { "id": 1, "form_title": "Java Backend Feedback", "tech_name": "Java", "practice": "Digital", "is_active": true }
  ],
  "error": null,
  "status": "success"
}
```

---

## POST /api/v1/feedback/templates

**Auth required**: Bearer token
**Roles**: Admin

Create a new feedback form template.

### Request
```json
{
  "tech_name": "Python",
  "practice": "Digital",
  "form_title": "Python Backend Feedback",
  "parameters": [
    { "section_name": "Core Skills", "parameter_name": "Python OOP", "max_score": 10, "param_order": 1 }
  ]
}
```

### Response 201
```json
{
  "data": { "id": 2, "form_title": "Python Backend Feedback" },
  "error": null,
  "status": "success"
}
```
