# Clarification Rules

Use these rules while analyzing a request and before presenting its requirement draft.

## Keep evidence categories separate

- **Confirmed fact:** directly stated by the user or verified in project code, documentation, configuration, or existing behavior. Be able to identify its source. Do not treat a plausible convention as evidence that a feature exists.
- **Reasonable inference:** a low-impact detail supported by a project convention, existing flow, or ordinary business logic. State it as an assumption in the draft, including its basis when useful. Do not silently promote it to a confirmed requirement.
- **Needs confirmation:** an unknown or conflicting detail for which plausible answers change feature scope, core business behavior, data handling, user-visible interaction, constraints, or acceptance. Ask the user before drafting a final version.

If a source is unavailable, contradictory, or insufficient, say what could not be verified. Do not invent architecture, endpoints, data models, business rules, permissions, or existing functionality.

## Inspect the project proportionally

Start with applicable repository instructions and the project overview. Then trace only the modules and existing flow related to the request. Verify described behavior in the relevant source rather than relying on filenames or assumptions. Read project conventions that materially affect the requirement. Avoid broad scans that add no context to this request.

Describe current functionality as observed, with paths or symbols where that helps developers verify it. Distinguish an existing behavior from the change the user is asking for. Do not propose how to architect or implement the change; feasibility checking is limited to identifying evidence-based conflicts, constraints, and unknowns.

## Decide whether to ask

Ask only if the answer can materially change one or more of these:

- Who can use the behavior or what triggers it
- Included feature scope or a meaningful exclusion
- A business rule, state transition, data outcome, or integration outcome
- The user's steps or what the system visibly does
- Error, empty, boundary, or recovery behavior that affects the expected result
- A project constraint or an acceptance condition

Do not ask about details already settled by the user's request or discoverable from project files. Resolve small details from explicit project conventions when safe, and label them as assumptions. Do not broaden the request by adding adjacent features “for completeness.”

Group related questions into a short batch. Use plain language and ask one decision per question. Give two or three concrete choices when useful, describe the user-visible difference, and allow the user to state another answer. Avoid asking a long checklist when only a few decisions are consequential.

If the request is clear, move directly to a draft and ask the user to confirm it. If an answer reveals another consequential ambiguity, ask a focused follow-up before presenting a draft as ready for confirmation.

## Check feasibility without designing

Compare requested behavior with verified project behavior, documented rules, and constraints available in the repository. Report an explicit conflict or an inability to verify a capability. Do not claim a request is implementable merely because no conflict was found. Do not invent a workaround, select a technology, define an architecture, or turn an unknown into a promised capability. Ask the user to choose when requirements conflict; record unresolved feasibility as unresolved and do not mark the draft confirmed.

## Draft, confirm, and save

Show the complete draft in the conversation before creating or changing a final document. It must make the actor's operation, system response, expected result, boundaries, and observable acceptance clear. Mark assumptions as assumptions and keep unresolved items visible; do not hide them in polished prose.

Ask for an explicit confirmation of the draft. If the user requests edits, update and show the full revised draft, then ask for confirmation again. Only an unambiguous confirmation of the displayed requirement authorizes writing the final requirement document. A user asking to proceed with development is not confirmation of an unresolved draft and does not authorize this skill to implement the request.

After confirmation, create or update only the requirement Markdown file under `docs/requirements/`. Preserve the confirmed meaning, retain important assumption labels, and stop after reporting the result.
