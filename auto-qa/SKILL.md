---
name: auto-qa
description: Create complete automated testing and release-acceptance deliverables from user-provided code, modules, API controllers/routers, diffs, FastAPI or Spring Boot services, interface specifications, or project snippets. Use when Codex must act as a QA automation engineer to generate executable unit, API, integration, boundary, negative, and idempotency tests plus Markdown test plans, test cases, and go/no-go acceptance reports.
---

# Auto QA

Use this skill to turn a code change or interface description into a runnable QA delivery package. Act as a senior software test engineer, backend architect, and QA automation expert. The output must help decide whether the feature can go online.

## Non-Negotiable Contract

Always produce these deliverables:

- `test_plan.md`
- `test_cases.md`
- `test_code/`
- `test_report.md`

Do not stop at analysis. Generate executable test code with real assertions. Never emit assertion-free tests, vague sample tests, or tests that require live external dependencies. Mock databases, queues, remote HTTP calls, cloud services, mail/SMS providers, and time-sensitive services unless the project already provides a local test fixture.

API testing is mandatory. If a web API surface is detected, generate runnable HTTP-level tests. If no web API surface is present, still include an explicit API Test section explaining that no HTTP API was detected, identify any callable contract boundary, and generate the closest executable contract test for that boundary. If no executable boundary can be inferred, mark the release judgment as "not ready" until an API or contract surface is supplied.

## Workflow

1. Inspect the input and surrounding project context.
   - Classify the input as function/class, API controller/router, diff, FastAPI module, Spring Boot module, interface spec, or project snippet.
   - Identify language, framework, package manager, test runner, routes/endpoints, schemas/DTOs, dependencies, persistence, external calls, and existing test conventions.
   - Prefer existing project test style, fixtures, factories, naming, dependency injection, and response wrapper conventions.

2. Build a test model.
   - Map functional requirements to testable behaviors.
   - Separate modules and responsibility boundaries.
   - Identify happy paths, null/empty input, invalid type, overflow/length limits, duplicate requests/idempotency, bad requests, authorization or validation errors, downstream failures, and persistence effects.
   - Identify observability or performance checks only when the code exposes a measurable boundary.

3. Generate the Markdown deliverables.
   - Write `test_plan.md` with scope, module breakdown, goals, and categorized strategy.
   - Write `test_cases.md` as a Markdown table with the required columns.
   - Write `test_report.md` with execution status, risks, and explicit online judgment.

4. Generate `test_code/`.
   - Python: use `pytest`; for FastAPI use `fastapi.testclient.TestClient`; use `httpx` only when async or external-client behavior requires it.
   - Java: use JUnit 5 and Mockito; for Spring Boot API tests use MockMvc or SpringBootTest according to the project style.
   - Include only runnable, concrete tests. Use mocks/fakes for external dependencies. Assert status codes, response JSON shape, error format, and core side effects.

5. Validate when possible.
   - Run the relevant test command if the project dependencies are available.
   - If tests cannot be run, state the exact blocker in `test_report.md` and mark execution counts as "not executed" rather than fabricating pass counts.

## `test_plan.md` Requirements

Include these sections:

- Feature scope
- Module breakdown
- Test objectives
- Test strategy with all categories below:
  - Unit Test
  - API Test
  - Integration Test
  - Boundary Test
  - Negative Test
  - Idempotency Test

For API Test, always name the API surface tested or explicitly state that no HTTP API was detected and which contract boundary is tested instead.

## `test_cases.md` Requirements

Use exactly this table shape:

```markdown
| 用例ID | 测试类型 | 测试场景 | 输入 | 预期输出 | 是否通过 |
|---|---|---|---|---|---|
```

Cover at least:

- Happy Path
- Null/Empty
- Invalid Type
- Overflow
- Idempotency
- Bad Request

Add integration, persistence, security, authorization, concurrency, or performance cases when relevant. Use `未执行` until tests have actually been run.

## API Test Requirements

For FastAPI, generate tests that use:

- `TestClient(app)` or the project's existing app fixture
- HTTP request simulation for each detected route
- Status code assertions for success and failure paths, including 200 or 201, 400 or 422, and 500 when an internal failure path is mockable
- JSON structure assertions, including required fields and error response format
- Dependency overrides or monkeypatching for repositories/services/external clients

For Spring Boot, generate tests that use:

- `@WebMvcTest` plus mocked collaborators for controller-slice tests, or `@SpringBootTest` plus `@AutoConfigureMockMvc` when project integration wiring is needed
- `MockMvc` HTTP requests
- `status()` assertions
- `jsonPath()` assertions for response body and error format
- Mockito stubbing and verification for service/repository/external dependencies

API tests must verify:

- HTTP status codes: success, bad request or validation error, and internal error when safely mockable
- Request parameter and body validation
- Complete response structure
- Error response format
- Optional basic response-time threshold only when stable and meaningful in local tests

## Test Code Standards

Use project-native paths when a repository exists. Otherwise create a standalone `test_code/` tree with clear package/module names and minimal fixtures needed to run the tests after the user places the source under test beside them.

Python expectations:

- Use `pytest`.
- Use fixtures for setup and dependency overrides.
- Use `unittest.mock`, `pytest-mock`, or monkeypatch for external dependencies.
- Prefer `tmp_path` for filesystem effects.
- Include assertions for return values, raised exceptions, response bodies, state changes, and mocked interactions.

Java expectations:

- Use JUnit 5.
- Use Mockito for collaborators.
- Use MockMvc for Spring MVC APIs.
- Use `assertThrows`, AssertJ, or JUnit assertions for unit behavior.
- Use JSON Path for API response structure.

Do not:

- Generate only illustrative pseudo-tests.
- Leave TODO placeholders inside test bodies.
- Depend on real network services, production databases, real credentials, or mutable wall-clock time.
- Claim tests passed unless they were executed successfully.

## `test_report.md` Requirements

Include:

- Test execution result:
  - Total test cases
  - Passed count
  - Failed count
  - Not executed count, if any
  - Test command used, if executed
- Risk analysis:
  - Potential bug points
  - Exception-handling risks
  - API instability risks
  - Performance risks, when applicable
  - Test coverage gaps
- Online judgment:
  - `可上线` only when generated tests are runnable, critical tests pass or are confidently covered, API testing exists for the exposed API surface, and no blocking risk remains.
  - `不可上线` when tests cannot run, critical coverage is missing, API surface is absent but required, severe risks remain, or failures are detected.

State the reason for the judgment in one or two concrete paragraphs.

## Output Layout

When creating files, use this layout:

```text
test_plan.md
test_cases.md
test_code/
  python/ or java/ or framework-native paths
test_report.md
```

If working inside a user's repository, place tests where the project expects them when that is clearly discoverable, and mirror the deliverables in the requested output location if the user asks for a package. If no location is specified, create a local QA delivery folder and provide links to the generated files.
