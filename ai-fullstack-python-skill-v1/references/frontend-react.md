# Frontend React Rules

Apply these rules to every React frontend task.

## Architecture

- Pages go under `pages/` or `views/`, following the existing project convention.
- Reusable UI goes under `components/`.
- HTTP calls go under `api/`.
- State management goes under `store/` or `stores/` when using Zustand, Redux Toolkit, Jotai, or another project-approved store.
- Hooks go under `hooks/`.
- Routing goes under `router/` when the project uses client-side routing.
- Utility functions go under `utils/`.
- Do not call backend endpoints directly inside JSX or scattered component handlers when an API wrapper should exist.
- Do not duplicate API URLs across pages.

## Directory Example

```text
frontend/src/
  api/
    http.ts
    user.ts
  components/
    UserForm.tsx
  hooks/
    useUserQuery.ts
  pages/
    User/
      index.tsx
  stores/
    userStore.ts
  router/
    index.tsx
  utils/
```

## Component Rules

- Each page/component must include a Chinese comment explaining its purpose when the file is created or substantially modified.
- Use controlled components for editable form fields unless the existing project uses a form library pattern.
- Use explicit loading state for async operations.
- Handle success and error responses explicitly.
- Keep page-level orchestration in pages/views and reusable display logic in components.
- Keep props typed when using TypeScript.
- Extract repeated effects or async state handling into hooks only when reuse or clarity justifies it.

## API Rules

- Use a shared Axios or fetch client.
- Configure `baseURL`, timeout, request interceptors, and response interceptors in one file.
- Return backend unified response consistently.
- Long AI workflow requests need a longer timeout or async task polling.
- API wrappers must use meaningful function names such as `submitRagQuestion` instead of generic `postData`.

## State Rules

- Use shared stores for user session, auth token, app settings, workflow task status, or cross-page result state.
- Do not put purely local form state into global stores.
- If React Query, TanStack Query, SWR, or similar tools exist, use them for server cache instead of duplicating cache state in a store.

## Required React Deliverables

When generating React features, include:

- Page under `pages/` or `views/`
- Reusable components under `components/` when UI is shared or complex
- API wrapper under `api/`
- Hook under `hooks/` when async behavior or reuse warrants it
- Store under `stores/` only when shared client state is needed
- Loading, success, empty, and error states
