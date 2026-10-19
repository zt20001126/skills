# Codex Skills Library

**项目标识：** `codex-skills-library`

**项目类型：** 可复用的 Codex / AI Agent Skills 集合

本仓库集中维护面向服装创作、内容生产和软件工程的 skills。每个 skill 都是一个独立目录，以 `SKILL.md` 作为入口；需要时可附带模板、参考资料、脚本和配置。

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
| [`feature-implementation-planner`](feature-implementation-planner/SKILL.md) | 先澄清功能需求并核对代码库，再生成按日期命名、可审阅的分步实现方案文档。 |
| [`auto-qa`](auto-qa/SKILL.md) | 根据代码或接口资料生成自动化测试、测试计划、测试用例和验收报告。 |
| [`hookshot-backend-development`](hookshot-backend-development/SKILL.md) | 按 Hookshot Backend 项目的规范开发、修复、重构和审查 Python 后端代码。 |

## 使用方式

1. 打开对应目录中的 `SKILL.md`，确认 skill 的适用范围和工作流程。
2. 在支持 skills 的 AI 工具中启用该 skill，并按工具约定调用；例如 `$seedance_video`。
3. 按需查看同目录中的 `references/`、`prompt_template.md`、配置文件或 `scripts/`。

每个 skill 自行定义触发条件、输入要求、输出格式和边界；以它的 `SKILL.md` 为准。

## 新增 Skill

1. 从 [`templates/skill-template/SKILL.md`](templates/skill-template/SKILL.md) 创建新目录，目录名使用唯一的小写 kebab-case，例如 `product-image-review`。
2. 完成 `SKILL.md` 的 `name` 和 `description`，并按需新增 `references/`、`scripts/`、`agents/` 或配置文件。
3. 在本 README 的合适分类中登记 skill 和用途。
4. 本地运行 `python scripts/validate_skills.py`，确保元数据和目录索引有效。
5. 提交前按 [`CONTRIBUTING.md`](CONTRIBUTING.md) 检查内容和资源。

新增约定和审核清单见 [`CONTRIBUTING.md`](CONTRIBUTING.md)。仓库级 AI 协作规则见 [`AGENTS.md`](AGENTS.md)。

## 仓库结构

```text
codex-skills-library/
├── <skill-name>/                 # 一个 skill 一个目录，必须包含 SKILL.md
│   ├── SKILL.md                  # skill 入口和核心规则
│   ├── agents/                   # 可选：工具集成元数据
│   ├── references/               # 可选：详细参考资料
│   ├── scripts/                  # 可选：可复用辅助脚本
│   └── ...                       # 可选：模板、配置和示例
├── templates/skill-template/     # 新 skill 起始模板
├── scripts/                      # 仓库维护工具
├── .github/workflows/            # 自动元数据校验
├── .gitignore                    # 本地缓存和生成文件忽略规则
├── .gitattributes                # 统一文本文件换行格式
├── AGENTS.md                     # 仓库级 AI 协作约定
├── CONTRIBUTING.md               # 新增和维护约定
├── SKILL_*.md                    # 图片生成和 Skill 系统实现参考文档
└── README.md                     # 项目说明和 skill 索引
```

## 开发参考文档

- [服装图片生成实现流程](SKILL_IMAGE_GENERATION_FLOW.md)：说明前后端如何根据用户选择的 skill 组装 Prompt 并调用图片模型。
- [Skill 系统开发文档](SKILL_SYSTEM_DEVELOPMENT_DOC.md)：介绍 skill 的概念、存储方式及系统实现思路。
