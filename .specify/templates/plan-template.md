# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]

**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/plan-template.md` for the execution workflow.

## Summary

[Extract from feature spec: primary requirement + technical approach from research]

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.11+ (backend) · React 18+ / TypeScript 5+ (frontend)

**Primary Dependencies**: FastAPI + SQLAlchemy 2.x + Alembic (backend) · Vite + React Router (frontend)

**Storage**: PostgreSQL 14+ — database `smarthiremain001` (mandatory per constitution)

**Testing**: pytest + httpx (backend) · Vitest / React Testing Library (frontend)

**Target Platform**: Local server (Python ASGI) + browser (React SPA)

**Project Type**: Three-tier web application (React frontend / Python REST API / PostgreSQL)

**Performance Goals**: API p95 < 500 ms for standard CRUD operations

**Constraints**: All three tiers MUST align with `.specify/memory/constitution.md` Principles I–V.
No legacy stack (Angular / Spring Boot / Node.js / Express) permitted.

**Scale/Scope**: 11 user personas · 23 feature modules (see `BRD-AND-COMPLETE-DOCS.md`)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify all of the following before proceeding:

- [ ] Frontend implementation uses React (not Angular, Vue, or other frameworks)
- [ ] Backend implementation uses Python (not Node.js, Java, or other runtimes)
- [ ] Database target is PostgreSQL `smarthiremain001` (no other DB)
- [ ] API contracts (Pydantic schemas) defined before frontend development starts
- [ ] Alembic migration created for all new/changed DB entities
- [ ] No hard-coded credentials in any source file
- [ ] OWASP Top 10 self-review noted for security-sensitive endpoints

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
