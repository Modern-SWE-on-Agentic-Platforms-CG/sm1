# API Contract: Interview Bookings & To-Do

**Base path**: `/api/v1/bookings`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## POST /api/v1/bookings (Book an interview slot)

**Auth required**: Bearer token
**Roles**: Recruiter, Admin

Books a specific interviewer slot for a candidate. A UUID-based meeting link is generated
automatically. Email notification is logged to `logs/email.log`.

### Request
```json
{
  "candidate_detail_id": 1001,
  "interviewer_calendar_id": 101,
  "interview_type": "L1",
  "skill_id": 1,
  "created_by": "recruiter@smartrecruit.local"
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `candidate_detail_id` | int | yes | Must exist |
| `interviewer_calendar_id` | int | yes | Must be `Available`; set to null for direct booking |
| `interview_type` | string | yes | L1 / L2 / L3 |
| `skill_id` | int | yes | Must exist in `technology_master` |
| `is_direct_booked` | bool | no | True = bypass availability check |

### Response 201
```json
{
  "data": {
    "recruiter_calendar_id": 501,
    "candidate_detail_id": 1001,
    "candidate_name": "Rahul Sharma",
    "interviewer_calendar_id": 101,
    "panel_email": "jane.doe@smartrecruit.local",
    "panel_name": "Jane Doe",
    "interview_type": "L1",
    "interview_date": "2026-06-01",
    "from_time": "2026-06-01T10:00:00+05:30",
    "to_time": "2026-06-01T11:00:00+05:30",
    "meeting_link": "https://meet.smartrecruit.local/meeting/f7a3b2c1-...",
    "feedback_submitted": false
  },
  "error": null,
  "status": "success"
}
```

**Side effects**:
- `interviewer_calendar.slot_status` → `"Booked"`
- `candidate_detail.overall_status` → `"{interview_type} Scheduled"` (e.g., `"L1 Scheduled"`)
- Status history entry created
- Email logged: interviewer + candidate receive scheduling notification

### Response 409 — Slot already booked
```json
{
  "data": null,
  "error": "This slot is no longer available",
  "status": "error"
}
```

---

## POST /api/v1/bookings/direct (Direct booking — bypass availability)

**Auth required**: Bearer token
**Roles**: Recruiter, Admin

Books an interview without requiring an existing `interviewer_calendar` slot.

### Request
```json
{
  "candidate_detail_id": 1001,
  "panel_email": "expert@smartrecruit.local",
  "interview_type": "L2",
  "skill_id": 1,
  "from_time": "2026-06-03T14:00:00+05:30",
  "to_time": "2026-06-03T15:00:00+05:30",
  "interview_date": "2026-06-03"
}
```

### Response 201
Same shape as `POST /api/v1/bookings`, with `is_direct_booked: true` and `interviewer_calendar_id: null`.

---

## PUT /api/v1/bookings/{booking_id} (Reschedule)

**Auth required**: Bearer token
**Roles**: Recruiter, Admin

Reverts the old slot to `Available`, books a new slot, and logs updated notification emails.

### Request
```json
{
  "new_interviewer_calendar_id": 105,
  "reason": "Panel conflict"
}
```

### Response 200
```json
{
  "data": {
    "recruiter_calendar_id": 501,
    "new_slot_id": 105,
    "meeting_link": "https://meet.smartrecruit.local/meeting/new-uuid",
    "interview_date": "2026-06-02",
    "from_time": "2026-06-02T11:00:00+05:30",
    "to_time": "2026-06-02T12:00:00+05:30"
  },
  "error": null,
  "status": "success"
}
```

---

## DELETE /api/v1/bookings/{booking_id} (Cancel)

**Auth required**: Bearer token
**Roles**: Recruiter, Admin

Cancels a booking and reverts the interviewer slot to `Available`.

### Response 200
```json
{
  "data": { "message": "Booking cancelled successfully" },
  "error": null,
  "status": "success"
}
```

**Side effects**:
- `interviewer_calendar.slot_status` → `"Available"`
- Email logged: cancellation notification to interviewer + candidate

---

## GET /api/v1/bookings/today

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Admin

Returns all interviews scheduled for today.

### Response 200
```json
{
  "data": {
    "interviews": [
      {
        "recruiter_calendar_id": 501,
        "candidate_name": "Rahul Sharma",
        "panel_name": "Jane Doe",
        "panel_email": "jane.doe@smartrecruit.local",
        "interview_type": "L1",
        "from_time": "2026-06-01T10:00:00+05:30",
        "to_time": "2026-06-01T11:00:00+05:30",
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

## GET /api/v1/bookings/week

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Admin

### Query Parameters
| Param | Type | Required | Description |
|---|---|---|---|
| `week_start` | date | no | ISO 8601 date; defaults to current week Monday |

### Response 200
```json
{
  "data": {
    "week_start": "2026-06-01",
    "week_end": "2026-06-07",
    "slots": [
      {
        "recruiter_calendar_id": 501,
        "interview_date": "2026-06-01",
        "candidate_name": "Rahul Sharma",
        "panel_name": "Jane Doe",
        "interview_type": "L1",
        "from_time": "2026-06-01T10:00:00+05:30",
        "to_time": "2026-06-01T11:00:00+05:30",
        "feedback_submitted": false
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/bookings/pending-feedback

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Admin

Returns bookings where `feedback_submitted = false` and `interview_date < today`.

### Response 200
```json
{
  "data": {
    "pending": [
      {
        "recruiter_calendar_id": 499,
        "candidate_name": "Priya Menon",
        "panel_name": "John Smith",
        "panel_email": "john.smith@smartrecruit.local",
        "interview_type": "L1",
        "interview_date": "2026-05-25",
        "days_overdue": 1
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/bookings/candidates

**Auth required**: Bearer token
**Roles**: Recruiter, PMO, PracticeLead, Admin

Returns all candidates associated with the logged-in recruiter's bookings (for to-do list status update).

### Response 200
```json
{
  "data": {
    "candidates": [
      {
        "candidate_detail_id": 1001,
        "candidate_name": "Rahul Sharma",
        "overall_status": "L1 Scheduled",
        "skill_name": "Java",
        "valid_next_statuses": ["L1 Selected", "L1 Rejected", "L1 Hold"]
      }
    ]
  },
  "error": null,
  "status": "success"
}
```
