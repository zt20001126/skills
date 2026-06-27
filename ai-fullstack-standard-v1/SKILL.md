---
name: ai-fullstack-standard-v1
description: Strongly constrained enterprise code generation standard for Java + Vue + AI projects. Use when Codex/ChatGPT/AI IDE must generate, refactor, review, or extend code for Java Spring Boot backends, Vue frontends, and AI modules involving Workflow, Agent, or RAG, while enforcing Alibaba Java P3C style, Controller/Service/Mapper layering, Vue views/components/api/store layering, Chinese comments, no magic values, DTO/VO/Entity separation, unified Result and BusinessException, and engineering-grade maintainability.
---

# AI Fullstack Standard V1

Use this skill as a mandatory engineering gate before generating or modifying Java + Vue + AI project code. Treat the rules as constraints, not suggestions.

## Invocation

Use one of these invocation forms:

```text
@skill:AI_FULLSTACK_STANDARD_V1
```

```text
Use $ai-fullstack-standard-v1 to implement <task>.
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

- Do not put business logic in Controller.
- Do not call AI models directly from Controller or ordinary Service code; route model calls through the AI facade or AI node.
- Do not mix DTO, VO, and Entity.
- Do not place SQL in Controller or Service.
- Do not hardcode magic values; use constants, enums, configuration properties, or application.yml.
- Do not create fields in Entity/DTO/VO without Chinese comments.
- Do not create Config classes without Chinese comments explaining purpose, affected modules, and notes.
- Do not use string-concatenated logs; use placeholder logs such as `log.info("taskId={}", taskId)`.
- Do not generate unlayered Vue code; use `views/`, `components/`, `api/`, and `store/` or `stores/`.
- Do not generate Workflow/Agent/RAG code without explicit input, process, model/tool/retrieval, and output boundaries.

## Required Workflow

1. Inspect the existing project structure before editing.
2. Classify the task:
   - Backend Java/Spring Boot: read `references/backend-java.md`.
   - Vue frontend: read `references/frontend-vue.md`.
   - AI Workflow/Agent/RAG: read `references/ai-modules.md`.
   - Examples or comparison requested: read `references/examples.md`.
3. Design file placement before writing code.
4. Generate or edit code with required Chinese comments.
5. Validate against `references/acceptance-checklist.md`.
6. Run available build/tests when feasible.
7. In the final response, report changed files and validation results.

## Default Directory Contract

Prefer the existing project's established structure. If creating a new project or module, use:

```text
backend/
  controller/
  service/
  service/impl/
  mapper/
  entity/
  dto/
  vo/
  config/
  common/

frontend/
  views/
  components/
  api/
  store/ or stores/

ai/
  workflow/
  agent/
  rag/
```

For modular backends, the following is also valid and preferred for growing systems:

```text
backend/src/main/java/<base-package>/
  common/
  config/
  module/<business-module>/
    controller/
    service/
    service/impl/
    mapper/
    entity/
    dto/
    vo/
  ai/
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

- Backend Java/Spring Boot rules: `references/backend-java.md`
- Vue frontend rules: `references/frontend-vue.md`
- AI Workflow/Agent/RAG rules: `references/ai-modules.md`
- Acceptance checklist: `references/acceptance-checklist.md`
- Usage examples and bad/good comparisons: `references/examples.md`
