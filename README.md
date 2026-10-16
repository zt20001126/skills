# Skills

面向服装创作与软件工程的 AI Skills 集合。每个技能目录以 `SKILL.md` 为入口，并可包含参考文档、Prompt 模板、配置文件和脚本。

## 技能目录

### 服装设计与内容创作

| Skill | 用途 |
| --- | --- |
| [`rei-kawakubo-inspired`](rei-kawakubo-inspired/SKILL.md) | 生成受先锋解构、雕塑感廓形、非对称结构和高对比配色启发的服装概念与图片 Prompt。 |
| [`yohji-yamamoto-inspired`](yohji-yamamoto-inspired/SKILL.md) | 生成受黑色垂坠、宽松廓形、日式剪裁和非对称解构启发的服装概念与图片 Prompt。 |
| [`fashion_model_conversion`](fashion_model_conversion/SKILL.md) | 为服装电商、社交媒体和品牌内容制定模特图方案，并生成英文图片 Prompt。 |
| [`seedance_video`](seedance_video/SKILL.md) | 为 Seedance 文生视频、图生视频和多镜头创作生成方案、分镜及英文视频 Prompt。 |

### 软件工程与质量保障

| Skill | 用途 |
| --- | --- |
| [`ai-fullstack-python-skill-v1`](ai-fullstack-python-skill-v1/SKILL.md) | 为 FastAPI、SQLAlchemy、Pydantic、Vue/React 和 AI 模块提供分层开发规范。 |
| [`ai-fullstack-standard-v1`](ai-fullstack-standard-v1/SKILL.md) | 为 Java Spring Boot、Vue 和 AI 模块提供分层开发规范及工程约束。 |
| [`ai-software-engineering-decision-gate-v2`](ai-software-engineering-decision-gate-v2/SKILL.md) | 通过需求澄清和技术选型门禁，逐步形成 PRD、TDD 与 TODO。 |
| [`lean-engineering-agent`](lean-engineering-agent/SKILL.md) | 以精简的阶段流程完成需求确认、技术方案选择和工程交付物规划。 |
| [`auto-qa`](auto-qa/SKILL.md) | 根据代码或接口资料生成自动化测试、测试计划、测试用例和验收报告。 |
| [`hookshot-backend-development`](hookshot-backend-development/SKILL.md) | 按 Hookshot Backend 项目的规范开发、修复、重构和审查 Python 后端代码。 |

## 使用方式

1. 打开对应目录中的 `SKILL.md`，确认技能的适用范围和工作流程。
2. 在支持 Skills 的 AI 工具中启用该技能，然后用 `$技能目录名` 指定它；例如 `$seedance_video`。
3. 按需查看该技能目录中的 `references/`、`prompt_template.md`、配置文件或 `scripts/`。这些文件为主技能提供补充资料和可复用资源。

具体触发条件、输入要求、输出格式和限制以各技能自己的 `SKILL.md` 为准。

## 开发参考文档

- [服装图片生成实现流程](SKILL_IMAGE_GENERATION_FLOW.md)：说明前后端如何根据用户选择的 Skill 组装 Prompt 并调用图片模型。
- [Skill 系统开发文档](SKILL_SYSTEM_DEVELOPMENT_DOC.md)：介绍 Skill 的概念、存储方式及系统实现思路。

## 仓库结构

```text
skills/
├── <skill-name>/
│   ├── SKILL.md
│   ├── agents/       # 可选：工具集成元数据
│   ├── references/   # 可选：补充规范与参考资料
│   ├── scripts/      # 可选：辅助脚本
│   └── ...           # 可选：Prompt 模板和配置
├── README.md
└── SKILL_*.md        # Skill 系统相关开发文档
```
