# Current project map and source-of-truth notes

## Current integration points

- Application entry: `main.py`
- Application factory: `bootstrap/app_factory.py`
- Router registration: `bootstrap/routes.py`
- Global exception registration: `bootstrap/exceptions.py`
- Configuration: `settings.py`
- Database sessions: `infra/db.py`
- CRUD primitives: `infra/persistence/sql.py`
- Redis: `infra/rdb.py`
- Authentication dependencies: `core/auth.py`
- Common ID/time: `shared/common.py`
- API result envelope: `schema/result.py`
- Business exception: `exceptions/common.py`
- Celery application and queue registration: `celery_app.py`
- New cohesive business modules: `modules/`
- Tests: `tests/`

## Documentation drift

Resolve known stale documentation examples as follows:

| Stale example | Current source |
|---|---|
| `utils.sql.BaseCrud` | `infra.persistence.sql.BaseCRUD` |
| `utils/db.py` | `infra/db.py` |
| a single root `agent/` package | current code uses legacy `agent_v1`/`agent_v2`; put new Agent business under `modules/` |
| fixed pool size 200/100 | `infra/db.py` uses environment-configurable conservative defaults |
| unittest-only testing | inspect current tests and use the repository's working pytest/unittest-compatible style |

Treat legacy violations as compatibility constraints or technical debt, not templates. Do not copy raw exception exposure, direct SQL outside CRUD, embedded secrets, oversized service files, or inconsistent HTTP status behavior.

## Excluded convention sources

Do not derive conventions from:

- `modules/selection_agent`
- `modules/listing_agent`
- `spacex`

The user identified these directories as not belonging to the inherited project baseline. They may be read or changed only when the active request explicitly requires it; their patterns do not override this Skill.
