# Frontend Vue Rules

Apply these rules to every Vue frontend task.

## Architecture

- Pages go under `views/`.
- Reusable UI goes under `components/`.
- HTTP calls go under `api/`.
- State management uses Pinia under `store/` or `stores/`.
- Utility functions go under `utils/`.
- Do not call backend endpoints directly inside templates.
- Do not duplicate API URLs across pages.

## Component Rules

- Each page/component must include a Chinese comment explaining its purpose when the file is created or substantially modified.
- Use `v-model` for editable form fields.
- Use loading state for async operations.
- Handle success and error responses explicitly.
- Keep page-level business orchestration in views and reusable display logic in components.

## API Rules

- Use a shared Axios instance.
- Configure `baseURL`, timeout, and response interceptors in one file.
- Return backend `Result<T>` consistently.
- Long AI workflow requests need a longer timeout or async task polling.

## Pinia Rules

- Use stores for shared state such as user session, auth token, app settings, workflow task status, or cross-page result state.
- Do not put purely local form state into Pinia.

## Directory Example

```text
frontend/src/
  api/
    codeReview.js
    http.js
  components/
    ResultPanel.vue
  stores/
    app.js
  views/
    CodeReview/
      index.vue
```
