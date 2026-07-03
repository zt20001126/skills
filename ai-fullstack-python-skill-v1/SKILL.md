---
name: ai-fullstack-python-skill-v1
description: Strongly constrained enterprise code generation standard for Python fullstack + AI projects. Use when Codex/ChatGPT/AI IDE must generate, refactor, review, or extend code for FastAPI backends, SQLAlchemy persistence, Pydantic DTO/schemas, Vue or React frontends, and AI modules involving Workflow, Agent, or RAG, while enforcing layered architecture, Chinese comments, no magic values, schema/model separation, unified response and business exceptions, no direct model calls from API routes, and engineering-grade maintainability.
---

# AI Fullstack Python Skill V1

Use this skill as a mandatory engineering gate before generating or modifying Python fullstack + AI project code. Treat the rules as constraints, not suggestions.

## Invocation

Use one of these invocation forms:

```text
@skill:AI_FULLSTACK_PYTHON_SKILL_V1
```

```text
Use $ai-fullstack-python-skill-v1 to implement <task>.
```

Codex must automatically:

1. Identify backend, frontend, and AI-module scope.
2. Choose the correct layered directory structure.
3. Generate code under the correct layer only.
4. Add required Chinese comments.
5. Run or recommend validation commands.
6. Reject or repair non-compliant code before final response.

## Non-Negotiable Rules

Fail the task if any generated code violates these rules:

- Do not put business logic in FastAPI route handlers.
- Do not call AI models directly from route handlers, ordinary service code, or frontend code; route model calls through the AI facade, AI client, or AI node.
- Do not mix SQLAlchemy ORM models, Pydantic request schemas, response schemas, and domain DTOs.
- Do not place SQL or ORM query details in route handlers.
- Do not hardcode magic values; use constants, enums, settings classes, environment variables, or config files.
- Do not create SQLAlchemy models, Pydantic schemas, settings classes, or AI boundary objects without Chinese comments explaining purpose and business meaning.
- Do not create configuration modules without Chinese comments explaining purpose, affected modules, and operational notes.
- Do not use string-concatenated logs; use placeholder or structured logs such as `logger.info("task_id=%s status=%s", task_id, status)`.
- Do not generate unlayered Vue or React code; use the required `views/` or `pages/`, `components/`, `api/`, and `store/` or `stores/` layers.
- Do not generate Workflow/Agent/RAG code without explicit input, process, model/tool/retrieval, and output boundaries.
- Do not commit API keys, tokens, connection strings, or model secrets.

## Required Workflow

1. Inspect the existing project structure before editing.
2. Classify the task:
   - FastAPI + SQLAlchemy + Pydantic backend: read `references/backend-fastapi.md`.
   - Vue frontend: read `references/frontend-vue.md`.
   - React frontend: read `references/frontend-react.md`.
   - AI Workflow/Agent/RAG: read `references/ai-modules.md`.
   - Examples or comparison requested: read `references/examples.md`.
3. Design file placement before writing code.
4. Generate or edit code with required Chinese comments.
5. Validate against `references/acceptance-checklist.md`.
6. Run available lint, type-check, build, or tests when feasible.
7. In the final response, report changed files and validation results.

## Default Directory Contract

Prefer the existing project's established structure. If creating a new project or module, use:

```text
backend/
  app/
    api/
      v1/
        routes/
    core/
    db/
    models/
    schemas/
    repositories/
    services/
    dependencies/
    exceptions/
    common/
    ai/
      workflow/
      agent/
      rag/
  tests/

frontend/
  src/
    api/
    components/
    views/ or pages/
    store/ or stores/
    router/
    utils/
```

For modular backends, the following is also valid and preferred for growing systems:

```text
backend/app/
  common/
  core/
  db/
  modules/
    <business_module>/
      api/
      models/
      schemas/
      repositories/
      services/
      dependencies/
      exceptions/
  ai/
    common/
    workflow/
    agent/
    rag/
```

## Output Contract

When this skill is used, produce code that is ready for a real project, not pseudo-code, unless the user explicitly asks for a design only.

For implementation tasks, include:

- Files changed or created.
- Commands run and results.
- Any intentionally deferred behavior.
- Any required environment variables or configuration.

## References

- FastAPI backend rules: `references/backend-fastapi.md`
- Vue frontend rules: `references/frontend-vue.md`
- React frontend rules: `references/frontend-react.md`
- AI Workflow/Agent/RAG rules: `references/ai-modules.md`
- Acceptance checklist: `references/acceptance-checklist.md`
- Usage examples and bad/good comparisons: `references/examples.md`
