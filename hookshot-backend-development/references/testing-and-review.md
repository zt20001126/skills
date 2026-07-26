# Testing, validation, and review

## Contents

- Required test surfaces
- Agent-specific tests
- Verification workflow
- Review checklist

## Required test surfaces

Add focused tests for changed behavior:

- Pydantic boundary and validation cases;
- CRUD conditions, ordering, pagination, soft deletion, and tenant scope;
- service success, expected failure, transaction rollback, and authorization;
- router dependency and response contract;
- external integration timeout/error mapping with mocks;
- regression coverage for a bug fix.

Do not call live LLM, Redis, OSS, payment, email, or third-party APIs in unit tests. Mock at the integration boundary. Keep optional live integration tests clearly separated.

## Agent-specific tests

Test:

- each node in isolation;
- every conditional route;
- loop termination and maximum steps;
- malformed LLM/tool output;
- prompt boundary behavior where practical;
- tool schema, authorization, timeout, retry, and safe errors;
- task duplicate delivery and idempotency;
- worker interruption and recovery;
- SSE heartbeat, resume cursor, replay deduplication, authorization, and terminal events.

## Verification workflow

Before handoff:

1. Inspect the diff and preserve unrelated changes.
2. Compile or import-check changed Python files.
3. Run the smallest relevant test set, then a broader set when risk warrants it.
4. Run the bundled convention checker on changed files.
5. Search changed code for direct SQL outside CRUD and raw exception exposure.
6. Confirm router registration, task registration, worker queue consumption, configuration, and `.env.example` updates.
7. Report commands/results in user-facing language and state what was not run.

Do not claim tests passed when they were skipped, failed to collect, or required unavailable infrastructure.

## Review checklist

- Does each layer own the correct responsibility?
- Are all queries and mutations encapsulated by CRUD?
- Is a multi-write transaction atomic?
- Are owner and tenant filters applied before reading or mutating?
- Are soft-deleted rows excluded?
- Can retries or duplicate Celery delivery repeat a side effect?
- Can raw exceptions, provider data, secrets, or internal paths reach a user or LLM?
- Are inputs and LLM outputs bounded and validated?
- Do external calls have timeouts and correct retry policy?
- Are Agent loops bounded and recoverable?
- Are new routes/tasks/configuration fully registered?
- Are comments/docstrings Chinese and type annotations complete?
- Do tests prove both behavior and security boundaries?
