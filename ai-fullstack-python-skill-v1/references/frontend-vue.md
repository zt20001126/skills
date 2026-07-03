# Frontend Vue Rules

Apply these rules to every Vue frontend task.

## Architecture

- Pages go under `views/`.
- Reusable UI goes under `components/`.
- HTTP calls go under `api/`.
- State management uses Pinia under `store/` or `stores/`.
- Routing goes under `router/`.
- Utility functions go under `utils/`.
- Do not call backend endpoints directly inside templates or page event handlers when an API wrapper should exist.
- Do not duplicate API URLs across pages.

## Directory Example

```text
frontend/src/
  api/
    http.ts
    user.ts
  components/
    UserForm.vue
  stores/
    user.ts
  router/
    index.ts
  views/
    User/
      index.vue
```

## Component Rules

- Each page/component must include a Chinese comment explaining its purpose when the file is created or substantially modified.
- Use `v-model` for editable form fields.
- Use explicit loading state for async operations.
- Handle success and error responses explicitly.
- Keep page-level business orchestration in views and reusable display logic in components.
- Keep component props and emitted events typed when the project uses TypeScript.
- Do not place cross-page shared state in local component state.

## API Rules

- Use a shared Axios or fetch client.
- Configure `baseURL`, timeout, request interceptors, and response interceptors in one file.
- Return backend unified response consistently.
- Long AI workflow requests need a longer timeout or async task polling.
- API wrappers must use meaningful function names such as `createWorkflowTask` instead of generic `request`.

## Pinia Rules

- Use stores for shared state such as user session, auth token, app settings, workflow task status, or cross-page result state.
- Do not put purely local form state into Pinia.
- Keep async actions in stores only when the state is genuinely shared.

## Required Vue Deliverables

When generating Vue features, include:

- View page under `views/`
- Reusable components under `components/` when UI is shared or complex
- API wrapper under `api/`
- Store under `stores/` only when shared state is needed
- Loading, success, empty, and error states
