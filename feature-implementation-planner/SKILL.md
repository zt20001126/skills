---
name: feature-implementation-planner
description: Clarify feature requirements and inspect the existing codebase before producing a reviewable, step-by-step implementation plan document. Use when a user wants a feature planned before coding, needs requirement clarification, or asks for architecture, file-change, implementation-step, or acceptance planning. This skill produces the plan and waits for review before code changes.
---

# Feature Implementation Planner

Turn a feature request into a codebase-grounded implementation plan. Resolve implementation-critical ambiguity with the user first, document the proposed design in the project, then stop for review. The plan should show where each responsibility belongs and how every step will be accepted.

## Workflow

### 1. Inspect the project

Before asking the user about project facts, inspect the repository and its conventions:

- Locate the project root and read applicable `AGENTS.md` files, the root README, architecture documents, and relevant module documentation.
- Find the feature's existing routes, entry points, services, domain models, persistence, UI, integrations, and nearby tests as applicable. Trace the current flow far enough to know where the change belongs.
- Follow existing naming, layering, dependency direction, error handling, API, and test conventions. Note any project-specific skills or instructions that apply.
- Use exact paths and symbols found in the repository. Label proposed new paths as new; never present an unverified path as an existing file.
- Keep investigation focused on the feature. Do not edit implementation code during this planning workflow.

**Completion check:** You can identify the relevant existing modules and project conventions, or you have recorded what could not be inspected and why.

### 2. Check requirement readiness

Map the request to the information needed to design the feature:

- User or system actor and relevant permissions
- Trigger, inputs, outputs, and observable user or system behavior
- Main flow, important alternate flows, and failure behavior
- Business rules, data ownership, validation, and state changes
- Integrations, platform constraints, compatibility needs, and non-functional needs when relevant
- Scope boundaries and observable acceptance criteria

Compare this map with the user's request and what the repository can establish. Ask the user only about unresolved choices that could change behavior, data, security, compatibility, architecture, scope, or acceptance. Do not ask for facts that are discoverable in the repository. Group related questions into a short, concrete batch; offer answer choices when they make answering easier. Avoid re-asking items the user has already answered.

Treat an ambiguity as **blocking** when different answers would lead to materially different implementation or acceptance. Resolve all blocking ambiguities before writing the final plan. Record non-blocking assumptions in the document with their impact. If answers leave a blocking ambiguity, ask a focused follow-up instead of guessing or generating a supposedly final plan.

When the requirement is ready, briefly restate the agreed behavior and proceed to the plan; do not add a separate confirmation round unless a consequential interpretation still needs the user's decision.

**Completion check:** Every implementation-critical question is answered or verified from project context; remaining assumptions are explicit and do not prevent a coherent plan; acceptance criteria can be checked.

### 3. Design against the codebase

Produce a design that fits the repository rather than an abstract ideal architecture:

- Explain the relevant current structure and the proposed request/data flow.
- Assign each responsibility to an appropriate existing or new module. Keep responsibilities cohesive and dependencies directed through the project's established boundaries.
- Prefer existing abstractions and patterns when they fit. Explain why a new module or layer is needed. Avoid both dumping logic into an unrelated file and adding needless layers for a small change.
- Describe meaningful API, schema, persistence, UI, integration, and state changes only when the feature needs them.
- Before proposing an API or database change, inspect the existing routes/contracts and persistence models/migrations relevant to the feature. Make reuse the default: identify whether an existing endpoint, table, or field can serve the requirement. For every proposed addition or modification, explain why reuse or a smaller change cannot satisfy it. Do not invent fields or tables merely to mirror a request, response, or workflow state.
- Always make API and database impact explicit in the plan, even when there is none. List endpoints individually with method, path, action (add/modify/unchanged), contract changes, and compatibility impact. List tables and fields individually with action (add/modify/unchanged), purpose, and migration/backfill implications. If the repository evidence is incomplete, say what could not be verified; do not claim there is no impact based on missing evidence.
- Apply a minimal-change check: each proposed endpoint, table, field, index, or persistence layer must map to a confirmed requirement and observable acceptance criterion. Remove proposals with no such mapping, and record any unresolved data/API decision as blocking before finalizing the plan.
- Consider security and authorization, privacy, validation, failure handling, performance, observability, backward compatibility, migrations, rollout, and rollback when relevant. For irrelevant concerns, omit the section or state briefly why it does not apply.
- Compare alternatives only when there is a real decision with material trade-offs. Record the recommendation and reason; do not invent technology choices when the project already establishes them.
- Show the target structure for the affected area only. Clearly mark new files and changed files.

### 4. Write the implementation plan document

Use the scaffold in [`references/implementation-plan-template.md`](references/implementation-plan-template.md), adapting it to the feature's size. Keep all decision-critical sections; omit irrelevant sections instead of filling them with boilerplate. Small changes should produce a concise plan, while cross-module or data-changing work should include the needed architecture and operational detail.

Create the document under the project root at:

```text
docs/implementation-plans/YYYY-MM-DD-<功能名称>.md
```

For example: `docs/implementation-plans/2026-10-19-订单导出.md`.

Use the current date in the user's or project's local timezone. Use a concise feature name, preserve an established repository naming convention when one exists, and replace filename-invalid characters. If the target file already exists, inspect it first; do not overwrite an unrelated plan. Use a numeric suffix only to resolve a genuine same-day name collision.

The document must include:

- Confirmed requirements, scope, and expected final behavior
- Relevant current code structure, with verified file references
- Proposed architecture, module responsibilities, data/control flow, and design rationale
- A complete change inventory: exact file path, new/modify action, responsibility, and reason
- An explicit API impact inventory and database impact inventory, including an explicit “no change” result when applicable; each proposed change must be justified against the existing code and mapped to a confirmed requirement
- A target tree showing the affected code structure after the proposed change
- Ordered implementation steps; each step lists files, work, dependencies where applicable, and observable acceptance criteria
- A verification strategy that maps acceptance criteria to appropriate checks or tests
- Relevant assumptions, risks, and cross-cutting concerns

For each step, acceptance criteria must describe observable behavior or a concrete structural result, not vague phrases such as “works correctly” or “complete the logic.” Identify test locations or test types when discoverable. A plan describes checks to perform; never claim they passed unless they were actually run.

**Completion check:** The file exists at the required path; all proposed existing paths were verified; every new/changed file has a reason and responsibility; every implementation step has checkable acceptance criteria; the target structure agrees with the file inventory.

### 5. Deliver and pause

After writing the plan, give the user a concise summary and a link to the document. Mention any recorded assumptions or unresolved non-blocking risks. Stop before editing application code. Continue to implementation only after the user has reviewed the plan and explicitly asks to proceed; incorporate requested plan changes first.

## Planning principles

- The plan is grounded in the actual repository and confirmed user intent.
- A question is asked to resolve a consequential uncertainty, not to transfer codebase research to the user.
- Every proposed file has a clear owner, cohesive responsibility, and reason to exist.
- The plan is sized to the feature and stays executable rather than becoming a generic architecture essay.
- The implementation plan is the deliverable for this skill; code changes are a separate, user-directed phase.
