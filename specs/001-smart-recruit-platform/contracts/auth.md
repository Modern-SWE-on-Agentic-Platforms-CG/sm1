# API Contract: Authentication

**Base path**: `/api/v1/auth`
**Response envelope**: All responses use `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## POST /api/v1/auth/login

**Auth required**: None
**Roles**: Public

### Request
```json
{
  "email": "admin@smartrecruit.local",
  "password": "Admin@123"
}
```

| Field | Type | Required | Validation |
|---|---|---|---|
| `email` | string | yes | valid email format |
| `password` | string | yes | 1–128 chars |

### Response 200
```json
{
  "data": {
    "access_token": "<jwt>",
    "token_type": "bearer",
    "employee": {
      "emp_id": 1,
      "emp_name": "System Admin",
      "email_id": "admin@smartrecruit.local",
      "bu": "Corporate",
      "roles": ["Admin"]
    }
  },
  "error": null,
  "status": "success"
}
```

Cookie set: `access_token=<jwt>; HttpOnly; SameSite=Lax; Path=/; Max-Age=28800`

### Response 401
```json
{
  "data": null,
  "error": "Invalid email or password",
  "status": "error"
}
```

---

## GET /api/v1/auth/me

**Auth required**: Bearer token (or httpOnly cookie)
**Roles**: Any authenticated

### Response 200
```json
{
  "data": {
    "emp_id": 1,
    "emp_name": "System Admin",
    "email_id": "admin@smartrecruit.local",
    "bu": "Corporate",
    "roles": ["Admin"],
    "active_role": "Admin"
  },
  "error": null,
  "status": "success"
}
```

### Response 401
```json
{
  "data": null,
  "error": "Not authenticated",
  "status": "error"
}
```

---

## POST /api/v1/auth/logout

**Auth required**: Bearer token
**Roles**: Any authenticated

### Response 200
```json
{
  "data": { "message": "Logged out successfully" },
  "error": null,
  "status": "success"
}
```

Clears `access_token` httpOnly cookie.

---

## GET /api/v1/panel/roles?email={email}

**Auth required**: Bearer token
**Roles**: Any authenticated

Fetches available roles for a given employee (used in SelectRole page).

### Query Parameters
| Param | Type | Required |
|---|---|---|
| `email` | string | yes |

### Response 200
```json
{
  "data": {
    "roles": ["Recruiter", "PracticeLead"],
    "bu_name": "Digital"
  },
  "error": null,
  "status": "success"
}
```

---

## GET /api/v1/panel/bu?email={email}

**Auth required**: Bearer token
**Roles**: Any authenticated

Fetches the Business Unit for a given employee (used for home-route determination).

### Response 200
```json
{
  "data": { "bu_name": "SAP" },
  "error": null,
  "status": "success"
}
```
