# AI Module Rules

Apply these rules to Workflow, Agent, and RAG tasks.

## Common AI Rules

- Business code must not call the model directly.
- Use a unified AI facade such as `AiClient`.
- Keep Prompt construction explicit and commented.
- Store model names, API base URLs, timeouts, and feature switches in configuration.
- Never commit API keys or tokens.
- Add Chinese comments around model call boundaries, prompt construction, parsing, retry, timeout, and fallback logic.

## Workflow Structure

Workflow code must separate:

```text
input -> preprocess -> model -> postprocess -> output
```

Recommended packages:

```text
workflow/
  config/
  constant/
  context/
  definition/
  engine/
  enums/
  exception/
  node/
  registry/
```

Rules:

- Define workflow codes and node codes as constants.
- Use `WorkflowContext` to pass data between nodes.
- Use `WorkflowDefinition` to define node order.
- Use `WorkflowNodeRegistry` to decouple engine from concrete nodes.
- Each node must have Chinese comments describing input, output, and next node.
- A node must do one thing only.

## Agent Structure

Agent implementations must explicitly define:

- `goal`: what the agent is optimizing for.
- `tools`: which tools can be called and when.
- `memory`: what context is retained.
- `output schema`: the required structured result.

Recommended packages:

```text
agent/
  goal/
  tool/
  memory/
  schema/
  executor/
```

## RAG Structure

RAG implementations must separate:

```text
embedding -> retrieval -> rerank -> generation
```

Recommended packages:

```text
rag/
  embedding/
  retrieval/
  rerank/
  generation/
  document/
```

Rules:

- Document chunking strategy must be explicit.
- Retrieval parameters such as topK and score threshold must be configurable.
- Prompt must include retrieved context boundaries.
- Do not silently hallucinate when retrieval returns no useful context.
