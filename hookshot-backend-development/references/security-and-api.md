# API, errors, and security

## Contents

- Authentication and authorization
- Response contracts
- Exception safety
- Logging and secrets
- Input, uploads, and external content

## Authentication and authorization

Derive the current user from `core.auth` dependencies. Never accept a client `user_id` as identity. Apply ownership and tenant/distributor scope to CRUD conditions for reads, updates, deletion, retries, downloads, streams, and task results.

Separate public, authenticated, and administrative routers. Do not infer admin permission from a request field. Recheck authorization for background-task result access.

## Response contracts

Use `Result.success()` and `Result.error()` for ordinary JSON endpoints. Preserve an established endpoint's HTTP-status behavior. For a new Agent API, decide and test whether it uses legacy HTTP 200 plus `Result.code` or true HTTP status codes; do not mix policies inside the module.

Use dedicated responses for SSE, files, and provider webhooks. Still provide stable machine-readable error events or responses.

## Exception safety

Log the real error and expose a safe message:

```python
try:
    ...
except Exception:
    logger.exception("执行任务失败")
    return Result.error("任务执行失败，请稍后重试")
```

Prohibit raw exceptions in:

- `Result.error`;
- JSON `message`, `msg`, `error`, or `detail`;
- Agent tool results;
- graph state visible to the LLM;
- SSE events;
- persistent user-facing task error fields.

Use `CommonError` for expected business failures where the surrounding stack supports it. Do not catch broad exceptions merely to continue with corrupted partial state.

## Logging and secrets

Use `logger = logging.getLogger(__name__)`. Use `logger.exception` or `exc_info=True` when a stack is useful. Include stable task/user identifiers, not secrets.

Never log or return:

- API keys, passwords, JWTs, cookies, authorization headers;
- database or Redis URLs;
- full third-party requests/responses containing credentials;
- unbounded prompts, uploaded content, or binary data;
- internal filesystem paths or SQL.

Keep secrets in environment variables. Do not add real-secret defaults to `settings.py`, `.env.example`, tests, prompts, or fixtures.

## Input, uploads, and external content

Constrain strings, lists, pagination, file sizes, content types, URLs, and time ranges. Prevent SSRF by restricting user-controlled network destinations and resolving redirects safely. Treat uploaded files and fetched text as untrusted.

Normalize filenames and object keys. Do not construct local paths from untrusted input without containment checks. Validate third-party and LLM output before persistence or execution.
