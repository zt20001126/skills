# Agent and LangGraph development

## Contents

- Recommended decomposition
- State and graph
- Nodes
- Tools and prompts
- Long-running execution
- Streaming and recovery
- External integrations

## Recommended decomposition

Separate:

- `state`: typed graph state and reducers;
- `graph` or `workflow`: graph construction, edges, routing, compilation;
- `nodes`: focused state transitions;
- `tools`: LLM-callable capabilities;
- `prompts`: centralized prompt text and versions;
- `service`: API-to-workflow orchestration;
- `integrations`: third-party clients and response mapping;
- `tasks`: Celery entry points;
- CRUD/model modules: durable task and conversation state.

Do not build a single file that owns graph construction, prompts, SQL, external HTTP, SSE, and persistence.

## State and graph

Use `TypedDict`, Pydantic, or another explicit typed structure. Document ownership of each state field. Prefer narrow state updates over replacing the entire state. Keep persisted values serializable and bounded.

Construct the graph separately from execution. Use named route functions for conditional edges. Give every loop an explicit termination condition and maximum steps. Test each route and stop condition.

Initialize and close checkpointers and connection pools through application lifespan or another explicit resource lifecycle. Do not make network connections on import. Define whether missing persistence causes startup failure or a documented degraded mode.

## Nodes

Give each node one business responsibility. Keep nodes independent of FastAPI request/response types. Perform persistence through services/CRUD. Make retryable nodes idempotent. Validate data received from prior nodes instead of assuming arbitrary dictionaries are valid.

## Tools and prompts

Give tools:

- typed, bounded input schemas;
- precise Chinese docstrings describing appropriate use;
- stable structured output;
- safe error codes/messages;
- authorization and idempotency for state changes;
- request timeout and bounded retry for network calls.

Never return `str(exc)`, stack traces, credentials, raw provider responses, SQL, or internal paths to the LLM. Log details internally and return a stable failure code.

Keep prompts in `prompts/` when they are substantial. Separate system instructions from untrusted content with explicit delimiters. Limit inserted content. Treat web pages, uploaded documents, tool results, and user text as untrusted data, not instructions. Validate structured model output with Pydantic.

## Long-running execution

Move long Agent jobs, bulk generation, polling, and CPU-heavy work out of API request handlers. For Celery:

- register the task module in `celery_app.py`;
- declare a queue and ensure deployment workers consume it;
- pass only serializable identifiers and values;
- create sessions/clients inside the task and close them;
- configure soft/hard time limits;
- store progress and terminal state through CRUD;
- design for duplicate delivery and worker termination;
- map failures to safe persistent error codes.

## Streaming and recovery

For SSE or Redis Streams:

- send heartbeat events;
- support a stable resume cursor when the public contract requires it;
- deduplicate replayed events;
- stop work or detach safely on disconnect;
- cap event payload and retained history;
- authorize every subscription;
- persist enough state to recover after process or Redis loss.

Ensure terminal events are emitted once logically even if delivery is retried.

## External integrations

Wrap providers behind an integration module. Configure connect/read timeouts. Distinguish authentication, rate-limit, transient network, validation, and provider business failures. Retry only transient idempotent operations with bounded exponential backoff. Validate response status, content type, size, and schema before use.
