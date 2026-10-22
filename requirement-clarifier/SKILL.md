---
name: requirement-clarifier
description: Clarify an informal software request against the relevant project code and conventions, then create a user-confirmed Markdown requirement document. Use when a user needs requirements understood, checked, and made ready for later design or implementation; do not use for technical design or coding.
---

# Requirement Clarifier

Turn a user's natural-language request into a clear, feasible, project-grounded requirement document. This skill ends after the confirmed document is saved. Technical design, implementation planning, and coding belong to separate workflows.

## When to use

Use this skill when a user describes a software change in informal, incomplete, or ambiguous terms and wants the need analyzed, clarified, and documented before design or development.

Do not use it to choose technologies, design architecture or APIs, produce an implementation plan, or change application code. If the user asks for those as well, complete the requirement document first and leave the next phase to a separate workflow.

## Workflow

1. **Understand the request.** Restate the apparent user need internally and identify the intended actor, problem, desired outcome, and any stated boundaries. Do not start implementation.
2. **Inspect relevant project context.** Work from the project root. Read applicable `AGENTS.md` files and the relevant README, domain documentation, modules, UI, API, data definitions, and conventions. Follow the current behavior far enough to describe it accurately. Keep inspection focused; do not scan unrelated areas. Never guess the existence or behavior of a component. Record what could not be verified.
3. **Separate evidence.** Track project- or user-verified facts, reasonable inferences, and unresolved questions as distinct categories. Use existing project rules and established behavior for low-impact defaults, and label those defaults as assumptions. See [clarification-rules.md](references/clarification-rules.md).
4. **Resolve consequential ambiguity.** Ask a concise, grouped set of questions only when different answers could change scope, business behavior, data, user interaction, constraints, or acceptance. Do not ask for facts discoverable from the project. Continue with focused follow-ups if a material ambiguity remains. Do not silently decide a consequential question.
5. **Check feasibility against evidence.** Identify conflicts with verified project behavior, documented rules, or observable constraints. Explain limits and unknowns without inventing capabilities or proposing a technical solution. Ask the user to resolve requirement conflicts where needed.
6. **Present a requirement draft.** Once key questions are resolved—or the request is already sufficiently clear—show the complete, project-grounded draft in the conversation using the sections in [requirement-template.md](references/requirement-template.md). For a clear request, do not manufacture clarification questions; still request explicit confirmation of the draft.
7. **Revise and confirm.** Incorporate the user's changes and present the revised draft again. Do not create the final document until the user explicitly confirms the requirement content. A lack of objection, an unanswered question, or a request to “start” without confirming a still-ambiguous behavior is not confirmation.
8. **Save the final document.** After explicit confirmation, create `docs/requirements/` under the project root if needed, and save the confirmed content there using the naming rules below. Inspect existing files first, preserve any existing documents, and update the existing document when the user is revising that same requirement. Do not overwrite an unrelated document.
9. **Report and stop.** Give the saved file path and a short summary, note any explicit assumptions, and stop this workflow. Do not enter design, planning, or implementation.

## Document path and naming

- Save all final requirement documents in `<project-root>/docs/requirements/`.
- Use `YYYY-MM-DD-NNN-requirement-name.md`, where the date is the current local date for the project/user context, `NNN` is a three-digit per-day sequence starting at `001`, and the final segment is a concise English kebab-case topic name.
- Determine the next sequence from existing files for that date. If the intended name collides, choose a meaningful distinguishing topic name or the next unused sequence; never overwrite a different document.
- When editing the same confirmed requirement, update its existing file rather than creating a duplicate.
- Do not use generic names such as `new-requirement` or `test`.

## Boundaries

- This skill may inspect project files, ask questions, draft and revise requirement text in the conversation, and create or update only the confirmed Markdown requirement document in `docs/requirements/`.
- Do not modify business code, database contents or schemas, APIs, project configuration, tests, or unrelated documents and files.
- Do not create the final requirement file before explicit user confirmation of the displayed draft.
- Do not expand scope with independent features. Include only necessary behavior implied by the request or established project rules, and identify non-obvious defaults as assumptions.
- Do not present an inference as a confirmed fact. Omit irrelevant template sections or explain why they do not apply; never add filler.
- The generated document is the endpoint. Do not automatically continue into technical design, implementation planning, or code changes, even if the document identifies follow-up work.

## Resources

- Read [clarification-rules.md](references/clarification-rules.md) for evidence labels, ambiguity triage, questioning, and confirmation rules.
- Use [requirement-template.md](references/requirement-template.md) for the draft and final document structure.
