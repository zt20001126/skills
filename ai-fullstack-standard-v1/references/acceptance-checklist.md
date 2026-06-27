# Acceptance Checklist

Before final response, verify every applicable item.

## Backend

- [ ] Controller contains no business logic.
- [ ] Service contains business orchestration and key Chinese Step comments.
- [ ] Mapper only handles data access.
- [ ] DTO / VO / Entity are separated.
- [ ] `Result<T>` or the project equivalent is used.
- [ ] `BusinessException` or the project equivalent is used.
- [ ] No magic values remain in business code.
- [ ] Logs use placeholders, not string concatenation.
- [ ] Entity/DTO/VO classes and fields have Chinese comments.
- [ ] Config classes have Chinese comments explaining purpose, affected modules, and notes.
- [ ] SQL migrations include table and column comments.

## Frontend

- [ ] Pages are under `views/`.
- [ ] Reusable components are under `components/`.
- [ ] API calls are under `api/`.
- [ ] Shared state uses Pinia.
- [ ] Editable forms use `v-model`.
- [ ] Async actions have loading and error handling.

## AI

- [ ] Model calls go through the AI facade or model node.
- [ ] Prompt construction has Chinese comments.
- [ ] Workflow nodes declare input/output/next node in comments.
- [ ] Workflow/Agent/RAG code is structurally separated.
- [ ] API keys and model config are not hardcoded.

## Validation

- [ ] Build or test commands were run when feasible.
- [ ] Failure or skipped validation is reported clearly.
