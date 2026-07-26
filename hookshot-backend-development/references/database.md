# Database, transactions, and state

## Contents

- Sessions and CRUD
- Models
- Transactions
- Ownership and soft deletion
- Redis and durable state
- Migration expectations

## Sessions and CRUD

Use `Session = Depends(get_session)` in FastAPI. Use `with get_db() as session:` in synchronous background code. Ensure manually created sessions close on every path.

Prohibit `select`, `update`, `delete`, `session.exec`, `session.execute`, and `session.query` outside CRUD/persistence modules. Complex joins, aggregates, locks, and subqueries remain valid inside a named CRUD method.

Derive CRUD classes from:

```python
from infra.persistence.sql import BaseCRUD

class TaskCRUD(BaseCRUD[Task]):
    model_cls = Task
```

## Models

Use SQLModel table models and explicit table names. Use:

```python
from shared.common import beijing_time, get_snowflake_id
```

Use Snowflake IDs for application primary keys. Use Beijing time defaults for `created_at` and `updated_at`. Use `BigInteger` columns where database compatibility requires them.

Add `is_del` to entities that follow soft deletion. Add sizes, nullability, indexes, uniqueness, and foreign-key behavior deliberately. Replace magic status strings/numbers with constants or enums.

## Transactions

Define a service-level transaction boundary for multi-write operations:

1. Call CRUD writes with `commit=False`.
2. Commit once after all required writes succeed.
3. Roll back on failure.
4. Do not mix auto-committing CRUD calls with later dependent writes.

Use row locking or an atomic conditional update for concurrency-sensitive balances, points, task claiming, and state transitions. Do not implement read-check-write without protection when concurrent requests can race.

Make Celery tasks idempotent because late acknowledgement allows duplicate delivery. Store a business idempotency key or use an atomic state transition.

## Ownership and soft deletion

Include `user_id`, `distributor_id`, or another tenant key in CRUD lookup conditions when accessing user-owned resources. Do not load by public ID and authorize after mutation. Apply `is_del == False` consistently unless an administrative recovery path explicitly includes deleted data.

## Redis and durable state

Use shared Redis clients from `infra.rdb`. Prefix keys by business and environment convention. Set TTLs for temporary locks, streams, caches, and progress records. Do not treat possession of a Redis key, stream ID, or Celery task ID as authorization.

Keep durable business truth in PostgreSQL. Use Redis for cache, coordination, rate limiting, streams, locks, and ephemeral progress. Design recovery when Redis state disappears.

## Migration expectations

When schema changes are required:

- add a migration using the repository's established mechanism;
- make defaults and nullability safe for existing rows;
- avoid destructive or long table locks without an explicit rollout plan;
- update model, CRUD, schema, and tests together;
- do not execute schema changes automatically at module import.
