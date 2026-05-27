<!--
SYNC IMPACT REPORT
==================
Version change: 0.0.0 (template) → 1.0.0 (initial ratification)

Modified principles: N/A (initial creation — all principles are new)

Added sections:
  - Core Principles (5 principles)
  - Technology Stack & Constraints
  - Development Workflow & Quality Gates
  - Governance

Removed sections: N/A (initial creation)

Templates updated:
  ✅ .specify/memory/constitution.md (this file)
  ✅ .specify/templates/plan-template.md (Technical Context defaults aligned to Python/React/PostgreSQL)
  ✅ .specify/templates/spec-template.md (Constitution Check section added)
  ✅ .specify/templates/tasks-template.md (path conventions confirm frontend/backend split)

Follow-up TODOs:
  - TODO(DEPLOYMENT_TARGET): Deployment environment not yet specified (local dev confirmed;
    cloud/container target TBD). Insert production deployment config once determined.
-->

# Smart Hire (SmartRecruit) Constitution

## Core Principles

### I. Three-Tier Architecture (NON-NEGOTIABLE)

The application MUST be implemented exclusively as a three-tier system:

- **Frontend**: React (TypeScript preferred; JavaScript acceptable). All UI, routing,
  and user interaction logic lives here. No business logic may reside in the frontend
  beyond presentation concerns (formatting, validation feedback).
- **Backend**: Python. A single REST API service built with FastAPI (preferred) or Flask.
  All business logic, data processing, file handling, scheduling, and external integrations
  MUST be implemented in Python.
- **Database**: PostgreSQL, database name `smarthiremain001`, local installation.
  All persistent state MUST reside in PostgreSQL. No other databases, caches used as
  primary stores, or embedded databases are permitted.

Any feature previously implemented using Angular, Spring Boot, Node.js, Express, or any
other technology MUST be re-implemented within this stack before it can be considered
complete. Migration from the legacy stack is not optional.

### II. API-First Backend Design

The Python backend exposes all functionality exclusively via a versioned REST API
(`/api/v1/...`). Rules:

- The frontend MUST NOT access the database directly under any circumstances.
- Every backend capability is reachable through a documented HTTP endpoint.
- All API responses MUST use a consistent JSON envelope:
  `{ "data": ..., "error": null | "message", "status": "success" | "error" }`.
- API contracts (request/response schemas) MUST be defined before implementation begins.
  Use Pydantic models for schema validation on the Python side.
- CORS MUST be explicitly configured; the backend MUST NOT use wildcard origins in
  production.

### III. Database-First Data Modeling

All persistent data structures MUST be defined as PostgreSQL schema migrations before
application code references them. Rules:

- Use Alembic (with SQLAlchemy) as the migration framework. No raw DDL executed
  outside a migration file.
- The ORM (SQLAlchemy) is the only approved mechanism for database access from Python.
  Raw SQL strings inside application code are prohibited except inside Alembic migration
  scripts.
- The canonical schema lives in `backend/migrations/`. Every new entity or schema
  change requires a new migration file — never mutate existing migration files.
- Database credentials MUST be supplied via environment variables. They MUST NOT be
  hard-coded in source files. Approved variable names: `DB_HOST`, `DB_PORT`, `DB_NAME`,
  `DB_USER`, `DB_PASSWORD`.
  - Local development defaults: `DB_NAME=smarthiremain001`, `DB_PASSWORD=niit@123`.

### IV. Security by Design

Security controls are non-negotiable and MUST be implemented from the first feature:

- Authentication MUST use JWT (JSON Web Tokens). The backend issues and validates tokens;
  the frontend stores them only in `httpOnly` cookies or, at minimum, in-memory
  (never in `localStorage` in production builds).
- Authorization MUST be role-based (RBAC). Every API endpoint MUST declare which roles
  may access it; the backend enforces this via middleware/dependency injection.
- All user-supplied input MUST be validated at the API boundary using Pydantic before
  reaching business logic or the database. SQL injection is prevented by ORM usage
  (Principle III).
- Passwords and secrets MUST NOT appear in source control. Use `.env` files (git-ignored)
  or an environment variable manager.
- OWASP Top 10 compliance is a gate for every feature. Any code review that identifies
  an OWASP violation MUST block merging until resolved.

### V. Simplicity & Observability

Complexity must be justified; the default choice is always the simpler, more
understandable approach:

- YAGNI: Do not implement capabilities not required by the current specification.
  Abstractions added "for future use" are prohibited.
- The Python backend MUST emit structured JSON logs for every request (method, path,
  status, duration) and every error (type, message, stack trace). Use Python's standard
  `logging` module configured with a JSON formatter.
- Frontend errors that reach the user (unhandled exceptions, failed API calls) MUST be
  surfaced with a user-readable message and logged to the browser console in development.
- Environment parity: development, test, and production environments MUST use the same
  PostgreSQL version and the same Alembic migrations. "Works on my machine" is not
  acceptable.

