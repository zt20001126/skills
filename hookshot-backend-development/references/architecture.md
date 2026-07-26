# Architecture and module conventions

## Contents

- Layering
- New module layout
- Router
- Service
- CRUD and model boundaries
- Schemas and configuration
- Registration and dependency direction

## Layering

Use this dependency direction:

```text
Router -> Service -> CRUD -> Model / PostgreSQL
                    |
                    -> integrations / shared infrastructure
```

Do not let CRUD depend on services or routers. Do not let schemas import routers. Avoid circular imports and import-time network connections.

## New module layout

Create cohesive business modules:

```text
modules/<business_name>/
├── __init__.py
├── constants.py
├── router/
├── schema/
├── service/
├── crud/
├── model/
├── graph/ or workflow/   # Agent only
├── nodes/                # Agent only
├── tools/                # Agent only
├── prompts/              # Agent only
├── integrations/         # external providers
└── tasks.py              # Celery when needed
```

Create only directories required by the business. Use `snake_case` files and modules, `PascalCase` classes, `snake_case` functions and variables, and `UPPER_CASE` constants.

## Router

Limit routers to HTTP concerns:

- Declare path, method, tags, summary, dependencies, request schema, and response type.
- Obtain authenticated identity through `core.auth`.
- Obtain sessions through `infra.db.get_session`.
- Delegate immediately to a service.
- Use special Response classes only for SSE, files, webhooks, or an established contract.

Do not query the database, invoke an LLM, implement workflow transitions, manage transactions, or map large response structures in routers.

Register new routers centrally in `bootstrap/routes.py`. Keep `/api` and module prefixes consistent with neighboring current modules; do not silently change an existing public path.

## Service

Use services for:

- business validation and orchestration;
- owner/tenant authorization;
- CRUD coordination and transaction decisions;
- mapping models to response DTOs;
- calls to Agent workflows and integrations.

Keep framework-specific request objects out of domain logic unless the business requires request metadata. Break large services into focused modules instead of creating a new monolith.

## CRUD and model boundaries

Put every SQL statement in a CRUD class derived from `infra.persistence.sql.BaseCRUD`. Prefer the base methods and `FieldCondition`, `LogicalCondition`, and `OrderCondition`. Add a named method for a query whose meaning matters to the business.

Keep SQLModel table classes in `model/`. Do not use database models as public request schemas.

## Schemas and configuration

Use Pydantic v2 request/response models. Constrain lengths, ranges, collection sizes, and enums at the boundary. Use `field_validator` for normalization and cross-field validation where appropriate.

Add configuration centrally to `settings.py` with a business prefix. Parse numeric and boolean values explicitly. Update `.env.example` without secrets. Do not scatter `os.getenv()` calls through routers, services, nodes, or tools.

## Dependency direction

Reuse:

- application construction from `bootstrap`;
- authentication from `core.auth`;
- sessions from `infra.db`;
- persistence primitives from `infra.persistence.sql`;
- common IDs/time from `shared.common`;
- API envelopes from `schema.result`.

Do not create parallel clients or replacement infrastructure inside a module without a documented need.
