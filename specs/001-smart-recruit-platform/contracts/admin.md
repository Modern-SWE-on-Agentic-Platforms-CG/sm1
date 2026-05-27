# API Contract: Administration & Master Data

**Base path**: `/api/v1/admin`
**Response envelope**: `{ "data": T, "error": str|null, "status": "success"|"error" }`

---

## Tower Management

### GET /api/v1/admin/towers
**Auth**: Bearer | **Roles**: Admin, BUAdmin, PracticeAdmin

Returns all towers (BU-scoped for BUAdmin/PracticeAdmin).

**Response 200**: `{ "data": { "items": [{ "id": 1, "tower_name": "Java", "is_active": true }] } }`

### POST /api/v1/admin/towers
**Auth**: Bearer | **Roles**: Admin

```json
{ "tower_name": "Java" }
```
- **409** if `tower_name` already exists: `{ "error": "TOWER ALREADY EXISTS" }`
- **Response 201**: `{ "data": { "id": 1, "tower_name": "Java", "is_active": true } }`

### DELETE /api/v1/admin/towers/{id}
**Auth**: Bearer | **Roles**: Admin
- **400** if tower has active references: `{ "error": "Cannot delete tower with active references" }`
- Soft-delete sets `is_active=false`.
- **Response 200**: `{ "data": { "message": "Tower deactivated" } }`

---

## Skill / Technology Management

### GET /api/v1/admin/skills
**Auth**: Bearer | **Roles**: Admin, BUAdmin, PracticeAdmin

**Response 200**: `{ "data": { "items": [{ "id": 1, "tech_name": "Spring Boot", "skill_group": "Backend", "tower_id": 1, "is_active": true }] } }`

### POST /api/v1/admin/skills
**Auth**: Bearer | **Roles**: Admin

```json
{ "tech_name": "Spring Boot", "skill_group": "Backend", "tower_id": 1 }
```
- **409** if `tech_name` already exists in the same tower: `{ "error": "TECHNOLOGY ALREADY EXISTS" }`
- **Response 201**: `{ "data": { "id": 5, "tech_name": "Spring Boot" } }`

### PUT /api/v1/admin/skills/{id}
**Auth**: Bearer | **Roles**: Admin

```json
{ "tech_name": "Spring Boot", "skill_group": "Backend", "tower_id": 1, "is_active": true }
```
**Response 200**: updated skill object

### DELETE /api/v1/admin/skills/{id}
**Auth**: Bearer | **Roles**: Admin — soft-delete

---

## Source Management

### GET /api/v1/admin/sources
**Auth**: Bearer | **Roles**: Admin

**Response 200**: `{ "data": { "items": [{ "id": 1, "source_name": "Naukri", "is_active": true }] } }`

### POST /api/v1/admin/sources
**Auth**: Bearer | **Roles**: Admin

```json
{ "source_name": "LinkedIn" }
```
- **409** on duplicate: `{ "error": "SOURCE ALREADY EXISTS" }`
- **Response 201**: `{ "data": { "id": 2, "source_name": "LinkedIn" } }`

### DELETE /api/v1/admin/sources/{id}
**Auth**: Bearer | **Roles**: Admin — soft-delete

---

## Vendor Management

### GET /api/v1/admin/vendors
**Auth**: Bearer | **Roles**: Admin

**Response 200**: `{ "data": { "items": [{ "id": 1, "vendor_name": "TechHire", "source_id": 2, "is_active": true }] } }`

### POST /api/v1/admin/vendors
**Auth**: Bearer | **Roles**: Admin

```json
{ "vendor_name": "TechHire", "source_id": 2 }
```
- **409** on duplicate: `{ "error": "VENDOR ALREADY EXISTS" }`
- **Response 201**: vendor object

### DELETE /api/v1/admin/vendors/{id}
**Auth**: Bearer | **Roles**: Admin — soft-delete

---

## SAP Capability & Skill Management

### GET /api/v1/admin/sap-capabilities
**Auth**: Bearer | **Roles**: Admin, BUAdmin, PracticeAdmin (SAP BU only)

**Response 200**: `{ "data": { "items": [{ "id": 1, "capability_name": "SAP ABAP" }] } }`

### POST /api/v1/admin/sap-capabilities
**Auth**: Bearer | **Roles**: Admin

```json
{ "capability_name": "SAP ABAP" }
```

### GET /api/v1/admin/sap-skills
**Auth**: Bearer | **Roles**: Admin, BUAdmin (SAP)

**Response 200**: `{ "data": { "items": [{ "id": 1, "skill_name": "Z Programming", "capability_id": 1 }] } }`

### POST /api/v1/admin/sap-skills
**Auth**: Bearer | **Roles**: Admin

```json
{ "skill_name": "Z Programming", "capability_id": 1 }
```

---

## Approver DL Management

### GET /api/v1/admin/approver-dl
**Auth**: Bearer | **Roles**: Admin

**Response 200**: `{ "data": { "items": [{ "id": 1, "tower_id": 1, "dl_email": "lead-dl@example.com", "dl_title": "Java TL", "level": "TowerLead" }] } }`

### POST /api/v1/admin/approver-dl
**Auth**: Bearer | **Roles**: Admin

```json
{ "tower_id": 1, "dl_email": "lead-dl@example.com", "dl_title": "Java TL", "level": "TowerLead" }
```

### PUT /api/v1/admin/approver-dl/{id}
**Auth**: Bearer | **Roles**: Admin

### DELETE /api/v1/admin/approver-dl/{id}
**Auth**: Bearer | **Roles**: Admin

---

## Role Comment Management

### GET /api/v1/admin/role-comments
**Auth**: Bearer | **Roles**: Admin

**Response 200**: `{ "data": { "items": [{ "id": 1, "role_id": 2, "comment_text": "Standard Recruiter note" }] } }`

### POST /api/v1/admin/role-comments
**Auth**: Bearer | **Roles**: Admin

```json
{ "role_id": 2, "comment_text": "Standard Recruiter note" }
```

### DELETE /api/v1/admin/role-comments/{id}
**Auth**: Bearer | **Roles**: Admin

---

## Trigger Job (Dev/Admin only)

### GET /api/v1/admin/trigger-job/{job_name}
**Auth**: Bearer | **Roles**: Admin

Manually triggers a scheduled background job for testing.

| `job_name` | Description |
|---|---|
| `aging-sla` | Sends aging SLA notifications |
| `interview-reminder` | Sends upcoming interview reminders |
| `feedback-reminder` | Sends pending feedback reminders |
| `export-cleanup` | Deletes exports older than 7 days |

**Response 200**: `{ "data": { "message": "Job aging-sla triggered", "entries_processed": 3 } }`
