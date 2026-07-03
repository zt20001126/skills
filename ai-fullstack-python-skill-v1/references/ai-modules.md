# AI Module Rules

Apply these rules to Workflow, Agent, and RAG tasks.

## Common AI Rules

- Business code must not call the model directly.
- Route handlers must not call the model directly.
- Frontend code must not call model providers directly.
- Use a unified AI facade such as `AiClient`, `ModelClient`, or the existing project equivalent.
- Keep prompt construction explicit and commented.
- Store model names, API base URLs, timeouts, temperature, retry counts, vector-store settings, and feature switches in configuration.
- Never commit API keys or tokens.
- Add Chinese comments around model call boundaries, prompt construction, parsing, retry, timeout, fallback logic, and structured output validation.
- Use Pydantic schemas for AI inputs, tool inputs, tool outputs, and model outputs when structure matters.
- Log model request metadata safely; never log secrets or full sensitive prompts unless the project has an approved redaction policy.

## Recommended AI Directory Structure

```text
backend/app/ai/
  common/
    ai_client.py
    schemas.py
    settings.py
  workflow/
    context.py
    definition.py
    engine.py
    nodes/
    registry.py
  agent/
    goals/
    tools/
    memory/
    schemas/
    executor.py
  rag/
    document/
    embedding/
    retrieval/
    rerank/
    generation/
```

## Workflow Structure

Workflow code must separate:

```text
input -> preprocess -> model/tool node -> postprocess -> output
```

Rules:

- Define workflow codes and node codes as constants or enums.
- Use a workflow context object to pass data between nodes.
- Use a workflow definition to define node order.
- Use a node registry to decouple the engine from concrete nodes.
- Each node must have Chinese comments describing input, output, and next node.
- A node must do one thing only.
- Node input and output should use typed Pydantic schemas when feasible.
- Long-running workflows must expose task status, polling, cancellation, or background execution behavior.

## Agent Structure

Agent implementations must explicitly define:

- `goal`: what the agent is optimizing for.
- `tools`: which tools can be called and when.
- `memory`: what context is retained.
- `planning`: how steps are selected or constrained.
- `output schema`: the required structured result.

Recommended packages:

```text
agent/
  goals/
  tools/
  memory/
  schemas/
  executor.py
```

Rules:

- Tool inputs and outputs must be typed.
- Tool execution failures must be converted into structured observations or business exceptions.
- Agent output must be validated before returning to business code.
- Do not let the model invent tool results; tool results must come from actual tool calls or explicit mock/test fixtures.

## RAG Structure

RAG implementations must separate:

```text
document -> chunking -> embedding -> retrieval -> rerank -> generation
```

Recommended packages:

```text
rag/
  document/
  embedding/
  retrieval/
  rerank/
  generation/
```

Rules:

- Document loading and chunking strategy must be explicit.
- Embedding model, vector store, topK, score threshold, rerank switch, and context window limits must be configurable.
- Prompt must include retrieved context boundaries.
- Do not silently hallucinate when retrieval returns no useful context.
- Return citations, source IDs, or chunk metadata when the feature requires traceability.
- Separate ingestion endpoints/jobs from query endpoints.
