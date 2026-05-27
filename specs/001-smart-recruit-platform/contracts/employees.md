# API Contract: Employees & Panel Registration

**Base path**: `/api/v1/employees`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## POST /api/v1/employees (Register new employee)

**Auth required**: Bearer token
**Roles**: Admin

### Request
```json
{
  "emp_name": "Jane Doe",
  "email_id": "jane.doe@smartrecruit.local",
  "password": "Welcome@2026",
  "location": "Pune",
  "grade": "C5",
  "bu": "Digital",
  "practice": "Cloud",
  "market_unit": "FIN",
  "account": "HSBC",
  "organisation": "CIS",
  "roles": ["Interviewer"],
  "technologies": [1, 3],
  "towers": ["Java", "Cloud"]
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `emp_name` | string | yes | 1–200 chars |
| `email_id` | string | yes | valid email; must be unique |
| `password` | string | yes | 8–128 chars |
| `roles` | string[] | yes | each must exist in `role_master` |
| `technologies` | int[] | no | each must be valid `technology_master.id` |
| `towers` | string[] | no | |

### Response 201
```json
{
  "data": {
    "emp_id": 42,
    "emp_name": "Jane Doe",
    "email_id": "jane.doe@smartrecruit.local",
    "bu": "Digital",
    "roles": ["Interviewer"],
    "technologies": [{"id": 1, "tech_name": "Java"}, {"id": 3, "tech_name": "Python"}]
  },
  "error": null,
  "status": "success"
}
```

### Response 400 — Duplicate email
```json
{
  "data": null,
  "error": "Employee with this email already exists",
  "status": "error"
}
```

---

## GET /api/v1/employees

**Auth required**: Bearer token
**Roles**: Admin, BUAdmin, PracticeAdmin

### Query Parameters
| Param | Type | Required | Description |
|---|---|---|---|
| `bu` | string | no | Filter by Business Unit |
| `role` | string | no | Filter by role name |
| `is_active` | bool | no | Default true |
| `page` | int | no | Default 1 |
| `page_size` | int | no | Default 20, max 100 |

### Response 200
```json
{
  "data": {
    "items": [
      {
        "emp_id": 42,
        "emp_name": "Jane Doe",
        "email_id": "jane.doe@smartrecruit.local",
        "bu": "Digital",
        "grade": "C5",
        "is_active": true,
        "roles": ["Interviewer"],
        "technologies": [{"id": 1, "tech_name": "Java"}]
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

## GET /api/v1/employees/{emp_id}

**Auth required**: Bearer token
**Roles**: Admin, BUAdmin, PracticeAdmin

### Response 200
```json
{
  "data": {
    "emp_id": 42,
    "emp_name": "Jane Doe",
    "email_id": "jane.doe@smartrecruit.local",
    "location": "Pune",
    "grade": "C5",
    "bu": "Digital",
    "practice": "Cloud",
    "is_active": true,
    "roles": ["Interviewer"],
    "technologies": [{"id": 1, "tech_name": "Java"}],
    "towers": ["Java"]
  },
  "error": null,
  "status": "success"
}
```

### Response 404
```json
{
  "data": null,
  "error": "Employee not found",
  "status": "error"
}
```

---

## PUT /api/v1/employees/{emp_id}

**Auth required**: Bearer token
**Roles**: Admin

### Request
Same fields as POST (all optional except at least one must be provided). `email_id` cannot be changed.

### Response 200
```json
{
  "data": { "emp_id": 42, "emp_name": "Jane Doe Updated", "..." : "..." },
  "error": null,
  "status": "success"
}
```

---

## DELETE /api/v1/employees/{emp_id}/skills/{technology_id}

**Auth required**: Bearer token
**Roles**: Admin

Removes a technology skill from an employee's profile.

### Response 200
```json
{
  "data": { "message": "Skill removed successfully" },
  "error": null,
  "status": "success"
}
```

---

## PUT /api/v1/employees/{emp_id}/roles

**Auth required**: Bearer token
**Roles**: Admin

Replaces the employee's role assignments.

### Request
```json
{
  "roles": ["Interviewer", "PracticeLead"]
}
```

### Response 200
```json
{
  "data": { "emp_id": 42, "roles": ["Interviewer", "PracticeLead"] },
  "error": null,
  "status": "success"
}
```