## Technology Stack & Constraints

### Approved Technologies

| Layer | Technology | Version Constraint |
|-------|------------|--------------------|
| Frontend | React | 18+ |
| Frontend language | TypeScript | 5+ (JavaScript acceptable) |
| Frontend build | Vite or Create React App | Latest stable |
| Backend | Python | 3.11+ |
| Backend framework | FastAPI (preferred) or Flask | Latest stable |
| Backend ORM | SQLAlchemy | 2.x |
| Backend migrations | Alembic | Latest stable |
| Backend auth | python-jose / PyJWT | Latest stable |
| Database | PostgreSQL | 14+ |
| Database name | `smarthiremain001` | Fixed (mandatory) |

### Prohibited Technologies (in this project)

- Angular, Vue, or any non-React UI framework
- Spring Boot, Java, Node.js, Express, or any non-Python backend runtime
- MongoDB, MySQL, SQLite, Redis (as primary store), or any non-PostgreSQL database
- AWS S3, AWS SES, or cloud-specific services unless the feature specification
  explicitly mandates them and a local/mock equivalent is provided for development

### Repository Structure

```
smarthire/
├── frontend/          # React application
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── services/  # API client layer
│   │   └── hooks/
│   └── tests/
├── backend/           # Python API service
│   ├── app/
│   │   ├── api/       # Route handlers (versioned: api/v1/)
│   │   ├── models/    # SQLAlchemy ORM models
│   │   ├── schemas/   # Pydantic request/response schemas
│   │   ├── services/  # Business logic
│   │   └── core/      # Auth, config, middleware
│   ├── migrations/    # Alembic migration files
│   └── tests/
├── .env.example       # Template for required environment variables
└── docker-compose.yml # Optional: local development orchestration
```

### Non-Functional Requirements

- API response time MUST be under 500 ms (p95) for standard CRUD operations.
- The system MUST support the 11 user personas defined in the BRD (`BRD-AND-COMPLETE-DOCS.md §1`).
- All 23 feature modules described in `BRD-AND-COMPLETE-DOCS.md §3` MUST be implemented.
- File uploads (Excel, PDF) MUST be handled server-side in Python; files MUST be stored
  in the local filesystem or PostgreSQL `BYTEA` column (not S3) unless explicitly changed
  by a future constitution amendment.

## Development Workflow & Quality Gates

### Feature Development Cycle

1. A feature specification (`spec.md`) MUST exist and be approved before implementation.
2. An implementation plan (`plan.md`) MUST document the API contracts and data model
   changes before any code is written.
3. Alembic migration files MUST be created and reviewed before the ORM models that
   depend on them.
4. Frontend development MUST NOT begin until the corresponding API endpoint contract
   is defined (even if the implementation is a stub).
5. All three layers (frontend component, backend route, database migration) for a feature
   MUST be delivered together. Partial deployments that leave the system in an
   inconsistent state are prohibited.

### Code Review Gates

Every pull request MUST satisfy all of the following before merge:

- [ ] No placeholder bracket tokens (`[ALL_CAPS]`) in production code or config.
- [ ] No hard-coded credentials, secrets, or environment-specific values.
- [ ] All new API endpoints covered by at least one integration test.
- [ ] OWASP Top 10 self-review checklist completed by the author.
- [ ] Alembic migration for any schema change is included.
- [ ] Frontend service layer (`src/services/`) used for all API calls
  (no `fetch`/`axios` directly in components).

### Environment Configuration

All environment variables are documented in `.env.example`. The following variables are
MANDATORY and MUST be set before the application starts:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smarthiremain001
DB_USER=<postgres_user>
DB_PASSWORD=niit@123
SECRET_KEY=<jwt_secret_min_32_chars>
FRONTEND_ORIGIN=http://localhost:5173
```

## Governance

This constitution supersedes all prior conventions, legacy technology choices, and
informal practices. It applies to every contributor and every feature.

**Amendment Procedure**:
- MAJOR version bump: removal or redefinition of a Core Principle, or prohibition of
  an approved technology. Requires explicit written rationale and a migration plan.
- MINOR version bump: addition of a new principle, approved technology, or mandatory
  section. Requires rationale.
- PATCH version bump: clarifications, wording fixes, or non-semantic refinements.

**Compliance**:
- All PRs are reviewed against this constitution. A PR that violates a NON-NEGOTIABLE
  principle MUST be blocked regardless of other review outcomes.
- Constitution compliance is part of the Definition of Done for every task.
- Runtime guidance is in `BRD-AND-COMPLETE-DOCS.md` for feature detail and in
  `specs/` for feature-specific contracts.

**Versioning Policy**: Semantic versioning (`MAJOR.MINOR.PATCH`) as defined above.

**Version**: 1.0.0 | **Ratified**: 2026-05-26 | **Last Amended**: 2026-05-26
