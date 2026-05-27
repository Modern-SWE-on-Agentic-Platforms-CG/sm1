# API Contract: Interviewer Slots

**Base path**: `/api/v1/slots`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## POST /api/v1/slots (Create a single available slot)

**Auth required**: Bearer token
**Roles**: Interviewer, Admin

### Request
```json
{
  "skill_id": 1,
  "slot_date": "2026-06-01",
  "from_time": "2026-06-01T10:00:00+05:30",
  "to_time": "2026-06-01T11:00:00+05:30",
  "is_weekend_drive": false
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `skill_id` | int | yes | Must exist in `technology_master` |
| `slot_date` | date | yes | ISO 8601; must not be in the past |
| `from_time` | datetime | yes | ISO 8601 with timezone |
| `to_time` | datetime | yes | Must be after `from_time` |
| `is_weekend_drive` | bool | no | Default false |

### Response 201
```json
{
  "data": {
    "interviewer_calendar_id": 101,
    "emp_id": 42,
    "skill_id": 1,
    "skill_name": "Java",
    "slot_date": "2026-06-01",
    "from_time": "2026-06-01T10:00:00+05:30",
    "to_time": "2026-06-01T11:00:00+05:30",
    "slot_status": "Available",
    "is_weekend_drive": false
  },
  "error": null,
  "status": "success"
}
```

### Response 409 — Time overlap
```json
{
  "data": null,
  "error": "Slot overlaps with an existing slot at this time",
  "status": "error"
}
```

---

## GET /api/v1/slots

**Auth required**: Bearer token
**Roles**: Interviewer (own slots), Recruiter, Admin, PMO

Fetches slots for calendar display.

### Query Parameters
| Param | Type | Required | Description |
|---|---|---|---|
| `emp_id` | int | no | Filter by interviewer; Interviewer role: defaults to own emp_id |
| `from_date` | date | no | Start of calendar range (default: current week start) |
| `to_date` | date | no | End of calendar range (default: current week end) |
| `status` | string | no | Available / Booked / Interviewed / Pending |
| `skill_id` | int | no | Filter by technology |

### Response 200
```json
{
  "data": {
    "slots": [
      {
        "interviewer_calendar_id": 101,
        "emp_id": 42,
        "emp_name": "Jane Doe",
        "skill_id": 1,
        "skill_name": "Java",
        "slot_date": "2026-06-01",
        "from_time": "2026-06-01T10:00:00+05:30",
        "to_time": "2026-06-01T11:00:00+05:30",
        "slot_status": "Available",
        "is_weekend_drive": false,
        "calendar_color": "#4CAF50"
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/slots/available

**Auth required**: Bearer token
**Roles**: Recruiter, Admin

Returns available (unbooked) slots for recruiter booking search.

### Query Parameters
| Param | Type | Required | Description |
|---|---|---|---|
| `skill_id` | int | yes | Technology filter |
| `from_date` | date | yes | Search window start |
| `to_date` | date | yes | Search window end |

### Response 200
```json
{
  "data": {
    "slots": [
      {
        "interviewer_calendar_id": 101,
        "emp_id": 42,
        "emp_name": "Jane Doe",
        "skill_name": "Java",
        "slot_date": "2026-06-01",
        "from_time": "2026-06-01T10:00:00+05:30",
        "to_time": "2026-06-01T11:00:00+05:30"
      }
    ]
  },
  "error": null,
  "status": "success"
}
```

---

## PUT /api/v1/slots/{slot_id} (Reschedule a slot)

**Auth required**: Bearer token
**Roles**: Recruiter, Interviewer (own slots), Admin

### Request
```json
{
  "from_time": "2026-06-01T14:00:00+05:30",
  "to_time": "2026-06-01T15:00:00+05:30",
  "slot_date": "2026-06-01"
}
```

### Response 200
```json
{
  "data": {
    "interviewer_calendar_id": 101,
    "from_time": "2026-06-01T14:00:00+05:30",
    "to_time": "2026-06-01T15:00:00+05:30",
    "slot_status": "Available"
  },
  "error": null,
  "status": "success"
}
```

### Response 409 — Overlap after reschedule
```json
{
  "data": null,
  "error": "Rescheduled time overlaps with an existing slot",
  "status": "error"
}
```

---

## DELETE /api/v1/slots/{slot_id}

**Auth required**: Bearer token
**Roles**: Recruiter, Interviewer (own slots), Admin

If the slot is in `Booked` status, the associated booking is also cancelled and the linked
candidate's booking record is updated.

### Response 200
```json
{
  "data": { "message": "Slot deleted successfully" },
  "error": null,
  "status": "success"
}
```

### Response 409 — Cannot delete booked slot without confirmed cancellation
```json
{
  "data": null,
  "error": "Slot is currently booked. Cancel the booking first or confirm force-delete.",
  "status": "error"
}
```

---

## POST /api/v1/slots/bulk-upload (Upload panel slot Excel)

**Auth required**: Bearer token
**Roles**: Interviewer, Admin

Accepts multipart form upload of an Excel file with slot data.

### Request
`Content-Type: multipart/form-data`
- `file`: Excel file (`.xlsx` or `.xls`); max 5 MB
- Minimum columns: `date`, `from_time`, `to_time`, `skill` (or `technology`)

### Response 200
```json
{
  "data": {
    "created": 15,
    "errors": [
      { "row": 3, "reason": "Slot overlaps with existing slot at 2026-06-01 10:00" },
      { "row": 7, "reason": "Unknown skill: 'ReactNative'" }
    ]
  },
  "error": null,
  "status": "success"
}
```
