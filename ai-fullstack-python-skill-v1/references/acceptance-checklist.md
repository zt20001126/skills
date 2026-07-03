# Acceptance Checklist

Before final response, verify every applicable item.

## Backend

- [ ] Route handlers contain no business logic.
- [ ] Services contain business orchestration and key Chinese Step comments.
- [ ] Repositories contain SQLAlchemy query and persistence logic only.
- [ ] SQLAlchemy models, Pydantic request schemas, response schemas, and internal DTOs are separated.
- [ ] A unified response or declared response schema is used.
- [ ] `BusinessException` or the project equivalent is used.
- [ ] No magic values remain in business code.
- [ ] Logs use placeholders or structured logging, not string concatenation.
- [ ] SQLAlchemy models and fields have Chinese comments or database comments.
- [ ] Pydantic schemas and fields have Chinese comments or `Field(description=...)`.
- [ ] Config/settings classes have Chinese comments explaining purpose, affected modules, and operational notes.
- [ ] Migrations include table and column comments when supported.

## Vue

- [ ] Pages are under `views/`.
- [ ] Reusable components are under `components/`.
- [ ] API calls are under `api/`.
- [ ] Shared state uses Pinia under `store/` or `stores/`.
- [ ] Editable forms use `v-model`.
- [ ] Async actions have loading, success, empty, and error handling.

## React

- [ ] Pages are under `pages/` or `views/`.
- [ ] Reusable components are under `components/`.
- [ ] API calls are under `api/`.
- [ ] Shared state uses the project-approved store under `store/` or `stores/`.
- [ ] Forms use controlled components or the existing form-library pattern.
- [ ] Async actions have loading, success, empty, and error handling.

## AI

- [ ] Model calls go through the AI facade, AI client, or model node.
- [ ] Prompt construction has Chinese comments.
- [ ] Workflow nodes declare input/output/next node in comments.
- [ ] Workflow/Agent/RAG code is structurally separated.
- [ ] Tool inputs, tool outputs, and model outputs are typed when structure matters.
- [ ] API keys and model config are not hardcoded.

## Validation

- [ ] Build, lint, type-check, or test commands were run when feasible.
- [ ] Failure or skipped validation is reported clearly.
