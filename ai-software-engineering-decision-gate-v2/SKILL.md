---
name: ai-software-engineering-decision-gate-v2
description: Human-in-the-loop software engineering decision gate for converting natural-language software ideas into clarified requirements, technology selection options, PRD, TDD, and executable TODO files. Use when the user asks for requirement clarification, technical architecture selection, PRD/TDD/TODO generation, software planning, engineering decision gates, or Chinese prompts involving 需求门禁, 需求澄清, 技术选型, PRD, TDD, TODO清单, 软件工程计划.
---

# AI Software Engineering Decision Gate v2

Use this skill as a strict state machine. Do not skip phases. Do not generate PRD, TDD, or TODO artifacts until the requirement has been clarified, the user has confirmed the structured requirement, and the user has selected a technology option.

## Core Rules

- Do not generate PRD, TDD, or TODO when requirements are unclear.
- Do not skip user confirmation.
- Do not default a technology stack.
- Do not silently fill unknown requirements.
- Do not output all phases at once.
- You may propose assumptions only when each one is explicitly marked with `【假设】`.
- Output in Markdown and keep responses structured, engineering-oriented, and non-chatty.

## Phase 1: Requirement Parsing

Evaluate whether the user's requirement is clear. A requirement is clear only when all of these are known:

- User role: who uses the system.
- Input: what the system receives.
- Output: what the system returns or produces.
- Core flow: the main steps, logic, or business process.

### If Requirement Is Unclear

Stop after asking clarification questions. Use exactly this structure:

```markdown
#### ❗不清晰点说明
- ...

#### ❓追问问题（3~10个）
- ...

#### 🧪可能假设（必须标注【假设】）
- 【假设1】...
- 【假设2】...
```

Do not enter technology selection, PRD, TDD, or TODO generation in this response.

### If Requirement Is Clear

Restate the requirement and ask for confirmation. Use this structure:

```markdown
#### ✅需求结构化复述
- 用户角色：
- 输入：
- 输出：
- 核心流程：

#### 📌功能拆解
- 功能1
- 功能2
- 功能3

请确认需求是否正确，确认后进入技术设计阶段。
```

Do not enter Phase 2 until the user explicitly confirms.

## Phase 2: Technology Selection

Only enter this phase after the user confirms the structured requirement. Present exactly three options and include these modules in each option when applicable:

- Web框架
- 数据库
- 缓存
- 消息队列
- 任务调度
- 架构模式（单体 / 微服务）
- 外部AI/第三方服务（如有）

Use this output structure:

```markdown
## 🅰 方案A：MVP极简方案
- 技术栈：
- 优点：
- 缺点：
- 适用场景：

## 🅱 方案B：标准生产方案（推荐）
- 技术栈：
- 优点：
- 缺点：
- 适用场景：

## 🅲 方案C：企业级高扩展方案
- 技术栈：
- 优点：
- 缺点：
- 适用场景：

请确认选择方案A、方案B或方案C，确认后生成工程文档文件。
```

Do not create files until the user selects a方案.

## Phase 3: Engineering Document Generation

Only enter this phase after the user selects a technology option. Generate file-level Markdown outputs, not only chat text.

Create exactly these files in the active workspace unless the user specifies another output directory:

- `prd.md`
- `tdd.md`
- `todo.md`

### PRD File Requirements

`prd.md` must contain:

- 产品概述
- 用户角色
- 功能列表
- 用户流程
- 页面/模块结构
- 非功能需求（性能/安全/扩展性）

### TDD File Requirements

`tdd.md` must contain:

- 系统架构设计
- 模块划分
- 数据库设计
- API设计
- 技术选型确认
- 核心流程图（文字版）
- 异步/任务设计（如需要）

### TODO File Requirements

`todo.md` must:

- Use Markdown checklist syntax.
- Split tasks by module.
- Make each task directly executable by a developer.

Example:

```markdown
- [ ] 用户模块开发
- [ ] 登录接口实现
- [ ] 数据库设计
```

After creating files, summarize the generated file paths and mention that the documentation was generated from the confirmed requirement and selected technology option.
