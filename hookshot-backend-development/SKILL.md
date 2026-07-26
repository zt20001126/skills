---
name: hookshot-backend-development
description: Enforce Hookshot Backend engineering conventions when creating, modifying, fixing, refactoring, testing, or reviewing Python code in E:\Work\hookshotbackend, especially new Agent businesses under modules/. Use for FastAPI routers, services, SQLModel models, CRUD, Pydantic schemas, LangGraph workflows, tools, prompts, Celery tasks, Redis, external integrations, security reviews, and AI-generated code. Exclude modules/selection_agent, modules/listing_agent, and spacex as convention sources unless the user explicitly asks to modify them.
---

# Hookshot Backend Development

Apply the repository's current engineering contract before writing code.

## Establish scope

1. Read the repository `AGENTS.md` completely.
2. Inspect the files directly involved in the request and their callers, registrations, models, CRUD, schemas, and tests.
3. Do not treat these directories as architectural or style examples:
   - `modules/selection_agent`
   - `modules/listing_agent`
   - `spacex`
4. Modify an excluded directory only when the user explicitly places it in scope.
5. Prefer current executable code over stale paths or numeric examples in documentation. Preserve explicit `AGENTS.md` safety requirements even when legacy code violates them.

## Load only relevant references

- Read [references/architecture.md](references/architecture.md) for every implementation or refactor.
- Read [references/database.md](references/database.md) when persistence, transactions, Redis state, models, or migrations are involved.
- Read [references/agent-development.md](references/agent-development.md) when adding or changing an Agent, LangGraph graph, node, tool, prompt, streaming endpoint, or background task.
- Read [references/security-and-api.md](references/security-and-api.md) for routers, authentication, external integrations, logging, errors, uploads, or user-visible/LLM-visible output.
- Read [references/testing-and-review.md](references/testing-and-review.md) before implementing tests, reviewing code, or handing off any code change.
- Read [references/project-map.md](references/project-map.md) when locating integration points or resolving conflicts between documentation and current code.

## Follow the implementation workflow

1. Restate the requested behavior and identify affected contracts.
2. Trace the existing call path before editing.
3. Place new business code under `modules/<business_name>/`; keep router, schema, service, CRUD, model, Agent workflow, tools, prompts, and integrations separated.
4. Reuse project infrastructure and public contracts. Do not duplicate database, authentication, response, logging, Redis, OSS, or Celery clients.
5. Put all database statements inside CRUD classes. Add a named CRUD method for a new query.
6. Keep routers thin. Put orchestration in services and Agent logic in graph/node/tool modules.
7. Validate external and LLM data at boundaries. Add timeouts, bounded retries, idempotency, and authorization where applicable.
8. Add or update focused tests with the implementation.
9. Run the narrowest meaningful tests, syntax/static checks, and the convention checker.
10. Report what changed, what was verified, and any verification not run.

## Enforce non-negotiable rules

- Use `infra.persistence.sql.BaseCRUD`; do not copy the stale `utils.sql.BaseCrud` path.
- Use `infra.db.get_session` or `get_db` for SQLModel sessions.
- Never execute raw SQLModel/SQLAlchemy statements in routers, services, Agent nodes/tools, or Celery tasks.
- Use `shared.common.get_snowflake_id` for primary keys and `shared.common.beijing_time` for application timestamps.
- Separate API schemas from database models.
- Use `schema.result.Result.success()` or `Result.error()` for ordinary JSON APIs unless an established special contract requires another response.
- Never expose raw exception strings, stack traces, credentials, internal paths, SQL, or third-party raw failures to users or LLMs. Log internal details and return stable safe messages.
- Derive identity from authentication dependencies; never trust a client-supplied `user_id`.
- Scope reads and writes by resource owner and tenant/distributor where applicable.
- Use Python 3.10+ type syntax and type every function parameter and return value.
- Write new comments and docstrings in Chinese.
- Keep secrets in environment variables with no real-secret defaults.
- Preserve unrelated user changes and avoid broad rewrites.

## Run the bundled checker

Run:

```powershell
python C:\Users\96598\.codex\skills\hookshot-backend-development\scripts\check_hookshot_conventions.py --root E:\Work\hookshotbackend
```

Pass changed Python files with repeated `--file` arguments for a focused check. Treat findings as review prompts: inspect context before changing legacy code.
